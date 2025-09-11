import pandas as pd

# === CONFIGURATION ===
excel_path = "input.xlsx"           # Input Excel file
sheet_name = "Sheet1"               # Sheet name
input_column = "Input"              # Column with raw steps
output_path = "output.xlsx"         # Output Excel file

# Load Excel
df = pd.read_excel(excel_path, sheet_name=sheet_name)

def process_input(cell):
    if pd.isna(cell):
        return pd.Series(["", ""])
    
    parts = str(cell).split("|")
    desc_list = []
    exp_list = []
    
    # Iterate in triplets (Step, Description, Expected)
    i = 1
    while i + 1 < len(parts):
        if "Step" in parts[i-1]:
            step_no = parts[i-1].strip()
            desc = parts[i].strip()
            exp = parts[i+1].strip()
            
            # Append with numbering in Description, but Expected only text
            desc_list.append(f"{step_no}: {desc}")
            exp_list.append(f"{step_no}: {exp}")
        i += 3
    
    return pd.Series(["\n".join(desc_list), "\n".join(exp_list)])

# Apply only to data rows (ignore first row)
df_data = df.iloc[1:].copy()
df_data[["Description (Design Steps)", "Expected (Design Steps)"]] = df_data[input_column].apply(process_input)

# Keep the header row unchanged and merge back
df_final = pd.concat([df.iloc[[0]], df_data], ignore_index=True)

# Save result
df_final.to_excel(output_path, sheet_name=sheet_name, index=False)

print(f"✅ Output written to {output_path}, sheet: {sheet_name}")