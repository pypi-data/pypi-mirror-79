#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allo
import click
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.group(invoke_without_command=True, help="Outil de télémaintenance et de mise à jour automatique Libriciel-SCOP")
@click.version_option()
@click.pass_context
def cmd(ctx):
    print("ALLO-NG v{} - Utilitaire de mise a jour automatique et telemaintenance".format(allo.__version__))
    """Allo CLI program."""
    if not ctx.invoked_subcommand:
        from allo.ansible import AlloAnsible
        AlloAnsible().install_dependencies()
        from allo.core import TestingAllo
        TestingAllo("PROD", False)


@cmd.command(help="Installation des dependances allo")
def init():
    from allo.ansible import AlloAnsible
    AlloAnsible().install_dependencies()


@cmd.command(help="Association de l'instance")
def assoc():
    from allo.core import TestingAllo
    print("Mode association :")
    TestingAllo("PROD", True)


@cmd.command(help="Lancement de la télémaintenance")
def telem():
    from allo.telem import AlloTelem
    from allo.configloader import ConfigLoader
    AlloTelem(ConfigLoader("PROD").config).connect()


@cmd.command(help="Installation du produit")
def install():
    print("Installation du produit :")
