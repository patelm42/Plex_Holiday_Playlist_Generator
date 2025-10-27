from plexapi.server import PlexServer
import re

# ====== CONFIGURATION ======
PLEX_URL = "http://localhost:32400"
PLEX_TOKEN = "YOUR_PLEX_TOKEN_HERE"
PLAYLIST_NAME = "Christmas TV Episodes"

# Common Christmas keywords to match in titles or summaries
CHRISTMAS_KEYWORDS = [
    "christmas", "xmas", "holiday", "santa", "elf", "snow", "noel",
    "winter wonderland", "yuletide", "mistletoe", "nativity"
]

def is_christmas_episode(episode):
    """Determine if an episode is Christmas-themed."""
    text = f"{episode.title.lower()} {episode.summary.lower() if episode.summary else ''}"
    return any(re.search(rf"\b{k}\b", text) for k in CHRISTMAS_KEYWORDS)

def main():
    # Connect to Plex
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print("Connected to Plex server:", plex.friendlyName)

    # Get all shows
    shows = plex.library.section("TV Shows")
    all_episodes = shows.search(libtype="episode")
    print(f"Scanning {len(all_episodes)} episodes...")

    # Find Christmas episodes
    christmas_eps = [ep for ep in all_episodes if is_christmas_episode(ep)]
    print(f"Found {len(christmas_eps)} Christmas episodes!")

    # Remove duplicates and sort
    unique_eps = {ep.ratingKey: ep for ep in christmas_eps}.values()
    sorted_eps = sorted(unique_eps, key=lambda e: (e.grandparentTitle, e.seasonNumber, e.index))

    # Create or update playlist
    playlist = next((p for p in plex.playlists() if p.title == PLAYLIST_NAME), None)
    if playlist:
        playlist.editItems(list(sorted_eps))
        print(f"Updated playlist '{PLAYLIST_NAME}' with {len(sorted_eps)} episodes.")
    else:
        plex.createPlaylist(PLAYLIST_NAME, list(sorted_eps))
        print(f"Created new playlist '{PLAYLIST_NAME}' with {len(sorted_eps)} episodes.")

if __name__ == "__main__":
    main()
