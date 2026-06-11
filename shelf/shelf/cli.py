import click
from datetime import date
from shelf import storage

TYPES = ["book", "movie", "show", "game"]
STATUSES = ["to-read", "to-watch", "to-play", "reading", "watching", "playing", "done"]


@click.group()
def main():
    pass


def _print_table(entries: list[dict]) -> None:
    id_w = max(max(len(str(e["id"])) for e in entries), 2)
    title_w = max(max(len(e["title"]) for e in entries), 5)
    type_w = max(max(len(e["type"]) for e in entries), 4)
    status_w = max(max(len(e["status"]) for e in entries), 6)
    rating_w = 6

    header = (
        f"{'ID':<{id_w}}  {'Title':<{title_w}}  {'Type':<{type_w}}  "
        f"{'Status':<{status_w}}  {'Rating':<{rating_w}}"
    )
    click.echo(header)
    click.echo("-" * len(header))

    for e in entries:
        rating_str = str(e["rating"]) if e["rating"] is not None else "---"
        click.echo(
            f"{e['id']:<{id_w}}  {e['title']:<{title_w}}  {e['type']:<{type_w}}  "
            f"{e['status']:<{status_w}}  {rating_str:<{rating_w}}"
        )


def _find(entries: list[dict], entry_id: int) -> dict | None:
    return next((e for e in entries if e["id"] == entry_id), None)


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

    _print_table(entries)


@main.command()
@click.argument("entry_id", metavar="ID", type=int)
@click.option("--status", default=None, type=click.Choice(STATUSES), help="New status")
@click.option("--rating", default=None, type=float, help="Rating")
@click.option("--note", default=None, help="Note")
def update(entry_id, status, rating, note):
    """Update an existing entry by ID."""
    entries = storage.load()
    entry = _find(entries, entry_id)

    if entry is None:
        click.echo(f"Error: no entry with ID {entry_id}.", err=True)
        raise SystemExit(1)

    if status is not None:
        entry["status"] = status
    if rating is not None:
        entry["rating"] = rating
    if note is not None:
        entry["note"] = note

    storage.save(entries)
    click.echo(f"Updated: {entry['title']}")


@main.command()
@click.argument("entry_id", metavar="ID", type=int)
def delete(entry_id):
    """Delete an entry by ID."""
    entries = storage.load()
    entry = _find(entries, entry_id)

    if entry is None:
        click.echo(f"Error: no entry with ID {entry_id}.", err=True)
        raise SystemExit(1)

    entries.remove(entry)
    storage.save(entries)
    click.echo(f"Deleted: {entry['title']}")


@main.command()
@click.argument("query")
def search(query):
    """Search entries by title (case-insensitive)."""
    entries = storage.load()
    needle = query.lower()
    matches = [e for e in entries if needle in e["title"].lower()]

    if not matches:
        click.echo("No results found.")
        return

    _print_table(matches)
