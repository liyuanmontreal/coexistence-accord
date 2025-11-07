import streamlit as st
from core.turn_manager import TurnManager
from core.state_store import state
from viz.plots import plot_dynamics

st.set_page_config(page_title="Eco-Policy Lab v2 — Coexistence Accord", layout="wide")

if "tm" not in st.session_state:
    st.session_state["tm"] = TurnManager()
tm = st.session_state["tm"]

st.sidebar.title("Eco-Policy Lab")
page = st.sidebar.radio("视图 View", ["Policy & Events", "Dynamics", "Export"])
media_bias = st.sidebar.slider("媒体偏向 Media Bias (-1 反政府 / 1 支持政府)", -1.0, 1.0, 0.0, 0.1)
st.sidebar.markdown("---")
st.sidebar.subheader("Global Indicators")
for k, v in state.global_metrics().items():
    st.sidebar.progress(v / 100.0)
    st.sidebar.write(f"**{k}: {v:.1f}**")

if page == "Policy & Events":
    event = tm.current_event()
    st.markdown("## 国际生态政策理事会")
    st.markdown(f"### 当前议题: **{event['title']}**")
    st.write(event["desc"])
    st.markdown("---")
    st.markdown("### 可选行动 Options")

    for key, choice in event["choices"].items():
        eff = choice["effects"]
        effects_text = (
            f"🌿 Biodiv {eff.get('biodiv',0):+d} | "
            f"💰 Economy {eff.get('economy',0):+d} | "
            f"🧍 Society {eff.get('society',0):+d} | "
            f"☁️ Climate {eff.get('climate',0):+d} | "
            f"🤝 Trust {eff.get('trust',0):+d}"
        )
        with st.container():
            st.markdown(f"**{choice['label']}**  \n{effects_text}")
            if st.button(f"执行方案 {key}", key=f"btn_{key}"):
                tm.apply_choice(eff, media_bias=media_bias)
                st.rerun()
        st.markdown('---')

elif page == "Dynamics":
    st.markdown("##  Dynamics")
    df = state.history_df()
    if df.empty:
        st.info("暂无历史数据，请先在 Policy & Events 页面执行若干轮决策。")
    else:
        st.write("最近10条记录：")
        st.dataframe(df.tail(10), use_container_width=True)
        fig = plot_dynamics(df)
        st.pyplot(fig)

elif page == "Export":
    st.markdown("## Export & Review")
    df = state.history_df()
    if df.empty:
        st.info("暂无可导出的历史数据，请先运行若干轮模拟。")
    else:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="下载模拟历史 CSV",
            data=csv,
            file_name="eco_policy_lab_history.csv",
            mime="text/csv",
        )
        st.write("预览：")
        st.dataframe(df.tail(10), use_container_width=True)

st.markdown("---")
st.caption("Eco-Policy Lab  — 生态多样性、社会信任与气候风险的政策实验平台。")
