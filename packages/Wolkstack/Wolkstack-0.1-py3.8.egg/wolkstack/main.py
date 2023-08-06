import sys
import click
from wolkstack.cli_tools import cli_tools

@click.group()
def fuck():
    """this sucks"""
    pass

@fuck.command(name='install', help='fuckity')
@click.option('--test1', default='1', help='test option')
def install_cmd(test1):
    click.echo('Hello world')

@click.command()
def initdb():
    click.echo('Initialized the database')

@click.group()
@click.version_option("1.0.0")
def main():
    """A CVE Search and Lookup CLI"""
    print("Hye")
    pass

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("CVE")
    main.add_command(initdb)
    main.add_command(cli_tools.cli_tools)
    main.add_command(fuck)
    main()
