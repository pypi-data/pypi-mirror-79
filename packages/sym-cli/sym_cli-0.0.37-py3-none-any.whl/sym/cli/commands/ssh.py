import re
from datetime import timedelta
from functools import wraps
from typing import Optional, Sequence

import click

from ..decorators import loses_interactivity, require_bins, require_login
from ..helpers.boto import host_to_instance
from ..helpers.global_options import GlobalOptions
from ..helpers.keywords_to_options import keywords_to_options
from ..helpers.options import resource_argument
from ..helpers.ssh import ensure_ssh_key, raw_ssh, start_ssh_session
from .sym import sym

SSH_MAN = """
     ssh [-AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface] [-b bind_address] [-c cipher_spec]
         [-D [bind_address:]port] [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
         [-i identity_file] [-J destination] [-L address] [-l login_name] [-m mac_spec] [-O ctl_cmd]
         [-o option] [-p port] [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
         [-w local_tun[:remote_tun]] destination [command]
"""


def parse_ssh_man(ssh_man):
    flags_pattern = re.compile(r"ssh \[-(\w+)\]")
    options_pattern = re.compile(r"\[-(\w) (\S+)\]")

    flags = list(flags_pattern.search(ssh_man)[1])
    options = options_pattern.findall(ssh_man)

    return (flags, options)


def ssh_options(fn):
    flags, options = parse_ssh_man(SSH_MAN)
    for flag in flags:
        fn = click.option(f"-{flag}", flag, is_flag=True)(fn)
    for (option, name) in options:
        fn = click.option(f"-{option}", metavar=f"<{name}>", multiple=True)(fn)
    return fn


@sym.command(
    short_help="Start a SSH session", context_settings={"ignore_unknown_options": True}
)
@resource_argument
@ssh_options
@click.option("-p", "--port", default=22, type=int, show_default=True)
@click.argument("destination", required=False)
@click.argument("command", nargs=-1, required=False)
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("aws", "session-manager-plugin", "ssh")
@require_login
def ssh(
    options: GlobalOptions,
    resource: str,
    destination: Optional[str],
    port: int,
    command: Sequence[str],
    **kwargs,
) -> None:
    ssh_args = keywords_to_options([kwargs])

    if not destination:
        raw_ssh({"p": str(port)}, *ssh_args)

    client = options.create_saml_client(resource)
    instance = host_to_instance(client, destination)
    start_ssh_session(client, instance, port, args=ssh_args, command=command, wrap=False)

