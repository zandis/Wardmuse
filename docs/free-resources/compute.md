# Free compute survey (2026-11-23, Asia/Taipei)

Scope: free compute a small project can use legitimately with **one account per provider** (no account farming). Card-required trials are not counted as free unless marked. Every row cites an official page that was fetched on 2026-11-23; "unverified" means the official page was not readable or did not state the fact in this run, so treat it as a lead, not a fact.

Hard rules for everything below:

- **No real patient data or PHI on any free tier.** None of these offers a BAA or a data-processing guarantee. Use synthetic data only.
- **No Oracle upgrade or payment.** The Oracle A1 host stays on Always Free limits; this survey does not suggest changing that.
- Providers change terms often. Re-check the linked page before relying on a number.

## Summary table

| Provider | Free spec | Card at sign-up? | Persistence / idle reclaim | Fit for gateway or eval runner | Region notes | Source |
|---|---|---|---|---|---|---|
| **Oracle Always Free** (we use it) | Always Free services incl. Arm A1 and AMD compute (this project: 4 OCPU / 24 GB A1) | Yes (verification hold) | Permanent; accounts idle 30 days or more may be treated as abandoned and suspended; one account per person | Current home | Home region fixed at sign-up | [oracle.com/cloud/free](https://www.oracle.com/cloud/free/) |
| **Google Cloud e2-micro** | 1 non-preemptible `e2-micro`, 30 GB-month standard disk, 1 GB outbound (see page) per month | Yes (billing account) | Permanent while within Free Tier limits | Small second node (1 GB RAM is tight for LiteLLM + Postgres) | Only `us-west1`, `us-central1`, `us-east1` | [Free Tier list](https://docs.cloud.google.com/free/docs/free-cloud-features.md.txt) |
| Google Cloud Free Trial | $300 credit, 90 days | Yes | Ends after 90 days or when the credit is spent | Trial, not free | Any | same page |
| **Northflank Sandbox** | Up to $20/month of resources on Northflank Cloud: 2 services, 2 jobs, 1 database; "always on, no sleeping"; also one BYOC cluster slot | **No** ("No card needed") | Always on | Good second small service (e.g. 0.5 vCPU / 1 GB plan is $12/month, so about 1.6 of them fit in $20) | See dashboard regions (unverified) | [northflank.com/pricing](https://northflank.com/pricing) |
| **Altare Always Free** | 6 GB RAM, 1.5 CPU, 10 GB disk shared by up to 4 servers; 10 GB U3 (S3-compatible) + 5 buckets; 1 GB KV; 10 Edge Functions, 3M requests/month; 3 PR previews per app | No (stated "free for every team") | Server package persists; free tier is tied to the platform's "AFK earnings / bolts" model, details unverified | OK for a small non-sensitive service; **young service, no track record or compliance statements seen** | 11 regions: us-iad, us-lax, de-fra, se-kna, fi-hel, gb-lon, plus others; U3 in US/EU/Asia | [altare.gg](https://altare.gg/en/) |
| **Altare Go** | Linux machine 4 CPU / 8 GB / 40 GB, **max 12 h**, 3 at once (15 on Plus), controlled with `altr` CLI or `altr mcp` | No | Ephemeral, deleted at the end | Good throwaway eval/test runner | Chosen per machine | [altare.gg](https://altare.gg/en/) |
| **Koyeb Free Instance** | 1 web service: 512 MB RAM, 0.1 vCPU, 2 GB SSD, per organisation; plus a free Postgres limited to 5 h active time and 1 GB | Pricing FAQ says card validation applies when a card is entered; whether the free web service needs one at sign-up is unverified | Scales to zero after 1 h without traffic; cannot be disabled; docs say "should not be used for production" | Status page, redirector, health receiver. Too small for LiteLLM | Frankfurt or Washington D.C. only | [Instances](https://www.koyeb.com/docs/reference/instances), [Scale-to-zero](https://www.koyeb.com/docs/run-and-scale/scale-to-zero), [FAQ](https://www.koyeb.com/docs/faqs/pricing) |
| **Render Free** | Free web service 512 MB RAM; 750 instance hours/month per workspace; free Postgres 256 MB / 100 connections | Not stated on the pages read (unverified) | Spins down after 15 min without inbound traffic, about 1 min to wake, local files lost; free Postgres expires after 30 days | Status page or webhook receiver only | Global regions | [Pricing](https://render.com/pricing), [Free docs](https://render.com/docs/free) |
| **Railway Free** | $1/month usage credit, 1 vCPU / 0.5 GB per service, 1 project, 3 services, 0.5 GB volume | **No** | Serverless: sleeps after 5-10 min without outbound traffic; the Free plan "does not expire" | Tiny worker or cron-like jobs | n/a | [railway.com/pricing](https://railway.com/pricing) |
| Railway Free Trial | $5 one-time credit, 30 days | No | Stops when the trial ends | Trial only | n/a | same page |
| Railway Sandboxes (free plan) | Ephemeral Linux VMs, up to 2 vCPU / 2 GB, 10 running, 5 min idle timeout; billed from the $1 credit | No | Destroyed on idle timeout | Short eval/test runs only, the credit is small | n/a | same page |
| **Fly.io** | Free plan: $1 credit with no card, $5/month usage once a card is added; up to 3 Machines | Needed for the $5/month | Pay-as-you-go thereafter | Not free in practice | Many | [Pricing](https://fly.io/docs/about/pricing/) |
| **Cloudflare Workers (Free)** | 100,000 requests/day, 10 ms CPU per invocation; static assets free and unlimited | No | Serverless | Status page, health receiver, small proxy (not a long-lived gateway: CPU limit) | Global edge | [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/) |
| Cloudflare Containers | Billed only under the $5/month Workers Paid plan (Free plan row is N/A) | Paid | n/a | Not free | n/a | [Containers pricing](https://developers.cloudflare.com/containers/pricing/) |
| **Deno Deploy (Free)** | 1M requests/month, 10 h active CPU, 1 month metrics | Not stated (unverified) | Serverless | Small status or webhook handler | Global | [deno.com/deploy/pricing](https://deno.com/deploy/pricing) |
| **Vercel Hobby** | Free, with usage limits; if exceeded you wait up to 30 days for features to resume | No | Serverless | Static or small functions. Hobby is for personal, non-commercial use (carried over from the 2026-11-15 audit; the terms page was not readable in this run, unverified) | Global | [Hobby plan](https://vercel.com/docs/plans/hobby) |
| **Netlify Free** | Credit-based: free plan is "always free" with hard monthly limits; when reached, **all** projects on the account pause until the next cycle | No | Serverless/static | Static status page only | Global | [netlify.com/pricing](https://www.netlify.com/pricing/) |
| **GitHub Actions** | Standard runners are **free in public repositories**; private repos draw from a monetary included amount | No extra | Ephemeral per job | Best default eval/test runner for this public repo | GitHub-hosted | [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) |
| **GitHub Codespaces** | Free personal account: 120 compute hours + 15 GB-month storage per month (a 2-core machine counts 2x, so about 60 h); blocked, not billed, if no payment method | No | Stops when idle; storage persists while the codespace exists | Interactive dev box, not a service | GitHub regions | [Codespaces billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) |
| **Google Cloud Shell** | Free; 50 h/week quota; 5 GB persistent disk; disk deleted after 120 days without use | Needs a Google Cloud project (card not stated for Shell) | Session-based | Admin shell only | Google-chosen | [Cloud Shell limits](https://docs.cloud.google.com/shell/docs/limitations) |
| **Hugging Face Spaces** | Static Spaces free. **Gradio and Docker Spaces now need a paid plan to create** (free accounts keep up to 2 ZeroGPU Gradio Spaces). CPU Basic is 2 vCPU / 16 GB, ephemeral disk | No for static | Ephemeral disk | Static status page only. No longer a free runner | Hub-managed | [Spaces overview](https://huggingface.co/docs/hub/spaces-overview) |
| **Google Colab (free)** | Free GPUs/TPUs, not guaranteed; runtimes are deleted when idle and have a maximum lifetime; **SSH shells, remote desktops, and web UIs for content generation are disallowed on free runtimes** | No | Ephemeral | Notebook experiments only. Violates ToS if used as a server | Google-chosen | [Colab FAQ](https://research.google.com/colaboratory/faq.html) |
| **Lightning AI (Free)** | Up to 30 credits to start; 1 free Studio that runs 24/7 but must restart every 4 h; "up to 50 free GPU hours" on the pricing page | No ("No credit card") | Studio persists; 4 h restart | Notebook or GPU experiments. Not a service host | n/a | [lightning.ai/pricing](https://lightning.ai/pricing) |
| **Modal Starter** | $30/month free compute credit, 3 seats, pay-as-you-go beyond | Not stated (unverified) | Serverless functions | Batch eval jobs that need GPUs or fan-out | Region selection listed under Starter | [modal.com/pricing](https://modal.com/pricing) |
| AWS Free plan | Up to $200 in credits over 6 months; account closes on its own at the end of the free plan | Sign-up details unverified | 6 months only | Time-limited, not free long term | Any | [aws.amazon.com/free](https://aws.amazon.com/free/) |
| Azure, IBM Cloud, Alibaba Cloud, Kaggle, Gitpod/Ona | **Unverified.** The official pages were JavaScript-only or did not state limits in this run. Older sources describe 12-month or credit offers for Azure and Alibaba, a Lite plan for IBM, a weekly GPU quota for Kaggle. | | | | | Not relied on |

## Recommendations

### (a) Second always-on small service (status page, health receiver, small API)

1. **Northflank Sandbox.** No card, "always on, no sleeping", $20/month of resources. It is the only no-card option found that does not sleep. Fits one 0.5 vCPU / 1 GB service plus a job. Not for PHI; keep it to non-sensitive endpoints.
2. **Google Cloud e2-micro** (US regions only). Truly permanent, but it needs a billing account (card) and has 1 GB RAM and is far from Taiwan. Only if the owner decides to give a card to Google; that is a payment decision, not made here.
3. **Altare Always Free.** 4 server slots in one 6 GB pool, no card, many regions. Because the service is young and its stability and security are not evidenced, use it for low-risk workloads only, and never put LiteLLM keys on it.

Do not use Render, Koyeb, Railway, Deno or Netlify free tiers for anything that must answer promptly: they sleep, pause or stop.

### (b) Ephemeral eval/test runners

1. **GitHub Actions** on the public Wardmuse repo. Free, clean machine each job, already wired to CI.
2. **Altare Go** machines (4 CPU / 8 GB / 40 GB, up to 12 h, 3 at a time) for runs longer than a job, or when the runner needs a clean Debian box and SSH. Driven by `altr` or its MCP server. Treat as untrusted: synthetic data only, no keys beyond a throwaway.
3. **Codespaces** (about 60 h of 2-core per month) for interactive debugging.

Colab free is not allowed for server-style use; Modal's $30/month credit is the option if an eval needs GPUs.

### (c) Backup and status page

1. **Cloudflare Workers/static assets (Free).** No card, static assets unlimited, 100k requests/day. Best status page.
2. **Altare U3** (10 GB, S3-compatible, no egress fee) as an offsite copy of non-sensitive config backups. Encrypt before upload. Keep a second copy elsewhere because the provider is new.
3. **Hugging Face static Space** or **GitHub Pages** as a fallback status page (GitHub Pages was not re-verified in this run).

## How this was checked

Pages were fetched with a plain HTTP client on 2026-11-23 and the relevant lines read. JavaScript-only pages could not be read and are marked unverified. Prices and limits are as printed on the pages that day.
