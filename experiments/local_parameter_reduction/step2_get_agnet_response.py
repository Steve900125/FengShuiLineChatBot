from pathlib import Path
from typing import Dict, Any, List
import json
import sys


FILE = Path(__file__).resolve()
ROOT = FILE.parents[2] 
NOW_DIR = FILE.parents[0] 
DATA_DIR = ROOT / 'data'

SEARCH_LOG_FILE = DATA_DIR / 'search_result.json'
QA_DATASET_FILE = NOW_DIR / 'qa_dataset.json'

def load_json(path: Path) -> Any:
    if not path.exists():
        print(f"Error: 檔案不存在 → {path}")
        sys.exit(1)
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: 無法解析 JSON 檔案 {path}：{e}")
        sys.exit(1)


def main():
    # read qa dataset
    qa_dataset_dic = load_json(QA_DATASET_FILE)
    print( qa_dataset_dic)

if __name__ == "__main__":
    main()