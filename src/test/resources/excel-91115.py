import pandas as pd

# === CONFIGURATION ===
excel_path = "input.xlsx"           # Input Excel file
sheet_name = "Sheet1"               # Sheet name
input_column = "Input"              # Column with raw steps
output_path = "output.xlsx"         # Output Excel file

# Load Excel
df = pd.read_excel(excel_path, sheet_name=sheet_name)

def split_row(cell):
    """Split one row into Step, Description, Expected"""
    if pd.isna(cell):
        return None
    parts = str(cell).split("|")
    if len(parts) >= 3 and "Step" in parts[0]:
        step_no = parts[0].strip()
        desc = parts[1].strip()
        exp = parts[2].strip()
        return step_no, desc, exp
    return None

# Process each row
descriptions = []
expecteds = []

for cell in df[input_column].dropna()[1:]:  # skip first header row
    result = split_row(cell)
    if result:
        step_no, desc, exp = result
        descriptions.append(f"{step_no}: {desc}")
        expecteds.append(f"{step_no}: {exp}")

# Consolidate all into one row
consolidated = pd.DataFrame({
    "Description (Design Steps)": ["\n".join(descriptions)],
    "Expected (Design Steps)": ["\n".join(expecteds)]
})

# Save to Excel
consolidated.to_excel(output_path, index=False, sheet_name=sheet_name)

print(f"✅ Consolidated Excel written to {output_path}")