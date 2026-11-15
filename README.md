# Pale Blue Flame

*Nobody has lit a fire there yet.*

NASA has spent years setting small, careful fires in space. A sheet of cotton and fiberglass, almost a metre long, burned on a cargo ship after it left the Space Station. Acrylic rods burned in a small wind tunnel on the Space Station itself. And every one of those material fires burned in the same kind of air: Space Station air, normal pressure, 14 to 22% oxygen.

The places people want to live next are a bit different than the places these experiments were taken. A base on the Moon, a pressurized rover, a habitat on Mars: NASA plans them with more oxygen and thinner air. In that air, the data has nothing.

So we built a page that asks one question, and is honest about the answer.

We made it for the NASA Space Apps Challenge 2026, for the challenge [Flame in Freefall](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/): an SI-powered dashboard that summarizes, ranks and interprets NASA's microgravity combustion research for fire safety.

## The one question

**Would this burn here?** You pick a material and a place, or you ask in your own words ("would my running shoe burn in a Moon rover?"). The page answers in one of two ways:

- **NASA tested this.** Real fires with that material burned in air like that place's. Tested is not the same as safe: what happened in each fire is on its experiment page.
- **We don't know. No matching test.** NASA tested the material, but only in different air. Not tested here does not mean safe.

It sounds like a small answer. Turns out it is the finding. NASA's proposed atmosphere for Moon and Mars habitats is 34% oxygen at 0.56 atm, and no material fire in the data we used comes near it. One NASA investigation, ACME BRE, says in its own record that burning continued without airflow in elevated-oxygen air like that. In normal 21% air, the same flames went out.

## What is on the page

The site is one page.

- **The first screen.** The question, the verdict, a picture of the places (Earth, the Space Station, a spacewalk, the Moon, Mars) and the oxygen chart. Arrows appear on the chart one at a time: where NASA's fires burned, where your place is, and the part that nobody tested.
- **Look closer.** One row of tabs below the first screen:
  - *The gap*: each material fire by oxygen and cabin pressure, with the places where people plan to live.
  - *Experiments*: the 24 investigations, ranked for the place you chose and sorted into prevent, detect and suppress. Open one to read its summary. You can compare two.
  - *A real fire*: the heat sensors of Saffire-I, replayed.
  - *Back on Earth*: where space fire safety came home.
  - *The data*: the tests for each material, as a chart, a table and a CSV file.
- **The ask bar.** It stays at the bottom of the screen.

Move the pointer across a chart to read its values. Click a dot to open its experiment, or a place to choose it.

## What is in this repository

| Folder | Contents |
|---|---|
| `notebooks/01_explore_the_data.ipynb` | A tour of NASA's fire data: 24 investigations, their test tables, papers and raw files. Read this first. |
| `notebooks/02_clean_the_data.ipynb` | The steps that change the test tables into one table of 263 material tests. |
| `data/` | The files that the site reads: `material_tests.csv`, `experiments.json`, `places.json`, `summaries.json` and `saffire1_sensors.json`. |
| `webapp/` | The website (Vue 3, Vite, SVG and D3). The photographs are in `webapp/public/img/`. |
| `backend/` | The question service (FastAPI and LangGraph, with DeepSeek). |

## Run the site

You need Node 18 or a later version.

1. Go to the `webapp` folder.
2. Install the packages.
3. Start the development server.
4. Open `http://localhost:5173` in a browser.

```sh
cd webapp
npm install
npm run dev
```

The site works without a network connection. The question box needs the backend.

## The site online

The site is online at **https://mtaimourz.github.io/pale-blue-flame/**. GitHub Pages serves it from the `gh-pages` branch. To publish a new version, run `webapp/scripts/deploy-pages.sh`: it builds the static site and pushes the build to that branch.

The online copy has no backend and no API key. The five example questions show saved replies from the question service (`data/answers.json`). For every other question, the page says that live answers need the backend with a DeepSeek API key. To ask anything, run the site and the backend on your computer, as the next section shows.

## Run the question box

You need Python 3.11 or a later version, [uv](https://docs.astral.sh/uv/) and a DeepSeek API key.

1. Open a second terminal.
2. Go to the `backend` folder.
3. Set the `DEEPSEEK_API_KEY` variable to your key.
4. Start the backend on port 8787.

```sh
cd backend
export DEEPSEEK_API_KEY=your-key
uv run uvicorn app:app --port 8787
```

The site sends `/api` requests to the backend. **Keep the key in the backend. Do not put the key in the website.** If the backend does not run, the question box shows a message. The other parts of the site continue to work.

## Show the site at a stand

1. Open `http://localhost:5173/?stand=1#/burn` in a browser.
2. Set the browser to full screen.

The stand view shows one 16:9 screen with no menus. It shows a new example every six seconds.

## How the AI works

The AI does one task. It identifies the materials of an everyday object, for example "a plastic shroud, a circuit board, a metal heatsink". A fixed table in our code then selects the nearest material that NASA tested. The verdict, the numbers and the charts come from NASA's data, not from the AI. If no material in the data is similar, the page tells you. Examples are a metal spoon and water.

The AI also wrote the experiment summaries from the NASA record of each investigation. Each line shows the part of the record that it comes from. Our code removed each line without a real source. "What they found" shows a result only if the NASA record states that result. **Read the summaries before you quote them.**

The file `backend/eval_cases.py` sends 14 everyday questions to the backend and checks the answers. Run it after each change to the AI.

## Sources and limits

The data comes from the [NASA Physical Sciences Informatics](https://psi.nasa.gov/physci/repo/search?q=combustion) database, Combustion Science. Of the 24 records, 23 have the CC0-1.0 license. The atmosphere of each place comes from NASA technical reports. The file `data/places.json` gives the link for each report.

Know these limits before you use the data:

- NASA tables do not record the pressure of the material tests. We use cabin pressure (approximately 1 atm), and the data shows this assumption.
- "No matching test" applies only to the data that we used. It does not apply to all fire tests.
- The atmospheres for the Moon, the rover and Mars are proposals. Real missions can be different.
- The background is a drawing of a spiral galaxy, made by `webapp/scripts/make-galaxy.py`. It is not a photograph or a star map.
- The distances in the picture are real numbers, but the picture is not to scale.
- No Moon base or pressurized rover exists yet. Their pictures are NASA concept art.

The pictures are from NASA:

| Picture | NASA image |
|---|---|
| Earth | Apollo 17, `as17-148-22727` |
| Moon | Galileo, `PIA00405` |
| Mars | Viking, `PIA00407` |
| Space Station | Expedition 66 mosaic, photographed from a Crew Dragon (2021) |
| Spacewalk | STS-41B, Bruce McCandless, `s84-27017` |
| Pressurized rover | Artemis pressurized rover, artist's concept ([NASA](https://www.nasa.gov/feature/living-and-working-on-the-moon/)) |
| Moon base | Artemis Lunar Surface Habitat, concept art |

We hope one thing is hard to miss when you leave. We know a great deal about fire in one kind of air, and almost nothing about the air we are about to live in.
