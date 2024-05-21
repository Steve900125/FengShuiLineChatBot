from langchain.tools import BaseTool
# LangChain tools declear
from pydantic import BaseModel, Field
# Check the type of variable
from typing import Optional
# Some variable can be optional
from typing import Type

from functions import FengShui_Tools


class FengShuiRecommendationInput(BaseModel):

    feng_shui_name : str = Field(..., description = """
            此變數 feng_shui_name 是風水類型的名稱需要關鍵字即可不要有其他符號例如 /n，
            一律採用繁體中文輸入，例如對門煞
            記得遇到錯字請自動修正 
        """ )
    
    
class FengShuiRecommendationTool(BaseTool):
    name = 'FengShui_advice'
    description = """
        幫助使用者理解風水相關問題
        採用繁體中文做處理避免亂碼影響程式執行
        重點 ： 這是一個幫助使用者得到風水建議的功能
        輸入 ： 風水種類來當作參數
        輸出 ： 你必需像個最佳的風水專家回覆你找到的資料與問候，並且將資料以格式化方式回覆
        格式如下 ： (1) 風水問題 (2) 發生條件 (3) 解釋
        如果使用者位提供必要資訊你可以要求對方提供更多資訊
    """
    args_schema: Type[BaseModel] = FengShuiRecommendationInput

    def _run(self, feng_shui_name : str ):

        target = FengShui_Tools.get_fengshui_advice(feng_shui_name )
        return target

    def _arun(self, feng_shui_name : str):
        raise NotImplementedError("This tool does not support async")

    