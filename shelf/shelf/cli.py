import click


@click.group()
def main():
    pass


@main.command()
def hello():
    click.echo("shelf is working")
