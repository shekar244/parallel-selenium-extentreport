import os
import zipfile
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import tempfile

# Base folder where all reports (or ZIPs) reside
base_folder = "test-reports"
output_csv = os.path.join(base_folder, "extent_report_test_details.csv")

# Function to parse datetime from format: "5/19/2025 18:55"
def parse_time(time_str):
    try:
        return datetime.strptime(time_str.strip(), "%m/%d/%Y %H:%M")
    except:
        return None

# Extract details from an HTML report
def extract_from_html(file_path):
    results = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

        # Report Start and End Times (only once per report)
        start_span = soup.find("span", string="Start Time")
        end_span = soup.find("span", string="End Time")

        report_start = parse_time(start_span.find_next("span").text.strip()) if start_span else None
        report_end = parse_time(end_span.find_next("span").text.strip()) if end_span else None

        # Individual test names (usually <span class='test-name'>)
        for test_name_span in soup.find_all("span", class_="test-name"):
            test_name = test_name_span.text.strip()

            # Try to find nearby start and end time
            container = test_name_span.find_parent("li")
            test_start = None
            test_end = None

            if container:
                start_tag = container.find("span", string="Start Time")
                end_tag = container.find("span", string="End Time")

                if start_tag:
                    test_start = parse_time(start_tag.find_next("span").text.strip())
                if end_tag:
                    test_end = parse_time(end_tag.find_next("span").text.strip())

            results.append({
                "Test Name": test_name,
                "Test Start Time": test_start.strftime("%Y-%m-%d %H:%M") if test_start else "",
                "Test End Time": test_end.strftime("%Y-%m-%d %H:%M") if test_end else "",
                "Report File": os.path.relpath(file_path, base_folder)
            })
    return results

# Process files recursively (including ZIPs)
all_test_data = []

for root, dirs, files in os.walk(base_folder):
    for file in files:
        file_path = os.path.join(root, file)

        if file.lower().endswith(".html"):
            all_test_data.extend(extract_from_html(file_path))

        elif file.lower().endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    zip_ref.extractall(tmp_dir)

                    # Look for HTML files inside extracted content
                    for dirpath, _, zip_files in os.walk(tmp_dir):
                        for zip_file in zip_files:
                            if zip_file.lower().endswith(".html"):
                                html_path = os.path.join(dirpath, zip_file)
                                all_test_data.extend(extract_from_html(html_path))

# Write output to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Test Name", "Test Start Time", "Test End Time", "Report File"])
    writer.writeheader()
    for row in all_test_data:
        writer.writerow(row)

print(f"✅ Extracted data from HTMLs & ZIPs saved to: {output_csv}")