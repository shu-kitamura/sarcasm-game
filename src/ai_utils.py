import os
import json
import dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, AnalyzeTextOutputType, AnalyzeTextResult

dotenv.load_dotenv()

def create_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_version="2025-04-01-preview",
        azure_endpoint=os.getenv("GPT5_ENDPOINT"),
        api_key=os.getenv("GPT5_API_KEY")
    )

def generate_situation() -> str:
    client = create_client()

    response = client.responses.create(
        model="gpt-5-mini",
        instructions= (
            "あなたは『京都風嫌味』ゲーム用のシチュエーション生成器です。"
            "目的：ユーザが“表向きは丁寧・内側に皮肉”を言いやすい状況を作る。"
            "制約：直接的な罵倒・差別・暴力の誘発は禁止。"
            "出力：3行以内、日本語のみ。1行目=あなたは○○です、2~3行目=相手の行動や発言（具体）"
            "ジャンル：職場、学校、ご近所、親戚、友人、SNS、趣味、冠婚葬祭、旅行、買い物などを均等に使用してください。"
            "例："
            "あなたは会社の先輩。\n後輩が朝10時に出社してきました（始業は9時）。\n机にコーヒーを置き、のんびり椅子に座ったところで、あなたが一言。"
            "あなたは町内会の会計係。\n会合で隣の役員が金色の派手な着物を見せびらかしています。\n周囲はやや引き気味です。\n"
            "あなたは友人グループの一員。\nSNSで一人の友人が旅行の写真を100枚連投し続けています。\n通知が止まりません。"
            "余計な前置き・解説は書かない。"
        ),
        input=f"嫌味・皮肉を言いやすい状況を生成してください。",
    )

    return response.output_text

def evaluate_content_safety(sarcasm: str) -> dict:
    endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("CONTENT_SAFETY_API_KEY")

    client = ContentSafetyClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )

    request = AnalyzeTextOptions(text=sarcasm)
    response = client.analyze_text(request)

    result_dict = {}

    for item in response.categories_analysis:
        result_dict[item.category] = item.severity

    return result_dict

def evaluate_sarcasm(sarcasm: str, situation: str) -> dict:
    content_safety_results = evaluate_content_safety(sarcasm)

    evaluate_target = {
        "sarcasm": sarcasm,
        "situation": situation,
        "content_safety": content_safety_results
    }
    
    client = create_client()

    response = client.responses.create(
        model="gpt-5-mini",
        instructions= (
            "あなたは『京都風嫌味』ゲームの評価者です。"
            "目的：与えられた sarcasm（ユーザの発話）、situation（状況）、"
            "content_safety（Content Safety の評価値）をもとに、"
            "京都風嫌味としての完成度を総評する。"
            "総評は文章のみで3〜5文。"
            "禁止：現実的なアドバイス、相手との関係性や感情面の注意喚起、"
            "表情や声色の提案、改善案、言い方のコツ、長文の解説。"
            "出力は総評の文章のみで、余計な前置きや後書きは書かない。"
        ),
        input=json.dumps(evaluate_target, ensure_ascii=False),
    )

    evaluate_result = {
        "content_safety": content_safety_results,
        "evaluation": response.output_text
    }

    return evaluate_result
