import os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# === Configuration ===
PROCESSED_LOG_FILE = "processed_files.csv"
DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"

# === Load processed file names to avoid re-processing ===
def load_processed_files():
    if os.path.exists(PROCESSED_LOG_FILE):
        return set(pd.read_csv(PROCESSED_LOG_FILE)['filename'])
    return set()

def save_processed_file(filename):
    mode = 'a' if os.path.exists(PROCESSED_LOG_FILE) else 'w'
    header = not os.path.exists(PROCESSED_LOG_FILE)
    with open(PROCESSED_LOG_FILE, mode) as f:
        if header:
            f.write("filename\n")
        f.write(f"{filename}\n")

# === Extract test data from one HTML file ===
def extract_tests_from_html(html_path):
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    test_data = []

    for test in soup.select("ul.test-collection > li"):
        test_name = "Unknown"
        test_status = "Unknown"
        test_start = ""
        test_end = ""
        duration = ""

        name_span = test.select_one("span.test-name")
        if name_span:
            test_name = name_span.text.strip()

        status_span = test.select_one("span.test-status")
        if status_span:
            test_status = status_span.text.strip()

        start_span = test.select_one("span.test-started-time")
        if start_span:
            test_start = start_span.text.strip()

        end_span = test.select_one("span.test-ended-time")
        if end_span:
            test_end = end_span.text.strip()

        # Fallback if end time is missing
        if not test_end or test_end.strip() == "":
            timestamps = test.select("td.timestamp")
            if timestamps:
                last_step_time = timestamps[-1].text.strip()
                if test_start and len(test_start.split()) == 2:
                    test_date = test_start.split()[0]
                    test_end = f"{test_date} {last_step_time}"

        # Duration calculation
        try:
            if test_start and test_end:
                start_dt = datetime.strptime(test_start, DATETIME_FORMAT)
                end_dt = datetime.strptime(test_end, DATETIME_FORMAT)
                duration = round((end_dt - start_dt).total_seconds() / 60, 2)
            else:
                duration = ""
        except Exception as e:
            print(f"⚠️  Error parsing duration for {test_name}: {e}")
            duration = ""

        test_data.append({
            "HTML Report": os.path.basename(html_path),
            "Test Name": test_name,
            "Test Status": test_status,
            "Start Time": test_start,
            "End Time": test_end,
            "Duration (mins)": duration
        })

    return test_data

# === Generate summary report DataFrame ===
def summarize_test_durations(df):
    df["Start Time"] = pd.to_datetime(df["Start Time"], errors="coerce")
    df["End Time"] = pd.to_datetime(df["End Time"], errors="coerce")
    df = df.dropna(subset=["Start Time", "End Time"])

    df["Duration (mins)"] = round((df["End Time"] - df["Start Time"]).dt.total_seconds() / 60, 2)
    df["Start+Duration"] = list(zip(df["Start Time"], df["Duration (mins)"]))

    grouped = df.groupby("Test Name")["Start+Duration"].agg(
        SortedRuns=lambda x: [d for _, d in sorted(x)]
    ).reset_index()

    agg_stats = df.groupby("Test Name")["Duration (mins)"].agg(
        Count="count", Total_Time="sum", Max_Time="max"
    ).reset_index()

    merged = pd.merge(grouped, agg_stats, on="Test Name")

    max_runs = merged["SortedRuns"].apply(len).max()
    run_columns = pd.DataFrame(merged["SortedRuns"].tolist(),
                               columns=[f"run-{i+1}" for i in range(max_runs)])

    summary_df = pd.concat([
        merged[["Test Name", "Count", "Total_Time", "Max_Time"]],
        run_columns
    ], axis=1)

    return summary_df

# === Main runner to process folder and generate Excel ===
def extract_all_reports_from_folder(folder_path, output_excel):
    all_data = []
    processed = load_processed_files()

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".html") and file not in processed:
                html_path = os.path.join(root, file)
                print(f"🔍 Processing: {html_path}")
                try:
                    test_info = extract_tests_from_html(html_path)
                    if test_info:
                        all_data.extend(test_info)
                        save_processed_file(file)
                except Exception as e:
                    print(f"❌ Error reading {file}: {e}")

    if all_data:
        df = pd.DataFrame(all_data)
        summary_df = summarize_test_durations(df)

        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="test run details")
            summary_df.to_excel(writer, index=False, sheet_name="summary report")

        print(f"\n✅ {len(df)} test entries written to '{output_excel}' with summary.")
    else:
        print("\n⚠️ No new HTML reports to process.")

# === Example usage ===
if __name__ == "__main__":
    folder_to_scan = "Reports"  # Update this to your HTML reports folder
    output_excel = "Test_Run_Details.xlsx"
    extract_all_reports_from_folder(folder_to_scan, output_excel)