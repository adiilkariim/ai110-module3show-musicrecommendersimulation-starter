"""
Command line runner for the Music Recommender Simulation.

Runs the recommender for several user profiles and prints the top results.
"""

from src.recommender import load_songs, recommend_songs, STRATEGIES

# Ranking mode: "genre_first", "mood_first", or "energy_focused"
MODE = "genre_first"

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.8,
        "popularity": 80, "decade": "2020s", "mood_tags": ["uplifting", "sunny"],
        "allow_explicit": False, "language": "english",
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True,
        "popularity": 50, "decade": "2020s", "mood_tags": ["cozy", "focused"],
        "language": "instrumental",
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False,
        "popularity": 70, "decade": "2000s", "mood_tags": ["aggressive", "driving"],
        "language": "english",
    },
    # Edge case: conflicting preferences (sad mood but very high energy)
    "Sad but Energetic": {
        "genre": "indie", "mood": "sad", "energy": 0.9,
        "popularity": 40, "decade": "2010s", "mood_tags": ["lonely"],
        "language": "english",
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    strategy = STRATEGIES[MODE]
    print(f"Loaded songs: {len(songs)}")
    print(f"Ranking mode: {strategy.name}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy)

        print(f"\n=== {name} ===")
        print(f"Profile: {user_prefs}\n")
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{i}. {song['title']} - Score: {score:.2f}")
            print(f"   Because: {explanation}")


if __name__ == "__main__":
    main()
