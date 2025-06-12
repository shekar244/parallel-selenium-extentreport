import os
import pandas as pd

def summarize_test_durations(file_path):
    # Get directory of the input file
    base_dir = os.path.dirname(file_path)

    # Load the CSV
    df = pd.read_csv(file_path)

    # Convert start and end times to datetime
    df["Test Start Time"] = pd.to_datetime(df["Test Start Time"])
    df["Test End Time"] = pd.to_datetime(df["Test End Time"])

    # Calculate duration in minutes
    df["Duration (min)"] = (df["Test End Time"] - df["Test Start Time"]).dt.total_seconds() / 60

    # Group by test name and compute aggregates
    grouped = df.groupby("Test Name")["Duration (min)"].agg(
        Durations=lambda x: sorted(x, reverse=True),  # Sort each test's durations high→low
        Count="count",
        Total_Time="sum",
        Max_Time="max"
    ).reset_index()

    # Expand duration list into run columns
    max_runs = grouped["Durations"].apply(len).max()
    run_columns = pd.DataFrame(grouped["Durations"].tolist(),
                               columns=[f"run-{i+1}" for i in range(max_runs)])

    # Combine all parts
    result_df = pd.concat([
        grouped[["Test Name", "Count", "Total_Time", "Max_Time"]],
        run_columns
    ], axis=1)

    # Sort rows by Total_Time descending
    result_df = result_df.sort_values(by="Total_Time", ascending=False)

    # Save output to the same folder
    output_path = os.path.join(base_dir, "test_duration_summary.csv")
    result_df.to_csv(output_path, index=False)
    print(f"✅ Summary saved to: {output_path}")

# Example usage
file_path = r"C:\Your\Folder\Path\test_data.csv"  # 🔁 Replace with actual CSV path
summarize_test_durations(file_path)