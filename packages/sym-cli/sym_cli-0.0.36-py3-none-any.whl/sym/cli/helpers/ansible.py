from contextlib import ExitStack
from textwrap import dedent
from typing import Optional, Tuple

from ..decorators import intercept_errors, run_subprocess
from ..helpers.config import SymConfigFile
from ..helpers.contexts import push_envs
from ..helpers.params import get_ssh_user
from ..helpers.ssh import SSHKeyPath
from ..saml_clients.aws_profile import AwsCredentialsPath, AwsProfile

AnsibleSSHPath = "ansible/ssh"
AnsibleSSHProfile = "sym-ansible"


def create_ssh_bin(client):
    proxy_client = client.clone(klass=AwsProfile, resource=AnsibleSSHProfile)
    ssh_bin = proxy_client.subconfig(AnsibleSSHPath)
    # fmt: off
    ssh_bin.put(dedent(
        f"""
        #!/bin/bash

        export PYTHONUNBUFFERED=1

        sym {proxy_client.cli_options} ssh {proxy_client.resource} "$@"
        """
    ).lstrip())
    # fmt: on
    ssh_bin.path.chmod(0o755)
    return ssh_bin


def run_ansible(
    client: "SAMLClient",
    command: Tuple[str, ...],
    ansible_aws_profile: Optional[str],
    ansible_sym_resource: Optional[str],
    binary: str = "ansible",
):
    if ansible_aws_profile:
        client = client.clone(klass=AwsProfile, resource=ansible_aws_profile)
    elif ansible_sym_resource:
        client = client.clone(resource=ansible_sym_resource)

    args = [
        binary,
        *command,
        f"--user={get_ssh_user()}",
        f"--private-key={str(SymConfigFile(file_name=SSHKeyPath))}",
    ]
    if client.debug:
        args.append("-vvv")

    client.write_creds(path=AwsCredentialsPath, profile=AnsibleSSHProfile)

    with push_envs(
        {
            "ANSIBLE_SSH_EXECUTABLE": str(create_ssh_bin(client)),
            "ANSIBLE_SSH_RETRIES": str(2),
        }
    ):
        client.exec(*args, suppress_=True)
