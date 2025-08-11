import streamlit as st
from ai_utils import generate_situation, evaluate_sarcasm, mock_situation

# TODO: 生成中と評価中に、実行中であることがわかるような表示が必要

def main() -> None:
    """Streamlit アプリのエントリポイント。

    - テキスト入力欄
    - 提出ボタン
    提出時に内容を表示します。
    """
    st.set_page_config(page_title="Sarcasm Game", page_icon="🎭", layout="centered")
    st.title("Sarcasm Game")

    if st.button("新しい状況を生成"):
        st.session_state.update({"situation": mock_situation()})

        with st.container(border=True):
            st.subheader("状況説明")
            st.write(st.session_state.situation.replace("。", "。  ")) # 改行のために半角スペースをつける

    with st.form("input_form"):
        user_text = st.text_input("入力して、提出ボタンを押してください", key="user_text", placeholder="例: 皮肉な一言をどうぞ…")
        submitted = st.form_submit_button("提出")

    if submitted:
        evaluate_input(user_text, st.session_state.situation)

def evaluate_input(user_text: str, situation: str):
    if not situation:
        st.warning("状況を生成してください。")
        return

    if user_text:
        st.success(f"受け取りました: {user_text}")
        res = evaluate_sarcasm(user_text, situation)
        print(res)
    else:
        st.warning("入力が空です。テキストを入力してください。")

if __name__ == "__main__":
    st.session_state.setdefault("situation", "")
    main()
