# shelf

A command-line tool for tracking books, movies, TV shows, and games. Entries are stored locally in `~/.shelf/data.json` so your list is always available offline and never tied to an account.

## Usage

```
# Add an entry (--type and --status are required; --note is optional)
shelf add "Dune" --type book --status done
shelf add "The Bear" --type show --status watching --note "season 2 is great"
shelf add "Elden Ring" --type game --status to-play

# List all entries
shelf list

# Filter by type, status, or rating
shelf list --type book
shelf list --status done
shelf list --rating 9
```
