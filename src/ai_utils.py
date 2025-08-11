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
            "例：あなたは会社の先輩。\n後輩が朝10時に出社してきました（始業は9時）。\n机にコーヒーを置き、のんびり椅子に座ったところで、あなたが一言。"
            "余計な前置き・解説は書かない。"
        ),
        input=f"嫌味・皮肉を言いやすい状況を生成してください。",
    )

    return response.output_text

def mock_situation() -> str:
    return "あなたは会社の先輩。後輩が朝10時に出社してきました（始業は9時）。机にコーヒーを置き、のんびり椅子に座ったところで、あなたが一言。"

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
            "あなたは『京都風嫌味』ゲーム用の嫌味評価器です。"
            "目的：ユーザが入力した皮肉な一言（sarcasm）が、与えられた状況（situation）に対して適切かどうかを評価する。"
            "sarcasm と situation に加えて Content Safety の結果を考慮して、評価する。"
            # TODO: システムプロンプト改善
        ),
        input=json.dumps(evaluate_target, ensure_ascii=False),
    )

    evaluate_result = {
        "content_safety": content_safety_results,
        "evaluation": response.output_text
    }

    return evaluate_result
