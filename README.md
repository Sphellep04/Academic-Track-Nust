# 🎓 Academic Progress Dashboard — Shapopi Phellep

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![NUST](https://img.shields.io/badge/University-NUST%20Namibia-003366)](https://www.nust.na)

---

## The Story Behind This Dashboard

People look at a transcript and see numbers. A grade here, a fail there, a retake somewhere in between. What they don't see is everything that sat behind those numbers — the commute you couldn't afford, the laptop that could barely open two tabs, the test you missed because the month had run out before it had.

This dashboard exists because I wanted to tell the full story, not just show the results.

---

### Act 1 — Before NUST

I didn't start here. Before NUST, I was at UNAM studying Secondary Education — Mathematics and Physical Science. On paper, a solid path. In reality, it wasn't mine.

I was a dancer. Still am, in some way that never fully leaves you. But dancing came with a circle, and that circle wasn't pointed anywhere good. I knew it, and I knew I had to move — not just institutions, but environments entirely. So I made a decision: go to Windhoek, stop dancing, reset, rebuild.

What I didn't know was that Windhoek has its own jungle.

---

### Act 2 — Year 1 Was Fine, Until It Wasn't

First year at NUST went reasonably well. New city, new degree, new version of myself — I was motivated. But the city has a pull of its own, and somewhere between orientation and second semester, I got carried away. Not dramatically. Just slowly, the way focus slips when you're not watching it.

Then Year 2 came, and the weight of everything started to show up in the numbers.

Living in Katutura — one of the furthest points from campus — meant that getting to a lecture wasn't just a matter of showing up. It was a budget decision. Some mornings, the money wasn't there, so neither was I. Missed classes turned into missed tests. Late submissions. Pressure stacking up with nowhere to put it.

The laptop situation didn't help. A Lenovo with 2GB of RAM is a documentation machine at best. I couldn't practice, couldn't run environments, couldn't do half the practical work the degree required. I learned what I could, when I could, with what I had. Looking back, investing in a proper machine earlier would have changed a lot — but I wasn't wise enough then to see it as an investment rather than an expense.

Trading also found its way into the picture at some point — another pull on attention, time, and focus. I won't draw it all out, but it had its effect. What I will say is that I've since found a way to carry all of it — trading, work, school, and life — without any one of them swallowing the others. That balance took real time to build. But it's built.

Those years were hard. The data shows it clearly: 2022 was my lowest point. Three fails in one semester. That's not a statistic I'm hiding — it's a chapter I earned.

---

### Act 3 — Making the Move

In 2023, I made a plan and moved closer to campus. It sounds small. It wasn't.

Proximity changed everything. Getting to class was no longer a financial calculation. I was present more, engaged more, and the results followed almost immediately. The grades began to climb. You can see it in the dashboard — the upward trend from 2023 onward isn't luck. It's what consistency looks like when the basic barriers are removed.

That move was one of the best decisions I made in this degree.

---

### Act 4 — DTN and the Long Game

If one module has defined the difficulty of this journey, it's DTN — Data Networks. Three attempts. Various circumstances. It has been the stubborn one.

But something shifted when the academics stopped and the real world began.

In the second semester of 2025, I had no modules and no internship secured. Instead of waiting it out, I entered the MICT Hackathon — partly out of determination, partly because it was the only door I could see. We made it through. That hackathon led directly to an internship opportunity at Salt Essentials IT, and on **2 February 2026** I walked in for my first day of work. That opportunity turned into something I didn't expect: an education of a different kind.

At Salt, I was doing real work for the first time. Internal projects, industry exposure, and labs — networking labs, specifically — that started to unlock things DTN had been trying to teach me in theory. Practical experience did what textbooks couldn't quite do alone.

I'm currently doing my WIL (Work Integrated Learning). My first DTN test recently came back at 66%. For that module, and where I've come from with it, that number means more to me than any A I've ever gotten. DTN is the last wall, and it's coming down.

---

### Where I Am Now

Expected graduation: **October 2026.**

The dashboard you're looking at is a record of four years of navigating a degree with limited resources, wrong environments, costly mistakes, and — eventually — the kind of growth that only comes from being genuinely tested.

I started this as a student who had too much going on and not enough going right. I'm finishing it as someone who learned, slowly and sometimes painfully, what it takes to stay the course.

The grades got better. So did I.

---

## About the Dashboard

An interactive 6-tab academic progress dashboard built in Python and Streamlit, visualising four years of academic data from NUST's BSc Computer Science (Software Development) programme.

### Features

| Tab | Description |
| --- | ----------- |
| 📊 Overview | KPI cards, year-by-year summary, grade distribution, academic timeline, PDF export |
| 📈 Charts | Interactive Plotly charts — marks, trends, heatmap, box plots |
| 📋 Module Details | Searchable, colour-coded full module record |
| 🔁 Retake Tracker | Attempt-by-attempt progress for every retaken module |
| 🧮 GPA Calculator | Estimated GPA per year and overall, with degree classification |
| 🎯 What-If Simulator | Project future GPA based on pending module marks |
| 📖 My Story | The full context behind the numbers |

### Tech Stack

```text
streamlit    — dashboard framework
plotly       — interactive charts
pandas       — data processing
scipy        — trend / regression analysis
fpdf2        — PDF report export
openpyxl     — Excel data reading
```

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/Academic-Track-Nust.git
cd Academic-Track-Nust

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch
streamlit run streamlit_app.py
```

App opens at **`http://localhost:8501`**

---

## Deploy for Free (Streamlit Community Cloud)

1. Push this repo to GitHub (make it public)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Select the repo, set the main file to `streamlit_app.py`
4. Click **Deploy** — you get a free public URL instantly

---

*BSc Computer Science — Software Development | Namibia University of Science and Technology*
*Shapopi Phellep | Expected Graduation: October 2026*
