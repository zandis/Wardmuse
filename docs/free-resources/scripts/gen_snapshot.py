import json,collections,os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
from data import *
# JSON snapshot
snap={"generated_at":CHECKED,"timezone":"Asia/Taipei","rules":"read-only audit; official pages only; no sign-ups","sources":{"primary":"https://github.com/ripienaar/free-for-dev/blob/master/README.md","secondary":["https://github.com/mnfst/awesome-free-llm-apis","https://web.archive.org/web/20260806034947/https://github.com/cheahjs/free-llm-api-resources"]},"providers":[]}
for x in LLM:
    snap["providers"].append({"provider":x["n"],"category":"LLM 推理","status":x["st"],"key_limits":x["lim"],"card_required":x["card"],"taiwan_usable":x["tw"],"api":x["api"],"notable_models":x["models"],"trains_on_input":x["trains"],"tos_notes":x["tos"],"listed_in":x["src"],"source_url":x["url"],"pricing_url":x["pricing"],"changelog_url":x["changelog"] or None,"checked_at":CHECKED})
for x in INFRA:
    snap["providers"].append({"provider":x["n"],"category":x["cat"],"status":x["st"],"key_limits":x["lim"],"card_required":x["card"],"taiwan_usable":x["tw"],"data_phi":x["data"],"commercial_use":x["com"],"reclaim_sleep_expiry":x["recl"],"muse_fit":x["fit"],"trains_on_input":x["trains"],"source_url":x["url"],"pricing_url":x["pricing"],"changelog_url":x["changelog"] or None,"checked_at":CHECKED})
json.dump(snap,open(os.path.join(OUT,"free-tier-snapshot.json"),"w"),ensure_ascii=False,indent=1)
cl=collections.Counter(x["st"] for x in LLM); ci=collections.Counter(x["st"] for x in INFRA)
print("LLM",len(LLM),dict(cl)); print("INFRA",len(INFRA),dict(ci)); print(sorted(set(x["cat"] for x in INFRA)))