"""
Command line runner for the Music Recommender Simulation.

Runs the recommender for several user profiles and prints the top results.
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    # Edge case: conflicting preferences (sad mood but very high energy)
    "Sad but Energetic": {"genre": "indie", "mood": "sad", "energy": 0.9},
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {name} ===")
        print(f"Profile: {user_prefs}\n")
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{i}. {song['title']} - Score: {score:.2f}")
            print(f"   Because: {explanation}")


if __name__ == "__main__":
    main()
