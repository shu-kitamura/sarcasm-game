import streamlit as st


def main() -> None:
    """Streamlit アプリのエントリポイント。

    - テキスト入力欄
    - 提出ボタン
    提出時に内容を表示します。
    """
    st.set_page_config(page_title="Sarcasm Game", page_icon="🎭", layout="centered")
    st.title("Sarcasm Game")

    # TODO: 生成AIで状況説明を生成する
    situation = """
        あなたは町内会の集まりに参加中。
        隣に座ったご近所さんが、今日はやけに派手な金色の着物を着ています。
        本人は自慢げに「どう？これ新調したの」と言っています。
    """

    with st.container(border=True):
        st.subheader("状況説明")
        st.write(situation.replace("。", "。  ")) # 改行のために半角スペースをつける

    with st.form("input_form", enter_to_submit=False):
        user_text = st.text_input("入力して、提出ボタンを押してください", key="user_text", placeholder="例: 皮肉な一言をどうぞ…")
        submitted = st.form_submit_button("提出")

    st.markdown("---")

    if submitted:
        if user_text and user_text.strip():
            st.success(f"受け取りました: {user_text}")
            # TODO: 生成AIで皮肉な一言を評価する
        else:
            st.warning("入力が空です。テキストを入力してください。")

if __name__ == "__main__":
    # このスクリプトは `streamlit run src/main.py` で実行してください。
    main()
