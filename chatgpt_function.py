
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