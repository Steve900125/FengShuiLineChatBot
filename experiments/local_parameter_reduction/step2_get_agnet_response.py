from pathlib import Path
from typing import Any, Dict, List
import json
import sys
import time

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # 到達專案根目錄
NOW_DIR = FILE.parents[0]
DATA_DIR = ROOT / 'data'
sys.path.insert(0, str(ROOT))

SEARCH_LOG_FILE = DATA_DIR / 'search_result.json'
QA_DATASET_FILE = NOW_DIR / 'qa_dataset.json'
EVALUATE_RESULT_FILE = NOW_DIR / 'evaluate_result.json'

from agent_main import create_agent
from langchain_core.messages import HumanMessage, SystemMessage


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_null_search_log():
    logs = load_json(SEARCH_LOG_FILE) or []
    logs.append([])
    save_json(SEARCH_LOG_FILE, logs)


def one_time_agent(question: str) -> str:
    time.sleep(5)
    agent = create_agent()
    config = {'configurable': {'thread_id': 'tester'}}
    sys_prompt = '''
    1. 你是一位房地產輔助機器人負責協助使用者，
    2. 請不要提問使用者不存在的功能例如房型等
    3. 僅依照現有存在的參數描述做提問
    4. 若只提供區資訊而該縣市只有一個可不用詢問，先由區反推縣市
    '''
    SystemMessage(content=sys_prompt)
    agent.update_state(config, {'messages': sys_prompt})
    response = agent.invoke({'messages': [HumanMessage(content=question)]}, config)
    return response['messages'][-1].content


def ensure_file_exists(path: Path, default: Any) -> None:
    """
    確保 JSON 檔案存在，若不存在則建立並寫入預設內容。
    """
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=2)


def main():
    # 確認 QA dataset 存在
    if not QA_DATASET_FILE.exists():
        print(f"Error: QA dataset not found → {QA_DATASET_FILE}")
        sys.exit(1)

    # 載入 QA 資料
    qa_dataset = load_json(QA_DATASET_FILE) or {}

    # 確保 SEARCH_LOG_FILE 與 EVALUATE_RESULT_FILE 存在（初始化）
    ensure_file_exists(SEARCH_LOG_FILE, [])
    ensure_file_exists(EVALUATE_RESULT_FILE, {'summary': {}, 'results': []})

    # 清空 search log
    try:
        save_json(SEARCH_LOG_FILE, [])
    except Exception as e:
        print(f"Error initializing search log: {e}")
        sys.exit(1)

    results: List[Dict[str, Any]] = []
    correct_count = 0

    # 逐題執行
    for idx, q_id in enumerate(qa_dataset):
        question = qa_dataset[q_id].get('question', '')
        expected = qa_dataset[q_id].get('answer')

        # 呼叫 agent
        try:
            answer = one_time_agent(question)
        except Exception as e:
            print(f"Agent error on question {q_id}: {e}")
            answer = ""
        
        # 檢查並補齊 search log 長度
        logs = load_json(SEARCH_LOG_FILE) or []
        while idx >= len(logs):
            append_null_search_log()
            logs = load_json(SEARCH_LOG_FILE) or []
        this_search = logs[idx]

        # 顯示問題與回應
        print(f"Question: {question}")
        print(f"Agent response: {answer}")

        # 判斷正確性
        correct = (this_search == expected)
        if correct:
            correct_count += 1

        # 收集結果
        results.append({
            'question': question,
            'agent_response': answer,
            'expected_answer': expected,
            'search_results': this_search,
            'correct': correct
        })

    # 計算摘要
    total = len(results)
    summary = {
        'total_questions': total,
        'correct_count': correct_count,
        'incorrect_count': total - correct_count,
        'accuracy_percent': round(correct_count / total * 100, 2) if total else 0
    }

    # 輸出評估結果
    try:
        save_json(EVALUATE_RESULT_FILE, {'summary': summary, 'results': results})
    except Exception as e:
        print(f"Error saving evaluate result: {e}")
        sys.exit(1)
    print(f'Evaluation completed. Summary: {summary}')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
