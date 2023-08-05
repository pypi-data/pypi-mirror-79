import click
import untangle
import base64
import json
import re
import sys
from subprocess import Popen, PIPE, STDOUT
from urllib.error import HTTPError


from indico_install.utils import options_wrapper, run_cmd
from indico_install.infra.input_utils import download_indicoapi_data, auth_with_gsutil
from indico_install.infra.single_node import single_node
from indico_install.infra.gke import gke
from indico_install.infra.aks import aks

# Here we try and include the EKS function
# It depends on boto3 which may not be installed
# in which case we include a stub instead
try:
    from indico_install.infra.eks import eks
except Exception:

    @click.command("eks")
    def eks():
        """Not available"""
        pass


@click.group("infra")
@click.pass_context
def infra(ctx):
    """
    Indico infrastructure setup and validation. Supports EKS, GKE, and single node installations.

    EKS Note! must install package with "eks" extras for EKS
    """
    pass


@infra.command("generate-saml")
@click.pass_context
@click.argument("host", required=True, type=str)
@click.argument("metadata_url", required=True, type=str)
def generate_saml(ctx, host, metadata_url):
    """
    Generate and inject SAML settings from Azure AD Saml2
    Before running, complete the following steps:
    1. Register the indico platform as an app registration in Azure AD
    2. Add https://<indico IPA hostname>/auth/users/saml/acs" to the web redirection url whitelist

    HOST is the URL of the indico platform
    METADATA_URL is the federation metadata URL

    Example usage:
    indico infra generate-saml app.indico.io https://login.microsoftonline.com/12346-78910-11121314/federationmetadata/2007-06/federationmetadata.xml

    """
    try:
        obj = untangle.parse(metadata_url)
    except HTTPError:
        click.secho("Federation URL not found. Please check that this is the correct URL", fg="red")
        return
    svc = obj.EntityDescriptor.IDPSSODescriptor.SingleSignOnService[0]["Location"]
    endpoint = obj.EntityDescriptor["entityID"]

    der = base64.b64decode(
        obj.EntityDescriptor.Signature.KeyInfo.X509Data.X509Certificate.cdata
    )
    ssl = Popen(
        ["openssl", "x509", "-fingerprint", "-inform", "der", "-noout"],
        stdout=PIPE,
        stdin=PIPE,
    )
    out = ssl.communicate(input=der)[0]
    bts = out.decode().rstrip().split("=")[1].split(":")[0:20]
    fin = "".join(bts).lower()

    jac = {
        "url": "https://" + host + "/auth/users/saml/acs",
        "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
    }
    jsl = {
        "url": "https://" + host + "/auth/users/saml/sls",
        "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
    }
    jsp = {
        "entityId": "https://" + host + "/auth/users/saml/metadata",
        "assertionConsumerService": jac,
        "singleLogoutService": jsl,
        "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
    }
    jso = {"url": svc, "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"}
    jsu = {"url": svc, "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"}
    jid = {
        "entityId": endpoint,
        "singleSignOnService": jso,
        "singleLogoutService": jsu,
        "certFingerprint": fin,
    }
    stg = {"strict": "true", "debug": "true", "sp": jsp, "idp": jid}
    settings_content = json.dumps(stg, indent=4)
    run_cmd(f"""kubectl create secret generic indico-sso-secrets --from-literal=settings.json='{settings_content}'""")

@infra.command("download-apidata")
@click.pass_context
@click.argument("version", required=True, type=str)
@click.option(
    "--extract/--no-extract",
    default=True,
    show_default=True,
    help="Automatically extract the downloaded TAR",
)
@options_wrapper()
def download_api_data(ctx, version, *, extract, deployment_root, **kwargs):
    """
    Download VERSION of API data TAR from google cloud to local --deployment-root.
    Un-tar the file into a directory of the same name, also in the deployment-root
    VERSION is something like "v7".

    Requires Authentication with GSutil to download the TAR, but will attempt to auth with an existing key if it exists.

    Will not download TAR if it already exists.
    Will not extract the TAR if the data directory already exists in --deployment-root
    """
    auth_with_gsutil(deployment_root)
    download_indicoapi_data(deployment_root, version=version, extract=extract)


for command_group in [single_node, gke, eks, aks]:
    infra.add_command(command_group)
