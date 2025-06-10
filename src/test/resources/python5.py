import os
import csv
from bs4 import BeautifulSoup

# Root folder where HTML files are stored
report_folder = "test-reports"
output_csv = os.path.join(report_folder, "extent_report_test_details.csv")

# CSV headers
header = ["File Path", "Test Name", "Test Status", "Test Start Time", "Test End Time", "Time Taken"]

rows = []

# Recursively search for all HTML files
for root, dirs, files in os.walk(report_folder):
    for filename in files:
        if filename.endswith(".html"):
            file_path = os.path.join(root, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

                # Find all test blocks
                test_blocks = soup.find_all("li", class_="collection-item test")

                for test in test_blocks:
                    # Extract fields
                    test_name_tag = test.find("span", class_="test-name")
                    status_tag = test.find("span", class_="test-status")
                    start_time_tag = test.find("span", class_="test-started-time")
                    end_time_tag = test.find("span", class_="test-ended-time")
                    time_taken_tag = test.find("span", class_="test-time-taken")

                    # Extract text safely
                    test_name = test_name_tag.text.strip() if test_name_tag else "N/A"
                    status = status_tag.text.strip() if status_tag else "N/A"
                    start_time = start_time_tag.text.strip() if start_time_tag else "N/A"
                    end_time = end_time_tag.text.strip() if end_time_tag else "N/A"
                    time_taken = time_taken_tag.text.strip() if time_taken_tag else "N/A"

                    rel_path = os.path.relpath(file_path, report_folder)
                    rows.append([rel_path, test_name, status, start_time, end_time, time_taken])

# Write to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

print(f"✅ Test-level report saved at: {output_csv}")