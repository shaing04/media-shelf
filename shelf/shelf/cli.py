import click
from datetime import date
from shelf import storage

TYPES = ["book", "movie", "show", "game"]
STATUSES = ["to-read", "to-watch", "to-play", "reading", "watching", "playing", "done"]


@click.group()
def main():
    pass


@main.command()
@click.argument("title")
@click.option("--type", "media_type", required=True, type=click.Choice(TYPES), help="Media type")
@click.option("--status", required=True, type=click.Choice(STATUSES), help="Current status")
@click.option("--note", default=None, help="Optional note")
def add(title, media_type, status, note):
    """Add a new media entry."""
    entries = storage.load()
    entry = {
        "id": storage.next_id(entries),
        "title": title,
        "type": media_type,
        "status": status,
        "rating": None,
        "note": note,
        "added_date": date.today().isoformat(),
    }
    entries.append(entry)
    storage.save(entries)
    click.echo(f"Added: {title} ({media_type})")


@main.command("list")
@click.option("--type", "media_type", default=None, type=click.Choice(TYPES), help="Filter by type")
@click.option("--status", default=None, type=click.Choice(STATUSES), help="Filter by status")
@click.option("--rating", default=None, type=float, help="Filter by rating")
def list_entries(media_type, status, rating):
    """List media entries with optional filters."""
    entries = storage.load()

    if media_type:
        entries = [e for e in entries if e["type"] == media_type]
    if status:
        entries = [e for e in entries if e["status"] == status]
    if rating is not None:
        entries = [e for e in entries if e["rating"] == rating]

    if not entries:
        click.echo("No entries found.")
        return

    id_w = max(len(str(e["id"])) for e in entries)
    id_w = max(id_w, 2)
    title_w = max(len(e["title"]) for e in entries)
    title_w = max(title_w, 5)
    type_w = max(len(e["type"]) for e in entries)
    type_w = max(type_w, 4)
    status_w = max(len(e["status"]) for e in entries)
    status_w = max(status_w, 6)
    rating_w = 6

    header = (
        f"{'ID':<{id_w}}  {'Title':<{title_w}}  {'Type':<{type_w}}  "
        f"{'Status':<{status_w}}  {'Rating':<{rating_w}}"
    )
    separator = "-" * len(header)
    click.echo(header)
    click.echo(separator)

    for e in entries:
        rating_str = str(e["rating"]) if e["rating"] is not None else "---"
        click.echo(
            f"{e['id']:<{id_w}}  {e['title']:<{title_w}}  {e['type']:<{type_w}}  "
            f"{e['status']:<{status_w}}  {rating_str:<{rating_w}}"
        )
