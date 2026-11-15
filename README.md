# Pale Blue Flame

*Nobody has lit a fire there yet.*

![Pale Blue Flame demo: the verdict, the oxygen chart, the five tabs and a question about a GPU on Mars](docs/demo.gif)

The [full demo video (29 seconds, MP4)](https://drive.google.com/file/d/1_hw8IykJUlofG4zQl76rkk30fFltZF2W/view?usp=sharing) has sound.

NASA did many small, controlled fire tests in space. On a cargo ship, a sheet of cotton and fiberglass, almost 1 meter long, burned. That ship had left the Space Station. Acrylic rods burned in a small wind tunnel on the Space Station. All of these material fires burned in the same type of air: Space Station air, at normal pressure, with 14% to 22% oxygen.

The next places for people are different from the places of these experiments. NASA plans a base on the Moon, a pressurized rover and a base on Mars with more oxygen and lower pressure. For that air, the data has no tests.

Thus, we made a page that asks one question. The page gives an honest answer.

We made the page for the NASA Space Apps Challenge 2026, for the challenge [Flame in Freefall](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/): "an SI-powered dashboard that summarizes, ranks and interprets NASA's microgravity combustion research for fire safety".

## The one question

The question is **"Would this burn here?"** You select a material and a place. Or, you ask about an object in your own words, for example "would my running shoe burn in a Moon rover?". The page gives one of two answers:

- **NASA tested this.** Real fires with that material burned in air that is almost the same as the air of that place. A tested material is not necessarily safe. The experiment page of each fire shows the result.
- **We don't know. No matching test.** NASA tested the material, but only in different air. A material without a test is not necessarily safe.

This answer is short, but it is the main result. NASA's proposed air for Moon and Mars bases has 34% oxygen at 0.56 atm. No material fire in our data is near that air. The NASA record of one investigation, ACME BRE, gives an important result. In high-oxygen air of this type, the flames continued to burn without airflow. In normal air with 21% oxygen, the same flames stopped.

## What is on the page

The site has one page.

- **The first screen.** It shows the question, the verdict, a picture of the places (Earth, the Space Station, a spacewalk, the Moon, Mars) and the oxygen chart. Arrows come into view on the chart one by one. They show where NASA's fires burned, where your place is, and the range that has no tests.
- **Look closer.** This is one row of tabs below the first screen:
  - *The gap*: each material fire by oxygen and cabin pressure, with the places where people plan to live.
  - *Experiments*: the 24 investigations, in order of importance for the place that you selected. They are in three groups: prevent, detect and suppress. Open an investigation to read its summary. You can compare two investigations.
  - *A real fire*: the data of the heat sensors of Saffire-I, shown again in time order.
  - *Back on Earth*: the space fire-safety technologies that people now use on Earth.
  - *The data*: the tests for each material, as a chart, a table and a CSV file.
- **The ask bar.** It stays at the bottom of the screen.

To read the values of a chart, move the pointer across the chart. To open the experiment of a dot, click the dot. To select a place, click the place.

## What is in this repository

| Folder | Contents |
|---|---|
| `notebooks/01_explore_the_data.ipynb` | A tour of NASA's fire data: 24 investigations, their test tables, papers and raw files. Read this notebook first. |
| `notebooks/02_clean_the_data.ipynb` | The steps that change the test tables into one table of 263 material tests. |
| `data/` | The files that the site reads: `material_tests.csv`, `experiments.json`, `places.json`, `summaries.json` and `saffire1_sensors.json`. |
| `webapp/` | The website (Vue 3, Vite, SVG and D3). The photographs are in `webapp/public/img/`. |
| `backend/` | The question service (FastAPI and LangGraph, with DeepSeek). |
| `docs/` | The demo GIF. |

## Run the site

You must have Node 18 or a later version.

1. Go to the `webapp` folder.
2. Install the packages.
3. Start the development server.
4. Open `http://localhost:5173` in a browser.

```sh
cd webapp
npm install
npm run dev
```

The site operates without a network connection. The question box must have the backend.

## The site online

The site is online at **https://mtaimourz.github.io/pale-blue-flame/**. GitHub Pages gets the site from the `gh-pages` branch.

To publish a new version, run `webapp/scripts/deploy-pages.sh`. This script builds the static site and pushes the build to the `gh-pages` branch.

The online copy has no backend and no API key. The five example questions show saved answers from the question service (`data/answers.json`). For all other questions, the page tells you that live answers must have the backend with a DeepSeek API key. To ask any question, run the site and the backend on your computer. The next section gives the steps.

## Run the question box

You must have Python 3.11 or a later version, [uv](https://docs.astral.sh/uv/) and a DeepSeek API key.

1. Open a second terminal.
2. Go to the `backend` folder.
3. Set the `DEEPSEEK_API_KEY` variable to your key.
4. Start the backend on port 8787.

```sh
cd backend
export DEEPSEEK_API_KEY=your-key
uv run uvicorn app:app --port 8787
```

The site sends `/api` requests to the backend.

**Keep the key in the backend. Do not put the key in the website.**

If the backend does not operate, the question box shows a message. The other parts of the site continue to operate.

## Show the site at a stand

1. Open `http://localhost:5173/?stand=1#/burn` in a browser.
2. Set the browser to full screen.

The stand view shows one 16:9 screen with no menus. It shows a new example each six seconds.

## How the AI works

The AI does one task. It identifies the materials of an everyday object, for example "a plastic shroud, a circuit board, a metal heatsink". Then, a fixed table in our code selects the nearest material that NASA tested. The verdict, the numbers and the charts come from NASA's data, not from the AI. If no material in the data is almost the same, the page tells you. A metal spoon and water are two examples.

The AI also wrote the experiment summaries from the NASA record of each investigation. Each line shows the part of the record that it comes from. Our code removed each line that had no real source. "What they found" shows a result only if the NASA record gives that result.

**Read the summaries before you quote them.**

The file `backend/eval_cases.py` sends 14 everyday questions to the backend and checks the answers. Run this file after each change to the AI.

## Sources and limits

The data comes from the Combustion Science records of the [NASA Physical Sciences Informatics](https://psi.nasa.gov/physci/repo/search?q=combustion) database. Of the 24 records, 23 have the CC0-1.0 license. The air of each place comes from NASA technical reports. The file `data/places.json` gives the link to each report.

Know these limits before you use the data:

- The NASA tables do not record the pressure of the material tests. We use cabin pressure (approximately 1 atm). The data shows this assumption.
- "No matching test" applies only to the data that we used. It does not apply to all fire tests.
- The air for the Moon, the rover and Mars is a proposal. Real missions can be different.
- The background is a drawing of a spiral galaxy. The script `webapp/scripts/make-galaxy.py` makes this drawing. It is not a photograph or a star map.
- The distances in the picture are real numbers, but the picture is not to scale.
- A Moon base and a pressurized rover do not exist at this time. Their pictures are NASA concept art.

We know much about fire in one type of air. We know almost nothing about the air where people will live next.
