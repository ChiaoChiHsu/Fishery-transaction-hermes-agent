---
name: plot-skill
description: Generates a plot based on the provided fishery data and user prompt.
---
**Introduction**: This skill enables generating customized Python code for visualizing fishery transaction data using Plotly. The agent must intelligently determine the X-axis granularity (Monthly vs. Yearly vs. Continuous Date) based on the date range in the user's data. The default behavior is to create a dual-axis trend chart with price on the primary Y-axis and quantity on the secondary Y-axis, aggregated by month. However, the agent should be flexible to adjust the chart type, aggregation method, and styling based on specific user requests.
**Goal**: Generate complete, runnable Python code that processes fishery data and creates appropriate visualizations, allowing for flexible adjustments based on user requirements.
### **Implementation Steps**

**Pitfalls**
- When the data spans multiple years, aggregating only by `Month` will collapse different years together (e.g., January 2022 and January 2023 appear on the same X‑axis point). In such cases, modify the script to create a `YearMonth` column (e.g., `2022-01`) and aggregate by that column instead. Adjust the Plotly X‑axis to use the `YearMonth` labels to preserve chronological order.
- If `pandas` or `plotly` are not installed, use the provided Chart.js fallback (`references/chartjs_fallback.md
references/roc_conversion_notes.md`).

**Pitfalls & Alternatives**
- The original implementation assumes `pandas` and `plotly` are installed. If those packages are unavailable, use a lightweight fallback that generates an HTML file with Chart.js (as demonstrated in this session). Include a reference script `references/chartjs_fallback.md
references/roc_conversion_notes.md` with the fallback code.
- When patching, ensure the fallback HTML uses the same data aggregation logic (monthly averages) to keep visual consistency.
1. **Temporal Handling (CRITICAL)**:
   - **Single Year**: If the user query or data focus on one year, aggregate by `Month` (1-12).
   - **Multi-Year**: If the query covers multiple years (e.g., "5-year trend"), create a `YearMonth` (e.g., "2020-01"), `Year` (e.g., "2020") column or a datetime object to ensure the X-axis progresses chronologically.
   **Core Plotting**:
   - Primary Axis: `Avg_Price`, `Upper_Price`, `Middle_Price`, `Lower_Price`.
   - Secondary Axis: `Trans_Quantity` (Dash line).
   - Comparison: If the user compares multiple fish categories (e.g., "Tilapia vs Seabass"), create separate traces for each category on the same axes.

2. **Reference Demo Code**: Base your implementation on the demo code at [demo_plot.py](./scripts/demo_plot.py). Core logic includes:
   - Data load from JSON file
   - Data conversion to DataFrame
   - Month extraction from TransDate
   - Monthly aggregation (mean for prices, sum for quantity)
   - Dual-axis Plotly subplot creation
   - Price traces on primary axis
   - Quantity trace on secondary axis
   - Specific layout settings

3. **Flexible Adjustments**: Based on user prompts, modify:
   - Chart types, colors, styling
   - Axis labels, titles (e.g., x-axis title as Time ; y-axis title as Price (TWD/kg))
   - Data filtering/grouping
   - Additional traces/subplots
   - Layout customizations

4. **Code Generation**: 
   - Output complete, self-contained Python code.


### **Constraints**
- If `result` is empty or `None`, return early with a clear message (e.g., `print("沒有資料可以繪製圖表。")`) and do not build chart objects.
- Preserve original data fields (`TransDate`, `Upper_Price`, `Middle_Price`, `Lower_Price`, `Avg_Price`, `Trans_Quantity`) through processing steps.
- Use `pandas` for data transformation and `plotly.graph_objects` + `plotly.subplots.make_subplots` for chart generation.
- Provide complete Python code that can run directly (including imports, data preparation, and function definition).
- Default to the reference demo flow (month extraction, aggregation, dual-axis trend chart) unless the user explicitly requests a different chart type or aggregation method.

### Additional Pitfalls & Tips
- **SSL verification errors**: The MOA Open Data API may present an invalid SSL certificate. Work around by adding `verify=False` to `requests.get` calls.
- **Title/legend overlap**: Adjust the title position (e.g., `title.y=0.92`) and set legend placement with `legend=dict(y=1.12, x=0.5, xanchor='center')` to keep them separate.
- **Multi‑year X‑axis**: For data spanning multiple years, create a `YearMonth` column (convert ROC year to Gregorian and combine with month) and use it as the X‑axis. This shows each month across years in chronological order.
- **Tick label readability**: When using a Year‑Month axis, rotate tick labels (`tickangle=45`) to avoid crowding.

- If `result` is empty or `None`, return early with a clear message (e.g., `print("沒有資料可以繪製圖表。")`) and do not build chart objects.
- Preserve original data fields (`TransDate`, `Upper_Price`, `Middle_Price`, `Lower_Price`, `Avg_Price`, `Trans_Quantity`) through processing steps.
- Use `pandas` for data transformation and `plotly.graph_objects` + `plotly.subplots.make_subplots` for chart generation.
- Provide complete Python code that can run directly (including imports, data preparation, and function definition).
- Default to the reference demo flow (month extraction, aggregation, dual-axis trend chart) unless the user explicitly requests a different chart type or aggregation method.
