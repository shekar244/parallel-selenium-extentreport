import csv
from datetime import datetime
from collections import defaultdict
import os

# Input and output file paths
input_csv = "test-reports/extent_report_test_details.csv"
summary_csv = "test-reports/extent_report_summary.csv"

# Parse datetime safely
def parse_time(t_str):
    try:
        return datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S")
    except:
        return None

# Dictionary to hold summaries
test_summary = defaultdict(lambda: {
    "runs": 0,
    "total_duration_sec": 0.0,
    "longest_duration_sec": 0.0,
    "shortest_duration_sec": float("inf")
})

# Read input test details
with open(input_csv, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        test_name = row["Test Name"]
        start_time = parse_time(row["Test Start Time"])
        end_time = parse_time(row["Test End Time"])

        if test_name and start_time and end_time:
            duration = (end_time - start_time).total_seconds()
            data = test_summary[test_name]
            data["runs"] += 1
            data["total_duration_sec"] += duration
            data["longest_duration_sec"] = max(data["longest_duration_sec"], duration)
            if duration > 0:
                data["shortest_duration_sec"] = min(data["shortest_duration_sec"], duration)

# Write summary to output CSV
with open(summary_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Test Name",
        "Number of Runs",
        "Total Duration (seconds)",
        "Average Duration (seconds)",
        "Longest Duration (seconds)",
        "Shortest Duration (seconds)"
    ])

    for test_name, data in test_summary.items():
        avg = data["total_duration_sec"] / data["runs"]
        shortest = data["shortest_duration_sec"] if data["shortest_duration_sec"] != float("inf") else 0
        writer.writerow([
            test_name,
            data["runs"],
            round(data["total_duration_sec"], 2),
            round(avg, 2),
            round(data["longest_duration_sec"], 2),
            round(shortest, 2)
        ])

print(f"✅ Summary with shortest & longest durations saved to: {summary_csv}")