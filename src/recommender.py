import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict, field

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: str = ""
    mood_tags: List[str] = field(default_factory=list)
    explicit: bool = False
    language: str = ""

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_popularity: Optional[int] = None
    favorite_decade: Optional[str] = None
    favorite_mood_tags: List[str] = field(default_factory=list)
    allow_explicit: bool = True
    language: Optional[str] = None

class RankingStrategy:
    """Base ranking strategy: decides how much genre, mood, and energy are worth."""
    name = "Base"
    genre_weight = 2.0
    mood_weight = 1.0
    energy_weight = 1.0

    def score_core(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        """Score the genre, mood, and energy rules using this strategy's weights."""
        score = 0.0
        reasons = []

        if song["genre"] == user_prefs["genre"]:
            score += self.genre_weight
            reasons.append(f"genre match (+{self.genre_weight:.1f})")

        if song["mood"] == user_prefs["mood"]:
            score += self.mood_weight
            reasons.append(f"mood match (+{self.mood_weight:.1f})")

        energy_points = self.energy_weight * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

        return score, reasons

class GenreFirst(RankingStrategy):
    """Genre matters most (the original weights)."""
    name = "Genre-First"

class MoodFirst(RankingStrategy):
    """Mood matters most, so songs that fit the feeling beat songs that only fit the genre."""
    name = "Mood-First"
    genre_weight = 1.0
    mood_weight = 2.0

class EnergyFocused(RankingStrategy):
    """Energy closeness matters most; genre and mood are small bonuses."""
    name = "Energy-Focused"
    genre_weight = 0.5
    mood_weight = 0.5
    energy_weight = 3.0

STRATEGIES = {
    "genre_first": GenreFirst(),
    "mood_first": MoodFirst(),
    "energy_focused": EnergyFocused(),
}

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], strategy: Optional[RankingStrategy] = None):
        self.songs = songs
        self.strategy = strategy

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for the user, highest score first."""
        prefs = _profile_to_prefs(user)
        return sorted(self.songs, key=lambda s: score_song(prefs, asdict(s), self.strategy)[0], reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of why the song scored the way it did."""
        _, reasons = score_song(_profile_to_prefs(user), asdict(song), self.strategy)
        return ", ".join(reasons)

def _profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the user_prefs dict format used by score_song."""
    prefs = {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
        "mood_tags": user.favorite_mood_tags,
        "allow_explicit": user.allow_explicit,
    }
    if user.target_popularity is not None:
        prefs["popularity"] = user.target_popularity
    if user.favorite_decade is not None:
        prefs["decade"] = user.favorite_decade
    if user.language is not None:
        prefs["language"] = user.language
    return prefs

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]:
                row[key] = float(row[key])
            row["popularity"] = int(row["popularity"])
            row["mood_tags"] = row["mood_tags"].split(";") if row["mood_tags"] else []
            row["explicit"] = row["explicit"] == "1"
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict, strategy: Optional[RankingStrategy] = None) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return (score, reasons); defaults to Genre-First."""
    strategy = strategy or GenreFirst()
    score, reasons = strategy.score_core(user_prefs, song)

    if "likes_acoustic" in user_prefs:
        is_acoustic = song["acousticness"] >= 0.5
        if user_prefs["likes_acoustic"] == is_acoustic:
            score += 0.5
            reasons.append("acoustic preference match (+0.5)")

    if "popularity" in user_prefs:
        popularity_points = 0.5 * (1 - abs(song["popularity"] - user_prefs["popularity"]) / 100)
        score += popularity_points
        reasons.append(f"popularity closeness (+{popularity_points:.2f})")

    if "decade" in user_prefs and song["release_decade"] == user_prefs["decade"]:
        score += 0.5
        reasons.append(f"{song['release_decade']} decade match (+0.5)")

    shared_tags = [tag for tag in song["mood_tags"] if tag in user_prefs.get("mood_tags", [])]
    if shared_tags:
        tag_points = 0.3 * len(shared_tags)
        score += tag_points
        reasons.append(f"mood tags {'/'.join(shared_tags)} (+{tag_points:.1f})")

    if not user_prefs.get("allow_explicit", True) and song["explicit"]:
        score -= 1.0
        reasons.append("explicit content penalty (-1.0)")

    if "language" in user_prefs and song["language"] == user_prefs["language"]:
        score += 0.5
        reasons.append(f"{song['language']} language match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, strategy: Optional[RankingStrategy] = None) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, strategy)
        scored.append((song, score, ", ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
