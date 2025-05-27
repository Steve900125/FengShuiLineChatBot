from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from pathlib import Path
import sys

# —— 路徑設定 ——
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
sys.path.insert(0, str(ROOT))
from functions.area_information import get_cities_by_district

class AreaInformationInput(BaseModel):
    district_name: str = Field(
        ..., 
        description="鄉鎮市區參數，用來查詢縣市（繁體中文）"
    )

class AreaInformationTool(BaseTool):
    name: str = "area-information"  # 明確易懂的工具名稱
    description: str = "查詢鄉鎮市區所屬縣市"
    args_schema: type[BaseModel] = AreaInformationInput

    def _run(self,district_name: str) -> str:
        cities = get_cities_by_district(district_name)
        if not cities:
            return f"{district_name} 查無資料"
        return ", ".join(cities)

    async def _arun(self, tool_input: AreaInformationInput) -> str:
        # 若不支援 async，也請改簽名對應 args_schema
        return self._run(tool_input)
