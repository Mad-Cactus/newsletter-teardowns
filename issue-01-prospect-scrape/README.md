# Prospect Scrape — Find Warm Leads in Public Data

Turn public records into a ranked prospect list using a coding agent. This is the teardown from [The Cactus Dispatch Issue #1](https://madcactus.org/newsletter).

## What this does

A coding agent (Claude Code, Codex, pi) interviews you, finds the public sources where your customers' pain shows up, pulls one real record, builds the tool, and ranks every company currently in the problem state by urgency. Output: a ranked call list (CSV or dashboard).

## The prompt

Paste this whole thing into your coding agent. It interviews you first, discovers the data sources itself, and doesn't build until it has seen one real record:

```
Build me a tool that finds companies going through the problem my product solves
right now, and ranks them by how badly they need me.

Before you write any code, interview me. One question at a time, plain language.

1. Start by asking for my company's website. Read it and tell me what you think
   I sell and who I sell it to, then let me correct you.
2. Ask what a customer went through right before they needed me.
3. Figure out where evidence of that moment shows up in public. Good hunting
   grounds: Secretary of State registrations, state licensing boards, OSHA/FDA/
   SEC/FCC records, court records (PACER, state portals), county property
   records, FEC filings, IRS 990s via ProPublica, data.gov, Census API, and
   Socrata open-data portals. Suggest sources for my industry I haven't thought of.
4. Search those sources and the open web for my industry and geography. For each
   candidate source, report the URL, whether it has an API or needs scraping,
   what fields are available, and any rate limits or terms of service.
5. Ask me where I want the ranked list to land. A CSV is fine.
6. Ask me for one real example record from the best source. If I'm not sure
   which field to pull, help me find and pull the right one. Study it before you
   design anything. Do not invent field names.
7. When you can play back my product, my customer, the moment they got burned,
   the data sources, and the ranking logic, and I say yes, build it.

When you build:
- Pull the records, find everyone currently in the problem state, rank by
  urgency (most recent first, strongest buying signal as tiebreak).
- Output a CSV or a Streamlit dashboard with filters, whichever I picked in step 5.
- Add a verification function that re-checks each result against the original
  source, flags any row that doesn't match, and outputs a "needs manual review"
  list. Never skip this: hallucinated rows are worse than no rows.
```

## Reference: public source catalog

The prompt above already tells the agent where to hunt. Keep this table for picking sources yourself, or for steering the agent when it guesses wrong.

### Government / regulatory data

| Signal | Source | How to access |
|--------|--------|---------------|
| Business registrations | Secretary of State (per state) | Search portals, some have APIs |
| Professional licenses | State licensing boards | Scrapable HTML, some APIs |
| OSHA violations | osha.gov | API available |
| FDA inspections / warnings | fda.gov | API + open data |
| SEC filings | sec.gov/edgar | Full API (EDGAR) |
| FCC licenses | fcc.gov | API available |
| Court records | PACER, state court portals | Scrapable, some paid |
| Property records | County assessor sites | Scrapable HTML |
| Campaign finance | fec.gov | API available |
| Nonprofit filings (990) | IRS, ProPublica | ProPublica API (free) |

### Common API directories

- **data.gov** — US government open data catalog (thousands of datasets)
- **CDC, EPA, NOAA** — all have public APIs
- **Census Bureau API** — demographic + business data
- **Socrata** — open data platform used by many cities/states

## The verification loop

The most important part. Coding agents hallucinate field names when you don't give them a real example record. The verification function cross-references each result against the original source and flags mismatches.

In the teardown: 585 companies scored, 3 wrong, all caught before anyone acted.

## Starter server

[`starter/`](starter/) has a uv + FastAPI skeleton with the same shape — ingest, rank, serve, and a `/run` placeholder where the agent wires your data source. Hand it to your agent alongside the prompt if you want an API instead of a one-off script.

## License

MIT
