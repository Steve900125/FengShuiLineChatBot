from langchain.tools import BaseTool
# LangChain tools declear
from pydantic import BaseModel, Field
# Check the type of variable
from typing import Optional
# Some variable can be optional
from typing import Type

from functions import RealEstate_Tools

# 根據使用者條件決定符合條件的房地產資料回傳給使用者
# 可以輸入縣市、區域、最高價格限制、最低價格限制
# Input variables definition in here
class RealEstateRecommendationInput(BaseModel):
    # Variable descriptio and Type define

    # Optional means "Not Qequired Variable"
    # "None" in the Field() also mean "Not Qequired Variable"
    # "..." in the Field() mean "Qequired Variable"
    city_county : str = Field(..., description = """
            一律採用繁體中文輸入，這個變數 city_county 是臺灣的縣/市名稱
            採用完整名稱作為輸入，例如 ： 台中->臺中市、台北->臺北市、雲林->雲林縣、 
            記得 "台" 跟 "臺" 是相同意思，但一律採用 "臺" 作爲標準，遇到錯字請自動修正為標準輸入
        """ )
    
    district : Optional[str] = Field( None , description = """
            一律採用繁體中文輸入，這個變數 district 是臺灣的區域名稱                         
            採用完整名稱作為輸入，例如 ：  西區、中正區、大安區 
            記得 "台" 跟 "臺" 是相同意思，但一律採用 "臺" 作爲標準，遇到錯字請自動修正為標準輸入
        """ )
 
    price_upper_limit : Optional[int] = Field(None ,  description = """
            price_upper_limit 代表預算的金額上限，該變數的單位為萬
            舉例來說 ： '十萬' -> 10 , '1000萬' -> 1000 , '50000000' -> 5000
            如果對方有提供可以選擇放入
        """ )
    
    price_lower_limit : Optional[int] = Field(None , description= """
            price_lower_limit 代表預算的金額下限，該變數的單位為萬
            舉例來說 ： '十萬' -> 10 , '1000萬' -> 1000 , '50000000' -> 5000
            如果對方有提供可以選擇放入
        """ )    
    
class RealEstateRecommendationTool(BaseTool):
    name = 'search_target_house'
    description = """
        重點 ： 這是一個幫助使用者找到屬於自己想要的房屋資訊的程式
        縣市區域採用繁體中文做處理避免亂碼應響程式執行
        輸入 ： 透過 ( 縣市名稱 區域名稱 價格上限 價格下限 ) 來當作參數
        當對方只給大約的價格時你可以上下加上 500 萬當作範圍輸入
        輸出 ： 你必需像個最佳的客服回覆你找到的資料與問候，並且將資料以格式化方式回覆
        格式如下 ： 房子名稱 ｜ 位置 ｜ 價格 
        如果沒有你要的必要資訊或不清楚的情況你可以再詳細跟客戶做詢問
    """
    args_schema: Type[BaseModel] = RealEstateRecommendationInput

    def _run(self, city_county : str , district : Optional[str] = None , price_upper_limit : Optional[int] = None, price_lower_limit : Optional[int] = None):

        target = RealEstate_Tools.search_target_house(city_county , district , price_upper_limit , price_lower_limit )

        return target


    def _arun(self, city_county : Optional[str], district : Optional[str] ,price_upper_limit : Optional[int] , price_lower_limit : Optional[int]):
        raise NotImplementedError("This tool does not support async")


#schema = RealEstateRecommendationInput.model_json_schema()
#print(schema)

#hi = RealEstateRecommendationTool()
#ans = hi._run(self= hi,city_county =  "臺北市", district = "中山區", price_upper_limit = 2000 , price_lower_limit = 50)
#print(ans)
    