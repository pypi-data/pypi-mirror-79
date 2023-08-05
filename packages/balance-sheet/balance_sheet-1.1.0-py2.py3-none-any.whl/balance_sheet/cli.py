import click
from . import program


@click.command()
def main():
    """A personal balance sheet running in SQLite and Python3"""
    program.Program().run()


if __name__ == "__main__":
    main()