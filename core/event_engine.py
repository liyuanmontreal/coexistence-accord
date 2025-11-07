import pandas as pd
import random
import ast
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "events.csv"
df = pd.read_csv(DATA_PATH)

def safe_parse(s):
    # 安全解析事件效果列，自动补引号并补全字段
    if pd.isna(s):
        return {"biodiv":0,"economy":0,"society":0,"climate":0,"trust":0}
    s = str(s).strip()
    if not s.startswith("{"):
        s = "{" + s
    if not s.endswith("}"):
        s = s + "}"

    # 自动给未加引号的键添加引号
    s = re.sub(r'([{,]\s*)([a-zA-Z_]\w*)(\s*:)', r'\1"\2"\3', s)

    try:
        data = ast.literal_eval(s)
    except Exception as e:
        print("⚠️ 解析错误:", s, "|", e)
        data = {}

    for k in ["biodiv","economy","society","climate","trust"]:
        data.setdefault(k, 0)
    return data

def draw_event():
    if df.empty:
        return {
            "id": "NONE",
            "title": "无事件 / No Event",
            "desc": "当前年度没有特别事件，请根据长期目标继续推进政策。",
            "choices": {
                "A": {"label": "维持现状", "effects": {"biodiv":0,"economy":0,"society":0,"climate":0,"trust":0}},
                "B": {"label": "象征性环保声明", "effects": {"biodiv":1,"economy":-1,"society":1,"climate":1,"trust":1}},
            },
        }

    row = df.sample(1).iloc[0]
    return {
        "id": row["id"],
        "title": row["title"],
        "desc": row["desc"],
        "choices": {
            "A": {
                "label": row["choiceA_label"],
                "effects": safe_parse(row["choiceA_effects"])
            },
            "B": {
                "label": row["choiceB_label"],
                "effects": safe_parse(row["choiceB_effects"])
            }
        }
    }
