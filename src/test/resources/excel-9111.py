import pandas as pd

# === CONFIGURATION ===
excel_path = "input.xlsx"           # Your Excel file path
sheet_name = "Sheet1"               # Your sheet name
input_column = "Input"              # Column that contains the raw input text
output_path = "output.xlsx"         # Output file name

# Load Excel
df = pd.read_excel(excel_path, sheet_name=sheet_name)

def process_input(cell):
    if pd.isna(cell):
        return pd.Series(["", ""])
    
    parts = str(cell).split("|")
    desc_list = []
    exp_list = []
    
    # Skip header row if present
    if len(parts) >= 3 and "Description" in parts[1] and "Expected" in parts[2]:
        return pd.Series(["", ""])
    
    # Iterate in triplets (Step, Description, Expected)
    i = 1
    while i + 1 < len(parts):
        if "Step" in parts[i-1]:
            step_no = parts[i-1].strip()
            desc = parts[i].strip()
            exp = parts[i+1].strip()
            
            # Append with numbering
            desc_list.append(f"{step_no}: {desc}")
            exp_list.append(f"{step_no}: {exp}")
        i += 3
    
    # Return consolidated columns with line breaks
    return pd.Series(["\n".join(desc_list), "\n".join(exp_list)])

# Apply transformation
df[["Description (Design Steps)", "Expected (Design Steps)"]] = df[input_column].apply(process_input)

# Save result to new Excel
df.to_excel(output_path, sheet_name=sheet_name, index=False)

print(f"✅ Output written to {output_path}, sheet: {sheet_name}")