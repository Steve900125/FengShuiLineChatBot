from pathlib import Path
import json

# ─── 常數設定 ────────────────────────────────────
ROOT_DIR           = Path(__file__).resolve().parents[1]
DATA_DIR           = ROOT_DIR / 'data'
CITY_COUNTY_FILE   = DATA_DIR / 'CityCountyData.json'
REVERSE_FILE       = DATA_DIR / 'DistrictToCities.json'

# ─── 建立或載入「區→縣市清單」映射 ─────────────────────────
def _load_or_build_mapping() -> dict[str, list[str]]:
    # 若快取檔已存在，直接讀取
    if REVERSE_FILE.exists():
        with REVERSE_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)

    # 否則從原始資料建立映射
    if not CITY_COUNTY_FILE.exists():
        raise FileNotFoundError(f"找不到檔案：{CITY_COUNTY_FILE}")
    with CITY_COUNTY_FILE.open('r', encoding='utf-8') as f:
        city_data = json.load(f)

    mapping: dict[str, list[str]] = {}
    for city in city_data:
        cname = city.get('CityName')
        for area in city.get('AreaList', []):
            district = area.get('AreaName')
            if district and cname:
                mapping.setdefault(district, []).append(cname)

    # 寫入快取
    REVERSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with REVERSE_FILE.open('w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    return mapping

# 全域快取
_district_to_cities: dict[str, list[str]] | None = None

def get_cities_by_district(district_name: str) -> list[str]:
    """
    唯一對外函式：傳入區名，回傳可能的縣市清單（List[str]）。
    若查無資料，回傳空清單。
    """
    print("區域查詢:",district_name)
    global _district_to_cities
    if _district_to_cities is None:
        _district_to_cities = _load_or_build_mapping()
    print("查詢縣市:",_district_to_cities.get(district_name, []))
    return _district_to_cities.get(district_name, [])


# ─── 測試範例 ───────────────────────────────────
if __name__ == "__main__":
    for d in ["中正區", "西區", "溪口鄉", "不存在區域"]:
        cities = get_cities_by_district(d)
        if cities:
            print(f"{d} → {cities}")
        else:
            print(f"{d} → 查無資料")

