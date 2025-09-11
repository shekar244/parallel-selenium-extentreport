import pandas as pd

# Load input Excel
df = pd.read_excel("input.xlsx")

def process_input(cell):
    if pd.isna(cell):
        return pd.Series(["", ""])
    
    # Split by '|' while preserving text
    parts = str(cell).split("|")
    
    desc_list = []
    exp_list = []
    
    # Skip header row if present
    if "Description" in parts[1] and "Expected" in parts[2]:
        return pd.Series(["", ""])
    
    # Iterate in triplets (Step, Desc, Expected)
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

# Apply transformation on the Input column
df[["Description (Design Steps)", "Expected (Design Steps)"]] = df["Input"].apply(process_input)

# Save result
df.to_excel("output.xlsx", index=False)
print("✅ Excel file created in consolidated format: output.xlsx")