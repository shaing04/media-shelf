import click
import random as _random
from datetime import date
from shelf import storage

TYPES = ["book", "movie", "show", "game"]
STATUSES = ["to-read", "to-watch", "to-play", "reading", "watching", "playing", "done"]

DONE_VERB = {
    "book": "Read",
    "movie": "Watched",
    "show": "Watched",
    "game": "Played",
}


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
@click.option("--sort", default=None, type=click.Choice(["title", "type", "status", "rating", "date"]), help="Sort by field")
def list_entries(media_type, status, rating, sort):
    """List media entries with optional filters and sorting."""
    entries = storage.load()

    if media_type:
        entries = [e for e in entries if e["type"] == media_type]
    if status:
        entries = [e for e in entries if e["status"] == status]
    if rating is not None:
        entries = [e for e in entries if e["rating"] == rating]

    if sort == "title":
        entries = sorted(entries, key=lambda e: e["title"].lower())
    elif sort == "type":
        entries = sorted(entries, key=lambda e: (e["type"], e["title"].lower()))
    elif sort == "status":
        entries = sorted(entries, key=lambda e: (STATUSES.index(e["status"]), e["title"].lower()))
    elif sort == "rating":
        entries = sorted(entries, key=lambda e: (e["rating"] is None, -(e["rating"] or 0)))
    elif sort == "date":
        entries = sorted(entries, key=lambda e: e["added_date"])

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


@main.command()
@click.argument("entry_id", metavar="ID", type=int)
def done(entry_id):
    """Mark an entry as done (read/watched/played based on type)."""
    entries = storage.load()
    entry = _find(entries, entry_id)

    if entry is None:
        click.echo(f"Error: no entry with ID {entry_id}.", err=True)
        raise SystemExit(1)

    entry["status"] = "done"
    storage.save(entries)
    verb = DONE_VERB[entry["type"]]
    click.echo(f"{verb}: {entry['title']}")


@main.command("random")
@click.option("--type", "media_type", default=None, type=click.Choice(TYPES), help="Filter by type")
def random_entry(media_type):
    """Pick a random entry that isn't done yet."""
    entries = storage.load()
    pool = [e for e in entries if e["status"] != "done"]

    if media_type:
        pool = [e for e in pool if e["type"] == media_type]

    if not pool:
        click.echo("Nothing to pick from.")
        return

    e = _random.choice(pool)
    click.echo(f"ID:     {e['id']}")
    click.echo(f"Title:  {e['title']}")
    click.echo(f"Type:   {e['type']}")
    click.echo(f"Status: {e['status']}")
    click.echo(f"Rating: {e['rating'] if e['rating'] is not None else '---'}")
    click.echo(f"Note:   {e['note'] if e['note'] else '---'}")


@main.command()
def stats():
    """Show summary statistics for your shelf."""
    entries = storage.load()

    if not entries:
        click.echo("No entries yet.")
        return

    click.echo("By type:")
    for t in TYPES:
        count = sum(1 for e in entries if e["type"] == t)
        click.echo(f"  {t}: {count}")

    click.echo("\nBy status:")
    for s in STATUSES:
        count = sum(1 for e in entries if e["status"] == s)
        if count:
            click.echo(f"  {s}: {count}")

    click.echo("\nAverage rating by type:")
    for t in TYPES:
        ratings = [e["rating"] for e in entries if e["type"] == t and e["rating"] is not None]
        if ratings:
            click.echo(f"  {t}: {sum(ratings) / len(ratings):.1f}")
        else:
            click.echo(f"  {t}: N/A")
