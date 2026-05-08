# Wona.news

African media intelligence platform. Aggregates African and international news, summarizes it, and contextualizes each story through five African ideological perspectives. Independent. Continental. Diasporic.

> Reclaiming the African narrative, one story at a time.

## What this is

Wona.news is a Ground.news-style news intelligence platform built around African ideological frameworks instead of Western left/right politics. The MVP includes:

- Daily ingestion from a configurable list of RSS sources (BBC Africa, Le Monde Afrique, Jeune Afrique, RFI, Al Jazeera, AllAfrica, The Continent, Agence Ecofin, ORTB, Premium Times, Daily Maverick, and others)
- Automatic clustering of articles covering the same story
- Heuristic orientation pre-tagging across 5 perspectives (Panafricaniste, Critique Post-Coloniale, Nationaliste, Pre-Colonial Référentiel, Diaspora)
- Manual override via a small tagging CLI
- Blindspot detection, flagging stories underreported across source categories
- Editorial frontend, hand-rolled HTML/CSS/JS, no framework, deploy-anywhere
- Optional FastAPI server for dynamic data delivery

## Architecture

```
RSS sources
    |
    v
fetch_rss  ->  clean  ->  cluster  ->  classify  ->  blindspot
                                          ^
                                          |
                                     manual_tags.json
    |
    v
data/articles.json  -->  scripts/sync_data.sh  -->  frontend/data/articles.json
    ^                                                       |
    |                                                       v
api/main.py (FastAPI, optional)                       frontend (static)
```

The pipeline writes a single canonical `data/articles.json`. The frontend reads it directly when deployed as a static site, or it can be served via the FastAPI layer when dynamic features are needed.

## Project structure

```
wona-news/
  archives/                    Original v1, v2, v3 frontends and the toy sentiment script
  api/
    main.py                    FastAPI server
  data/
    articles.json              Canonical story output (pipeline writes this)
    orientations.json          The 5+1 orientation taxonomy
    sources.json               RSS source registry
    manual_tags.json           Created by tag_cli, not committed
  frontend/
    index.html                 Canonical UI
    assets/styles.css          Editorial design system
    assets/app.js              Vanilla JS, fetches data/*.json
    data/                      Synced copies for static deploys
  pipeline/
    __init__.py
    config.py                  Paths and runtime constants
    fetch_rss.py               Feedparser ingestion
    clean.py                   Body fetch, BeautifulSoup cleaning
    summarize.py               LexRank summary with regex fallback
    classify.py                Keyword-based orientation scoring
    cluster.py                 TF-IDF cosine clustering
    blindspot.py               Coverage-ratio blindspot scoring
    tag_cli.py                 Manual tagging CLI
    store.py                   JSON read/write
    run.py                     Orchestrator
  scripts/
    sync_data.sh               Copies data/ into frontend/data/
  .github/workflows/
    ingest.yml                 Daily ingestion on cron
  requirements.txt
  vercel.json                  Vercel deploy config
  netlify.toml                 Netlify deploy config
```

## Local setup

Requires Python 3.11 or newer.

```bash
git clone <repo>
cd wona-news
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the pipeline

```bash
python -m pipeline.run                   # full run, fetches article bodies
python -m pipeline.run --no-bodies       # RSS only, much faster, useful for dev
python -m pipeline.run --limit 3         # restrict to first 3 sources
python -m pipeline.run --verbose         # debug logging
```

The pipeline writes to `data/articles.json`. After every run, sync the data into the frontend:

```bash
bash scripts/sync_data.sh
```

## Viewing the frontend locally

The simplest path is a static server from the `frontend/` directory:

```bash
python -m http.server 8080 --directory frontend
# then open http://localhost:8080
```

If you want the frontend to talk to a live API instead of static JSON, edit `frontend/index.html` and add this before the `<script src="assets/app.js">` tag:

```html
<script>window.WONA_API_URL = "http://localhost:8000/api";</script>
```

## Running the API

```bash
uvicorn api.main:app --reload --port 8000
```

Endpoints:

| Method | Path                       | Notes                                        |
|--------|----------------------------|----------------------------------------------|
| GET    | `/api/health`              | Liveness check                                |
| GET    | `/api/articles`            | Optional `?orientation=`, `?blindspot=`, `?region=`, `?limit=` |
| GET    | `/api/articles/{story_id}` | Single story                                  |
| GET    | `/api/orientations`        | Full taxonomy                                 |
| GET    | `/api/sources`             | Source registry                               |
| GET    | `/api/blindspots`          | Stories sorted by blindspot score             |

CORS is open for GET requests, so any frontend can consume it.

## Manual tagging CLI

The pipeline produces heuristic orientation scores from keyword matches. To override them with editorial judgment:

```bash
python -m pipeline.tag_cli list                    # show all stories and their tagged status
python -m pipeline.tag_cli show <story_id>         # show full story details
python -m pipeline.tag_cli tag <story_id>          # interactive 0-100 prompts per orientation
```

Manual tags persist to `data/manual_tags.json` and override heuristic classification on the next pipeline run.

## Orientation taxonomy

The taxonomy is defined in `data/orientations.json` and is the canonical contract for the entire system.

| ID                            | FR                          | EN                       | Color    |
|-------------------------------|-----------------------------|--------------------------|----------|
| `panafricaniste`              | Panafricaniste              | Pan-Africanist           | `#2D8654` |
| `post_colonial_critique`      | Critique Post-Coloniale     | Post-Colonial Critique   | `#D17141` |
| `nationaliste`                | Nationaliste                | Nationalist              | `#C99A24` |
| `pre_colonial_referentiel`    | Référentiel Pré-Colonial    | Pre-Colonial Referential | `#5089A8` |
| `diaspora`                    | Diaspora                    | Diaspora-centered        | `#7E5E96` |
| `post_colonial` (secondary)   | Post-Colonial               | Post-Colonial            | `#8B6F47` |

Add a new orientation by extending the file. Every consumer reads it dynamically.

## Source registry

Sources are categorized into three buckets used by the blindspot heuristic:

- `international`: Western press covering Africa (BBC, France 24, RFI, Le Monde, Al Jazeera, CNN)
- `panafrican`: Continental and pan-African outlets (Jeune Afrique, AllAfrica, The Continent, Agence Ecofin, Africanews)
- `local`: Country-specific outlets (ORTB Benin, Premium Times Nigeria, Daily Maverick South Africa)

A story is flagged as a blindspot when its sources concentrate in fewer than half the available categories or when only a single source is reporting it.

To add a source, append to `data/sources.json` with `id`, `name`, `rss_url`, `language`, `country_origin`, `category`, `logo_initials`. Optional `filter_keywords` restrict which entries from a feed are kept (useful for general feeds like Al Jazeera).

## Deployment

### Vercel

The repository ships with `vercel.json`. Connect the repo on Vercel, no extra config needed. Build runs `bash scripts/sync_data.sh` and serves `frontend/`.

```bash
vercel deploy --prod
```

### Netlify

Same idea via `netlify.toml`. Connect the repo and Netlify picks up the config.

### GitHub Actions cron

`.github/workflows/ingest.yml` runs the pipeline daily at 06:00 UTC, syncs the data into `frontend/data/`, and commits both back to the repo. Vercel or Netlify then redeploys on the push.

To trigger a manual run from the Actions tab, use **Run workflow**.

You need to grant the workflow write permission. Repo settings, Actions, General, Workflow permissions, set to **Read and write**.

### Local cron alternative

If you prefer to run the pipeline on a server you control:

```bash
0 6 * * * cd /path/to/wona-news && /path/to/.venv/bin/python -m pipeline.run && bash scripts/sync_data.sh
```

## Design notes

- Typography: Fraunces (display serif) and IBM Plex Sans (body), both Google Fonts. IBM Plex Mono is reserved for source labels and meta to give that wire-service feel.
- Palette: warm sand backgrounds, deep editorial navy, five orientation colors tuned to feel earthy rather than corporate. No red. No blue accents that would echo Western political coding.
- The orientation bar on every story card is a single stacked Ground.news-style segment bar. Hover any segment for the percentage tooltip.
- The "Angle Mort" treatment on blindspot cards uses the post-colonial critique orange as a deliberate choice. Underreporting is itself a colonial-era pattern of the global press.
- Layout is 3-column on desktop, collapses to 2-column then single column responsively. The Daily Briefing sidebar drops first because it duplicates content; the Blindspot panel is the last to fold.

## What is intentionally deferred

| Capability                     | Status     | Notes                                                |
|--------------------------------|------------|------------------------------------------------------|
| AI orientation classification  | Deferred   | xlm-roberta fine-tune planned. Hooks present in `classify.py`. |
| Translation pipeline           | Deferred   | All sources kept in original language for MVP.       |
| User accounts and auth         | Deferred   | UI shows Sign In, but no backend auth wired.         |
| Newsletter delivery            | Deferred   | UI present, no SMTP integration.                     |
| Database (Postgres, Elasticsearch) | Deferred | JSON file is enough for MVP daily volumes.         |
| Mobile native app              | Out of scope | Web first, responsive.                            |

Each is a clean boundary, not a half-built feature.

## Roadmap

1. Validate ingestion against real RSS for one week, tune `CLUSTER_SIMILARITY_THRESHOLD`
2. Tag a baseline of 200 stories manually to build a labeled dataset
3. Fine-tune `xlm-roberta-base` on the labeled set, swap into `classify.py`
4. Add light auth (magic link) to gate manual tagging
5. Move from JSON to Postgres when daily volume crosses ~500 stories
6. Add Twitter and TikTok ingestion behind a content creator allowlist (Nathalie Yamb, Kemi Seba, etc.)
7. Marketplace for licensed African research and analysis

## License

Proprietary, all rights reserved. Contact the maintainer before reuse.

## Contact

Luc Anthony Nkounkou — `lucanthony07@gmail.com`
