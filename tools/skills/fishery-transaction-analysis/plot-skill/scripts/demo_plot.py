import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

def plot_fishery_analysis(result):
    if not result:
        print("沒有資料可以繪製圖表。")
        return

    # 1. 資料轉換與預處理
    df = pd.DataFrame(result)
    # 提取月份 (從 TransDate 的第 4-5 位，例如 1090102 -> 01)
    df['Month'] = df['TransDate'].str.slice(3, 5).astype(int)
    
    # 2. 按月份聚合數據
    monthly_data = df.groupby('Month').agg({
        'Upper_Price': 'mean',
        'Middle_Price': 'mean',
        'Lower_Price': 'mean',
        'Avg_Price': 'mean',
        'Trans_Quantity': 'sum'
    }).reset_index().sort_values('Month')

    

    # 3. 建立雙 Y 軸圖表
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 4. 加入價格線條 (左側 Y 軸)
    # 平均價 (粗線)
    fig.add_trace(
        go.Scatter(x=monthly_data['Month'], y=monthly_data['Avg_Price'], 
                   name="Average Price", line=dict(color='dodgerblue', width=1.5), mode='lines+markers'),
        secondary_y=False,
    )
    
    
    # 高、中、低價 (細線/淡色)
    colors = {
        'avg': '#1F77B4',     # 藍色 (平均價)
        'upper': '#2CA02C',   # 綠色 (高價)
        'middle': '#FF7F0E',  # 橘色 (中價)
        'lower': '#D62728',   # 紅色 (低價)
        'qty': '#000000'      # 黑色 (交易數量)
    }
    # 價格線條 (左側 Y 軸)
    price_traces = [
        ('Avg_Price', 'Average Price', colors['avg'], 1.5),
        ('Upper_Price', 'Upper Price', colors['upper'], 1.5),
        ('Middle_Price', 'Middle Price', colors['middle'], 1.5),
        ('Lower_Price', 'Lower Price', colors['lower'], 1.5)
    ]
    for col, name, color, width in price_traces:
        fig.add_trace(
            go.Scatter(x=monthly_data['Month'], y=monthly_data[col], 
                      name=name, line=dict(color=color, width=width)),
                      secondary_y=False
        )

    # 5. 加入交易數量線條 (右側 Y 軸 - 虛線)
    fig.add_trace(
        go.Scatter(x=monthly_data['Month'], y=monthly_data['Trans_Quantity'],
                   name="Transaction Quantity", line=dict(color=colors['qty'],
                   dash='dash', width=3)), secondary_y=True
    )

    # 6. 設定字體與佈局
    fig.update_layout(
        title={
            'text': "1090101-1091231 Monthly Trend (金目鱸/三重)",
            'y':0.95, # 移動標題，不要跟圖重疊
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=22, family="sans-serif") # 標題字體
        },
        font=dict(family="sans-serif", size=14), # 全域字體
        xaxis=dict(title_text="Month", tickmode='linear', tick0=1, dtick=1), # 確保橫軸顯示 1 到 12 月
        yaxis=dict(title_text="Price (TWD/kg)"), # 左側縱軸標題
        yaxis2=dict(title_text="Transaction Quantity"), # 右側縱軸標題
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) # 圖例
    )

    return fig

# 呼叫範例
if __name__ == "__main__":
    USER_API_KEY = "USER_API_KEY"
    json_path = "USER_JSON_PATH"    # ex: "/workspace/fishery_data.json"

    # EXAMPLE USER PROMPT: "幫我畫出 2020 年金目鱸在三重的價格與交易量趨勢圖，時間範圍從 1090101 到 1091231。"
    result = open (json_path, 'r', encoding='utf-8')
    result = json.load(result)
    plot_fishery_analysis(result)