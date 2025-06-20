import os
import pandas as pd

def summarize_test_durations(file_path):
    # Get the directory of the input file
    base_dir = os.path.dirname(file_path)

    # Load CSV into a DataFrame
    df = pd.read_csv(file_path)

    # Convert time columns to datetime
    df["Test Start Time"] = pd.to_datetime(df["Test Start Time"], errors="coerce")
    df["Test End Time"] = pd.to_datetime(df["Test End Time"], errors="coerce")

    # Drop rows where either time is missing
    df = df.dropna(subset=["Test Start Time", "Test End Time"])

    # Calculate duration in minutes
    df["Duration (min)"] = (df["Test End Time"] - df["Test Start Time"]).dt.total_seconds() / 60

    # Attach start time with duration for sorting
    df["Start+Duration"] = list(zip(df["Test Start Time"], df["Duration (min)"]))

    # Group by test name and sort each group's runs by start time
    grouped = df.groupby("Test Name")["Start+Duration"].agg(
        SortedRuns=lambda x: [d for _, d in sorted(x)]
    ).reset_index()

    # Add Count, Total, Max
    agg_stats = df.groupby("Test Name")["Duration (min)"].agg(
        Count="count",
        Total_Time="sum",
        Max_Time="max"
    ).reset_index()

    # Merge both summaries
    grouped = pd.merge(grouped, agg_stats, on="Test Name")

    # Expand SortedRuns into run-1, run-2, ...
    max_runs = grouped["SortedRuns"].apply(len).max()
    run_columns = pd.DataFrame(grouped["SortedRuns"].tolist(),
                               columns=[f"run-{i+1}" for i in range(max_runs)])

    # Final DataFrame
    result_df = pd.concat([
        grouped[["Test Name", "Count", "Total_Time", "Max_Time"]],
        run_columns
    ], axis=1)

    # Save to CSV
    output_path = os.path.join(base_dir, "test_duration_summary.csv")
    result_df.to_csv(output_path, index=False)
    print(f"✅ Summary saved to: {output_path}")

# Example usage
file_path = r"C:\Your\Folder\Path\test_data.csv"  # 🔁 Replace with actual file path
summarize_test_durations(file_path)
