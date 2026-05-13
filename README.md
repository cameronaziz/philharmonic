# Philharmonic

Autonomous job application pipeline for Cameron Aziz.

## Structure

```
data/
  companies.json   — target companies to poll (ATS provider, slug, industry tags)
  jobs.json        — job postings discovered and scored
  preferences.json — attribute-level learning signals
scripts/
  restore.py       — restore Hyperagent Tables from this backup
```

## Data Model

### companies.json
Each row is a target company with ATS provider/slug, industry tags (comma-separated, multi-value),
poll status, and scoring metadata.

Industry tags: `ai_engineering`, `healthtech`, `fintech`, `dev_tools`, `react_typescript`, `high_comp_signal`

### jobs.json
Job postings from Greenhouse/Lever/Ashby polling. Includes fit_score, effective_score, and pipeline_state.

effective_score = fit_score × age_decay × location_multiplier × preference_multiplier

### preferences.json
Attribute-level signals updated after each select/skip/approve action.
Feeds the preference_multiplier component of effective_score.

## Backup Schedule
This repo is updated after every major pipeline run (company adds, score updates, submits).
If Hyperagent Tables are wiped, run `scripts/restore.py --restore` to rebuild from here.

## Links
- Telegram bot: @jobconductor_bot
- Agent: Philharmonic Jobs (Hyperagent)
