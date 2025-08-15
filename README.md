# sarcasm-game

「京都人になろう」ゲームのソースコード。  

## 概要

1. ChatGPT5-mini が状況を生成する
2. ユーザが嫌味を入力する
3. Azure AI Content Safety が嫌味を評価する
4. 以下を ChatGPT5-mini に渡して、コメント


## 使用技術

- Streamlit
- Azure AI Content Safety
- Azure AI Foundry

## 構成

```
src
├── main.py     # Streamlitの表示処理
└── ai_utils.py # AI関係の処理
```
