# 
import pandas as pd
import random
def search_target_house( city_county , district , price_upper_limit , price_lower_limit ):

    # Initinal the input values
    house_data = None
    requirement = "縣市名稱：" + str(city_county) + "區域：" + str(district) + "價格上限" + str(price_upper_limit) + "價格下限" + str(price_lower_limit)
    print('傳入的資料如下 ：')
    print(requirement)
    if price_upper_limit == None:
        price_upper_limit = 2000
    if price_lower_limit == None:
        price_lower_limit = 0
    
    # Search data from database

    # Return data
    
    # Test Code 
    
    # 建立假資料
    # 生成每個區都有2筆資料的 data 字典
    data = {
        'house_name': ['House_' + str(i) for i in range(1, 11)],
        'price': [random.randint(500, 2000) for _ in range(10)],  # 價格範圍設置為 500-2000 萬
        'city_county': ['臺北市'] * 10,
        'district': [district for district in ['大安區', '大同區', '中山區', '松山區', '信義區'] for _ in range(2)]
    }
    df = pd.DataFrame(data)
    
    print(df)
    df = df[(df['price'] >=  price_lower_limit ) & (df['price'] <= price_upper_limit)]

    #filtered_dic = {k: v for k, v in arguments.items() if v is not None }
    
    if city_county  != None:
        df = df[ df['city_county'] == city_county]
    
    if district != None:
        df = df[ df['district'] == district]

    house_data = df.to_json(orient='records', force_ascii=False)

    print('符合條件的資料如下 ：')
    print(house_data)
    if house_data == None :

        house_data = "很抱歉我們目前沒有符合您搜索條件的房屋" + requirement 

    return house_data 