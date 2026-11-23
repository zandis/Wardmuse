from data import *
import collections,os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
c=lambda a,s:sum(1 for x in a if x["st"]==s)
o=["# free-for.dev 盤點（for Muse stack / routing）","","查核日期 2026-11-15（台北時間）。主清單 free-for.dev；mnfst/awesome-free-llm-apis 和 cheahjs/free-llm-api-resources（Wayback 2026-08-06）當 LLM 交叉比對。全部回到官方頁面查核；只讀，沒有註冊任何帳號。","",
"機器可讀快照：free-tier-snapshot.json","","## 統計","","| 狀態 | LLM | Infra |","|---|---|---|"]
for s in ["可用","可用但有限制","不建議","已失效"]: o.append(f"| {s} | {c(LLM,s)} | {c(INFRA,s)} |")
o.append(f"| 合計 | {len(LLM)} | {len(INFRA)} |")
o+=["","## 這次的變動（對比 cheahjs 2026-08 快照與 free-for.dev）","",
"- Cerebras → 已失效：官方 FAQ 說沒有永久免費層，只剩 30 天 $5 trial，要驗證付款方式（8 月還有 5 RPM / 1M TPD 免費）。",
"- Mistral La Plateforme → 已失效：Free 模式不含 API，要開 billing（8 月的 Experiment 免費層要同意訓練，已取消）。",
"- SambaNova → 可用但有限制：新的 Free Tier，不用綁付款，20 RPM / 20 RPD / 200K TPD（8 月只有 $5 trial）。",
"- Vercel AI Gateway → 可用但有限制：每月 $5 credit，只限 Free Tier 模型；Hobby 條款限個人非商業。",
"- Fly.io → 已失效：只剩 7 天 / $1 trial（free-for.dev 已過時）。",
"- AWS 改成 credits 制 Free plan（最多 $200、6 個月）。",
"- Cloudflare Queues 免費方案每天含 10,000 operations。","","## Muse 建議架構","","| 層 | 建議的免費選項 | 現況 / 待辦 |","|---|---|---|"]
for a,b,h in ARCH: o.append(f"| {a} | {b} | {h} |")
o+=["","## LLM routing 供應商","","| 供應商 | 狀態 | 免費額度 | 卡 / 電話 | 台灣 | API / LiteLLM | 重點模型 | 會拿輸入訓練 | 資料 / ToS | 來源 |","|---|---|---|---|---|---|---|---|---|---|"]
for x in LLM: o.append("| "+" | ".join([x["n"],x["st"],x["lim"],x["card"],x["tw"],x["api"],x["models"],x["trains"],x["tos"],x["url"]]).replace("\n"," ")+" |")
o+=["","## Infra 免費層"]
cats=[]
for x in INFRA:
    if x["cat"] not in cats: cats.append(x["cat"])
for k in cats:
    o+=["",f"### {k}","","| 服務 | 狀態 | 免費額度 | 卡 | 台灣 | 資料 / PHI | 商用 | 休眠 / 回收 / 到期 | 和 Muse 怎麼搭 | 來源 |","|---|---|---|---|---|---|---|---|---|---|"]
    for x in INFRA:
        if x["cat"]==k: o.append("| "+" | ".join([x["n"],x["st"],x["lim"],x["card"],x["tw"],x["data"],x["com"],x["recl"],x["fit"],x["url"]])+" |")
o+=["","## 建議的 routing 分層","",
"- fast：1 Groq gpt-oss-20b、Gemini 3.1 Flash-Lite → 2 CF glm-4.7-flash / gpt-oss-20b → 9 OpenRouter :free",
"- cheap：1 Gemini 3.5 Flash-Lite、Groq gpt-oss-20b → 2 CF granite-4.0-h-micro → 3 Z AI GLM-4.7-Flash（只放 public）→ 9 OpenRouter lfm",
"- smart：1 Gemini 4 Hydrogen、3.8 Flash、Groq gpt-oss-120b → 2 CF gpt-oss-120b → 3 SambaNova DeepSeek-V3.1 / gpt-oss-120b（每天 20 次）→ 4 Gonka DeepSeek-V4-Flash（只放 public）→ 8 Cohere（trial）→ 9 OpenRouter",
"- long-context：1 Gemini 3.8 Flash / 4 Hydrogen（1M）→ 3 Z AI GLM-4.7-Flash（200K）→ 9 OpenRouter nemotron-3.5-lightning",
"- vision（新 alias）：1 Groq qwen3.8-27b、Gemini → 2 CF llama-4-scout / gemma-4-26b",
"- embed / rerank：gemini-embedding-2 → CF bge-m3（維度不同，不能混用同一個 index）；rerank 用 Cohere trial",
"- 緊急備援：OVH 匿名端點（每模型 2 RPM）",
"- private 類：只能用 Groq（ZDR）、Cloudflare、OVH 匿名、本地模型；SambaNova 資料政策未明，先不放；PHI 只走本地","",
"## 和現有 gateway 比還缺什麼","",
"1. Cloudflare Workers AI token（要 Chang-Fu 本人建）","2. Gemini 4 Hydrogen、Gemma 4（現有 key，只要改設定）","3. Groq qwen/qwen3.8-27b + vision alias（qwen3.6 已在 2026-09-14 下線）","4. 移除 Gemini 2.5（PR #7）；2.5 會在 2026-12-01 自動轉到 3.8 Flash / 3.5 Flash-Lite","5. PR #1：SiliconFlow 國際站沒有免費模型，應改標付費；NIM 應標成免費、只限原型開發","6. OpenRouter 目前 50 RPD；一次買 10 credits 可升到 1000 RPD，要 Chang-Fu 決定","7. SambaNova、Z AI 還沒接（都要另外註冊帳號，由 Chang-Fu 決定）","8. Stack 其他層：R2 備份、UptimeRobot + healthchecks.io、Resend 告警、GHCR 映像，都要 Chang-Fu 自己開帳號","",
"## ToS 衝突","",
"- Gemini API：所有方案都禁止用在臨床實務或醫療建議；免費層不可送敏感或個人資料（Health bot 硬限制）",
"- Cohere trial：不得用於 production 或商用","- NVIDIA NIM：只限原型開發；不可送個人或機密資料","- Vercel Hobby / AI Gateway 免費層：只能個人或非商業使用","- Koyeb Free Instance：官方說不可用於 production","- ModelScope：非商用，還要中國實名","- OpenRouter / Gonka：禁止多帳號、禁止轉售；單人自用 gateway 沒問題","- onomeo / Kilo / LLM7：共用額度或免 key 通道，違反 ToS-clean 規則","",
"沒有任何一家明文禁止「單人經自己的 gateway 轉發」。會拿輸入訓練或記錄的（不能碰任何醫療資料）：Gemini 免費層、Kilo 免費模型、NVIDIA NIM、Cohere trial（可能）、OpenRouter 部分免費上游；SambaNova 未寫明。","",
"## 自動維護","","快照 free-tier-snapshot.json 每家都有 provider、category、status、key_limits、card_required、trains_on_input、commercial_use、reclaim_sleep_expiry、source_url、pricing_url、changelog_url、checked_at。每週抓 pricing_url / changelog_url 做 diff 即可。產生腳本：/workspace/reports/gen/（data.py 是唯一資料來源，gen.py 產生 JSON，md.py 產生本檔）。","",
"未能確認：Modal 是否要綁卡、Kaggle 官方 GPU 時數（要登入）、CockroachDB 免費額度、Qdrant / Pinecone / Zilliz 閒置政策、Better Stack 細節、Mistral Codestral 免費端點、OpenCode Zen。"]
open(os.path.join(OUT,"_full-audit.md"),"w").write("\n".join(o)+"\n")
