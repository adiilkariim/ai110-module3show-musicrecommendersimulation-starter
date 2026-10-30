# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->

---

## Design Discussion: Subjective Features

**Prompt:**

> But what are the measurement units? It seems difficult to recommend a song using features like danceability, since they can be subjective. A user might want to dance to a sad song—or to rap, metal, or happy music. How does the app recommend the right song when people's preferences are subjective? Is there a formula it uses?

**AI answer (summary):**

- **No units.** Energy, danceability, valence, and acousticness are scores from 0.0 to 1.0, not physical measurements. Real platforms estimate them by analyzing audio (beat strength, loudness, rhythm) or from human labels. In this dataset the values are simulated.
- **No "right" song (no ground truth).** The recommender does not understand music. It only finds songs whose labels and numbers are closest to what the user described. If a label doesn't match how the user feels, the recommendation will be off.
- **Mixing features is possible.** Because the score adds points from each feature independently, a "sad + danceable" song can still rank highest for a user who wants both. Nothing forces sad and danceable to be opposites. (Danceability is not in the scoring yet.)
- **How real apps handle subjectivity.** They rely heavily on behavior: skips, replays, playlist adds, and what similar users liked (collaborative filtering). This learns each user's personal idea of "danceable" instead of trusting one fixed score.

**What I took from it:**

Treating subjective labels like "sad" or "danceability" as facts is a limitation of my content-based recommender, and I will document it in the Limitations and Bias section of the model card.
