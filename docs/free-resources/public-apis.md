# 免費公開 API 與服務盤點（Wardmuse / TrialBox）

查核時間：2026-11-16 23:55（台北時間 Asia/Taipei）。只列免帳號、只要 email、免費 key 或免費授權即可用的公眾來源，以及可自架／免費網域與學術額度。**本回合沒有註冊或申請任何帳號。**

適用專案：Wardmuse（原 Muse stack；Oracle VM 上的 LiteLLM、Health bot、Gate-1 中文醫學事實評估、Ceresus）與 TrialBox（REDCap／FHIR、臨床試驗工具）。

## 結論

這類「不必付費的公眾伺服器」確實很多，尤其是文獻、試驗登記、美國與台灣政府開放資料。它們和免費 LLM 額度不同：多數是資料或學術 API，適合做**引用與接地**，不適合放病人資料。

建議第一步：做一個引用／接地工具，串 **PubMed E-utilities**（可先免 key，3 rps）+ **Europe PMC**（免帳號，OA 全文）+ **食藥署／健保用藥開放資料**（台灣商品名與許可證）。這三個都不必先註冊。UMLS、OMIM、ICD-11 等要授權或 key 的，等本人決定再申請。

## 建議優先接入的十項

1. PubMed E-utilities（可選免費 key）— Gate-1／Health bot 文獻檢索
2. Europe PMC — OA 全文與引用
3. Crossref（加 mailto）+ Unpaywall（email 參數）— DOI、撤稿、OA PDF
4. ClinicalTrials.gov API v2 — TrialBox 主登記庫（本回合活體 2.0.5）
5. 台灣：data.gov.tw 目錄 + 食藥署許可證／仿單 + 健保用藥與特約院所
6. RxNorm + openFDA（可選免費 key）— 藥名與美國安全資訊，須標管轄區
7. MeSH — 查詢擴展
8. Synthea + 自架 HAPI（rootless Podman）— TrialBox 合成 FHIR；公開 hapi.fhir.org 只做連通測試
9. 疾管署開放資料（CKAN）— 台灣疫情背景
10. Cloudflare Pages（文件站）+ 本機 Meilisearch／Qdrant 索引上述公開語料；可選 OpenTimestamps 為公開評測快照做雜湊存證

## 條款與風險（必讀）

- **禁止 PHI**：所有公眾 API 與免費層都沒有 BAA，也不可把真實病人資料送到公開 FHIR 測試伺服器、Colab、IPFS 或任何鏈上。
- **UMLS**：個人免費授權，約 5 個工作天；部分詞表（尤其 SNOMED）有額外限制，再散布前要讀附錄。台灣 SNOMED 會員與機構授權須另行確認。
- **OMIM**：條款偏嚴，官方頁本回合被擋，先不要接入產品。
- **MedlinePlus Connect**：不可把 ASHP 藥品衛教正文攝入系統，只能連回。
- **arXiv／期刊全文**：中繼資料常可自由用，PDF 多半不可自架。
- **台灣臨床試驗舊 CDE 網已關閉**，改食藥署新站；本回合未核到公開 API。
- **加密貨幣／去中心化**：台灣已有《虛擬資產服務法》，VASP 許可制。不要代管或兌換他人資產。OpenTimestamps 只送檔案雜湊、不必持幣，適合公開產物存證；其他錢包、水龍頭、公共 RPC、Arweave 不建議納入產品。
- **Freenom 免費網域已於 2026-07-31 結束**，不要用。
- **muse-a1 資源**：4 核／24 GB 還夠，但不要再裝 Discourse、Synapse、Nextcloud 這類重服務與 LiteLLM、夜間 HAPI 搶資源。輕量的 Uptime Kuma、Meilisearch 較合適。

本表共 94 筆。擬合：高 22、中 40、低 23、不建議 8、已失效 1。

## 文獻

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| NCBI E-utilities / PubMed | PubMed 等 Entrez 庫的搜尋、摘要、PMID 中繼資料 | 免費 key（可選） | 是 | 免 key：每 IP 3 rps；免費 NCBI key：10 rps。大量工作建議週末或美東 21:00–05:00。建議帶 tool 與 email。 | 美國政府資料，一般可自由使用；期刊全文另受版權約束。建議註冊 tool/email。 | 本環境偶爾遇到 recaptcha；台灣一般可連。 | 高：Gate-1 與 Health bot 引用／接地的第一來源。 | https://www.ncbi.nlm.nih.gov/books/NBK25497/ |
| PMC OA / BioC / OAI-PMH | PMC 開放近用全文（BioC XML/JSON、OAI-PMH、雲端／FTP 資料集） | 免帳號 | 是 | 走 E-utilities 時同上；官方規定僅能用 Cloud、OAI-PMH、E-utilities、BioC 做自動化擷取，禁止用其他方式大批抓文章。 | 授權依每篇文章授權條款；非 OA 不可批量下載。使用者自行遵守版權。 | 同 NCBI。 | 高：Health bot／Gate-1 需要 OA 全文時用。 | https://www.ncbi.nlm.nih.gov/pmc/tools/developers/ |
| Europe PMC REST | 3,300 萬篇以上文獻、OA 全文連結、引用網路、註解 API、補助資料 | 免帳號 | 是 | 官方 REST 頁未寫死數字；維運信件稱每 IP 約 10 rps。大批請用 cursorMark、OAI-PMH 或 FTP，不要深分頁。 | API 本身免費，商用呼叫可以；文獻內容仍受各出版者／作者版權保護。不可自動化批量下載非 OA 全文。 | EBI 主機，台灣可連。 | 高：與 PubMed 互補，OA 全文與引用特別適合接地。 | https://europepmc.org/developers |
| Semantic Scholar Graph API | 論文、作者、引用、SPECTER2 embedding、推薦、批量資料集 | 免費 key（可選，建議） | 是 | 未認證：所有匿名用戶共用約 1,000 rps，高峰可能再被限。申請 key 後入門額度為各端點 1 rps（保留容量，學術／非營利優先審）。 | 免費開放語料；key 勿分享。商用個案審查。 | 未見封鎖。 | 中：補引用圖與推薦；不要當唯一醫學來源。 | https://www.semanticscholar.org/product/api |
| OpenAlex | 全球學術圖譜（works／authors／sources），資料 CC0 | 免費 key（可選） | 是 | 2026-02 起廢止 polite pool／mailto。免 key：10 rps、每日預算約 $0.10，游標翻頁不可用。免費 key：30 rps、每日 $1；超過 5 個布林運算或語意搜尋更嚴。 | 資料 CC0；API 有用量預算，可加值付費。 | 未見封鎖。 | 中：文獻計量、機構／作者消歧；Gate-1 可用但不取代 PubMed。 | https://help.openalex.org/api/authentication/ |
| Crossref REST API | DOI 中繼資料、基金、授權、撤稿（含 Retraction Watch）、摘要（部分有版權） | 只要 email（mailto，可選但強烈建議） | 是 | 2025-12-01 起：公開池單筆 5 rps／併發 1，列表 1 rps／併發 1；禮貌池（mailto）單筆 10 rps／併發 3，列表 3 rps／併發 3。Metadata Plus 付費更高。超限 429。 | 免註冊。幾乎所有中繼資料無版權、可任意使用；部分摘要可能有出版者／作者版權。 | 未見封鎖。 | 高：DOI 解析、撤稿檢查，接地必備。 | https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/ |
| Unpaywall | 依 DOI 查最佳 OA 全文／PDF 連結 | 只要 email（必填參數，不必註冊） | 否 | 官方產品頁寫每天 10 萬次；未公布每秒上限。無 email 會 422。標題搜尋據傳已於 2026-09-18 停用（本回合官方頁為 JS，未能直接核到停用公告）。大批請改 OpenAlex 快照。 | 免費 REST；資料現與 OpenAlex 對齊。 | 未見封鎖。 | 高：把 DOI 轉成可引用的 OA PDF。 | https://unpaywall.org/products/api |
| CORE API | 全球 OA 論文中繼資料與全文機器介接 | 免帳號（註冊可加快） | 是 | 未註冊：10 秒內 1 次批次或 5 次單筆。註冊／會員較快，機構／企業可能不再免費。 | 可用於商用，但受 T&Cs；註冊時須說明用途。使用請引用 CORE 論文。 | 未見封鎖。 | 中：OA 全文備援；優先用 Europe PMC。 | https://core.ac.uk/services/api |
| arXiv API | 預印本中繼資料（題名、摘要、分類）；鼓勵連回摘要頁 | 免帳號 | 是 | 舊版 API／OAI-PMH／RSS：每 3 秒最多 1 次，單一連線。不可靠多機繞限。 | 中繼資料 CC0。全文多為非專屬散布權，除非 CC 授權，否則不可自架 PDF。個人或研究可取用全文。 | 未見封鎖。 | 中：方法學／計算預印本；醫學預印本優先 medRxiv。 | https://info.arxiv.org/help/api/tou.html |
| bioRxiv / medRxiv API | 預印本中繼資料、摘要、授權、後來正式出版 DOI；支援 medRxiv 與 bioRxiv | 免帳號 | 是 | 官方頁未寫速率；結果分頁（細節 30 筆、出版 100 筆）。請節流。 | 各篇授權欄不同（常為 CC）；保留預印本質疑、不可當正式證據。 | 未見封鎖。 | 中：Gate-1 可作「尚未同儕審查」對照，須標示預印本。 | https://api.biorxiv.org/ |

## 臨床與藥品

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| ClinicalTrials.gov API v2 | 美國登記的臨床試驗與結果，JSON／CSV；本回合活體版本 2.0.5，資料時間 2026-11-16T10:00:05Z | 免帳號 | 是 | 官方未公布速率；請帶識別用 User-Agent、分頁間暫停。舊 /api/query/ 已於 2024-06-25 退役。 | 美國政府作品，對境內外免費提供；請歸功 NLM／ClinicalTrials.gov。少數紀錄可能有第三方版權。 | 可連。台灣試驗若有在此登記也可查。 | 高：TrialBox 的第一試驗登記來源。 | https://clinicaltrials.gov/data-api/api |
| WHO ICTRP | 各國試驗登記彙整搜尋（trialsearch.who.int） | 免帳號（入口） | 是 | 未找到與 CT.gov v2 同級的公開 REST。以入口或匯出為主。 | WHO 資料使用條款適用；用於發現，細節仍回原登記庫核對。 | 可連。 | 中：補 CT.gov 沒有的非美登記；不建議當自動化主源。 | https://www.who.int/clinical-trials-registry-platform |
| openFDA | FDA 藥品不良事件、標示、召回、藥品與器材等 | 免費 key（可選） | 是 | 免 key：每 IP 每分鐘 240、每天 1,000。免費 key：每 key 每分鐘 240、每天 12 萬。 | 原則 CC0／公有領域，可商用；部分第三方著作會標示。建議歸功但非強制。不保證資料完整，不能當臨床決策唯一依據。 | 可連。美國資料，須與 TFDA 對照。 | 高：藥品安全與標示接地；Health bot 引用時要標管轄區。 | https://open.fda.gov/apis/authentication/ |
| DailyMed | 美國藥品仿單／SPL（本回合頁面顯示約 158,955 份標示）、Web Services 與整包下載 | 免帳號 | 是 | 說明頁未寫死速率；有 Web Services 與批次檔。請節流，大批用下載。 | NLM 服務；標示為公司提交給 FDA 的內容，使用時注意版權與「非完整清單」聲明。 | 可連。 | 中：英文仿單細節；台灣藥品以 TFDA 為準。 | https://dailymed.nlm.nih.gov/dailymed/webservices-help.cfm |
| RxNorm / RxNav | 美國藥物名稱標準化、RXCUI、RxClass、RxTerms、可處方子集 | 免帳號（進階可選 UMLS key） | 是 | 預設每 IP 20 rps；超過 429。選用 UMLS UTS key 可升到 100 rps。建議快取 12–24 小時。 | 多數端點不需授權。唯一例外：/rxcui/{id}/proprietary 需有效 UMLS 授權。RxClass 含 SNOMED，受 UMLS 附錄約束。NLM 不提供個別醫療建議。2027-02 將更名 RxNorm Tools。 | 可連。 | 高：藥名對照很有用；台灣商品名還要接健保／TFDA。 | https://lhncbc.nlm.nih.gov/RxNav/TermsofService.html |
| MedlinePlus Connect | 以 ICD／SNOMED／RxCUI／LOINC／CPT 等代碼回傳病人衛教連結 | 免帳號 | 是 | 免註冊。官方未寫速率。 | 服務免費。藥品衛教是 ASHP 授權內容，禁止把該版權內容攝入或掛品牌到 EHR；只能連回去。若要嵌入須向 ASHP 另行授權。 | 可連；內容以英文／西語為主，中文有限。 | 中：Health bot 可當「衛教連結」層，不要抓正文。 | https://medlineplus.gov/connect/overview.html |
| UMLS（含 API） | 統一醫學語言系統、概念對照、部分詞表瀏覽與 REST API | 免費授權（個人） | 否 | 個人授權、約 5 個工作天審核。API：每 IP 20 rps，建議快取 12–24 小時。 | NLM 不收費。授權只發給個人。部分來源（尤其 SNOMED）有額外限制或在非會員國可能收費。再散布前必須讀附錄，未涵蓋的用途要問來源單位。每年有使用報告義務。 | 可申請。台灣是否為 SNOMED 會員國、能否免額外費，須向衛福部／SNOMED International 確認，不可假設可自由再散布。 | 中：術語對照很強，但授權重，不要當第一個接入項目。 | https://www.nlm.nih.gov/databases/umls.html |
| SNOMED CT | 臨床術語（問題清單、程序等） | 免費授權（視會員國） | 否 | 完整表需會員或 UMLS 途徑。瀏覽器可預覽。 | 受 SNOMED Affiliate 授權。會員國（含經 UMLS 附錄在美國等）通常免授權費；非會員國可能收費。禁止未授權再散布。 | 須確認台灣會員資格與機構授權，再決定能否用在產品。 | 中：EHR／TrialBox 編碼需要時再走正式授權。 | https://www.snomed.org/get-snomed |
| LOINC | 檢驗與臨床觀察通用代碼 | 免費授權（要註冊下載） | 否 | 下載需帳號；另有 FHIR 術語服務。 | 開放授權，商用與非商用都可（官方授權頁 2026-08-06 更新）。通常須標示 LOINC、不可改變代碼意義。細節以 loinc.org/license 為準。 | 可連。 | 中：TrialBox／檢驗對照；與健保碼對映要另做。 | https://loinc.org/license/ |
| ICD-11 WHO API | ICD-11 瀏覽、搜尋、線性化、（預覽）FHIR | 免費 key（OAuth2 client credentials） | 否 | 到 icd.who.int/icdapi 免費註冊，取得 client id/secret；token 約 1 小時。官方未寫速率。 | WHO 分類授權條款適用；用於編碼與瀏覽。不可把 API 憑證寫進公開程式庫。 | 可連。台灣臨床仍多用 ICD-10-CM／健保碼，ICD-11 可作對照。 | 中：國際分類對照；不是台灣申報碼。 | https://icd.who.int/docs/icd-api/API-Authentication/ |
| MeSH | NLM 醫學主題詞，PubMed 索引與層級 | 免帳號（下載／RDF） | 是 | 有 MeSH Browser、年度檔、MeSH RDF（id.nlm.nih.gov/mesh）。本回合未讀到獨立速率。 | 美國政府詞表，一般可自由使用，建議標示 MeSH／NLM。2026 年版已上線，Browser 可看 2026／2027。 | 可連。 | 高：Gate-1 查詢擴展與主題標註。 | https://www.nlm.nih.gov/mesh/meshhome.html |
| NLM Clinical Tables | 藥品、ICD、HCPCS 等自動完成 API，方便表單輸入 | 免帳號（典型） | 是 | 本回合未完整打開 apidoc；已知為公開自動完成服務，請節流。 | NLM 服務；勿當完整術語庫。 | 可連。 | 低：表單輔助，非主要知識源。 | https://clinicaltables.nlm.nih.gov/ |
| PubChem PUG REST | 化合物、生物活性、結構搜尋 | 免帳號 | 是 | 官方程式介接頁本回合被 recaptcha 擋。社群與舊官方慣例約 5 rps；大批用 FTP／下載。核到後再改數字。 | 美國政府資料，一般可自由使用。 | 本環境會碰到 recaptcha。 | 中：化學／藥理補充；Health bot 非第一優先。 | https://pubchem.ncbi.nlm.nih.gov/docs/programmatic-access |
| ChEMBL | 藥物與生物活性資料 REST、Beaker 化學工具 | 免帳號 | 是 | 官方 Web Services 文件未在首頁寫死速率；EBI 共用公平使用。請節流。 | 典型為 CC 類開放資料（以當前 ChEMBL 授權聲明為準），須署名。 | 可連。 | 中：藥理資料補充。 | https://chembl.gitbook.io/chembl-interface-documentation/web-services |
| DrugBank 開放部分 | 有限的開放詞彙／外部識別；完整庫為授權產品 | 要帳號／授權（完整庫） | 否 | Open Data 子集有限；完整學術或商用庫需申請，商用收費。 | 不可把付費庫當免費 API 用。只使用官方標為開放的部分。 | 可連。 | 低：不要當成免費主庫；優先 RxNorm、openFDA、TFDA。 | https://go.drugbank.com/releases/latest |

## 基因與表型

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| HPO（人類表型本體） | 罕見病／表型詞彙與註解 | 免帳號（下載） | 是 | 以 GitHub／OBO 下載為主。原 hpo.jax.org/data/ontology 本回合 404，改走 OBO／GitHub。 | 開放本體，通常須署名；以官方授權檔為準。 | 可連。 | 中：罕見病 Gate-1 有用。 | https://obofoundry.org/ontology/hp.html |
| OMIM API | 孟德爾遺傳疾病條目（需 key） | 免費 key | 否 | 須申請。官方說明頁本回合 403／挑戰頁。 | 歷來偏學術、限制再散布與商用；使用前務必讀官方 API 條款。不可把全文當開放資料。 | 本環境被擋。 | 低：遺傳疾病對照有價值，但條款嚴，先不要接進產品。 | https://www.omim.org/help/api |
| ClinVar | 變異與臨床意義彙整，FTP／每月更新 | 免帳號（下載） | 是 | 以 FTP／資料集為主；E-utilities 也可。官方文件頁本回合 recaptcha。 | 美國政府資料，一般可自由使用；解讀須保留不確定性。 | 可連。 | 中：遺傳變異補充，非第一優先。 | https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/ |
| gnomAD | 族群等位基因頻率、瀏覽器與資料下載；另有 GraphQL | 免帳號（下載／瀏覽） | 是 | API／條款頁本回合幾乎是前端殼。大批用官方下載，不要爬瀏覽器。 | Broad 條款通常允許學術與商用並要求署名；以 gnomad.broadinstitute.org/terms 為準（本回合未擷到正文）。不可把可識別基因組資料或 PHI 上傳。 | 可連。 | 中：變異頻率背景；非臨床報告依據。 | https://gnomad.broadinstitute.org/terms |

## FHIR與合成資料

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| HAPI 公開測試 FHIR 伺服器 | 公開 FHIR R4 測試端點，可讀寫範例資源 | 免帳號 | 是 | 資料可能被任何人改或清空；不穩、不保證。官方文件指向 Public Test Server。 | 禁止放真實病人資料或 PHI。僅供互通測試。 | 可連。 | 中：TrialBox 連線測試可以；正式測試請用 muse-a1 上 rootless 的自架 HAPI。 | https://hapi.fhir.org/ |
| SMART Health IT Sandbox | SMART-on-FHIR 啟動與合成病人，供 App 授權流程測試 | 免帳號（典型） | 是 | 公開沙盒，資料為合成。 | 禁止 PHI。僅開發測試。 | 可連。 | 中：若 TrialBox 要做 SMART 登入流程可用。 | https://launch.smarthealthit.org/ |
| Synthea | 開源合成病人產生器，輸出 FHIR／C-CDA 等；免費、無個資限制 | 免帳號（本機跑） | 是 | 在自己機器跑。公開模組偏美國保險與人口，要台灣情境須改模組。 | 官方：免費、無隱私／資安限制（合成、非真人）。MITRE 開源。 | 可在 muse-a1 用 rootless Podman 跑。 | 高：TrialBox 夜間測試的首選合成資料，不要用公開 FHIR 伺服器裝真資料。 | https://synthetichealth.github.io/synthea/ |

## 台灣政府

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| 政府資料開放平臺 data.gov.tw | 全國開放資料目錄、資料集清單 CSV、部分統計 API、各機關資料連結 | 免帳號（讀取） | 是 | 讀取開放資料一般不需 key。寫入／跨平臺發布才要機關 API Key。未在 M2M 頁看到全站統一 rps。各資料集授權與更新頻率不同。 | 多採「政府資料開放授權條款」，接近 CC，可商用，須標示來源。個別資料集可能另有條款。不可把未開放的公務資料當開放資料。 | 本機可連。這是台灣資料的總入口。 | 高：找衛福部、健保、TFDA、疾管署資料集的目錄。 | https://data.gov.tw/m2m |
| 健保署開放資料（用藥、特約院所） | 健保用藥品項、特約醫事機構等 | 免帳號（開放資料） | 是 | 資料多在 data.nhi.gov.tw 與 data.gov.tw。本回合 data.nhi.gov.tw TLS 握手失敗，改建議走 data.gov.tw 鏡像或稍後重試。 | 政府開放資料授權；屬給付與特約資料，不是仿單，也不是臨床指引。 | 從台灣應可連；本環境 TLS 失敗，列為需再確認直連。 | 高：Health bot 台灣商品名、院所名稱對照，價值很高。 | https://data.nhi.gov.tw/ |
| 食藥署 TFDA 開放資料（許可證／仿單） | 西藥／醫療器材許可證、仿單等開放資料 | 免帳號（開放資料） | 是 | data.fda.gov.tw 本回合只回 Swagger 殼（734 bytes），實際資料集請由 data.gov.tw 搜「藥品許可證」「仿單」或稍後重試食藥署平臺。 | 政府開放資料授權。仿單為核准標示，引用時保留原文、注意更新日。不可當即時處方審查。 | 應可連；本環境平臺殼不完整。 | 高：Health bot／Gate-1 台灣藥品接地的第一本地來源。 | https://data.fda.gov.tw/ |
| 疾管署開放資料（CKAN） | 傳染病統計、疫苗、旅遊疫情等；CKAN Action API（datastore_search） | 免帳號（讀取） | 是 | 典型 CKAN 讀取不需 key。本回合直連 data.cdc.gov.tw 失敗；次級來源與目錄仍顯示平台活著。另有 www.cdc.gov.tw RSS。 | 政府開放資料；統計已彙總，不是個案 PHI。 | 台灣應可連；本環境失敗。 | 高：疫情與衛教背景，Health bot 可引用官方統計。 | https://data.cdc.gov.tw/ |
| 衛福部統計處 | 衛生福利統計、生命統計、醫療資源等報表／開放資料 | 免帳號 | 是 | 多為定期表與檔案，不一定有細 API。 | 政府統計，引用請標年度與來源。 | 可連。 | 中：背景統計，不是即時診療依據。 | https://dep.mohw.gov.tw/DOS/ |
| 國家衛生研究院（國衛院） | 研究機構網站、部分研究報告與資料計畫，不是統一 Open API | 視資料集 | 否 | 無單一公眾 REST 總入口。 | 各計畫授權不同。 | 可連。 | 低：研究合作則有價值，不適合作為通用 API 層。 | https://www.nhri.edu.tw/ |
| 台灣藥品臨床試驗資訊網 | 衛福部食藥署管轄的台灣藥品臨床試驗案件資訊；舊 CDE 入口已關閉 | 未核到公開 API（網站可開） | 否 | www1.cde.org.tw/ct_taiwan/ 已公告關閉，改至 https://e-sub.fda.gov.tw/ClinicalTrialInfo/home。新站本回合為前端應用，未能核對免登入公開 API。 | 以食藥署網站條款為準。提交案件需要正式帳號；公開查詢範圍未在本回合核完。 | 可開網頁。 | 中：台灣試驗對照很重要，但自動化先走 CT.gov；此站先當人工查詢。 | https://e-sub.fda.gov.tw/ClinicalTrialInfo/home |

## 國際組織

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| WHO GHO OData API | 全球健康觀察站指標（死亡率、UHC、風險因子等） | 免帳號（典型） | 是 | 官方有 GHO OData 說明頁。本回合頁面正文擷取不完整，未讀到速率數字。 | WHO 資料使用／授權條款；引用請標 WHO。 | 可連。 | 中：國際比較背景，非台灣臨床指引。 | https://www.who.int/data/gho/info/gho-odata-api |
| 美國 CDC 開放資料 | data.cdc.gov 等 Socrata／資料集 API（監測、調查） | 免帳號或可選 app token | 是 | Socrata 常見有未認證節流；token 可提高。本回合未深核各資料集。 | 美國政府資料為主；不是台灣疫情官方來源。 | 可連。 | 低：方法學對照，Health bot 講台灣疫情應以疾管署為準。 | https://data.cdc.gov/ |
| World Bank Indicators API | 國家發展與部分衛生指標 | 免帳號 | 是 | 官方：已不再需要 API key 或其他認證。速率未在本回合讀到。 | 世銀資料使用條款；須標示來源。 | 可連。 | 低：宏觀衛生指標，Ceresus／研究背景。 | https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-api-documentation |
| OECD 衛生統計 | OECD 國家衛生支出、人力等；SDMX／資料 API | 免帳號（多數） | 是 | 本回合未深核最新 SDMX 端點與速率。 | OECD 資料條款，須署名。台灣非 OECD 會員，資料覆蓋有限。 | 可連。 | 低：國際比較有限。 | https://data.oecd.org/ |

## 學術運算

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| NCBI BLAST REST | 序列比對（公開 NCBI 伺服器或自架） | 免帳號 | 是 | 共用資源，優先互動使用者。24 小時內超過 100 次可能被改慢速佇列或封鎖。指南：至少每 10 秒一次；同一 RID 一分鐘最多輪詢一次；帶 email 與 tool；超過 50 次應在週末或美東夜間。大批請自架 BLAST+／雲端。 | BLAST 軟體為公有領域。公開伺服器不是給超大專案用的。 | 可連，但勿打爆公用伺服器。 | 低：偶發序列問題可以；不要做 Health bot 線上路徑。 | https://blast.ncbi.nlm.nih.gov/doc/blast-help/developerinfo.html |
| EBI Job Dispatcher / Dbfetch | BLAST、Clustal、InterProScan 等工具與資料庫抓取，有程式介面 | 免帳號（建議識別） | 是 | 有公平使用政策；大量作業應節流並自架或改用本地工具。 | EBI 服務條款；引用相應工具論文。不可送可識別人體序列當公開作業（當 PHI／人類基因資料處理）。 | 可連。 | 低：研究批次用，非產品熱路徑。 | https://www.ebi.ac.uk/jdispatcher/docs/ |
| Hugging Face Datasets（公開讀取） | 公開資料集下載與串流；部分需同意條款 | 免帳號可讀許多公開集；門控集要帳號 | 是 | 匿名下載有流量限制。推論 API 免費用戶已改為要買 credits（前次盤點已列失效）。Spaces 見後文。 | 各資料集授權不同；醫療集可能禁止臨床使用。不要上傳 PHI。 | 可連。 | 中：公開評測集、嵌入語料；Gate-1 可用公開醫學 QA，不可放病人資料。 | https://huggingface.co/docs/hub/en/datasets |

## 論壇

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| PTT（批踢踢） | 台灣 BBS，網頁或 telnet 可讀公開板 | 讀公開板免帳號；發文要帳號 | 是 | 無官方公共 API。大量爬文常被擋或違反站規。 | 站規與板規嚴格；過18板、個資、醫療板內容不可當臨床依據，也不可蒐集 PHI。 | 台灣可連；部分網路環境需過驗證。 | 不建議：最多做公眾情緒或謠言監測研究，不進 Health bot 知識庫。 | https://www.ptt.cc/bbs/index.html |
| Discourse / Flarum（自架） | 開源論壇，可架在自己的 VM | 軟體免費；要自己的主機 | 是 | Discourse 偏重（Postgres、Redis、Sidekiq，常要 2–4 GB）。Flarum 較輕。與 LiteLLM、TrialBox 搶資源。 | 開源授權。不要在公開論壇放 PHI。 | 可自架於 muse-a1，但不建議與現有服務共機。 | 低：社群文件可考慮；現階段不建議裝在 muse-a1。 | https://github.com/discourse/discourse |

## 電子郵件

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| Cloudflare Email Routing | 自有網域免費轉寄收信 | 要 Cloudflare 帳號 | 否 | 轉寄免費；任意對外寄信需 Workers Paid。 | CF 條款。信件經第三方，不寄 PHI。 | 可。 | 中：已在前次 infra 盤點列為可用；適合專案信箱轉到本人。 | https://developers.cloudflare.com/email-routing/ |
| Resend / Brevo / Mailjet 免費層 | 交易信／告警 SMTP 或 API | 要帳號 | 否 | Resend 約每月 3,000、每天 100；Brevo 每天 300（須審核）；Mailjet 每月 6,000、每天 200。 | 可商用（各家條款）；不寄 PHI。AgentMail 僅草稿。 | 可。 | 高：告警首選 Resend（前次已建議，尚未開）。 | https://resend.com/pricing |
| 臨時信箱（temp-mail 類） | 拋棄式收件地址 | 通常免帳號 | 是 | 不可靠、公開、常被註冊表單擋。 | 不應用於學術註冊、官方 key、或任何醫療相關帳號。有濫用與資料外洩風險。 | — | 不建議：不要用於 Wardmuse。 | — |

## 靜態網站

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| GitHub Pages | 從公開或私有 repo 發布靜態站 | 要 GitHub 帳號 | 否 | 免費層有流量與大小限制；公開 repo 免費。 | 不可放機密或 PHI。適合文件、狀態頁。 | 可。 | 中：專案文件備援。 | https://docs.github.com/pages |
| Cloudflare Pages | 靜態站與預覽部署 | 要 CF 帳號 | 否 | 免費；每月 build 次數有上限（前次盤點約 500）。 | 可商用。不放 PHI。 | 可。 | 高：Wardmuse 文件／狀態頁首選（前次已建議）。 | https://developers.cloudflare.com/pages/platform/limits/ |
| Codeberg Pages | Forgejo 託管的靜態頁，非營利 | 要 Codeberg 帳號 | 否 | 公平使用；容量小於商業平台。 | 開源／公益導向。適合公開文件備份。 | 可。 | 中：GitHub 的非營利備援。 | https://docs.codeberg.org/codeberg-pages/ |
| Neocities / Netlify Drop / surge.sh | 免或低門檻靜態上傳（Drop 甚至可拖放、不必完整帳號流程） | 視服務；Drop／surge 可很輕 | 否 | 免費額度小、品牌子網域。Netlify 免費層有 credits。 | 各家不同；Hobby 條款可能限非商用（Vercel 更明顯）。不放 PHI。 | 可。 | 低：示範頁可以；正式文件用 CF Pages 即可。 | https://www.netlify.com/drop/ |

## 路由隧道DNS

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| Cloudflare Tunnel | 不必開入站連接埠即可把本機服務曝光或接 Access | 要 CF 帳號 | 否 | 免費。管理頁建議加 Access。 | 開 proxy 時 CF 會終止 TLS。私流用 DNS-only 或 Tailscale。不曝 LiteLLM 到公網無防護。 | 可。 | 高：與現況吻合，優先於 ngrok。 | https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/ |
| Tailscale Funnel / Personal | Zero-config VPN；Funnel 可選把服務公開 | 要帳號 | 否 | Personal 永久免費、裝置不限、最多 6 人。Funnel 有流量與使用限制，不適合作為主要公網入口。 | 個人用條款。端到端加密。Funnel 會讓流量離開 tailnet，勿曝管理介面。 | 可。 | 高：SSH 與管理面走 tailnet，不要用 Funnel 曝 LiteLLM。 | https://tailscale.com/kb/1223/funnel |
| deSEC | 免費 DNS 託管，開源、強調安全，有 API | 要帳號 | 否 | 免費給所有人用。 | 非營利運作。Cloudflare 已涵蓋時非必需。 | 可。 | 低：CF 已夠用；可當 DNS 備援。 | https://desec.io/ |
| DuckDNS | 免費動態 DNS 子網域 | 要帳號 | 否 | 免費，託於 AWS。 | 適合家用動態 IP；muse-a1 已有穩定位址與 CF，不需要。 | 可。 | 低：用不到。 | https://www.duckdns.org/ |
| 公共 DNS／NTP（1.1.1.1、8.8.8.8、pool.ntp.org 等） | 解析與時間同步 | 免帳號 | 是 | 公平使用。VM 應使用可靠 NTP，避免憑證與簽名時間錯。 | 各解析器隱私政策不同（CF／Google）。不要把內部主機名稱洩漏到公共解析器日誌。 | 可。 | 中：基礎維運，不是產品功能。 | https://www.pool.ntp.org/zh/ |

## 雲端空間與筆記本

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| Hugging Face Spaces | 託管小 demo（Gradio／Streamlit 等） | 要帳號 | 否 | 免費 CPU 小額度；GPU 要付費或 credits。會休眠。 | 公開空間內容可視為公開。禁止 PHI。授權依空間與模型。 | 可。 | 中：公開 demo 可以；不要放 Health bot 正式後端。 | https://huggingface.co/docs/hub/en/spaces |
| Google Colab Free / Kaggle Notebooks | 免費或不保證的 GPU／TPU 時數，互動筆記本 | 要帳號（Kaggle 要手機驗證） | 否 | Colab 不保證、會回收；Kaggle 約每週數十小時 GPU（官方常要登入才顯示）。不可當線上 API。 | 資料會上雲。禁止 PHI。條款隨產品變。 | 可。 | 中：離線評估、embedding 批次（僅公開資料）。 | https://research.google.com/colaboratory/faq.html |
| Replit / StackBlitz / Gitpod / Codespaces 免費時數 | 雲端 IDE 與預覽 | 要帳號 | 否 | 免費時數有限，常休眠。GitHub Codespaces 對教育帳號較寬。 | 程式與環境在第三方。不要放 secrets／PHI。Gitpod 免費政策曾變動，用前再核。 | 可。 | 低：開發預覽可以；正式 CI 用 GitHub Actions + 自架 runner。 | https://github.com/features/codespaces |

## 檔案與學術倉儲

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| Zenodo | 研究產出存放、DOI、REST API | 讀公開紀錄通常可；上傳／管理要 token | 否 | 單檔與總量有上限（CERN 託管，學術向，額度比一般網盤寬）。API 要 User-Agent，有速率限制。Sandbox 發測試 DOI（10.5072）。 | 上傳者決定授權。適合公開報告、評測快照、軟體版本。禁止 PHI 與未授權臨床資料。 | 可。 | 高：Gate-1 公開評測與軟體發行的好去處。 | https://developers.zenodo.org/ |
| ORCID Public API | 讀取公開 ORCID 紀錄；Member API 才能寫入 | 免費 Public API 憑證（要註冊） | 否 | Public API 有自己的 ToS。Sandbox 免會員也可測。 | 讀公開資料可以；寫入需會員或經使用者 OAuth。遵守 Public APIs ToS。 | 可。 | 中：作者消歧、論文頁；非急件。 | https://info.orcid.org/documentation/api-tutorials/api-tutorial-read-data-on-a-record/ |
| OSF / figshare / archive.org | 學術專案、預印本、公開檔案與網頁典藏 | 讀公開多免帳號；上傳要帳號 | 是 | 各家免費層不同。Internet Archive 適合公開網頁快照。 | 上傳者授權。禁止 PHI。figshare／OSF 適合開放科學，不適合內部病歷。 | 可。 | 中：公開資料與網頁存證；內部備份仍用加密後的 R2。 | https://osf.io/ |
| Software Heritage | 開源軟體長期典藏與 API，可存 Git 歷史 | 讀取多公開；部分寫入要 token | 是 | 本回合舊文件 URL 404，根 API 有回應。請改用官方目前 docs。 | 適合把 Wardmuse 公開 repo 做長期存檔。 | 可。 | 低：開源保存，低優先。 | https://archive.softwareheritage.org/api/ |
| TWAREN／學術網路服務 | 臺灣學術網路、部分研究雲與授權資料庫走機構網 | 機構身分（長庚） | 否 | 不是公眾 API。校內授權資料庫、加速網段，通常需 VPN 或校園網。 | 機構授權，不得分享帳號或當公眾代理。仍不可把 PHI 放到未簽約環境。 | 長庚身分可用。這不是「免帳號公眾伺服器」。 | 中：本人用校園網取得全文或授權資料庫時有用，不要寫進對外 bot。 | https://www.twaren.net/ |

## 免費網域

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| Freenom（.tk / .cf / .gq 等） | 昔日免費國碼網域 | 已無免費層 | 否 | 免費層於 2026-07-31 結束；改為付費約每年 €9.95／USD 9.95。.ml／.ga 早已易手。註冊／續約流程不穩。 | 過去濫用與釣魚比例高，不適合作醫療品牌。 | 不要用。 | 已失效：已失效，不要申請。 | https://www.freenom.com/ |
| EU.org | 自 1996 年起提供免費三级域名（例 foo.eu.org），可自訂 NS | 要申請（人工審） | 否 | 審核可能慢、無客服保證。與歐盟無關。 | 目標是付不起 NIC 費用的個人或非營利。不適合作正式醫療產品主網域。 | 可申請。 | 低：實驗子域可以；對外品牌請用正式網域。 | https://nic.eu.org/ |
| is-a.dev | 經 GitHub 申請的免費 *.is-a.dev 子域（另有 is-a.bot） | 要 GitHub 帳號 | 否 | 開發者向、公開 PR 申請。可能有保留字。 | 有 ToS 與檢舉濫用。適合個人開發展示，不適合正式醫療站。 | 可。 | 低：個人 demo 可以。 | https://www.is-a.dev/ |
| js.org / pp.ua | js.org 僅限 JavaScript 專案子域；pp.ua 為烏克蘭免費域名之一 | 要申請 | 否 | js.org 有專案類型限制。pp.ua 有地緣與續存風險。 | 不要當醫療品牌網域。 | 可連。 | 不建議：不建議用於 Wardmuse 對外名稱。 | https://js.org/ |

## 免費IP

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| Hurricane Electric Tunnelbroker | 免費 IPv6 隧道，啟用後可申請 /48 | 要註冊 | 否 | 官方定位為開發／實驗。論壇稱不限流量，但「現況提供、無擔保」。東京／香港／新加坡有節點。 | 禁止垃圾信、DDoS、惡意程式、未授權入侵。須真實聯絡資料。位址僅能搭配此服務使用。 | 亞洲有節點。對 muse-a1 不是必需（已有公網）。 | 低：只有在需要原生 IPv6 實驗時才考慮；不要把管理面只綁在隧道上。 | https://www.tunnelbroker.net/ |
| Oracle / GCP 免費層公網 IP | 雲端 VM 附帶的公網 IPv4（OCI 已在用） | 雲帳號 | 否 | OCI Always Free 與 GCP e2-micro 各有額度與地區限制。多要一個公網 IP 可能耗額度或衍生費用。 | 雲條款。須設防火牆與 Access，不可把服務裸露在 0.0.0.0。 | OCI 無台灣區（用日本／美國等）。 | 中：muse-a1 已有公網 IP。不必另開。入口繼續用 Caddy + Tailscale / CF Access。 | https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm |
| Cloudflare / Tailscale 作為「不必有公網 IP」的替代 | 以隧道或 WireGuard 取代對公網 IP 的依賴 | 要帳號 | 否 | 見隧道各節。 | 同各服務。 | 可。 | 高：這才是正確方向，而不是找免費額外 IPv4。 | https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/ |

## 可自架

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| Gitea / Forgejo | 輕量 Git 伺服器，有 ARM64 映像 | 軟體免費 | 是 | 記憶體輕（數百 MB 級）。24 GB ARM 跑得動。 | 開源。私有 repo 仍不要放 PHI 或金鑰。公開程式繼續用 GitHub（zandis/Wardmuse）。 | 可在 muse-a1 用 rootless 跑。 | 中：最多當內部鏡像；不是現在的優先。 | https://forgejo.org/ |
| Uptime Kuma | 自架uptime 監控 | 軟體免費 | 是 | 非常輕。可與免費的 UptimeRobot 互補（外部視角仍建議留一家外部監控）。 | 開源。監控目標不要把密鑰寫進通知。 | 適配 muse-a1。 | 高：值得裝，負載極低。 | https://github.com/louislam/uptime-kuma |
| SearXNG | 自架綜合搜尋（可接學術來源） | 軟體免費 | 是 | 輕到中。注意不要把實例公開成開放代理而被濫用。 | 開源。若對公網開放，有濫用與法律風險。建議只在 tailnet。 | 可自架。 | 中：內部研究搜尋可以；不要公開。 | https://docs.searxng.org/ |
| Meilisearch | 輕量搜尋引擎，有 ARM64 | 軟體免費（自架） | 是 | 中等記憶體。適合索引 TFDA／PubMed 摘要等公開語料。 | 開源。只索引公開或已授權資料，不放 PHI。 | 可在 muse-a1 跑。 | 高：接地語料的本機搜尋，和 Qdrant 互補。 | https://www.meilisearch.com/ |
| n8n | 工作流自動化 | 軟體有免費自架版 | 是 | 中等資源。社群版與雲端條款不同。 | 不要在工作流裡傳 PHI 或金鑰到第三方。注意授權（Fair-code）對商業用途的限制。 | 可自架，但先不要與生產路由混用。 | 中：以後可做公開資料同步；現階段非必需。 | https://github.com/n8n-io/n8n |
| Nextcloud | 自架檔案同步／協作 | 軟體免費 | 是 | 中到重。與 LiteLLM 共機要限流量。 | 資料在自己機器仍須權限與備份。不是 HIPAA／個資法的自動合規。不要當病歷系統。 | 可裝，但優先級低（已有 Drive）。 | 低：暫時不建議裝在 muse-a1。 | https://nextcloud.com/ |
| Matrix（Synapse／較輕的 Conduit） | 去中心即時通訊 | 軟體免費 | 是 | Synapse 重；Conduit／Dendrite 較輕。公開聯邦有濫用與資安成本。 | 若聯邦公開，有內容與法律風險。禁止 PHI。 | 不建議與現有服務共機。 | 不建議：現階段不裝。 | https://matrix.org/ |
| Ollama 或 llama.cpp 小模型 | 在 24 GB ARM 上跑量化小模型（約 7B–13B 級） | 軟體免費，模型各有授權 | 是 | A1 無 GPU，CPU 推論慢。Ollama 對 aarch64 支援視版本。會明顯佔 CPU／記憶體，可能擠到 LiteLLM 與夜間 HAPI。 | 模型授權各異（有的禁醫療用途）。不可當臨床決策、不可送 PHI 到任何會外洩的紀錄。Oracle 閒置回收規則也要小心長期高負載與反向的「過閒」。 | 可實驗，應排在離峰並設 cgroup 上限。 | 中：離線實驗可以；不要當 Health bot 主模型。 | https://github.com/ollama/ollama |

## 去中心化

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| IPFS 免費 pinning（Pinata／Storacha／Filebase 等免費層） | 把公開內容釘在 IPFS | 要帳號 | 否 | 免費層容量小、可能變價或收斂。內容公開可被複製。 | 禁止違法內容。絕對不要釘 PHI 或未授權資料。台灣《虛擬資產服務法》管的是資產服務，單純用 pinning 存公開檔通常不是 VASP，但仍有個資與濫用風險。 | 可用於公開 OSS 產物，非必要。 | 低：公開靜態產物備援；正式備份仍用加密 R2。 | https://www.pinata.cloud/ |
| Arweave／Filecoin 小額上傳 | 永久或合約式儲存 | 要錢包或平台帳號 | 否 | 所謂「免費」通常極小或要代幣／第三方門檻。資料難以刪除。 | 不可上鏈 PHI（幾乎無法刪）。涉及代幣持有或代他人保管可能觸及台灣 VASP 規範。本專案不建議碰支付或代幣操作。 | 法規：金管會已有《虛擬資產服務法》及子法草案，VASP 採許可制。個人把雜湊存證 ≠ 經營交易所，但不要做代管、兌換、收受他人資產。 | 不建議：不建議。 | https://www.arweave.org/ |
| 公共 RPC／測試網／水龍頭 | 讀區塊鏈、領測試幣 | 常免帳號或要免費 key | 是 | 公共 RPC 不穩、有速率與濫用控管。測試幣無法律現金價值但仍有詐騙風險。 | 不要把生產密鑰、助記詞放在 VM 或聊天。不要對真實網路做自動交易。與 Wardmuse 主線無關。 | 同上，避免變成未經許可的資產服務。 | 不建議：不建議納入產品。 | — |
| Akash／Flux 等去中心化運算 | 用代幣租運算 | 要錢包 | 否 | 價格與可用性波動。節點信任模型與資料駐留不清楚。 | 不適合作為醫療或含個資工作負載。法遵與作業複雜度高。 | 涉及代幣支付，謹慎。 | 不建議：不建議。已有 OCI。 | https://akash.network/ |
| OpenTimestamps | 對檔案雜湊做比特幣時間戳存證；雜湊在瀏覽器或本機計算 | 免帳號 | 是 | 官方日曆伺服器免費、不必註冊或 API key，靠捐款營運。只把雜湊送出，不上傳原文。 | 證明的是「某雜湊在某時間前存在」，不是內容真實或醫療正確。不要把原文或 PHI 上傳到第三方。不需要持有或交易加密貨幣即可使用預設日曆。 | 只用雜湊存證，不經營資產服務，風險遠低於錢包／交易所。仍非正式公證。 | 中：適合為公開的 Gate-1 快照、簽署更新清單做稽核軌跡。 | https://opentimestamps.org/ |
| 可驗證憑證（W3C VC）／學術憑證基礎設施 | 標準化可驗證聲明，不一定要公鏈 | 視實作 | 否 | 要發行方、錢包與驗證流程，不是即插即用免費 API。 | 若用於醫療身分或授權，屬高度法遵議題，不可拿公開測試發行者當真。 | 醫療憑證須符合國內法規，不是 hobby 專案能上線的。 | 低：研究可以；產品先不做。 | https://www.w3.org/TR/vc-data-model-2.0/ |

## 學術額度

| 名稱 | 提供什麼 | 認證 | 免註冊即可用 | 速率／額度 | 授權／ToS | 台灣連線 | 擬合 | 來源 |
|---|---|---|---|---|---|---|---|---|
| GitHub Education／Student Pack | 教育身分可能取得 Codespaces、Copilot 等加碼 | 要教育驗證 | 否 | 教師／學生資格審核。內容與額度常變。 | 僅限符合資格的個人教育使用，不可分享帳號。 | 長庚教職或許可申請，須本人操作。 | 中：若符合，對開發有幫助。不要自動代申請。 | https://education.github.com/ |
| NVIDIA／Google／AWS 研究或教育 credits | 雲端或 GPU 點數，通常要提案 | 要申請與機構信箱 | 否 | 有期限、報告義務，核准不保證。 | 不得用於未核准的商業產品或 PHI。各計畫條款不同。 | 可以機構身分申請，須本人決定。 | 中：有明確 GPU 研究再申請；日常推理用現有免費 LLM 路由即可。 | https://www.nvidia.com/en-us/deep-learning-ai/education/ |
| Oracle for Research | 研究用 OCI 額度 | 要申請 | 否 | 與現有 tenancy／Always Free 關係要先問清楚，避免帳務混亂。 | 研究條款；他已有付費 tenancy（A1 免費額度已用滿）。動帳務須本人同意。 | 可詢問，但不要自動申請。 | 低：目前隔離用戶方案已夠，不必為 TrialBox 另開研究 VM。 | https://www.oracle.com/research/ |
| Cloudflare Project Galileo／新創方案 | 為受攻擊的公益或合格新創提供加強防護 | 要申請且資格嚴 | 否 | Galileo 針對受攻擊的弱勢或新聞／人權組織，不是一般專案福利。新創方案另有資格。 | 不要不符合資格還申請。 | Wardmuse 通常不符合 Galileo。 | 不建議：不建議申請 Galileo。一般免費 CF 已夠。 | https://www.cloudflare.com/galileo/ |
| 開源贊助／GitHub Sponsors 等 | 接受或申請開源資助 | 要公開專案與身份 | 否 | 不是「免費伺服器」。有稅務與揭露問題。 | 不要為了額度而把私有醫療專案硬公開。 | 若要公開募資須本人決定。 | 低：非現階段。 | https://github.com/sponsors |

## 方法與缺口

- 優先用官方文件頁（WebFetch 或 curl）。NCBI／PubChem／ClinVar 部分頁有 recaptcha；data.nhi.gov.tw 本環境 TLS 失敗；data.cdc.gov.tw、data.fda.gov.tw 內容不完整；OMIM、gnomAD 條款頁被擋或為前端殼。這些已在各列標明。
- 機器可讀列在 `public-apis.json`。
- 與 2026-11-15 的免費 LLM／infra 盤點互補：那份管推理額度與雲免費層，這份管公眾資料 API 與可自架服務。
