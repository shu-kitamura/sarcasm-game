# sarcasm-game

[京都人になろう](https://be-kyoto-cqfzh0argzhshpc2.eastasia-01.azurewebsites.net/) ゲームのソースコード。  

## 概要

1. GPT5-mini が状況を生成する
2. ユーザが嫌味を入力する
3. Azure AI Content Safety が嫌味を評価する
4. 以下を GPT5-mini に渡して、コメント


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
