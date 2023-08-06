import logging
import sys
from collections import deque
from os import chdir, path

import click

from nomnomdata.auth import NNDAuth

_logger = logging.getLogger(__name__)


@click.group(name="deploy")
def deploy():
    pass


@deploy.command(name="task")
@click.option(
    "-n",
    "--nominode",
    help="Specify the nomitall to update [nomitall-prod,nomitall-stage,custom_url]",
)
@click.option(
    "-c",
    "--channel",
    default="dev",
    type=click.Choice(["stable", "beta", "dev"]),
    help="Channel to deploy to",
)
@click.option("--dry-run", is_flag=True, help="Build engine but do not deploy")
@click.option(
    "-y", "--yes", "skip_confirm", is_flag=True, help="Skip confirmation prompt"
)
def task(nominode, channel, dry_run, skip_confirm):
    "Deploy a task configuration to a nominode"
    print(nominode, dry_run, channel, skip_confirm)
