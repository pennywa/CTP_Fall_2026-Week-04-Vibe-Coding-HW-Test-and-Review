# 🛠️ Build Log: MovieLens Vibe Coding & Dashboard Engineering

> **Assignment:** Week 4 — Vibe Coding & Streamlit Dashboard Build  
> **Author:** Penny Wang  
> **Date:** September 18, 2026[cite: 3] 
> **Workflow Architecture:** Dual-engine paradigm — Gemini as the architectural planning & critique partner ("thought bucket") $\to$ Cursor Composer as the targeted executor.

---

## Raw Penny Brain Vomit. AI hasn't touched this stream of thoughts:💭

Highlight my thinking process from beginning to end. my sanity check, I opened up those raw csv files to check the column names -> I saw movieID same column in both CSV files. Also how the year 1995 was in movie name but in a different case, let’s say you have a year or timestamp column. Gotta be careful and check data types and also when you filter and manipulate columns to always keep an eye out. Also me giving cursor the context markdown hw file and @ it so it can tell where to look for instead of searching my entire folder and wasting tokens. also how i plan my brain vomit in gemini first then spit it to cursor with a cleaned up version. lastly my call outs for the visual for question 2 and 4. just because i told AI explicitly to follow the rules. my takeaway is: AI STILL MESSES UP even after I supplied it the markdown file hw assignment instructions and told it to be on the lookout. I called the shots because visually I'm confused. There's not much visual variation. BUT also I asked it to build off and not delete what AI gave me to show the process. Build on top of it -> add human in the loop tab so it shows how I'm calling out AI's decision. For question 4, despite it being correct with the horizontal bar graph or whatever I still don't like it also for the sake of this demo I want to have a variety of plots to show so why not lollipop. Haha get the joke, human in the loop but adding my taste. and it's a lollipop chart? Anyways... Just as important to learn process but also to build intuition. I'm still trying to learn to build my intuition too. 

Disclaimer: Beyond this section, I used AI to help me re-write and organize my thoughts. 

---

## 🧠 Meta-Workflow & Engineering Philosophy

Before typing code, I set up a structured separation of concerns:
1. **Brain Vomit $\to$ Architecture First:** I don't prompt Cursor blindly with vague instructions. I use Gemini to dump initial thoughts, stress-test data mechanics (joins, regex traps, axes scaling), and synthesize clear, concise specifications.
2. **Context Window Optimization & Token Efficiency:** Instead of letting Cursor hallucinate or scrape my entire file tree, I committed `@Week4_Vibe_Coding_Dashboard_Build.md` directly into the workspace[cite: 3]. Using explicit `@` mentions constrained Cursor's attention to the assignment rubric and the Chart Toolkit, eliminating wasted tokens and random search calls.
3. **Data Integrity Sanity Checks:** Before merging or transforming, I audited the raw files:
   - Verified `movieId` is the shared primary/foreign key across both `movies.csv` and `ratings.csv`.
   - Chose an `inner` merge explicitly: ratings drive every homework question, so keeping unrated movies (which introduce `NaN` values) would pollute downstream calculations without adding value.
   - Identified that raw MovieLens doesn't ship with an extracted `year` column; it is trapped in parentheses inside `title` strings and requires regex extraction into an integer (`Int64`) to avoid ugly `.0` float artifacts in Streamlit.

---

## 📌 Moment 1: Environment Setup & Zero-Loss Ingestion

### 1. The Raw Input & Thought Process
When unzipping `ml-latest-small.zip`, the archive inherently contained an internal folder of the same name, creating a messy double-nested structure (`data/ml-latest-small/ml-latest-small/`). I flattened this immediately into `data/ml-latest-small/` so relative pathing on Streamlit Cloud wouldn't break[cite: 1]. 

### 2. The Structured Cursor Prompt
```text
I have two CSV files: `data/ml-latest-small/movies.csv` and `data/ml-latest-small/ratings.csv`.
In `app.py`, use `@st.cache_data` to load them.
1. Use regex on `movies['title']` to extract the 4-digit release year into a numeric column named `year`.
2. Create a `clean_title` column with the year removed from the title.
3. Inner merge `ratings` with `movies` on `movieId`.
4. Display `st.title('MovieLens Dashboard')`, a quick `st.write()` showing total row count and unique movie count, and `st.dataframe(df.head())` to verify data.
```

### 3. What the AI Produced on First Try
- Built the cached loader cleanly.
- Extracted the year and stripped it into `clean_title`.
- Successfully showed **100,836 rows** and **9,724 unique movies**[cite: 2].
- *Small AI Proactivity:* It cast `year` as a nullable integer (`Int64`), preventing `1995.0` float formatting.

### 4. Human Review & Decision
Confirmed data pipeline integrity against baseline parameters. Ready for charting.

---

## 📌 Moment 2: The Question 2 Low-Signal Failure (Genre Satisfaction)

### 1. The Context & Prompt Given to Cursor
I supplied Cursor the Chart Toolkit via `@Week4_Vibe_Coding_Dashboard_Build.md` and explicitly commanded it to handle Q2[cite: 3]:
```text
Question 2 — Genre Satisfaction:
- Calculate the average rating per genre using df_genres.
- Render a horizontal bar chart sorted descending from highest to lowest satisfaction.
- Ground the x-axis explicitly to [0, 5] so the 5-star scale remains accurate and is not exaggerated by auto-zooming.
```

### 2. What the AI Produced on First Try
- It followed the literal instructions: produced a sorted horizontal bar chart with the x-axis forced to `[0, 5]`[cite: 4].
- AI Defense: *"A horizontal bar chart grounded from 0 to 5 preserves the full rating scale and prevents visual exaggeration of small differences."*

### 3. The Human-in-the-Loop Callout: "This is a Bad Visualization"
Looking at the rendered output, my visual intuition immediately fired: **This is unhelpful AF.**
- **The Zero-Baseline Dilemma:** Because all 18 movie genres average between 3.2 and 3.9 stars, grounding the axis to zero wasted 70% of the visual ink on empty white/black space from 0 to 3[cite: 4].
- **Monolithic Block:** Every bar looked like the exact same blue rectangle[cite: 4]. The visual variation was virtually zero, making ranking decipherable only by squinting at text[cite: 4].
- **Takeaway:** Even when an AI follows your prompt to the letter, it does not possess *taste* or *visual empathy*. It cannot tell that a technically compliant chart is analytically useless.

### 4. Iteration & Refinement
Instead of erasing the AI's mistake, I turned it into a two-tab comparative learning interface:
- **Tab 1 (AI Output):** Preserved the flat 0–5 bar chart with the AI rationale, paired with my `st.warning` critique on why it's a low-signal visual.
- **Tab 2 (Human Refinement):** Replaced it with a **Cleveland Dot Plot** (`px.scatter`) focused tightly on `[3.0, 4.2]`. Dot plots encode value via spatial position rather than bar area, making axis truncation ethical. Added a vertical benchmark line at the catalog-wide average (~3.53) so viewers instantly see which genres outperform the baseline.

---

## 📌 Moment 3: The Question 4 Layout Catastrophe (Top Movies With a Floor)

### 1. The Context & Initial Cursor Output
For Question 4 (Top 5 movies with an interactive slider for rating floor), Cursor generated a default horizontal bar chart[cite: 5]:
```text
Question 4 — Best Movies, With a Floor:
- Add an interactive slider widget using st.slider for minimum rating count floor (10 to 200, default 50).
- Group by clean_title, aggregate mean rating and count, filter by slider.
- Extract top 5 highest-rated movies and display in horizontal bar chart sorted descending.
```

### 2. What Failed (Visual & Layout Collapse)
The output was broken across multiple dimensions:
- **Canvas Squeeze:** Plotly assigned almost 70% of the canvas width to category text labels to accommodate long titles[cite: 5].
- **Severe Clipping:** Even with massive margins, *Dr. Strangelove* got cut off mid-title (`or: How I Learned to Stop Worrying...`)[cite: 5].
- **Truncated Axis Label:** The x-axis title was shoved off the edge, reading `"Average ratir"`[cite: 5].
- **Identical Squares:** The top 5 films sat between 4.2 and 4.4, rendering 5 nearly identical blue blocks[cite: 5].
- **Zero Floor Context:** The entire point of the question is the *rating count floor*, yet the chart hid sample counts completely[cite: 5].

### 3. The Human-in-the-Loop Architectural Pivot
I realized: if a chart confuses me while I'm looking at it, it belongs in the trash. Furthermore, five items on a full-width dashboard looked repetitive next to the Q1/Q2 bar charts. I demanded a 3-stage evolution:
1. **Tab 1: Initial AI Output:** Raw, squished, clipped bar chart + AI rationale + Human critique exposing the layout failure and missing sample sizes.
2. **Tab 2: Refined Bar Chart:** Fixed Plotly layout margins (`l=220`), truncated titles to 35 characters, focused the scale to `[3.5, 5.0]`, and embedded inline annotations: `f"{rating:.2f} ★ (n={count})"`.
3. **Tab 3: Taste Refinement (Horizontal Lollipop Chart):** Slender horizontal stems starting from 3.5 leading to bold circular markers, directly displaying the rating and review counts. This maximized the data-to-ink ratio, added visual variety to the page, and instantly clarified why raising the floor from 50 to 150 rearranges the podium.

---

## 💡 Key Takeaways 

1. **AI Blind Spots are Real:** Supplying the assignment markdown, tagging files with `@`, and providing explicit toolkit rules helps, but **AI still messes up**. It defaults to mechanically obedient patterns that frequently produce low-signal, aesthetically broken, or unreadable visualizations.
2. **Context Management Matters:** Feeding raw dumps wastes tokens and confuses LLM reasoning. Framing thoughts in an external bucket (Gemini) before handing executable commands to Cursor kept code iterations tightly scoped and bug-free.
3. **Data Science Requires Intuition, Not Just Code Generation:** Vibe coding makes generation trivial, which shifts the real work to evaluation. Spotting that 3.2 vs 3.9 looks meaningless on a 0–5 bar chart—and knowing that a Cleveland dot plot or lollipop solves it—is where human data expertise actually lives. Although it still can be wrong in the sense that there might always be something better but at some point you just have to deliver a product, which is why you need to defend your decision.