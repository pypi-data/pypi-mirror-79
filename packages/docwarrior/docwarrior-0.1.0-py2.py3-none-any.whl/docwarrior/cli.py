"""Console script for docwarrior."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for docwarrior."""
    click.echo("Replace this message by putting your code into "
               "docwarrior.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    click.echo("args: ", args)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
