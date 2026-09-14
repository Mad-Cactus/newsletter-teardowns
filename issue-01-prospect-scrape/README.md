# Prospect Scrape — Find Warm Leads in Public Data

Turn public records into a ranked prospect list using a coding agent. This is the teardown from [The Cactus Dispatch Issue #1](https://madcactus.org/newsletter).

## What this does

A coding agent (Claude Code, Codex, pi) builds a Python tool that finds companies in a specific state (expired contracts, lapsed coverage, compliance flags), ranks them by urgency, and outputs a Streamlit dashboard.

## The prompt

Hand this to your coding agent:

```
I sell [your product] to [your ideal customer].
My customers only buy after they've experienced [the problem].

CRITICAL: paste ONE real record from your source below.
The agent will hallucinate field names without it.
Here is one real example record: [paste it].

Here's where the source data lives: [URL or description].

Build a Python tool that:
1. Pulls all records from the source
2. Finds everyone currently in [the problem state]
3. Ranks them by urgency (most recent = most urgent)
4. Outputs a Streamlit dashboard with filters

After building, add a verification function that:
- Re-checks each result against the original source
- Flags any row that doesn't match
- Outputs a "needs manual review" list
```

## Finding your data source

Every industry has public signals. The prompt needs a source URL — here's how to find yours.

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

### How to have an agent discover sources

If you don't know where the data lives, ask your coding agent to find it:

```
I need public data about [industry/topic] in [geography].
The signal I'm looking for is [companies that have experienced X].
Search for:
1. Government databases or registries that track this
2. APIs that expose this data
3. Public dashboards or search portals

For each source you find, tell me:
- The URL
- Whether it has an API or needs scraping
- What fields/fields are available
- Any rate limits or terms of service

Then pick the best one and build the tool.
```

### Common API directories

- **data.gov** — US government open data catalog (thousands of datasets)
- **CDC, EPA, NOAA** — all have public APIs
- **Census Bureau API** — demographic + business data
- **Socrata** — open data platform used by many cities/states

## The verification loop

The most important part. Coding agents hallucinate field names when you don't give them a real example record. The verification function cross-references each result against the original source and flags mismatches.

In the teardown: 585 companies scored, 3 wrong, all caught before anyone acted.

## License

MIT
