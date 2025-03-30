import json
import pandas as pd
import requests
from datetime import datetime
from io import BytesIO

url = "https://rosstat.gov.ru/storage/mediabank/ipc_mes_02-2025.xlsx"
response = requests.get(url)
df = pd.read_excel(BytesIO(response.content), sheet_name="01", header=None)

month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
               "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
latest_ipc = None
year = 2025

for row in range(4, len(df)):
    month = df.iloc[row, 0]
    if isinstance(month, str) and month.strip() in month_names:
        value = df.iloc[row, 34]
        if isinstance(value, (float, int)):
            latest_ipc = {
                "month": month.strip(),
                "ipc": round(float(value), 2)
            }

month_index = month_names.index(latest_ipc["month"]) + 1
start = f"{year}-{month_index:02d}-01"
days_in_month = pd.Period(start).days_in_month
end = f"{year}-{month_index:02d}-{days_in_month:02d}"

with open("ipc.json", encoding="utf-8") as f:
    ipc_data = json.load(f)

exists = any(entry["start"] == start for entry in ipc_data["data"])
if not exists:
    ipc_data["data"].append({
        "start": start,
        "end": end,
        "ipc": latest_ipc["ipc"],
        "days": days_in_month
    })
    ipc_data["generated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("ipc.json", "w", encoding="utf-8") as f:
        json.dump(ipc_data, f, ensure_ascii=False, indent=2)