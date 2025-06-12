import pandas as pd

def summarize_test_durations(input_csv_path, output_csv_path):
    # Load CSV
    df = pd.read_csv(input_csv_path)

    # Convert start and end times to datetime
    df["Test Start Time"] = pd.to_datetime(df["Test Start Time"])
    df["Test End Time"] = pd.to_datetime(df["Test End Time"])

    # Calculate duration in minutes
    df["Duration (min)"] = (df["Test End Time"] - df["Test Start Time"]).dt.total_seconds() / 60

    # Group by test name and collect durations
    grouped = df.groupby("Test Name")["Duration (min)"].apply(list).reset_index()

    # Expand the duration list into separate columns
    max_runs = grouped["Duration (min)"].apply(len).max()
    duration_columns = pd.DataFrame(grouped["Duration (min)"].tolist(), columns=[f"run-{i+1}" for i in range(max_runs)])

    # Combine with test name
    result = pd.concat([grouped["Test Name"], duration_columns], axis=1)

    # Save to CSV
    result.to_csv(output_csv_path, index=False)
    print(f"Summary saved to {output_csv_path}")

# Example usage
summarize_test_durations("test_data.csv", "summary_output.csv")