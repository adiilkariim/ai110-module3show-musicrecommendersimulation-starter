# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch suggests the top 5 songs from a small catalog that best fit a listener's stated taste. The user describes what they want (favorite genre, mood, energy level, and optional extras like decade or language), and the system ranks every song by how well it matches.

- **Built for:** classroom exploration of how content-based recommenders turn data into suggestions.
- **Assumes:** the user knows their own taste and can describe it with simple labels and numbers.
- **Not intended for:** real users or a real music app. It has no listening history, only 20 fictional songs, and cannot learn or adapt. It should not be used to make decisions about which artists get exposure.

---

## 3. How the Model Works  

Think of it as a points game. Every song starts at zero, and earns points for each way it matches what the user asked for:

- **Same genre** as the user's favorite: the biggest reward (+2).
- **Same mood:** +1.
- **Energy:** the closer the song's energy is to what the user wants, the more points (up to +1). A song that is exactly right gets the full point; one that is far off gets almost nothing.
- **Acoustic or not:** +0.5 if it matches whether the user likes acoustic music.
- **Popularity:** up to +0.5 for being close to how popular the user wants songs to be.
- **Decade:** +0.5 if it was released in the user's favorite decade.
- **Mood tags:** +0.3 for each detailed tag (like "cozy" or "nostalgic") the user also likes.
- **Explicit lyrics:** −1 if the user wants clean songs and the song is explicit.
- **Language:** +0.5 if it matches the user's language.

After every song has a score, the system sorts them from highest to lowest and shows the top 5, along with the list of reasons that earned each song its points.

**Changes from the starter logic:** the starter only had empty placeholders. I implemented the scoring and ranking, added the acoustic rule using the `likes_acoustic` field, and added five new song attributes (popularity, release decade, mood tags, explicit, language) with their own rules.

---

## 4. Data  

- **Size:** 20 fictional songs in `data/songs.csv` (10 from the starter, 10 added by me).
- **Attributes (15):** title, artist, genre, mood, energy, tempo, valence, danceability, acousticness, popularity, release decade, mood tags, explicit, language (plus an id).
- **Genres (16):** lofi (3), pop (2), rock (2), and one song each of indie pop, ambient, jazz, synthwave, hip-hop, metal, classical, country, edm, r&b, indie, reggae, and blues.
- **Moods (15):** happy, chill, intense, relaxed, moody, focused, confident, angry, peaceful, nostalgic, euphoric, romantic, sad, melancholy, energetic.
- **What I added:** 10 songs to cover genres and moods missing from the starter, and 5 new columns.
- **What's missing:** no lyrics, no real listening data, very few songs per genre, mostly English songs, and nothing from many world music traditions. Values like "danceability" and labels like "sad" are made up and subjective.

---

## 5. Strengths  

- **Clear, specific taste profiles work well.** The Chill Lofi profile returns all three lofi songs first, then other calm acoustic songs (ambient, jazz), which matches my intuition.
- **Energy closeness behaves sensibly.** Low-energy users get calm songs and high-energy users get loud songs, instead of everyone getting the loudest songs.
- **Every recommendation is explainable.** Each result lists exactly which rules gave it points, so it is easy to see why a song ranked where it did.
- **Detailed mood tags help.** For the Sad but Energetic profile, "Smoke and Strings" (a lonely blues song) made the top 5 only because of its "lonely" tag.

---

## 6. Limitations and Bias 

**Main weakness: genre dominates, and energy fills the gaps.** A genre match is worth +2, more than any other single rule, so a song in the right genre but the wrong mood can still beat songs that fit the user's mood much better. "Gym Hero" ranks #2 for the happy pop listener even though it is intense and loses a point for explicit lyrics, simply because it is pop. Once the few songs in the user's genre are used up, the rest of the top 5 is decided mostly by energy, so users with very different tastes but similar energy levels get the same filler songs ("Storm Runner" shows up for three of the four profiles, and "Neon Overdrive" and "Gym Hero" for two each). Because most genres have only one song, a fan of reggae or blues gets one good match and then four songs that only match on energy, which creates a filter bubble around loudness rather than real taste.

**Other limitations:**

- **Exact text matching:** "indie pop" gets no genre credit for a "pop" fan, and "melancholy" gets no credit for a "sad" fan.
- **Subjective labels treated as facts:** "sad" or danceability 0.89 are guesses, but the system trusts them completely.
- **No learning:** it never uses skips, likes, or what similar users enjoy, so it cannot discover new tastes.
- **Language rule can favor English:** most songs are English or instrumental, so non-English listeners have very few language matches.

---

## 7. Evaluation  

I tested four profiles (three normal and one edge case with conflicting preferences) and looked at whether the top 5 "felt right" for that listener. I also ran a weight experiment (genre halved, energy doubled), described in the README.

### Profile outputs

```
=== High-Energy Pop ===
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'popularity': 80, 'decade': '2020s', 'mood_tags': ['uplifting', 'sunny'], 'allow_explicit': False, 'language': 'english'}

1. Sunrise City - Score: 6.07
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98), popularity closeness (+0.49), 2020s decade match (+0.5), mood tags uplifting/sunny (+0.6), english language match (+0.5)
2. Gym Hero - Score: 3.33
   Because: genre match (+2.0), energy closeness (+0.87), popularity closeness (+0.46), 2020s decade match (+0.5), explicit content penalty (-1.0), english language match (+0.5)
3. Rooftop Lights - Score: 2.71
   Because: mood match (+1.0), energy closeness (+0.96), popularity closeness (+0.46), mood tags uplifting (+0.3)
4. Island Breeze Sunday - Score: 1.94
   Because: energy closeness (+0.78), popularity closeness (+0.36), mood tags sunny (+0.3), english language match (+0.5)
5. Storm Runner - Score: 1.82
   Because: energy closeness (+0.89), popularity closeness (+0.43), english language match (+0.5)
```

```
=== Chill Lofi ===
Profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True, 'popularity': 50, 'decade': '2020s', 'mood_tags': ['cozy', 'focused'], 'language': 'instrumental'}

1. Midnight Coding - Score: 6.54
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98), acoustic preference match (+0.5), popularity closeness (+0.46), 2020s decade match (+0.5), mood tags cozy/focused (+0.6), instrumental language match (+0.5)
2. Library Rain - Score: 5.75
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.95), acoustic preference match (+0.5), popularity closeness (+0.49), mood tags cozy (+0.3), instrumental language match (+0.5)
3. Focus Flow - Score: 5.28
   Because: genre match (+2.0), energy closeness (+1.00), acoustic preference match (+0.5), popularity closeness (+0.48), 2020s decade match (+0.5), mood tags focused (+0.3), instrumental language match (+0.5)
4. Spacewalk Thoughts - Score: 3.30
   Because: mood match (+1.0), energy closeness (+0.88), acoustic preference match (+0.5), popularity closeness (+0.42), instrumental language match (+0.5)
5. Coffee Shop Stories - Score: 2.23
   Because: energy closeness (+0.97), acoustic preference match (+0.5), popularity closeness (+0.46), mood tags cozy (+0.3)
```

```
=== Deep Intense Rock ===
Profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False, 'popularity': 70, 'decade': '2000s', 'mood_tags': ['aggressive', 'driving'], 'language': 'english'}

1. Storm Runner - Score: 6.58
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.99), acoustic preference match (+0.5), popularity closeness (+0.48), 2000s decade match (+0.5), mood tags aggressive/driving (+0.6), english language match (+0.5)
2. Neon Overdrive - Score: 4.76
   Because: genre match (+2.0), energy closeness (+0.98), acoustic preference match (+0.5), popularity closeness (+0.48), mood tags driving (+0.3), english language match (+0.5)
3. Gym Hero - Score: 3.68
   Because: mood match (+1.0), energy closeness (+0.97), acoustic preference match (+0.5), popularity closeness (+0.41), mood tags aggressive (+0.3), english language match (+0.5)
4. Iron Tempest - Score: 3.10
   Because: energy closeness (+0.93), acoustic preference match (+0.5), popularity closeness (+0.38), 2000s decade match (+0.5), mood tags aggressive (+0.3), english language match (+0.5)
5. Sunrise City - Score: 2.36
   Because: energy closeness (+0.92), acoustic preference match (+0.5), popularity closeness (+0.44), english language match (+0.5)
```

```
=== Sad but Energetic ===
Profile: {'genre': 'indie', 'mood': 'sad', 'energy': 0.9, 'popularity': 40, 'decade': '2010s', 'mood_tags': ['lonely'], 'language': 'english'}

1. Empty Platform - Score: 5.22
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.43), popularity closeness (+0.49), 2010s decade match (+0.5), mood tags lonely (+0.3), english language match (+0.5)
2. Iron Tempest - Score: 1.91
   Because: energy closeness (+0.93), popularity closeness (+0.47), english language match (+0.5)
3. Storm Runner - Score: 1.85
   Because: energy closeness (+0.99), popularity closeness (+0.36), english language match (+0.5)
4. Neon Overdrive - Score: 1.81
   Because: energy closeness (+0.98), popularity closeness (+0.33), english language match (+0.5)
5. Smoke and Strings - Score: 1.80
   Because: energy closeness (+0.54), popularity closeness (+0.46), mood tags lonely (+0.3), english language match (+0.5)
```

### Comparing the profiles

- **High-Energy Pop vs. Chill Lofi:** The two lists have no songs in common. Pop gets upbeat, mostly loud songs (energy 0.58–0.93), while Lofi shifts entirely to quiet, acoustic, instrumental songs (energy 0.28–0.42). This makes sense because energy, acoustic preference, and language all point in opposite directions.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, so they share "Gym Hero", "Storm Runner", and "Sunrise City". The difference is why: Gym Hero is #2 for Pop because it is pop, but #3 for Rock because it is intense and aggressive. Same song, different reasons.
- **High-Energy Pop vs. Sad but Energetic:** Only "Storm Runner" is shared, and only as filler at the bottom. Pop has two pop songs to fill the top, but there is only one indie song, so the Sad profile runs out of real matches after #1 and fills the list with loud songs.
- **Chill Lofi vs. Deep Intense Rock:** No overlap at all. These are opposite ends of the catalog (calm, acoustic, instrumental vs. loud, electric, aggressive), which is exactly what should happen.
- **Chill Lofi vs. Sad but Energetic:** No overlap, even though the Sad profile's #1 song ("Empty Platform", energy 0.33) is actually calm, like lofi. It doesn't show up for Lofi because it fails on genre, mood, and language. It shows that the label rules matter more than the "sound".
- **Deep Intense Rock vs. Sad but Energetic:** They share three songs (Storm Runner, Neon Overdrive, Iron Tempest) because both want energy around 0.9. For the Sad profile these songs only score on energy, not on sadness, so the list doesn't really feel sad. This is the clearest example of energy taking over when the genre runs out.

### Why "Gym Hero" keeps showing up

In plain language: Gym Hero is a loud, intense workout song, but it is labeled "pop". The system gives the biggest reward to matching genre, so a happy pop fan gets Gym Hero at #2 even though it doesn't sound happy. It also shows up for the rock fan because it is intense and high energy. It is not that the system thinks Gym Hero is a great song. It just happens to tick a lot of boxes, and the system can't tell that the boxes it ticks are not the ones that matter most to each listener.

### What surprised me

- One genre match (+2) was enough to beat several smaller matches. I expected the extra attributes to make the lists more balanced, but they mostly made the scores bigger without changing who is on top.
- The edge case profile (sad but high energy) didn't "break" the system. Instead, it quietly ignored the "sad" part after the first song. That kind of silent failure is easy to miss.

---

## 8. Future Work  

- **Partial genre and mood matches:** give some credit for related labels (e.g. "indie pop" for a "pop" fan, "melancholy" for "sad").
- **Diversity in the top 5:** penalize songs from an artist or genre already in the list, so users don't get the same artist twice or only loud filler songs.
- **Balance the weights:** lower the genre weight or scale it by how many songs exist in that genre, so small genres don't run out of matches so fast.
- **Use behavior data:** add simulated likes and skips so the system can learn a user's taste instead of relying only on labels.

---

## 9. Personal Reflection  

<!-- Write this section yourself, in your own words. Prompts from the assignment:
- What was your biggest learning moment during this project?
- How did using AI tools help you, and when did you need to double-check them?
- What surprised you about how simple algorithms can still "feel" like recommendations?
- What would you try next if you extended this project?
-->
