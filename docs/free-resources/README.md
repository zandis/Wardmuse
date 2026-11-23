# Free resources research

A date-stamped set of audits of free tiers and public services that Wardmuse might use. They are research notes, not the catalogue: the machine-readable, hand-maintained catalogue of AI services is `catalogue/catalogue.v1.json` (see [../catalogue.md](../catalogue.md)).

Nothing here is advice to sign up. No file contains keys, tokens, hostnames of our servers, account ids, or personal e-mail addresses. No real patient data or PHI should go to any free tier listed.

## Files

| File | Date | What it is |
|---|---|---|
| [compute.md](compute.md) | 2026-11-23 | Free VMs, container hosts, CI and dev machines, with specs, limits, card requirements, idle behaviour, region notes, and picks for a second always-on service, ephemeral runners, and a backup/status page. English. |
| [llm-apis.md](llm-apis.md) | 2026-11-15 | Free LLM API providers and the recommended routing architecture (zh-TW). |
| [infra.md](infra.md) | 2026-11-15 | The infrastructure part of the free-for.dev audit: hosting, databases, storage, DNS, CI, observability (zh-TW). Superseded for compute by compute.md. |
| [public-apis.md](public-apis.md) / [public-apis.json](public-apis.json) | 2026-11-16 | 94 public, mostly no-account APIs and services (literature, trial registries, open data, domains, hosting, crypto timestamping), 53 of them without an account (zh-TW). |
| [free-tier-snapshot.json](free-tier-snapshot.json) | 2026-11-15 | Machine-readable snapshot behind llm-apis.md and infra.md: 22 LLM and 60 infra entries with status, limits, card requirement, ToS notes, source URLs. |
| [scripts/](scripts/) | | `data.py` holds the entries; `gen_snapshot.py` writes the snapshot JSON; `gen_audit_md.py` writes the full Markdown audit to `_full-audit.md`. Python 3 standard library only. |

## Known changes since the first audits

- SambaNova's free tier now returns HTTP 402 and asks for a payment method on chat calls (checked 2026-11-22), so it is not usable. llm-apis.md still shows the 2026-11-15 view.
- NVIDIA NIM's free key works (33 models, slow).
- Hugging Face now requires a paid plan to create Docker or Gradio Spaces; static Spaces stay free (compute.md).
- Altare (altare.gg) is new in compute.md.

## Weekly refresh

1. The existing weekly page check (`muse catalog check --pages --report`, see [../catalogue.md](../catalogue.md#the-weekly-page-check)) flags changed source pages for the catalogue.
2. For these notes, edit the entries in `scripts/data.py`, set `CHECKED` to the new date, and run `python3 scripts/gen_snapshot.py` and `python3 scripts/gen_audit_md.py`. Running it overwrites `free-tier-snapshot.json`.
3. `compute.md` and `public-apis.*` are edited by hand. Re-fetch each official page, update the row, and change the date in the heading.
4. Mark anything you could not read as unverified rather than carrying an old number forward.

The notes are advisory; the catalogue and `config/` stay the source of truth for what the stack actually uses.
