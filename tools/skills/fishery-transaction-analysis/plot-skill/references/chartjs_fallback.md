# Chart.js fallback for fishery data visualization

This file contains a self‑contained Python script that generates an HTML file using Chart.js when the required Python packages (`pandas`, `plotly`) are not available.

```python
import json
import os

# ---------- Configuration ----------
# Path to the JSON file produced by `get-fishery-data`
json_path = '/Users/user1/workspace/jia-yi-wuguo-fish_3years.json'
# Output HTML file path
html_path = '/Users/user1/workspace/jia-yi-wuguo-fish_3years_plot.html'
# -----------------------------------

# Load the raw fishery transaction data
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Aggregate by ROC year‑month (e.g. "112-01")
agg = {}
for rec in data:
    td = str(rec.get('TransDate', ''))
    if len(td) < 5:
        continue
    year = int(td[:3])
    month = int(td[3:5])
    key = f"{year}-{month:02d}"
    if key not in agg:
        agg[key] = {
            'cnt': 0,
            'Upper_Price': 0,
            'Middle_Price': 0,
            'Lower_Price': 0,
            'Avg_Price': 0,
            'Trans_Quantity': 0,
        }
    a = agg[key]
    a['cnt'] += 1
    for k in ['Upper_Price', 'Middle_Price', 'Lower_Price', 'Avg_Price']:
        try:
            a[k] += float(rec.get(k, 0))
        except Exception:
            pass
    try:
        a['Trans_Quantity'] += float(rec.get('Trans_Quantity', 0))
    except Exception:
        pass

# Sort keys chronologically
sorted_keys = sorted(
    agg.keys(), key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1])
)
labels = []
avg_prices = []
upper_prices = []
mid_prices = []
lower_prices = []
quantities = []
for k in sorted_keys:
    a = agg[k]
    cnt = a['cnt'] or 1
    labels.append(k)
    avg_prices.append(a['Avg_Price'] / cnt)
    upper_prices.append(a['Upper_Price'] / cnt)
    mid_prices.append(a['Middle_Price'] / cnt)
    lower_prices.append(a['Lower_Price'] / cnt)
    quantities.append(a['Trans_Quantity'])

# Generate a simple HTML page that uses Chart.js to render the data
html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>嘉義 吳郭魚 近三年每月價格與交易量</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h2>嘉義 吳郭魚 近三年（112‑114）每月平均價格與交易量</h2>
    <canvas id="myChart" width="900" height="500"></canvas>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const chart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {labels},
                datasets: [
                    {{label: '平均價格', data: {avg_prices}, borderColor: 'blue', yAxisID: 'y1'}},
                    {{label: '高價', data: {upper_prices}, borderColor: 'green', yAxisID: 'y1'}},
                    {{label: '中價', data: {mid_prices}, borderColor: 'orange', yAxisID: 'y1'}},
                    {{label: '低價', data: {lower_prices}, borderColor: 'red', yAxisID: 'y1'}},
                    {{label: '交易量', data: {quantities}, borderColor: 'black', borderDash: [5,5], yAxisID: 'y2'}},
                ]
            }},
            options: {{
                scales: {{
                    y1: {{type: 'linear', position: 'left', title: {{display:true, text:'價格 (TWD/kg)'}}}},
                    y2: {{type: 'linear', position: 'right', title: {{display:true, text:'交易量 (kg)'}}, grid: {{drawOnChartArea:false}}}}
                }},
                plugins: {{title: {{display:true, text:'嘉義 吳郭魚 近三年每月價格與交易量'}}}}
            }}
        }});
    </script>
</body>
</html>'''

# Write the HTML file
os.makedirs(os.path.dirname(html_path), exist_ok=True)
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print('HTML fallback saved to', html_path)
```

The script mirrors the aggregation logic used in the Plotly version and produces the same visual insights without requiring any external Python libraries beyond the standard library.
