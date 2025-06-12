import os
import pandas as pd

def summarize_test_durations(file_path):
    # Get the directory of the input file
    base_dir = os.path.dirname(file_path)

    # Load the CSV
    df = pd.read_csv(file_path)

    # Convert date strings to datetime
    df["Test Start Time"] = pd.to_datetime(df["Test Start Time"])
    df["Test End Time"] = pd.to_datetime(df["Test End Time"])

    # Calculate duration in minutes
    df["Duration (min)"] = (df["Test End Time"] - df["Test Start Time"]).dt.total_seconds() / 60

    # Group durations by test name
    grouped = df.groupby("Test Name")["Duration (min)"].apply(list).reset_index()

    # Expand into run-1, run-2, ...
    max_runs = grouped["Duration (min)"].apply(len).max()
    run_columns = pd.DataFrame(grouped["Duration (min)"].tolist(),
                               columns=[f"run-{i+1}" for i in range(max_runs)])

    # Final output DataFrame
    result_df = pd.concat([grouped["Test Name"], run_columns], axis=1)

    # Save to same folder with a new name
    output_path = os.path.join(base_dir, "test_duration_summary.csv")
    result_df.to_csv(output_path, index=False)
    print(f"✅ Summary saved to: {output_path}")

# Example usage
file_path = r"C:\Your\Folder\Path\test_data.csv"  # Replace with your actual file path
summarize_test_durations(file_path)