import os
import csv
from bs4 import BeautifulSoup

# Folder where Extent Report HTML files are located
report_folder = "test-reports"
output_csv = "extent_report_summary.csv"

# CSV header
header = ["File Name", "Start Time", "End Time", "Scenario Names"]

# Data rows will be collected here
rows = []

# Loop through HTML files
for filename in os.listdir(report_folder):
    if filename.endswith(".html"):
        file_path = os.path.join(report_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

            # ✅ Start Time
            start_time_tag = soup.find("span", class_="panel-lead suite-started-time")
            start_time = start_time_tag.text.strip() if start_time_tag else "N/A"

            # ✅ End Time
            end_time_tag = soup.find("span", class_="panel-lead suite-ended-time")
            end_time = end_time_tag.text.strip() if end_time_tag else "N/A"

            # ✅ Scenario/Test Names
            scenario_tags = soup.find_all("div", class_="test-name")
            scenarios = [tag.text.strip() for tag in scenario_tags]
            scenario_list = "; ".join(scenarios) if scenarios else "N/A"

            # Add row
            rows.append([filename, start_time, end_time, scenario_list])

# ✅ Write to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

print(f"✅ Extraction complete. Output saved to: {output_csv}")