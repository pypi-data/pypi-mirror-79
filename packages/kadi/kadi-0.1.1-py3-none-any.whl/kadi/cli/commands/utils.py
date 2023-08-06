# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys

import click
from flask import current_app
from jinja2 import Template

from kadi.cli.main import kadi
from kadi.cli.utils import danger
from kadi.cli.utils import echo
from kadi.cli.utils import run_command
from kadi.cli.utils import success


DEFAULT_USER = "kadi"
DEFAULT_GROUP = "www-data"
DEFAULT_CONFIG_FILE = "/opt/kadi/config/kadi.py"


@kadi.group()
def utils():
    """Miscellaneous utility commands."""


@utils.command()
def secret_key():
    """Generate a random secret key."""
    echo(os.urandom(24).hex())


@utils.command()
def config():
    """Print the current app configuration."""
    config = [f"{k}: {v}" for k, v in current_app.config.items()]
    for item in sorted(config):
        echo(item)


def _generate_config(template_name, outfile=None, **kwargs):
    template_path = os.path.join(
        current_app.root_path, "cli", "templates", template_name
    )

    with open(template_path) as file:
        template = Template(file.read())

    rendered_template = template.render(**kwargs)

    if outfile is not None:
        if os.path.exists(outfile.name):
            danger(f"'{outfile.name}' already exists.")
            sys.exit(1)

        outfile.write(rendered_template)
        outfile.write("\n")

        success(f"File '{outfile.name}' generated successfully.")
    else:
        echo("\n" + rendered_template, bold=True)


@utils.command()
@click.option("--out", type=click.File(mode="w"), help="Output file (e.g. kadi.conf).")
def apache(out):
    """Generate a basic Apache web server configuration."""
    server_name = current_app.config["SERVER_NAME"]

    cert_file = click.prompt(
        "SSL/TLS certificate file", default=f"/etc/ssl/certs/{server_name}.pem"
    )
    key_file = click.prompt(
        "SSL/TLS key file", default=f"/etc/ssl/private/{server_name}.key"
    )
    chain_file = click.prompt(
        "SSL/TLS intermediate certificates chain file (optional)", default=""
    )
    log_dir = click.prompt("Base directory for server logs", default="/var/log/apache2")

    anonip_bin = None
    if click.confirm(
        "Anonymize IP addresses in access logs? Note that this will install the"
        " 'anonip' package in the current virtual environment if it is not installed"
        " already."
    ):
        run_command(["pip", "install", "anonip"])
        anonip_bin = os.path.join(sys.base_prefix, "bin", "anonip")

    _generate_config(
        "kadi.conf",
        outfile=out,
        server_name=server_name,
        kadi_root=current_app.root_path,
        storage_path=current_app.config["STORAGE_PATH"],
        misc_uploads_path=current_app.config["MISC_UPLOADS_PATH"],
        cert_file=cert_file,
        key_file=key_file,
        chain_file=chain_file,
        log_dir=log_dir,
        anonip_bin=anonip_bin,
    )


@utils.command()
@click.option("--out", type=click.File(mode="w"), help="Output file (e.g. kadi.ini).")
def uwsgi(out):
    """Generate a basic uWSGI application server configuration."""
    uid = click.prompt("User the server will run under", default=DEFAULT_USER)
    gid = click.prompt("Group the server will run under", default=DEFAULT_GROUP)
    kadi_config = click.prompt("Kadi config file", default=DEFAULT_CONFIG_FILE)

    _generate_config(
        "kadi.ini",
        outfile=out,
        kadi_root=current_app.root_path,
        venv_path=sys.base_prefix,
        uid=uid,
        gid=gid,
        kadi_config=kadi_config,
    )


@utils.command()
@click.option(
    "--out", type=click.File(mode="w"), help="Output file (e.g. kadi-celery.service)."
)
def celery(out):
    """Generate a basic systemd unit file for Celery."""
    uid = click.prompt("User the service will run under", default=DEFAULT_USER)
    gid = click.prompt("Group the service will run under", default=DEFAULT_GROUP)
    kadi_config = click.prompt("Kadi config file", default=DEFAULT_CONFIG_FILE)

    _generate_config(
        "kadi-celery.service",
        outfile=out,
        kadi_bin=os.path.join(sys.base_prefix, "bin", "kadi"),
        uid=uid,
        gid=gid,
        kadi_config=kadi_config,
    )


@utils.command()
@click.option(
    "--out",
    type=click.File(mode="w"),
    help="Output file (e.g. kadi-celerybeat.service).",
)
def celerybeat(out):
    """Generate a basic systemd unit file for Celery beat."""
    uid = click.prompt("User the service will run under", default=DEFAULT_USER)
    gid = click.prompt("Group the service will run under", default=DEFAULT_GROUP)
    kadi_config = click.prompt("Kadi config file", default=DEFAULT_CONFIG_FILE)

    _generate_config(
        "kadi-celerybeat.service",
        outfile=out,
        kadi_bin=os.path.join(sys.base_prefix, "bin", "kadi"),
        uid=uid,
        gid=gid,
        kadi_config=kadi_config,
    )
