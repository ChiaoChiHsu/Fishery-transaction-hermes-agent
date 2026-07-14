import requests
import json
import os
from pydantic import BaseModel, Field
from typing import Optional

# define parameter model
class FisheryQueryParams(BaseModel):
    start_date: str = Field(
        ..., 
        description="查詢開始日期，格式為民國年月日（YYYMMDD），例如：1090101"
    )
    end_date: str = Field(
        ..., 
        description="查詢結束日期，格式為民國年月日（YYYMMDD），例如：1091231"
    )
    product_code: Optional[str] = Field(
        None, 
        description="漁產品代碼。若未提供則查詢所有品項。"
    )
    product_name: Optional[str] = Field(
        None, 
        description="漁產品名稱，例如：'金目鱸'。若未提供則查詢所有品項。"
    )
    market_name: Optional[str] = Field(
        None, 
        description="交易市場名稱，例如：'三重'。若未提供則查詢所有市場。"
    )
    api_key: Optional[str] = Field(
        None, 
        description="農業部開放資料 API Key"
    )

def get_fishery_data(params: FisheryQueryParams):
    
    """
    根據 Pydantic 定義的參數，從API獲取過濾後的漁產資料，並過濾掉「休市」紀錄。
    """
    base_url = "https://data.moa.gov.tw/api/v1/"
    fishery_url = "FisheryProductsTransType/"
    url = base_url + fishery_url
    
    api_params = {
        "Start_time": params.start_date,
        "End_time": params.end_date,
        "api_key": params.api_key
    }

    # Optional parameters
    if params.product_name:
        api_params["SeafoodProdName"] = params.product_name
    if params.market_name:
        api_params["MarketName"] = params.market_name
    if params.product_code:
        api_params["SeafoodProdCode"] = params.product_code
    
    page = 1

    try:
        response = requests.get(url, params=api_params, verify=False)
        response.raise_for_status()  # 如果請求失敗會拋出異常

        # 取得原始 Data 列表
        raw_data = response.json().get("Data", [])
        _next = response.json().get("Next")
        print(f"第 {page} 頁，Next = {_next}，取得 {len(raw_data)} 筆")

        # 過濾: 排除休市
        all_filtered_data = [
            item for item in raw_data
            if item.get("SeafoodProdName") != "休市"
        ]

        while _next:
            page += 1
            api_params["page"] = str(page)

            response = requests.get(url, params=api_params, verify=False)
            response.raise_for_status()
            _page_data = response.json().get("Data", [])
            _next = response.json().get("Next")
            print(f"第 {page} 頁，Next = {_next}，取得 {len(_page_data)} 筆")

            page_filtered = [
                item for item in _page_data
                if item.get("SeafoodProdName") != "休市"
            ]
            all_filtered_data.extend(page_filtered)

        return all_filtered_data

    except requests.exceptions.RequestException as e:
        print(f"發生錯誤: {e}")
        return []


if __name__ == "__main__":
    USER_API_KEY = "J2TOE1V17U0QKJHUM6VDST9FRPOHL0"
    json_path = "/Users/user1/workspace/jia-yi-tilapia_five_years.json"    # output file
    
    # Example 1
    test_params = FisheryQueryParams(
        start_date="1050330",
        end_date="1150330",
        product_name="金目鱸",
        market_name="三重",
        api_key=USER_API_KEY
    )

    # get data
    result = get_fishery_data(test_params)

    if result:
        print(f"{test_params.start_date}-{test_params.end_date} {test_params.product_name} {test_params.market_name}取得 {len(result)} 筆已過濾的資料。")

        # 儲存JSON 檔案
        try:
            # ensure_ascii=False 確保中文不會變成亂碼
            # indent=4 讓檔案內容有縮排，方便人類閱讀
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f"資料已成功存入：{os.path.abspath(json_path)}")
        except Exception as e:
            print(f"存檔時發生錯誤: {e}")

    else:
        print("未能取得資料。")