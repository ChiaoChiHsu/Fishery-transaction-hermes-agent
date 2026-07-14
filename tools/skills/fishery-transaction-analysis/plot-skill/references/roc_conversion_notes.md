# ROC 日期轉換說明

本資料的 `TransDate` 欄位使用民國年（ROC）格式 `YYYMMDD`，其中前三位是民國年，後四位是月份與日期。例如 `1100703` 代表西元 2021-07-03（110+1911=2021）。

在跨年度的資料分析中，僅以 `Month` 進行聚合會把不同年份同月的資料混在一起，導致時間序列失真。建議在多年份情境下先把 ROC 日期轉為西元 `YYYY-MM-DD`，再產生 `YearMonth`（`YYYY-MM`）欄位，以此作為 X 軸，即可保留年分資訊，同時仍保持月度聚合的可讀性。

以下是 Python 轉換範例，已在本技能的示例腳本中使用：
```python
def roc_to_gregorian(date_str: str) -> str:
    s = str(date_str)
    roc_year = int(s[:3])
    month = int(s[3:5])
    day = int(s[5:7])
    greg_year = roc_year + 1911
    return f"{greg_year:04d}-{month:02d}-{day:02d}"
```

若使用 Pandas 可直接 `pd.to_datetime(df['GregorianDate']).dt.to_period('M')` 取得 `YearMonth`。
