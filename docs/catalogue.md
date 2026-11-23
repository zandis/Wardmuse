# The published catalogue

The catalogue is the list of free and trial allowances Wardmuse knows about: AI services, storage, compute, chain and messaging, plus the consumer subscriptions that are hand-off only. It is written by hand in `config/providers.yaml` and `config/resources/*.yaml`. This page describes the copy that is published as JSON for other projects to read, and the weekly check that says when a source page has changed.

The decision to publish it was taken on 2026-11-13 (work package A15). No maintained, machine-readable list of this kind was found in the ecosystem review (`docs/ecosystem-review-2026-11.md`, part 3.1).

## Licence

The published catalogue (the files under `catalogue/`) is licensed **CC BY 4.0**, chosen by the owner on 2026-11-15. The text is in `catalogue/LICENSE`. Anyone may copy and adapt it, provided they credit the source ("Wardmuse Stack service catalogue", with a link to this repository) and say what they changed. The rest of the repository, including the code that builds the catalogue, is Apache-2.0 (`LICENSE` at the root).

The setting is `LICENCE_SPDX` at the top of `scripts/publish_catalogue.py`; the JSON carries the same statement in its `licence` field. The catalogue states facts read from providers' own pages on the dates given; it is not advice, and providers change their terms.

## The files

| File | What it is |
|---|---|
| `catalogue/catalogue.v1.json` | The document, indented. |
| `catalogue/catalogue.v1.min.json` | The same document on one line. |
| `catalogue/schema/catalogue.v1.schema.json` | The JSON Schema (draft 2020-12) for the document. Every object is closed: a field that is not in the schema fails the build. |
| `catalogue/CHANGELOG.md` | A short entry whenever an entry changes. |
| `catalogue/releases/catalogue.v1.<date>.json` | A dated copy, written by `--release`. None exists yet. |

## The shape

One document:

| Field | Meaning |
|---|---|
| `schema_version` | `1.1`. A new optional field raises the second number (1.1 added optional `policy.clinical_use`). A change that breaks readers gets a new file name (`catalogue.v2.json`). |
| `generated_at` | The date given with `--date`, or else the newest `checked_on`. It is not a clock reading. |
| `catalogue_date` | The newest `checked_on` among the entries. |
| `release` | `draft` or `released`, and the release date. |
| `licence` | The status, the SPDX id once chosen, the statement, and the two options. |
| `source` | Repository-relative file names and the rule every fact follows. |
| `ai_services[]` | Cloud AI services and local runtimes. |
| `other_allowances[]` | Storage, compute, chain and messaging. |
| `subscriptions[]` | Consumer subscriptions. Hand-off only: the person opens their own account; nothing is routed through it. |
| `changes[]` | What changed since the previous release. Before the first release: since the first generated draft. |

Each entry holds only public facts:

- `id`, `name`, `kind`, `tier`, and what it is good for.
- `allowance`: the limits, each with its window (`minute`, `day`, `month`, `total`), unit, scope and condition; the reset rule; and a status.
  - `verified` means the number was read on the provider's own page on `checked_on`.
  - `estimated` means a working number that was not read on a page. None is published today.
  - `unknown` means the catalogue holds no confirmed number. It does not mean there is no allowance.
- `connection`: the method (`oauth_pkce`, `paste_key` or `none`), the page where a key is made, plain-language steps in English and Traditional Chinese, whether a card or a phone number is needed (`yes`, `no` or `unknown`), and `minutes_estimate`. The minutes are the maintainers' estimate, not a measurement, and are labelled `"basis": "estimate"`.
- `connection.env_names`: the names of the environment variables this project reads. Names only.
- `policy` and `terms`: whether inputs are used for training, whether people may review them, the region, where it is hosted, commercial use, and the account rules. `policy.clinical_use` is `forbidden` or `allowed` when that has been read in the terms, and is left out when it is unknown. `unknown` means nobody has confirmed it; treat it as the cautious answer.
- `models[]` for AI services: the model id as a LiteLLM route, its mode, the context window where the provider states one, and a price where the catalogue has one read on the provider's page. No price is recorded today.
- `checked_on`, `confidence` (`H`, `M` or `L`), `source_urls` and `notes`.

Confidence follows the catalogue's rule: `H` when every stated fact was read on the provider's pages, `M` when the main facts were and some fields are unknown, `L` when little is confirmed.

What is left out on purpose: key values (there are none in the catalogue), the key-check request used by `muse connect --test`, API base addresses, routing weights, alias names and local paths. `notes` are the maintainers' notes and sometimes mention this project's own settings by name.

Before anything is written, the generator checks the document. It must match the schema. Nothing in it may look like a key or token (the same detector that guards `config/`). It may not contain a local path or a field that is internal by name. If a check fails, nothing is written.

## Generating

```bash
python scripts/publish_catalogue.py            # rewrite catalogue/
python scripts/publish_catalogue.py --check    # exit 1 if catalogue/ is out of date with config/
muse catalog export [--out DIR] [--check]      # the same, from the command-line tool
muse catalog show openrouter [--json]          # one entry as it is published
```

The output is deterministic. Entries are in a fixed order and no clock is read, so two runs give the same bytes. `tests/test_publish_catalogue.py` runs the check, so the YAML and the published JSON cannot drift apart: after editing `config/`, regenerate and commit both.

`changes[]` is worked out against the document already in the output folder. It records entries added and removed, changed limits, changed policy facts, and changed dates and confidence, each with the earlier and the new value. Other changes (wording, steps, notes, models) are named without their text. When nothing changed, the list is kept as it is. The first change after a release starts the list again; the dated release copy keeps the earlier one.

## Keeping it honest: the rules

- Facts come from the provider's own pages only. Each entry is dated and cites the pages.
- A lead list is a list of names to look up. It is never a source of facts.
- Nothing signs up for anything, and nothing is added automatically.
- One entry and one key per provider. Consumer subscriptions are hand-off only.
- A fact that cannot be confirmed is written `unknown`. If the main facts cannot be confirmed, the entry is not added.

Broader, date-stamped research on free compute, LLM APIs, infrastructure and public APIs lives in [`docs/free-resources/`](free-resources/README.md). It is advisory and separate from this catalogue.

## The weekly page check

```bash
muse catalog check --pages --report            # writes catalog-check.json in the Wardmuse home folder
muse catalog check --pages --report FILE --max-pages 40 --delay 2 --leads
```

It only reads. It never edits `config/`, and it refuses to write its report there. Each source page is fetched once with a generic client name; the request carries nothing about the installation. There is a pause between requests to the same site (`--delay`, one second by default). `--max-pages N` caps a run, and the pages checked longest ago go first, so a capped weekly run still works through every page in turn. Exit codes are as before: 0 when there is nothing to do, 1 when an entry is stale or a page changed.

The report is small: the date, the stale entries, the changed and unreachable pages with the entries that cite them, counts for each level, and lead names when `--leads` is given. It holds no page content. The home's dashboard can read it later to show a line such as "3 pages changed since last week".

### Three levels

An earlier live run reported a help page as changed when nothing real had changed. The check now remembers two things for each page: a hash of all the visible text, and a hash of each **fact line**. A fact line is a line or sentence of visible text that holds a number and one of a small set of allowance words (requests, tokens, per day, per minute, free, limit, GB, neurons, calls, messages, 每日, 每分鐘, 免費, 則 and a few more), or one of the units the citing entries use. Dates and clock times are masked first, and "1,000" equals "1000".

| Level | Meaning | What to do |
|---|---|---|
| `unchanged` | The visible text is the same. | Nothing. |
| `text_changed` | The text differs, but the set of fact lines is the same: new wording, navigation, a banner, a new "last updated" date. | Low priority. |
| `facts_changed` | A fact line appeared, went away or changed. | Re-read the page, then edit the entry and its `checked_on` by hand. |

What the tests show on fixture pages (`tests/test_catalog_check.py`), in English and Traditional Chinese: a changed banner, navigation link, footer date or maintenance notice gives `text_changed`; a changed limit, a removed table row or a new plan line gives `facts_changed`; changed markup or scripts alone give `unchanged`.

### Limits of the heuristic

It cannot read.

- A number in a line with none of the words, such as a bare table cell holding "200", is not a fact line. A change to it shows as `text_changed` only.
- A line that has the words and a number but is not about the allowance, such as a counter reading "12,345 developers build for free", is a fact line. It raises `facts_changed` when it moves. That is a false alarm.
- A page drawn by scripts has little visible text to compare.
- A page can stay the same while the provider changes the allowance somewhere else.

So `text_changed` means "probably nothing", never "nothing". An entry still goes stale after 30 days whatever its pages say. One live measurement so far, on 2026-11-13: two runs a few minutes apart over the catalogue's 38 source pages. One page was unreachable both times. Of the other 37, 36 were `unchanged` and one, a Google help page, differed between the runs with nothing real changed. It was reported as `text_changed`, where the earlier check would have said "changed". Whether `facts_changed` stays quiet over weeks has not been measured; that needs a few weeks of reports.

## Checked on 2026-11-13

### Added: LINE Official Account messages (Taiwan)

`config/resources/messaging.yaml`, kind `messaging`, shown and not managed.

- Reply messages are not counted towards the plan's message count. Push, multicast, broadcast and narrowcast messages are. Source: <https://developers.line.biz/en/docs/messaging-api/pricing/>.
- The free plan in Taiwan (輕用量, NT$0) includes 200 messages a month and cannot buy more. The current price plan took effect on 2026-11-01; the announcement is dated 2026-09-01 and leaves the free plan unchanged. Source: <https://tw.linebiz.com/column/LINEOA-2026-Price-Plan/>.
- Recorded as unknown: the time zone the month turns over in, whether a card or a phone number is needed, the full address of the calls that read what is left, and LINE's terms on automation and reselling.

### Not added: Hugging Face

Hugging Face was to be added as an AI service with a sign-in connection. The sign-in facts were confirmed. The free allowance was not: **a free account has no included inference credits today.**

- Sign-in: OAuth with PKCE for public apps and a device-code flow (`https://huggingface.co/oauth/device`, then `https://huggingface.co/oauth/token`). The scope for inference is `inference-api` ("Make inference requests to Inference Providers on behalf of the user"). Source: <https://huggingface.co/docs/hub/oauth>.
- Allowance: the "Included Monthly Credits" table reads Free Users: None, with extra usage "yes (credits purchase required)". PRO users get $2.00 a month; Team and Enterprise get $2.00 per seat. Source: <https://huggingface.co/docs/inference-providers/pricing>. The pricing page agrees: "$2 of included inference credits monthly" appears under PRO only (<https://huggingface.co/pricing>).
- Routing: the installed LiteLLM 1.108.5 lists `huggingface` as a provider and resolves the `huggingface/` model prefix. This was checked in the installed package only; no provider was called.

The catalogue lists free and trial allowances that Wardmuse can suggest. An entry that offered a one-tap sign-in and then failed on the first request for want of credits would mislead. So no entry was added. If the owner wants it listed as a paid service, it needs: tier `paid`; one variable (`HF_TOKEN`) added to `.env.example`; model ids confirmed on Hugging Face's own model pages; prices, since a paid model is used automatically only when it has one; and a sign-in flow in `muse/connect.py`, which today implements only OpenRouter's. That flow would need an OAuth app registered with Hugging Face (a client id), the device-code or PKCE exchange, and a decision on token lifetime and refresh.
