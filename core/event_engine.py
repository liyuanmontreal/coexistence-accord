import pandas as pd
import random
import ast
import re

df = pd.read_csv("data/events.csv")

def safe_parse(s):
    """安全解析事件效果列，自动补引号并补全字段"""
    if pd.isna(s):
        return {"biodiv":0,"economy":0,"society":0,"climate":0}
    s = str(s).strip()
    if not s.startswith("{"):
        s = "{" + s
    if not s.endswith("}"):
        s = s + "}"

    # 自动补引号
    s = re.sub(r'([{,]\s*)([a-zA-Z_]\w*)(\s*:)', r'\1"\2"\3', s)

    try:
        data = ast.literal_eval(s)
        # 确保四个关键键都存在
        for k in ["biodiv", "economy", "society", "climate"]:
            if k not in data:
                data[k] = 0
        return data
    except Exception as e:
        print("⚠️ 解析错误:", s, "|", e)
        return {"biodiv":0,"economy":0,"society":0,"climate":0}

def draw_event():
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
