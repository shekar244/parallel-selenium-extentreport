import os
import zipfile
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import tempfile

# Base directory
base_folder = "test-reports"
output_csv = os.path.join(base_folder, "extent_report_test_details.csv")

# Parse "5/19/2025 18:55" to datetime
def parse_time(time_str):
    try:
        return datetime.strptime(time_str.strip(), "%m/%d/%Y %H:%M")
    except:
        return None

# Extract test info from a single HTML report
def extract_from_html(file_path, source_name):
    results = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

        for test_container in soup.find_all("li", class_="test"):
            name_tag = test_container.find("span", class_="test-name")
            test_name = name_tag.text.strip() if name_tag else "Unknown"

            # Find Start and End times
            test_start = None
            test_end = None

            start_label = test_container.find("span", string="Start Time")
            if start_label:
                start_value = start_label.find_next("span")
                test_start = parse_time(start_value.text.strip()) if start_value else None

            end_label = test_container.find("span", string="End Time")
            if end_label:
                end_value = end_label.find_next("span")
                test_end = parse_time(end_value.text.strip()) if end_value else None

            results.append({
                "Test Name": test_name,
                "Test Start Time": test_start.strftime("%Y-%m-%d %H:%M") if test_start else "",
                "Test End Time": test_end.strftime("%Y-%m-%d %H:%M") if test_end else "",
                "Report Source": source_name
            })
    return results

# Recursively find all HTML and ZIP files, process them
all_data = []

for root, _, files in os.walk(base_folder):
    for file in files:
        file_path = os.path.join(root, file)

        # Direct .html file
        if file.lower().endswith(".html"):
            all_data.extend(extract_from_html(file_path, os.path.relpath(file_path, base_folder)))

        # ZIP file - extract and process .html inside
        elif file.lower().endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    zip_ref.extractall(tmp_dir)
                    for zip_root, _, zip_files in os.walk(tmp_dir):
                        for zip_file in zip_files:
                            if zip_file.lower().endswith(".html"):
                                html_path = os.path.join(zip_root, zip_file)
                                all_data.extend(extract_from_html(html_path, os.path.relpath(file_path, base_folder)))

# Write results to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Test Name", "Test Start Time", "Test End Time", "Report Source"])
    writer.writeheader()
    writer.writerows(all_data)

print(f"✅ Final combined report saved to: {output_csv}")