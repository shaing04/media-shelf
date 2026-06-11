# shelf

A command-line tool for tracking books, movies, TV shows, and games. Entries are stored locally in `~/.shelf/data.json` so your list is always available offline and never tied to an account.

## Usage

Install with:

```
uv add "git+https://github.com/shaing04/media-shelf.git"
```

### Adding entries

```
shelf add "Dune" --type book --status done
shelf add "The Bear" --type show --status watching --note "season 2 is great"
shelf add "Inception" --type movie --status to-watch
shelf add "Elden Ring" --type game --status playing
```

`--type` accepts: `book`, `movie`, `show`, `game`  
`--status` accepts: `to-read`, `to-watch`, `to-play`, `reading`, `watching`, `playing`, `done`  
`--note` is optional.

### Listing entries

```
shelf list                          # show all entries
shelf list --type book              # filter by type
shelf list --status done            # filter by status
shelf list --rating 9               # filter by rating
shelf list --sort title             # sort by title, type, status, rating, or date
shelf list --type book --sort status
```

### Marking as done

```
shelf done 1    # prints "Read: Dune" / "Watched: The Bear" / "Played: Elden Ring"
```

Picks the right verb automatically based on media type.

### Updating an entry

```
shelf update 1 --status reading
shelf update 1 --rating 9.5 --note "even better the second time"
```

All flags (`--status`, `--rating`, `--note`) are optional — only what's provided is changed.

### Deleting an entry

```
shelf delete 2
```

### Searching by title

```
shelf search "bear"    # case-insensitive substring match, prints results as a table
```

### Random pick

```
shelf random            # pick a random entry that isn't done yet
shelf random --type book
```

### Stats

```
shelf stats    # total entries by type and status, average rating per type
```

### Exporting

```
shelf export                        # exports to shelf_export.md (default)
shelf export --format csv           # exports to shelf_export.csv
shelf export -o ~/backup/shelf.md   # custom output path
```

Markdown export groups entries by type in tables. CSV export includes all fields and imports cleanly into spreadsheets.
