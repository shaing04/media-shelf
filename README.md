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

```
# Add entries
uv run shelf add "Dune" --type book --status to-read
uv run shelf add "The Bear" --type show --status watching --note "season 2 is great"
uv run shelf add "Inception" --type movie --status to-watch
uv run shelf add "Elden Ring" --type game --status playing
```

`--type` accepts: `book`, `movie`, `show`, `game`  
`--status` accepts: `to-read`, `to-watch`, `to-play`, `reading`, `watching`, `playing`, `done`  
`--note` is optional.

```
# List entries
uv run shelf list
uv run shelf list --type book
uv run shelf list --status done
uv run shelf list --rating 9
uv run shelf list --sort title        # sort by: title, type, status, rating, date

# Mark as done (verb is chosen automatically: Read / Watched / Played)
uv run shelf done 1

# Update an entry (all flags optional, only provided fields are changed)
uv run shelf update 1 --status reading
uv run shelf update 1 --rating 9.5 --note "even better the second time"

# Delete an entry
uv run shelf delete 2

# Search by title (case-insensitive)
uv run shelf search "bear"

# Pick a random entry that isn't done yet
uv run shelf random
uv run shelf random --type book

# Show stats (counts by type and status, average rating per type)
uv run shelf stats

# Export your shelf
uv run shelf export                        # markdown → shelf_export.md
uv run shelf export --format csv           # CSV → shelf_export.csv
uv run shelf export -o ~/backup/shelf.md   # custom output path
```
