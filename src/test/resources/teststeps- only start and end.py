import os
import csv
from bs4 import BeautifulSoup

def extract_tests_from_html(html_path):
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    test_data = []

    # Loop through all test case <li> elements
    for test in soup.select("ul.test-collection > li"):
        test_name = "Unknown"
        test_status = "Unknown"
        test_start = ""
        test_end = ""

        # Test Name
        name_span = test.select_one("span.test-name")
        if name_span:
            test_name = name_span.text.strip()

        # Status
        status_span = test.select_one("span.test-status")
        if status_span:
            test_status = status_span.text.strip()

        # Start Time
        start_span = test.select_one("span.test-started-time")
        if start_span:
            test_start = start_span.text.strip()

        # End Time
        end_span = test.select_one("span.test-ended-time")
        if end_span:
            test_end = end_span.text.strip()

        # Fallback to last test step timestamp
        if not test_end or test_end.strip() == "":
            timestamps = test.select("td.timestamp")
            if timestamps:
                last_step_time = timestamps[-1].text.strip()
                if test_start and len(test_start.split()) == 2:
                    test_date = test_start.split()[0]
                    test_end = f"{test_date} {last_step_time}"

        test_data.append({
            "HTML Report": os.path.basename(html_path),  # ✅ Renamed for clarity
            "Test Name": test_name,
            "Test Status": test_status,
            "Start Time": test_start,
            "End Time": test_end
        })

    return test_data


def extract_all_reports_from_folder(folder_path):
    all_data = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".html"):
                html_path = os.path.join(root, file)
                print(f"🔍 Processing: {html_path}")
                test_info = extract_tests_from_html(html_path)
                all_data.extend(test_info)
    return all_data


def write_to_csv(data, output_csv):
    if not data:
        print("⚠️ No test data found.")
        return

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["HTML Report", "Test Name", "Test Status", "Start Time", "End Time"])
        writer.writeheader()
        writer.writerows(data)

    print(f"\n✅ CSV summary saved to:\n{output_csv}")


# ========= 🔁 USAGE ==========
if __name__ == "__main__":
    input_folder = r"C:\Path\To\Your\Reports"  # ⬅️ Update this
    output_csv = os.path.join(input_folder, "extent_test_summary.csv")

    all_tests = extract_all_reports_from_folder(input_folder)
    write_to_csv(all_tests, output_csv)