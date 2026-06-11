# shelf

A command-line tool for tracking books, movies, TV shows, and games. Entries are stored locally in `~/.shelf/data.json` so your list is always available offline and never tied to an account.

## Usage

Install inside an existing uv project. If you don't have one, create one first:

```
uv init my-project && cd my-project
uv add "git+https://github.com/shaing04/media-shelf.git"
```

> **WSL users:** work from your native Linux home directory (`~/`) and not from `/mnt/c/` to avoid I/O errors.

All commands are prefixed with `uv run`:

---

### Adding entries

```
uv run shelf add "Dune" --type book --status to-read
uv run shelf add "The Bear" --type show --status watching --note "season 2 is great"
```

| Flag | Required | Accepted values | Description |
|------|----------|-----------------|-------------|
| `--type` | Yes | `book`, `movie`, `show`, `game` | The kind of media you're tracking |
| `--status` | Yes | `to-read`, `to-watch`, `to-play` — not started yet; `reading`, `watching`, `playing` — in progress; `done` — finished | Where you currently are with this entry |
| `--note` | No | Any text | A short free-text note attached to the entry |

---

### Listing entries

```
uv run shelf list
uv run shelf list --type book
uv run shelf list --status done
uv run shelf list --rating 9
uv run shelf list --sort title
uv run shelf list --type book --sort status
```

| Flag | Accepted values | Description |
|------|-----------------|-------------|
| `--type` | `book`, `movie`, `show`, `game` | Only show entries of this type |
| `--status` | `to-read`, `to-watch`, `to-play`, `reading`, `watching`, `playing`, `done` | Only show entries with this status |
| `--rating` | Any number (e.g. `8`, `9.5`) | Only show entries with this exact rating |
| `--sort` | `title`, `type`, `status`, `rating`, `date` | Order results by this field; rated entries appear first when sorting by rating |

---

### Marking as done

```
uv run shelf done <id>
```

Sets the entry's status to `done` and prints a type-aware confirmation: `Read` for books, `Watched` for movies and shows, `Played` for games.

---

### Updating an entry

```
uv run shelf update <id> --status reading
uv run shelf update <id> --rating 9.5 --note "even better the second time"
```

| Flag | Accepted values | Description |
|------|-----------------|-------------|
| `--status` | `to-read`, `to-watch`, `to-play`, `reading`, `watching`, `playing`, `done` | Change the current status |
| `--rating` | Any number (e.g. `7`, `8.5`) | Set or update the numeric rating |
| `--note` | Any text | Set or update the note |

All flags are optional — only the fields you provide are changed.

---

### Deleting an entry

```
uv run shelf delete <id>
```

Permanently removes the entry with the given ID.

---

### Searching by title

```
uv run shelf search "bear"
```

Case-insensitive substring match against all entry titles. Results are shown in the same table format as `list`.

---

### Random pick

```
uv run shelf random
uv run shelf random --type book
```

Picks a random entry that isn't marked as `done` yet. Use `--type` to limit the pick to a specific media type.

---

### Stats

```
uv run shelf stats
```

Prints a summary of your shelf: total entries broken down by type and by status, and the average rating per type.

---

### Exporting

```
uv run shelf export                        # markdown → shelf_export.md (default)
uv run shelf export --format csv           # CSV → shelf_export.csv
uv run shelf export -o ~/backup/shelf.md   # custom output path
```

| Flag | Description |
|------|-------------|
| `--format` | Output format: `markdown` (default) or `csv` |
| `-o` / `--output` | File path to write to (defaults to `shelf_export.md` or `shelf_export.csv`) |

Markdown export groups entries by type in tables. CSV export includes all fields with a header row and imports cleanly into spreadsheets.
