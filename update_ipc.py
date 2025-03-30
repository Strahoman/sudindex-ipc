import json
import pandas as pd
from datetime import datetime
import calendar

# Загружаем существующий JSON
with open("ipc.json", encoding="utf-8") as f:
    ipc_data = json.load(f)

# Загружаем данные из R-выгрузки
df = pd.read_csv("ipc_from_r.csv")

added = False
for index, row in df.iterrows():
    year, month = row["Time"].split("-")
    start = f"{year}-{month}-01"
    days = calendar.monthrange(int(year), int(month))[1]
    end = f"{year}-{month}-{days:02d}"
    ipc_value = float(row["Value"])

    if not any(entry["start"] == start for entry in ipc_data["data"]):
        ipc_data["data"].append({
            "start": start,
            "end": end,
            "ipc": round(ipc_value, 2),
            "days": days
        })
        added = True

if added:
    ipc_data["generated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("ipc.json", "w", encoding="utf-8") as f:
        json.dump(ipc_data, f, ensure_ascii=False, indent=2)