# Data Loss Audit — The Cactus Dispatch Issue #2

Five-step audit your coding agent runs against its own project to find silent data loss: forked code copies, orphaned database files, dashboards reading stale data.

Full teardown: https://madcactus.org/newsletter

## The prompt

Hand this to whoever runs Claude Code for you:

> Claude Code is working in our project. Audit it for silent data loss before it costs us money.
>
> 1. List every copy of the project and every local database file. If there is more than one of either, stop new work and consolidate: commit everything, open one pull request, merge it.
> 2. Point the app at one canonical database (Supabase works). Local database files are for local apps only.
> 3. Write a one-page WORKFLOW.md: every session ends with a commit and a pull request. No merge until tests pass.
> 4. Verify: run `select count(*)` on the main table against production and compare it to what the dashboard shows. The numbers must match.
> 5. Keep a dated backup of production data off the cloud. An agent test run can wipe the live copy.
