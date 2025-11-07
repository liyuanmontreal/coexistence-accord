import streamlit as st
import pandas as pd
from core.turn_manager import TurnManager
from core.state_store import state

st.set_page_config(page_title="共栖协定 Coexistence Accord", layout="wide")

tm = TurnManager()

st.title(" 共栖协定 Coexistence Accord — UN Simulation Desk")

# Sidebar metrics
st.sidebar.header("Global Indicators")
for k, v in state.global_metrics().items():
    st.sidebar.progress(v / 100)
    st.sidebar.write(f"**{k}: {v:.1f}**")

# Display event
event = tm.current_event()
st.subheader(f" {event['title']}")
st.write(event['desc'])
st.write("---")

# --- 可选行动 (完全清理版) ---
st.markdown("###  可选行动 Options")

for key, choice in event["choices"].items():
    eff = choice["effects"]

    # 如果 effects 是字符串（例如 '{"biodiv":-7,...}'），先尝试解析
    if isinstance(eff, str):
        import ast
        try:
            eff = ast.literal_eval(eff)
        except Exception:
            eff = {"biodiv":0, "economy":0, "society":0, "climate":0}

    # 格式化成清晰指标行
    effects_text = (
        f"🌿 Biodiv {eff.get('biodiv',0):+d} | 💰 Economy {eff.get('economy',0):+d} | "
        f"🧍 Society {eff.get('society',0):+d} | ☁️ Climate {eff.get('climate',0):+d}"
    )

    with st.container():
        st.markdown(f"**{choice['label']}**  \n{effects_text}")
        # 注意：不再写 st.write(choice["effects"]) !!!
        if st.button(f"执行方案 {key}", key=f"btn_{key}"):
            tm.apply_choice(choice)
            st.rerun()
    st.markdown("---")



# Chart
st.write("### 📊 Global Trends")
df = state.history_df()
if not df.empty:
    st.line_chart(df.set_index("year"))


