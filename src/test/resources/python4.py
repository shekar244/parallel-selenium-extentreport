import os
import csv
from bs4 import BeautifulSoup

# Root folder where all Extent Reports are stored (including subfolders)
report_folder = "test-reports"
output_csv = os.path.join(report_folder, "extent_report_summary.csv")

# CSV header
header = ["File Path", "Start Time", "End Time", "Scenario Names"]

# Collect rows for CSV
rows = []

# Walk through all subdirectories
for root, dirs, files in os.walk(report_folder):
    for filename in files:
        if filename.endswith(".html"):
            file_path = os.path.join(root, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

                # ✅ Extract Start Time
                start_tag = soup.find("span", class_="panel-lead suite-started-time")
                start_time = start_tag.text.strip() if start_tag else "N/A"

                # ✅ Extract End Time
                end_tag = soup.find("span", class_="panel-lead suite-ended-time")
                end_time = end_tag.text.strip() if end_tag else "N/A"

                # ✅ Extract Scenario Names
                scenario_tags = soup.find_all("div", class_="test-name")
                scenarios = [tag.text.strip() for tag in scenario_tags]
                scenario_list = "; ".join(scenarios) if scenarios else "N/A"

                # ✅ Append full row with relative path
                rel_path = os.path.relpath(file_path, report_folder)
                rows.append([rel_path, start_time, end_time, scenario_list])

# ✅ Write the collected data to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

print(f"✅ Done! CSV saved at: {output_csv}")