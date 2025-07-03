import os
import csv
from bs4 import BeautifulSoup
from datetime import datetime

def extract_test_info_from_html(html_file):
    with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    results = []

    for container in soup.find_all("div", class_="container"):
        test_name = "Unknown"
        test_status = "Unknown"
        test_start = ""
        test_end = ""

        # Test Name
        name_span = container.find("span", class_="test-name")
        if name_span:
            test_name = name_span.text.strip()

        # Test Status
        status_span = container.find("span", class_="test-status")
        if status_span:
            test_status = status_span.text.strip()

        # Start Time
        start_span = container.find("span", class_="test-started-time")
        if start_span:
            test_start = start_span.text.strip()

        # End Time - primary
        end_span = container.find("span", class_="test-ended-time")
        if end_span:
            test_end = end_span.text.strip()

        # Fallback: use last test step timestamp if end time is missing
        if not test_end or test_end.strip() == "":
            step_timestamps = container.select("td.timestamp")
            if step_timestamps:
                last_step_time = step_timestamps[-1].text.strip()
                if test_start and len(test_start.split()) == 2:
                    test_date = test_start.split()[0]
                    test_end = f"{test_date} {last_step_time}"

        results.append({
            "Test Name": test_name,
            "Test Status": test_status,
            "Start Time": test_start,
            "End Time": test_end
        })

    return results


def write_to_csv(data, output_path):
    if not data:
        print("⚠️ No test data extracted.")
        return

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Test Name", "Test Status", "Start Time", "End Time"])
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Extracted test info written to: {output_path}")


# ====== 🔁 USAGE SECTION ======
if __name__ == "__main__":
    # Replace with your input HTML file path
    input_html = r"C:\Path\To\Your\extent_report.html"  # ⬅️ CHANGE THIS

    if not os.path.isfile(input_html):
        print(f"❌ File not found: {input_html}")
    else:
        test_data = extract_test_info_from_html(input_html)
        for entry in test_data:
            print(entry)

        output_csv = os.path.join(os.path.dirname(input_html), "extracted_test_info.csv")
        write_to_csv(test_data, output_csv)