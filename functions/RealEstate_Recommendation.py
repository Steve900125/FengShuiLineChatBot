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
            City name input by user For example, 台中->臺中市、台北->臺北市、雲林->雲林縣、 
            Note: In Chinese, "台" and "臺" have the same meaning. Therefore, we uniformly use "臺". 
            If a different input is provided, it will automatically be corrected to the standard county/city name.
            採用繁體中文輸入
        """ )
    
    district : Optional[str] = Field( None , description = """
            District name input by user For example, 西區、中正區、大安區 
            If there is a typographical error in the region's name,
            please use the correct region name that you know from your records as the parameter. 
            採用繁體中文輸入
        """ )
 
    price_upper_limit : Optional[int] = Field(None ,  description = """
            Enter the maximum budget amount, in units of ten thousand. For instance, '十萬' (one hundred thousand) 
            should be input as 10, '1000萬' (ten million) should be input as 1000, and '500000' should be input as 50.
        """ )
    
    price_lower_limit : Optional[int] = Field(None , description= """
            Enter the minimum budget amount, in units of ten thousand. For instance, '十萬' (one hundred thousand) 
            should be input as 10, '1000萬' (ten million) should be input as 1000, and '500000' should be input as 50.
        """ )    
    
class RealEstateRecommendationTool(BaseTool):
    name = 'search_target_house'
    description = """
        User want to buy the house and this function helps users find the most suitable house based on their budget or location.
        Input : The function has four parameters: "top_budget", "button_budget", "county/city", and "district".
        If the user says 'approximately', take the value provided by the user as the base and add or subtract 50 million as the range. If the user only mentions one number, you can judge whether it's the upper limit or the lower limit; the program will automatically handle None values, so you don't need to forcefully assign a value.
        Output: The target house data corresponds to the requirements.
        The ouput must contain this information :
        1. natural responsement
        2. house information  : house name | price | location 
    """
    args_schema: Type[BaseModel] = RealEstateRecommendationInput

    def _run(self, city_county : str , district : Optional[str] = None , price_upper_limit : Optional[int] = None, price_lower_limit : Optional[int] = None):

        target = RealEstate_Tools.search_target_house(city_county , district , price_upper_limit , price_lower_limit )

        return target


    def _arun(self,city_county : Optional[str], district : Optional[str] ,price_upper_limit : Optional[int] , price_lower_limit : Optional[int]):
        raise NotImplementedError("This tool does not support async")


#schema = RealEstateRecommendationInput.model_json_schema()
#print(schema)

#hi = RealEstateRecommendationTool
#ans = hi._run(self= hi,city_county =  "臺北市", district = "中山區", price_upper_limit = 2000 , price_lower_limit = 50)
#print(ans)
    