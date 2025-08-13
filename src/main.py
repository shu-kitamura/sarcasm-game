import streamlit as st
import pandas as pd
from ai_utils import generate_situation, evaluate_sarcasm

def main() -> None:
    """Streamlit アプリのエントリポイント。

    - テキスト入力欄
    - 提出ボタン
    提出時に内容を表示します。
    """
    st.title("Sarcasm Game")

    # 状況の生成ボタン
    if st.button("新しい状況を生成"):
        with st.spinner("状況を生成中..."):
            situation = generate_situation()
            st.session_state.update({"situation": situation})

    situation = st.session_state.get("situation")

    # 状況がある場合のみ表示
    if situation:
        with st.container(border=True):
            st.subheader("状況説明")
            st.write(situation)

        # フォームは状況生成後のみ表示
        with st.form("input_form", clear_on_submit=True):
            user_text = st.text_input(
                "入力して、提出ボタンを押してください",
                key="user_text",
                placeholder="例: 皮肉な一言をどうぞ…",
            )
            submitted = st.form_submit_button("提出")

        if submitted:
            with st.spinner("評価中..."):
                result = evaluate_input(user_text, situation)

            if result:
                display_result(user_text, result)

def evaluate_input(user_text: str, situation: str):
    if user_text:
        result = evaluate_sarcasm(user_text, situation)
        return result

def display_result(user_text: str, result: dict):
    cs_result: dict = result.get("content_safety")
    df = pd.DataFrame(
        list(cs_result.items()),
        columns=["カテゴリ", "スコア"]
    )

    with st.container(border=True):
        st.subheader("あなたの入力")
        st.write(user_text)
        st.subheader("点数")
        st.dataframe(df, hide_index=True)
        st.subheader("コメント")
        st.write(result.get("evaluation"))


if __name__ == "__main__":
    st.set_page_config(page_title="Sarcasm Game", page_icon="🎭", layout="centered")
    st.session_state.setdefault("situation", "")

    main()
