# 免費 LLM API 與路由（free-for.dev 盤點 · LLM 部分）（for Muse stack / routing）

查核日期 2026-11-15（台北時間）。主清單 free-for.dev；mnfst/awesome-free-llm-apis 和 cheahjs/free-llm-api-resources（Wayback 2026-08-06）當 LLM 交叉比對。全部回到官方頁面查核；只讀，沒有註冊任何帳號。

機器可讀快照：`free-tier-snapshot.json`（同目錄）

## 統計

| 狀態 | LLM | Infra |
|---|---|---|
| 可用 | 3 | 11 |
| 可用但有限制 | 9 | 33 |
| 不建議 | 7 | 15 |
| 已失效 | 3 | 1 |
| 合計 | 22 | 60 |

## 這次的變動（對比 cheahjs 2026-08 快照與 free-for.dev）

- Cerebras → 已失效：官方 FAQ 說沒有永久免費層，只剩 30 天 $5 trial，要驗證付款方式（8 月還有 5 RPM / 1M TPD 免費）。
- Mistral La Plateforme → 已失效：Free 模式不含 API，要開 billing（8 月的 Experiment 免費層要同意訓練，已取消）。
- SambaNova → 可用但有限制：新的 Free Tier，不用綁付款，20 RPM / 20 RPD / 200K TPD（8 月只有 $5 trial）。
- Vercel AI Gateway → 可用但有限制：每月 $5 credit，只限 Free Tier 模型；Hobby 條款限個人非商業。
- Fly.io → 已失效：只剩 7 天 / $1 trial（free-for.dev 已過時）。
- AWS 改成 credits 制 Free plan（最多 $200、6 個月）。
- Cloudflare Queues 免費方案每天含 10,000 operations。

## Muse 建議架構

| 層 | 建議的免費選項 | 現況 / 待辦 |
|---|---|---|
| 主機 | OCI A1 Always Free（2 OCPU / 12 GB） | 已有：muse-a1。要留意閒置回收規則；備案是 Hetzner 付費 VPS，不是其他免費層 |
| LLM gateway | LiteLLM（自架） | 已有。不要換成 Portkey 之類第三方 gateway |
| LLM 上游 | Groq + Gemini + Cloudflare Workers AI，OpenRouter :free 當最後一層；SambaNova 可當 smart 的小額備援 | 已有 Groq / Gemini / OpenRouter；缺 Cloudflare token；SambaNova 新發現 |
| TLS / 反代 | Caddy + Let's Encrypt | 已有 |
| 私網 / 管理入口 | Tailscale；要對外的頁面用 Cloudflare Access | Tailscale 待確認是否已裝；CF Access 未設 |
| DNS | Cloudflare DNS（private 流量 DNS-only） | 視網域現況 |
| CI / 映像 | GitHub Actions + GHCR | 已有 GHA；GHCR 未用 |
| 排程 | GitHub Actions cron；需要重試再加 Upstash QStash | 已有 |
| 資料庫 | LiteLLM 的 Postgres 放 A1 本機 | 已有（本機）；不需要雲端 DB |
| 向量 DB | 本機 Qdrant（Docker）；雲端 Qdrant / Zilliz 免費層只放 public | 未有 |
| 備份 | R2（加密後上傳），B2 備援 | 未設 |
| 監控 | UptimeRobot（外部）+ healthchecks.io（排程） | 未設 |
| 觀測 | Grafana Cloud 免費層（只送指標）；LLM trace 要嘛自架 Langfuse，要嘛 Langfuse Cloud 只送 public | 未設 |
| 寄信 | Resend（告警寄給自己），Brevo / Mailjet 備援 | 未設 |
| Secrets | 伺服器 .env（0600）+ GHA secrets | 已有 |
| GPU 批次 | Modal $30/月 或 Kaggle（只放 public 資料） | 不需要，除非要自跑 embedding |

## LLM routing 供應商

| 供應商 | 狀態 | 免費額度 | 卡 / 電話 | 台灣 | API / LiteLLM | 重點模型 | 會拿輸入訓練 | 資料 / ToS | 來源 |
|---|---|---|---|---|---|---|---|---|---|
| Google AI Studio（Gemini） | 可用 | 有免費層；官方不再公布各模型 RPM/RPD，以 AI Studio 為準（free-for.dev 寫 Flash 5 RPM / 20 RPD，Gemma 4 30 RPM / 14.4K RPD） | 不用卡 | 可（在名單內） | OpenAI 相容 + `gemini/` | Gemini 4 Hydrogen（新，免費）、3.8 Flash、3.5 / 3.1 Flash-Lite、Gemma 4、embedding-2；2.5 已淘汰 | 是（免費層） | 免費層會訓練＋人工審閱，不可送敏感或個人資料；全方案禁止臨床實務 / 醫療建議 | https://aistudio.google.com/docs/terms |
| Groq | 可用 | 30 RPM、1K RPD、8K TPM、200K TPD（gpt-oss / qwen3.8） | 不用卡 | 未見限制 | OpenAI 相容 + `groq/` | gpt-oss-120b、gpt-oss-20b、qwen3.8-27b（視覺） | 否 | 預設不保留、可開 ZDR；資料在美國；無 BAA | https://console.groq.com/docs/rate-limits |
| Cloudflare Workers AI | 可用 | 每天 10,000 Neurons（00:00 UTC 重置，超過就失敗、不扣錢）；gpt-oss-120b 約 100 次/天 | 不用卡 | 未見限制 | OpenAI 相容 + `cloudflare/` | gpt-oss-120b/20b、glm-4.7-flash、gemma-4-26b、llama-4-scout、bge-m3 | 否 | 不拿 Customer Content 訓練；標準推理不保留 | https://developers.cloudflare.com/workers-ai/platform/pricing/ |
| SambaNova Cloud | 可用但有限制 | Free Tier（不用綁付款）：20 RPM、20 RPD、200K TPD | 不用卡 | 未見限制 | OpenAI 相容 + `sambanova/` | DeepSeek-V3.1、Llama-3.3-70B、gpt-oss-120b；預覽 DeepSeek-V3.2、gemma-4-31b | 未明 | 隱私權政策沒寫 API 內容是否訓練，先當 standard 類 | https://docs.sambanova.ai/docs/en/models/rate-limits |
| OpenRouter | 可用但有限制 | :free 20 RPM；50 RPD（買過 credits 少於 10）或 1000 RPD（10 以上） | 免費不用卡 | 未見限制 | `openrouter/` | gemma-4-26b/31b、nemotron-3-ultra、openrouter/free | 視上游 | 禁多帳號繞限制、禁轉售 API；部分免費供應商會記錄或訓練 | https://openrouter.ai/docs/api-reference/limits |
| Vercel AI Gateway | 可用但有限制 | 每個 team 每月 $5 credit，只限 Free Tier 模型、較低 rate limit；免費層不能 BYOK | Vercel 帳號 | 未見限制 | OpenAI 相容 + `vercel_ai_gateway/` | Free Tier 合格模型（清單常變） | 視上游 | Hobby 方案條款限個人 / 非商業；資料經 Vercel 再到上游 | https://vercel.com/docs/ai-gateway/pricing |
| Z AI（GLM） | 可用但有限制 | GLM-4.7-Flash、4.6V-Flash 免費；有併發限制（清單寫 1） | 海外手機可 | 可 | OpenAI 相容（api.z.ai） | GLM-4.7-Flash（200K）、GLM-4.6V-Flash | 否（預設） | API 內容預設不訓練（明確同意才會）；可能在境外處理 | https://docs.z.ai/guides/overview/pricing |
| Gonka Broker | 可用但有限制 | 每月至少 1M tokens；免費期間 RPM 較低 | 簡訊驗證（不能用 VoIP） | 未見限制 | OpenAI 相容 | DeepSeek-V4-Flash、GLM-5.3-Flash、MiniMax-M2.7 | 不保證 | 跑在去中心化節點上，只能放 public；禁多帳號 | https://app.gonkabroker.com/terms-of-service |
| Cohere | 可用但有限制 | Trial 每月 1,000 calls、20 RPM | 不用卡 | 未見限制 | 相容 + `cohere_chat/` | Command A、R7B、Embed、Rerank | 可能 | Trial 不得用於 production / 商用；資料可能用於改進 | https://cohere.com/pricing |
| OVHcloud AI Endpoints | 可用但有限制 | 匿名：每 IP 每模型 2 RPM | 匿名不用 | 可（EU） | OpenAI 相容 | Qwen3.5-397B、gpt-oss-120b、Llama-3.3-70B | 否 | 官方說不儲存用戶資料 | https://help.ovhcloud.com/csm/en-public-cloud-ai-endpoints-getting-started |
| Aion Labs | 可用但有限制 | 每日免費 credit（清單寫 15 RPM、20K TPD） | 不用卡 | 未見限制 | OpenAI 相容 | aion-3.0 系列（角色扮演 / 寫作） | 否 | 不訓練、不儲存；允許商用 | https://www.aionlabs.ai/terms |
| NVIDIA NIM | 可用但有限制 | 免費限原型開發；RPM 依模型而定，不公開 | Developer Program | 未見限制 | `nvidia_nim/` | nemotron-3-ultra、gpt-oss-20b 等 160+ 個 | 會記錄 | production 要授權；不可送個人或機密資料，會記錄 | https://forums.developer.nvidia.com/t/nvidia-nim-faq/300317 |
| onomeo | 不建議 | 每人 60 次/5 小時；全體用戶合計 450 次/5 小時 | ? | ? | OpenAI 相容 | 多家 | ? | 跨用戶共用額度，等於 key pooling；beta | https://onomeo.com/ |
| Mediaworkbench.ai | 不建議 | 10 萬字（聊天 app） | ? | ? | 不是 API | — | ? | 無法接 routing | https://mediaworkbench.ai |
| Cohesivity | 不建議 | 每月 $5 credits | ? | ? | agent backend | — | ? | 不是推理供應商 | https://cohesivity.ai |
| Kilo Code gateway | 不建議 | 免 key，每 IP 每小時 200 次 | 不用 | ? | OpenAI 相容 | 免費池常變 | 是（免費模型） | 免 key 通道（PR #8 已不採用）；免費模型可能拿 prompt 訓練 | https://kilo.ai/docs/gateway/models-and-providers |
| LLM7.io | 不建議 | 60 RPM、每小時 250 次、每天 100K tokens，可能不經通知縮減 | 不用 | ? | OpenAI 相容 | gpt-oss-20b 等 | ? | 上游不透明；條款頁 404 | https://docs.llm7.io/limits |
| ModelScope | 不建議 | 每天約 250 魔粒（清單寫的 2000 RPD 已過時） | 中國實名 + 阿里雲 | 實際上不行 | OpenAI 相容 | Qwen3.x、DeepSeek V4 | ? | 非商用 | https://modelscope.cn/docs/model-service/API-Inference/limits |
| SiliconFlow | 不建議 | 中國站少數免費模型；國際站只有 $1 credit | 大陸證件實名 | 實際上不行 | OpenAI 相容 | Hunyuan-MT-7B、bge-m3、reranker | ? | PR #1 裡的國際站項目應改標付費 | https://siliconflow.cn/pricing |
| Cerebras | 已失效 | 官方 FAQ：沒有永久免費層；$5 trial credit 30 天到期，且要驗證付款方式（2026-08 cheahjs 還列 5 RPM / 1M TPD 免費） | 要付款方式 | — | `cerebras/` | gpt-oss-120b、zai-glm-4.7、gemma-4-31b（付費） | — | — | https://www.cerebras.ai/pricing |
| Mistral La Plateforme | 已失效 | 官方：Free 模式不含 API；建 key、用 API 都要開 billing 走 pay-as-you-go（2026-08 cheahjs 還列 Experiment 免費層，要同意拿資料訓練） | 要 billing | — | `mistral/` | — | — | 舊 Experiment 免費層要同意訓練 | https://docs.mistral.ai/getting-started/quickstart/ |
| Hugging Face Inference | 已失效 | 免費用戶要先買 credits | — | — | — | — | — | free-for.dev 寫的「每月 30k 字元」已過時 | https://huggingface.co/docs/inference-providers/pricing |

