# Example usage:
function_name = "recommend_by_budget_location"
function_description = '''
    User want to buy the house and this function helps users find the most suitable house based on their budget or location.
    Input : The function has four parameters: "top_budget", "button_budget", "county/city", and "district".
    Output: The target house data corresponds to the requirements.
'''
params = [
    {
        "name": "top_budget", "type": "integer", 
         "description": '''
            Enter the maximum budget amount, in units of ten thousand. For instance, '十萬' (one hundred thousand) 
            should be input as 10, '1000萬' (ten million) should be input as 1000, and '500000' should be input as 50.
         ''',
         "required" : False
    },
    {
        "name": "button_budget", "type": "integer", 
         "description": '''
             Enter the minimum budget amount, in units of ten thousand. For instance, '十萬' (one hundred thousand) 
             should be input as 10, '1000萬' (ten million) should be input as 1000, and '500000' should be input as 50.
         ''',
         "required" : False
    },
    {
        "name": "city_county", "type": "string", 
        "description": '''
            City name input by user For example, 台中->臺中市、台北->臺北市、雲林->雲林縣、 
            Note: In Chinese, "台" and "臺" have the same meaning. Therefore, we uniformly use "臺". 
            If a different input is provided, it will automatically be corrected to the standard county/city name.
            採用繁體中文輸入
        ''',
        "required" : False
    },
    {
        "name": "district", "type": "string", 
        "description": '''
            District name input by user For example, 西區、中正區、大安區 
            If there is a typographical error in the region's name,
            please use the correct region name that you know from your records as the parameter. 
            採用繁體中文輸入
        ''',
        "required" : False
    }
]

# name : function's name
# description : 解釋功能目的
# parameters : 傳入參數的解釋與定義
# params = [
#    {"name": "變數名稱", "type": "資料型態", "description": "變數的描述" , "required" : True or False},
#    {"name": "變數名稱", "type": "資料型態", "description": "變數的描述" , "required" : True or False}...........
#]  
#============================================================================#
def make_function_call_description(name: str, description: str, parameters: list) -> dict:
    function_description = {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
    }
    for param in parameters:
        param_name = param['name']
        param_type = param.get('type', 'string')  # Default type is 'string'
        param_desc = param['description']
        
        function_description["parameters"]["properties"][param_name] = {
            "type": param_type,
            "description": param_desc
        }
        
        if param["required"] == True:
            function_description["parameters"]["required"].append(param_name)

    return function_description



def call_functions():
    new_function = make_function_call_description(name = function_name ,description = function_description , parameters = params)
    return new_function 

