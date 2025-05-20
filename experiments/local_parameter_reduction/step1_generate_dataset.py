#!/usr/bin/env python3
# generate_dataset.py

import sys
from pathlib import Path
import json
from typing import Dict, Any, List

# ─── 1. 調整模組搜尋路徑 ──────────────────────────────────────────────
FILE         = Path(__file__).resolve()
NOW_DIR      = FILE.parent             # .../experiment/answer
PROJECT_ROOT = NOW_DIR.parent.parent   # .../SingleQuestionAnswer
sys.path.insert(0, str(PROJECT_ROOT))

# ─── 2. 載入 search_house ────────────────────────────────────────────
from functions.real_estate_functions import search_house


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
    # ─── 3. 路徑定義 ────────────────────────────────────────────────────
    city_towns_path = NOW_DIR / "city_towns.json"
    duplicate_path  = NOW_DIR / "duplicate_town_to_cities.json"
    split_path      = NOW_DIR / "split_city_district.json"
    output_path     = NOW_DIR / "qa_dataset.json"

    # ─── 4. 檢查並讀入 JSON ─────────────────────────────────────────────
    city_to_towns = load_json(city_towns_path)
    duplicate_map = load_json(duplicate_path)

    # ─── 5. 拆分重複 / 非重複 pairs ─────────────────────────────────────
    all_pairs       = [(city, town) for city, towns in city_to_towns.items() for town in towns]
    duplicate_pairs = [(c, t) for c, t in all_pairs if t in duplicate_map]
    nondup_pairs    = [(c, t) for c, t in all_pairs if t not in duplicate_map]

    # ─── 5.1 輸出中間檔案 split_city_district.json ───────────────────────
    split_data = {"duplicate": duplicate_pairs, "non_duplicate": nondup_pairs}
    try:
        with split_path.open("w", encoding="utf-8") as f:
            json.dump(split_data, f, ensure_ascii=False, indent=2)
        print(f"Saved split file: {split_path}")
    except Exception as e:
        print(f"Error: 無法寫入檔案 {split_path}：{e}")
        sys.exit(1)

    # ─── 6. 產生 QA dataset ─────────────────────────────────────────────
    qa_dataset: Dict[str, Any] = {}
    for idx, (city, district) in enumerate(nondup_pairs, start=1):
        qid      = f"Q{idx}"
        question = f"我要找{district}的房子，價格在2000萬以下"
        try:
            answer = search_house(
                city_county       = city,
                district          = district,
                price_upper_limit = 2000
            )
        except Exception as e:
            print(f"Warning: search_house 在 {city}-{district} 時發生錯誤：{e}")
            answer = []
        qa_dataset[qid] = {"question": question, "answer": answer}

    # ─── 7. 輸出 QA JSON ────────────────────────────────────────────────
    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(qa_dataset, f, ensure_ascii=False, indent=2)
        print(f"Saved QA dataset: {output_path} (共 {len(qa_dataset)} 筆)")
    except Exception as e:
        print(f"Error: 無法寫入檔案 {output_path}：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
