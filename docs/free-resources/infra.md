# Infra 免費層（free-for.dev 盤點 · Infra 部分）

查核日期 2026-11-15（台北時間）。資料來源與方法見 [llm-apis.md](llm-apis.md) 開頭。更新的運算資源調查見 [compute.md](compute.md)。

## Infra 免費層

### 主機 / 運算

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Oracle Cloud Always Free（A1） | 可用但有限制 | A1 每月 1,500 OCPU-h + 9,000 GB-h（約 2 OCPU / 12 GB）；10 TB egress | 要卡驗證 | 可（無台灣區，用日本 / 新加坡） | 自己的 VM，資料在自己手上；無 BAA，不放 PHI | 可 | 7 天內 CPU 95 百分位、網路、記憶體都 < 20% 可能被回收 | 使用中（muse-a1） | https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm |
| Google Cloud Free Tier | 可用但有限制 | 1 台 e2-micro（us-west1 / central1 / east1）、30 GB 標準 PD、北美出站每月 1 GB；新帳號 $300 / 90 天 | 要卡 | 可（機器在美國） | 自己的 VM；無 BAA，不放 PHI | 可 | 不回收；超量會收費 | 1 GB RAM 跑不動 LiteLLM，只適合當外部探針 / 備援 cron | https://cloud.google.com/free/docs/free-cloud-features |
| AWS Free plan | 不建議 | 新帳號 $100 + 最多再 $100 credits，6 個月；30+ 服務有 always-free 額度 | 要卡 | 可 | — | 可 | Free plan 6 個月或 credits 用完就結束 | 短期實驗用，不適合長駐 | https://aws.amazon.com/free/ |
| Azure Free | 不建議 | 新客戶 12 個月免費服務 + 首 30 天 credit；部分服務 always free | 要卡 | 可 | — | 可 | 12 個月後轉 pay-as-you-go | 短期實驗用 | https://azure.microsoft.com/en-us/pricing/free-services |
| Fly.io | 已失效 | 新帳號只剩 7 天 / $1 trial，舊的免費額度已取消 | 要卡 | — | — | — | trial 結束即停 | free-for.dev 仍寫有免費層，已過時 | https://fly.io/docs/about/pricing/ |
| Render | 不建議 | Free web service；免費 Postgres | 不用卡 | 可 | — | 可 | 閒置 15 分鐘休眠；免費 Postgres 30 天到期 | 冷啟動慢，DB 會過期 | https://render.com/docs/free |
| Railway | 不建議 | $5 trial，之後 Free 方案每月 $1 credit | — | 可 | — | 可 | 額度用完就停 | 額度太小 | https://docs.railway.com/reference/pricing/plans |
| Koyeb | 不建議 | 每組織 1 個 Free Instance：512 MB / 0.1 vCPU / 2 GB SSD | — | 可 | — | 官方說不可用於 production | 1 小時沒流量 scale to zero | 太小 | https://www.koyeb.com/docs/reference/instances |
| Hetzner | 不建議 | 沒有免費層（便宜付費 VPS） | — | 可（EU / US / 新加坡） | — | 可 | — | 只在 OCI 被回收時當付費備案 | https://www.hetzner.com/cloud/ |

### Serverless / 邊緣

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Cloudflare Workers | 可用 | 每天 10 萬請求、每次 10 ms CPU | 不用卡 | 可 | CF 處理流量；無 BAA，不放 PHI | 可 | 超量直接失敗，不扣錢 | 輕量 webhook / cron / 狀態頁；不適合跑 LiteLLM | https://developers.cloudflare.com/workers/platform/pricing/ |
| Cloudflare Pages | 可用 | 靜態站免費；每月 500 次 build（free-for.dev 數字） | 不用卡 | 可 | — | 可 | — | Muse 文件 / 狀態頁 | https://developers.cloudflare.com/pages/platform/limits/ |
| Cloudflare D1 | 可用但有限制 | 5 GB 總量、每天讀 500 萬 rows | 不用卡 | 可 | — | 可 | — | 只有搭 Workers 才用得到 | https://developers.cloudflare.com/d1/platform/pricing/ |
| Cloudflare KV | 可用但有限制 | 1 GB、每天 10 萬次讀 | 不用卡 | 可 | — | 可 | — | 同上 | https://developers.cloudflare.com/kv/platform/pricing/ |
| Cloudflare Queues | 可用但有限制 | 每天 10,000 operations | 不用卡 | 可 | — | 可 | — | 同上 | https://developers.cloudflare.com/queues/platform/pricing/ |
| Vercel Hobby | 可用但有限制 | 200 個專案、function 最長 300 秒 | 不用卡 | 可 | — | 條款限個人 / 非商業 | — | Muse 是個人用可以；Cloudflare 已涵蓋 | https://vercel.com/legal/terms |
| Netlify Free | 可用但有限制 | 每月 300 credits（build、頻寬、functions 共用） | 不用卡 | 可 | — | 可 | credits 用完當月停 | Cloudflare 已涵蓋 | https://www.netlify.com/pricing/ |
| Deno Deploy Free | 可用但有限制 | 每月 100 萬請求、20 GiB egress | 不用卡 | 可 | — | 可 | — | Cloudflare 已涵蓋 | https://deno.com/deploy/pricing |

### 物件儲存

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Cloudflare R2 | 可用 | 10 GB，egress 免費 | 不用卡 | 可 | 加密後再上傳；無 BAA，不放 PHI | 可 | — | ledger / DB 加密後異地備份（首選） | https://developers.cloudflare.com/r2/pricing/ |
| Backblaze B2 | 可用 | 10 GB | 不用卡 | 可 | 同上 | 可 | — | R2 的備援 | https://www.backblaze.com/cloud-storage/pricing |
| OCI Object Storage | 可用但有限制 | Always Free 10 GB | （同 OCI 帳號） | 可 | 同上 | 可 | — | 和 VM 同一個帳號，不算異地備份 | https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm |

### 資料庫

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Turso | 可用但有限制 | 100 個 DB、5 GB、每月 5 億次讀、1,000 萬次寫 | 不用卡 | 可 | — | 可 | 閒置只算儲存 | SQLite 邊緣副本，Muse 目前用不到 | https://turso.tech/pricing |
| Neon | 不建議 | 每專案 0.5 GB、100 個專案 | 不用卡 | 可 | — | 可 | 閒置 scale to zero | LiteLLM DB 放本機比較好 | https://neon.com/pricing |
| Supabase | 不建議 | 2 個專案、500 MB DB、1 GB 檔案 | 不用卡 | 可 | — | 可 | 1 週沒活動就暫停 | 會被暫停，不適合常駐 | https://supabase.com/pricing |
| MongoDB Atlas M0 | 不建議 | 512 MB | 不用卡 | 可 | — | 可 | — | stack 沒有 Mongo | https://www.mongodb.com/pricing |
| Upstash Redis | 不建議 | 1 個 DB、每月 50 萬指令 | 不用卡 | 可 | — | 可 | — | 單台 VM 不需要 | https://upstash.com/pricing/redis |
| Upstash QStash | 可用但有限制 | 每天 1,000 則訊息 | 不用卡 | 可 | — | 可 | — | 需要重試的 webhook / 排程，可當 GHA cron 的備援 | https://upstash.com/pricing/qstash |
| CockroachDB | 不建議 | 可免費建組織、不用卡；靜態頁看不到免費額度 | 不用卡 | 可 | — | ? | ? | 用不到 | https://www.cockroachlabs.com/pricing/ |

### 向量 DB

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Qdrant Cloud | 可用但有限制 | 1 個 cluster：0.5 vCPU / 1 GB RAM / 4 GB disk | 不用卡 | 可 | 向量也可能還原內容；private 類放本機 | 可 | 定價頁沒寫閒置政策 | RAG 先用本機 Qdrant（Docker 跑在 A1）；雲端只放 public | https://qdrant.tech/pricing/ |
| Pinecone Starter | 可用但有限制 | 免費；官方用例估算約 3 萬份 1024 維文件、每天約 1.5 萬次搜尋 | 不用卡 | 可 | 同上 | 可 | ? | 同上 | https://www.pinecone.io/pricing/ |
| Zilliz Cloud Free | 可用但有限制 | 5 GB、每月 250 萬 vCU | 不用卡 | 可 | 同上 | 可 | ? | 同上 | https://zilliz.com/pricing |
| Weaviate Cloud Free | 可用但有限制 | Always free，每人 1 個 cluster：10 萬 objects、1 GB 記憶體、10 GB disk、1 collection | 不用卡 | 可 | 同上 | 可 | ? | 同上 | https://weaviate.io/pricing |

### GPU / 推理額度

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Kaggle | 可用但有限制 | 每週約 30 小時 GPU（free-for.dev 數字；官方頁需登入才看得到） | 要手機驗證 | 可 | 資料會上 Kaggle；不放 PHI | 依條款 | 每次 session 有時限 | 離線評估 / embedding 批次，不能做線上服務 | https://www.kaggle.com/docs/notebooks |
| Google Colab Free | 可用但有限制 | 免費 GPU / TPU，但不保證、額度會變 | 不用卡 | 可 | 不放 PHI | 依條款 | 閒置會刪 VM，有最長壽命 | 同上 | https://research.google.com/colaboratory/faq.html |
| Modal Starter | 可用但有限制 | 每月 $30 免費 credit | 未確認 | 可 | — | 可 | 每月重置 | 短時間 GPU 批次（例如自己的 embedding / 小模型） | https://modal.com/pricing |
| Lightning AI | 可用但有限制 | 免費 hours + 最多 30 credits；1 個免費 Studio（4 小時重啟） | 不用卡 | 可 | — | 可 | 免費 Studio 每 4 小時重啟 | 同上 | https://lightning.ai/pricing |

### 寄信

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Resend | 可用 | 每月 3,000 封、每天 100 封、3 個網域 | 不用卡 | 可 | 信件內容經第三方；不寄 PHI | 可 | — | 告警 / 摘要寄給自己（首選） | https://resend.com/pricing |
| Brevo | 可用但有限制 | 每天 300 封（帳號要先審核） | 不用卡 | 可 | 同上 | 可 | — | Resend 的備援 | https://www.brevo.com/pricing/ |
| Mailjet | 可用但有限制 | 每月 6,000 封、每天 200 封 | 不用卡 | 可 | 同上 | 可 | — | 另一個備援 | https://www.mailjet.com/pricing/ |
| AgentMail | 可用但有限制 | 3 個 inbox、每月 3,000 封、3 GB | 不用卡 | 可 | 同上 | 可 | — | 給 agent 收發信用；目前 bot 已有自己的 inbox | https://www.agentmail.to/pricing |
| Cloudflare Email Routing | 可用但有限制 | 轉寄免費；寄給任意收件人要 Workers Paid | 不用卡 | 可 | — | 可 | — | 自有網域收信 | https://developers.cloudflare.com/email-routing/ |

### Auth

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Clerk | 可用但有限制 | 每月 50,000 MRU | 不用卡 | 可 | — | 可 | — | Muse 只有一個使用者，用 Tailscale / CF Access 就夠 | https://clerk.com/pricing |
| Auth0 | 可用但有限制 | 每月 25,000 MAU | 不用卡 | 可 | — | 可 | — | 同上 | https://auth0.com/pricing |

### 觀測

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Grafana Cloud | 可用但有限制 | 永久免費，保留 14 天 | 不用卡 | 可 | 指標 / 日誌不能帶 prompt | 可 | — | 先確認 LiteLLM 開源版的 Prometheus 指標 | https://grafana.com/pricing/ |
| Better Stack | 可用但有限制 | 個人專案免費（細節未完整查核） | 不用卡 | 可 | 同上 | 可 | — | UptimeRobot 的替代 | https://betterstack.com/pricing |
| Sentry Developer | 可用但有限制 | 1 人 | 不用卡 | 可 | 必須遮蔽 prompt 和回應 | 可 | — | 錯誤追蹤 | https://sentry.io/pricing/ |
| Axiom | 可用但有限制 | 永久免費額度 | 不用卡 | 可 | 日誌不能帶內容 | 可 | — | 日誌 | https://axiom.co/pricing |
| Langfuse Cloud Hobby | 可用但有限制 | 每月 50k units、保留 30 天 | 不用卡 | 可 | LiteLLM callback 會送 prompt 上雲；只送 public 類 | 可 | 30 天後刪資料 | LLM trace | https://langfuse.com/pricing |
| Langfuse 自架 | 可用但有限制 | 開源免費；要 Postgres + ClickHouse + Redis + S3 | — | 可 | 資料留在自己機器，private 類可用 | 可 | — | A1 12 GB 跑得動但吃資源；要上再評估 | https://langfuse.com/self-hosting |
| UptimeRobot | 可用 | 50 個監控、5 分鐘間隔，商用也可；SSL 監控要付費 | 不用卡 | 可 | — | 可 | — | 監控 /health 和 Caddy 對外端點 | https://uptimerobot.com/pricing/ |
| healthchecks.io | 可用 | 20 個 checks | 不用卡 | 可 | — | 可 | — | 週任務和備份的 dead-man switch | https://healthchecks.io/pricing/ |

### CI / Registry

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| GitHub Actions | 可用 | Free 每月含 $12 額度；公開 repo 和自架 runner 免費 | — | 可 | log 不要印 secrets | 可 | — | 使用中 | https://docs.github.com/en/billing/concepts/product-billing/github-actions |
| GHCR（GitHub Container Registry） | 可用 | 容器映像的儲存和流量目前免費（改政策前至少提前一個月通知） | — | 可 | image 裡不能有 .env | 可 | — | Muse 映像推到 GHCR，A1 直接 pull | https://docs.github.com/en/billing/concepts/product-billing/github-packages |
| Let's Encrypt | 可用 | 免費 | — | 可 | — | 可 | — | Caddy 自動處理（使用中） | https://letsencrypt.org/ |

### DNS / Tunnel / 零信任

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Tailscale Personal | 可用 | 永久免費，裝置不限，最多 6 人 | 不用卡 | 可 | WireGuard 端到端加密 | 個人用 | — | SSH、LiteLLM UI、dashboard 只走 tailnet | https://tailscale.com/pricing |
| Cloudflare DNS / Access / Tunnel | 可用但有限制 | DNS、WAF、Tunnel 免費；Zero Trust 最多 50 人 | 不用卡 | 可 | 開 proxy 時 CF 會解開 TLS；private 流量用 DNS-only 或 Tailscale | 可 | — | Access 擋管理頁 | https://www.cloudflare.com/plans/ |
| ngrok / Pinggy | 不建議 | 有限 | — | 可 | — | ? | — | Tailscale / CF Tunnel 已涵蓋 | https://ngrok.com/pricing |
| deSEC / DuckDNS | 不建議 | 免費 | — | 可 | — | 可 | — | Cloudflare 已涵蓋 | https://desec.io/ |

### Secrets

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Infisical | 可用但有限制 | 免費 5 個 identities，可自架 | 不用卡 | 可 | — | 可 | — | 選用；.env（0600）+ GHA secrets 已夠 | https://infisical.com/pricing |
| Doppler | 不建議 | 免費 3 人 | 不用卡 | 可 | — | 可 | — | 和 Infisical 重複 | https://www.doppler.com/pricing |

### 第三方 gateway

| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Portkey / Keywords AI / Future AGI | 不建議 | 每月 1 萬筆 log 等 | — | 可 | 會把 prompt 交給第三方 | ? | — | 和 LiteLLM 重複（第三方 gateway） | https://portkey.ai/pricing |

## 建議的 routing 分層

- fast：1 Groq gpt-oss-20b、Gemini 3.1 Flash-Lite → 2 CF glm-4.7-flash / gpt-oss-20b → 9 OpenRouter :free
- cheap：1 Gemini 3.5 Flash-Lite、Groq gpt-oss-20b → 2 CF granite-4.0-h-micro → 3 Z AI GLM-4.7-Flash（只放 public）→ 9 OpenRouter lfm
- smart：1 Gemini 4 Hydrogen、3.8 Flash、Groq gpt-oss-120b → 2 CF gpt-oss-120b → 3 SambaNova DeepSeek-V3.1 / gpt-oss-120b（每天 20 次）→ 4 Gonka DeepSeek-V4-Flash（只放 public）→ 8 Cohere（trial）→ 9 OpenRouter
- long-context：1 Gemini 3.8 Flash / 4 Hydrogen（1M）→ 3 Z AI GLM-4.7-Flash（200K）→ 9 OpenRouter nemotron-3.5-lightning
- vision（新 alias）：1 Groq qwen3.8-27b、Gemini → 2 CF llama-4-scout / gemma-4-26b
- embed / rerank：gemini-embedding-2 → CF bge-m3（維度不同，不能混用同一個 index）；rerank 用 Cohere trial
- 緊急備援：OVH 匿名端點（每模型 2 RPM）
- private 類：只能用 Groq（ZDR）、Cloudflare、OVH 匿名、本地模型；SambaNova 資料政策未明，先不放；PHI 只走本地

## 和現有 gateway 比還缺什麼

1. Cloudflare Workers AI token（要 Chang-Fu 本人建）
2. Gemini 4 Hydrogen、Gemma 4（現有 key，只要改設定）
3. Groq qwen/qwen3.8-27b + vision alias（qwen3.6 已在 2026-09-14 下線）
4. 移除 Gemini 2.5（PR #7）；2.5 會在 2026-12-01 自動轉到 3.8 Flash / 3.5 Flash-Lite
5. PR #1：SiliconFlow 國際站沒有免費模型，應改標付費；NIM 應標成免費、只限原型開發
6. OpenRouter 目前 50 RPD；一次買 10 credits 可升到 1000 RPD，要 Chang-Fu 決定
7. SambaNova、Z AI 還沒接（都要另外註冊帳號，由 Chang-Fu 決定）
8. Stack 其他層：R2 備份、UptimeRobot + healthchecks.io、Resend 告警、GHCR 映像，都要 Chang-Fu 自己開帳號

## ToS 衝突

- Gemini API：所有方案都禁止用在臨床實務或醫療建議；免費層不可送敏感或個人資料（Health bot 硬限制）
- Cohere trial：不得用於 production 或商用
- NVIDIA NIM：只限原型開發；不可送個人或機密資料
- Vercel Hobby / AI Gateway 免費層：只能個人或非商業使用
- Koyeb Free Instance：官方說不可用於 production
- ModelScope：非商用，還要中國實名
- OpenRouter / Gonka：禁止多帳號、禁止轉售；單人自用 gateway 沒問題
- onomeo / Kilo / LLM7：共用額度或免 key 通道，違反 ToS-clean 規則

沒有任何一家明文禁止「單人經自己的 gateway 轉發」。會拿輸入訓練或記錄的（不能碰任何醫療資料）：Gemini 免費層、Kilo 免費模型、NVIDIA NIM、Cohere trial（可能）、OpenRouter 部分免費上游；SambaNova 未寫明。

## 自動維護

快照 free-tier-snapshot.json 每家都有 provider、category、status、key_limits、card_required、trains_on_input、commercial_use、reclaim_sleep_expiry、source_url、pricing_url、changelog_url、checked_at。每週抓 pricing_url / changelog_url 做 diff 即可。產生腳本：/workspace/reports/gen/（data.py 是唯一資料來源，gen.py 產生 JSON，md.py 產生本檔）。

未能確認：Modal 是否要綁卡、Kaggle 官方 GPU 時數（要登入）、CockroachDB 免費額度、Qdrant / Pinecone / Zilliz 閒置政策、Better Stack 細節、Mistral Codestral 免費端點、OpenCode Zen。
