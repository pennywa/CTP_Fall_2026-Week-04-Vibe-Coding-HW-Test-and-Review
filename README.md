# 🎬 MovieLens Vibe Coding Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pennywa-ctp-fall-2026-week-04-vibe-coding-hw-test-an-app-hox6sx.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![Built with Cursor](https://img.shields.io/badge/Built%20With-Cursor%20Composer-9cf.svg)](https://www.cursor.com/)

> **Coursework:** CUNY Tech Prep (Fall 2026) — Week 04: Vibe Coding HW, Test & Review  
> **Author:** Penny Wang  
> **Live App:** [MovieLens Vibe Coding Dashboard](https://pennywa-ctp-fall-2026-week-04-vibe-coding-hw-test-an-app-hox6sx.streamlit.app/)

---

### 🚨 A Polite PSA for Fellow Data Science Cohort Mates

> **Hold up.** If you're a Data Science Fellow in my cohort currently scrolling this repo looking for easy answers...
>
> 🛑 **No cheating!** 
> 
> You're here to build your own intuition and wrestle with your own low-signal charts. Take inspiration from the architectural critique, but write your own prompts and make your own mistakes. Your future TA/mentors will thank you. 😉

---

## 💡 What This Project Actually Is

This is not a project where an LLM was given a loose prompt and blind trust. It is an exploration of **disciplined vibe coding** — using AI as a fast execution engine while keeping human data intuition firmly in the driver's seat.

### The Workflow Architecture
* **Planning / "Brain Vomit" Bucket:** Gemini (synthesizing messy ideas, evaluating data traps, and structuring rubric constraints).
* **Constrained Execution:** Cursor Composer anchored strictly to `@week-04-vibe-coding-hw-build.md` to avoid hallucinated dependencies and wasted tokens[cite: 3, 5].
* **Human-in-the-Loop Evaluation:** Calling out AI blind spots when a chart technically meets rubric specs but fails analytical common sense.

---

## 📊 Core Questions & Intentional Visual Evolutions

| Section | AI Default Failure Mode | Human-in-the-Loop Refinement |
|---|---|---|
| **Q1 — Genre Breakdown** | Would default to an 18-slice unreadable pie chart[cite: 1]. | Horizontal bar chart sorted descending; clear category labels without rotation[cite: 1]. |
| **Q2 — Genre Satisfaction** | Flat $[0, 5]$ bar chart compressing all 18 genres into a monolithic blue block between 3.2 and 3.9 stars[cite: 4]. | **Cleveland Dot Plot** zoomed to $[3.0, 4.2]$ with a catalog-wide mean benchmark (~3.53★). |
| **Q3 — Ratings Over Time** | Temporal line chart; noise from sparse historical data points. | Filtered out release years with $n < 20$ ratings to eliminate sample-size distortion. |
| **Q4 — Best Movies (With a Floor)** | Long titles crushed the canvas width into 5 identical blue squares; axis clipped to `"Average ratir"`[cite: 5]. | **3-Stage Evolution:** Naive AI $\to$ Margin-padded bar $\to$ **Taste-refined horizontal lollipop chart** with direct score/review annotations. |

---

## 🛠️ Deep Dive: The Build Log

Curious about the actual friction, failed prompt attempts, token management, and unedited thought process?

Check out **[`BUILD_LOG.md`](./BUILD_LOG.md)** for:
1. Zero-loss data ingestion and regex title parsing.
2. The exact critique notes when the default AI visualizations fell flat.
3. The raw, unfiltered human thought dump behind the engineering decisions.

---

## 🚀 Running Locally

```bash
# Clone the repository
git clone [https://github.com/pennywang/CTP_Fall_2026-Week-04-Vibe-Coding-HW-Test-and-Review.git](https://github.com/pennywang/CTP_Fall_2026-Week-04-Vibe-Coding-HW-Test-and-Review.git)
cd CTP_Fall_2026-Week-04-Vibe-Coding-HW-Test-and-Review

# Install runtime dependencies
pip install -r requirements.txt

# Launch the Streamlit dashboard
streamlit run app.py
```
