#!/usr/bin/env python3
"""
Excel Description Processor
==========================

A comprehensive solution for processing Excel files with pipe-separated description columns.
This script reads an Excel file, parses the Description column by splitting on the '|' symbol,
and populates the corresponding columns with structured test steps.

Features:
- Reads Excel files and identifies description columns
- Parses pipe-separated test steps
- Updates columns B & C with structured design steps and expected results
- Preserves existing data
- Provides detailed logging and verification
- Auto-activates virtual environment if needed

Author: AI Assistant
Date: 2025
"""

import sys
import os
import subprocess

def ensure_virtual_environment():
    """
    Ensure we're running in the virtual environment with required packages.
    If not, try to activate it and re-run the script.
    """
    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a virtual environment, continue normally
        return True
    
    # Check if pandas is available (our main dependency)
    try:
        import pandas
        return True
    except ImportError:
        pass
    
    # Try to find and activate virtual environment
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(script_dir, 'venv')
    
    if os.path.exists(venv_path):
        print("🔧 Virtual environment detected but not active. Activating and re-running...")
        
        # Determine the activation script path based on OS
        if os.name == 'nt':  # Windows
            activate_script = os.path.join(venv_path, 'Scripts', 'python.exe')
        else:  # Unix/Linux/macOS
            activate_script = os.path.join(venv_path, 'bin', 'python')
        
        if os.path.exists(activate_script):
            # Re-run the script with the virtual environment Python
            cmd = [activate_script] + sys.argv
            result = subprocess.run(cmd)
            sys.exit(result.returncode)
    
    # If we get here, we couldn't find or activate the virtual environment
    print("❌ Virtual environment not found or pandas not installed!")
    print("Please run the following commands first:")
    print("  python3 -m venv venv")
    print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# Ensure virtual environment is active before importing other packages
ensure_virtual_environment()

# Now we can safely import the required packages
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from typing import Tuple, Optional

# ========================================
# CONFIGURATION - UPDATE THESE VARIABLES
# ========================================
EXCEL_FILE = "Book1.xlsx"          # Excel file to process (change this to your file name)
SHEET_NAME = "Input"               # Sheet name containing the data (change if different)
CREATE_BACKUP = False               # Whether to create backup before processing (True/False)

# Examples:
# EXCEL_FILE = "MyTestData.xlsx"
# SHEET_NAME = "TestCases" 
# CREATE_BACKUP = False
# ========================================

class ExcelDescriptionProcessor:
    """Main class for processing Excel description columns."""
    
    def __init__(self, file_path: str, sheet_name: str = 'Input'):
        """
        Initialize the processor.
        
        Args:
            file_path (str): Path to the Excel file
            sheet_name (str): Name of the sheet to process (default: 'Input')
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.backup_created = False
    
    def create_backup(self) -> bool:
        """
        Create a backup of the original Excel file.
        
        Returns:
            bool: True if backup was created successfully
        """
        try:
            backup_path = f"{os.path.splitext(self.file_path)[0]}_backup.xlsx"
            import shutil
            shutil.copy2(self.file_path, backup_path)
            print(f"✅ Backup created: {backup_path}")
            self.backup_created = True
            return True
        except Exception as e:
            print(f"⚠️  Warning: Could not create backup: {e}")
            return False
    
    def examine_excel_structure(self) -> bool:
        """
        Examine the Excel file structure and display information.
        
        Returns:
            bool: True if examination was successful
        """
        try:
            print("📋 Examining Excel File Structure")
            print("=" * 60)
            
            # Check available sheets
            xls = pd.ExcelFile(self.file_path)
            print(f"Available sheets: {xls.sheet_names}")
            
            if self.sheet_name not in xls.sheet_names:
                print(f"❌ Sheet '{self.sheet_name}' not found!")
                print(f"Available sheets: {xls.sheet_names}")
                return False
            
            # Read the target sheet
            df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            print(f"\nSheet: {self.sheet_name}")
            print(f"Shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            
            # Check for required columns
            if 'Description' not in df.columns:
                print("❌ 'Description' column not found!")
                return False
            
            print("\n📊 Current Data Preview:")
            print("-" * 40)
            for idx, row in df.iterrows():
                desc_col_b = row.get('Description (Design Steps)', 'N/A')
                desc_col_c = row.get('Description (Expected Result)', 'N/A')
                
                print(f"Row {idx + 1}:")
                print(f"  Column A (Description): {'✓ Has data' if pd.notna(row['Description']) else '✗ Empty'}")
                print(f"  Column B (Design Steps): {'✓ Has data' if pd.notna(desc_col_b) else '✗ Empty (will be processed)'}")
                print(f"  Column C (Expected Result): {'✓ Has data' if pd.notna(desc_col_c) else '✗ Empty (will be processed)'}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error examining Excel structure: {e}")
            return False
    
    def parse_description_to_steps(self, description_text: str) -> Tuple[str, str]:
        """
        Parse the description text and extract structured steps.
        
        Args:
            description_text (str): The pipe-separated description text
            
        Returns:
            tuple: (design_steps, expected_results)
        """
        if pd.isna(description_text) or not description_text:
            return "", ""
        
        design_steps = []
        expected_results = []
        
        # Split by newlines to get each step line
        lines = str(description_text).split('\n')
        
        for line in lines:
            line = line.strip()
            # Skip header line and empty lines
            if not line or 'Step No' in line:
                continue
                
            # Split by pipe and extract step information
            if '|' in line:
                parts = [part.strip() for part in line.split('|') if part.strip()]
                
                # Expected format after splitting: ['Step-X', 'Action', 'Expected Result']
                if len(parts) >= 3:
                    step_num = parts[0]
                    action = parts[1]
                    result = parts[2]
                    
                    # Format for column B (Design Steps)
                    design_steps.append(f"{step_num}: {action}")
                    
                    # Format for column C (Expected Results)  
                    expected_results.append(f"{step_num}: {result}")
        
        # Join all steps with newlines
        design_steps_text = '\n'.join(design_steps)
        expected_results_text = '\n'.join(expected_results)
        
        return design_steps_text, expected_results_text
    
    def update_excel_columns(self) -> bool:
        """
        Update the Excel file by populating columns B and C based on Description column.
        
        Returns:
            bool: True if update was successful
        """
        try:
            print("\n🔄 Processing Excel File")
            print("=" * 60)
            
            # Load the workbook using openpyxl for better control
            wb = load_workbook(self.file_path)
            ws = wb[self.sheet_name]
            
            # Read the current data using pandas for easier manipulation
            df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            
            updates_made = 0
            
            # Process each row
            for idx, row in df.iterrows():
                description = row['Description']
                current_design_steps = row.get('Description (Design Steps)')
                current_expected_result = row.get('Description (Expected Result)')
                
                # Only update if columns B or C are empty (NaN)
                if pd.isna(current_design_steps) or pd.isna(current_expected_result):
                    print(f"\n📝 Processing Row {idx + 1}:")
                    
                    # Parse the description
                    design_steps, expected_results = self.parse_description_to_steps(description)
                    
                    if design_steps or expected_results:
                        # Update the Excel cells (using 1-based indexing for openpyxl)
                        excel_row = idx + 2  # +2 because Excel is 1-indexed and we have headers
                        
                        if pd.isna(current_design_steps) and design_steps:
                            ws.cell(row=excel_row, column=2, value=design_steps)  # Column B
                            print(f"  ✅ Updated Column B (Design Steps)")
                            print(f"     Content: {design_steps.replace(chr(10), ' | ')}")  # Show on one line
                        
                        if pd.isna(current_expected_result) and expected_results:
                            ws.cell(row=excel_row, column=3, value=expected_results)  # Column C
                            print(f"  ✅ Updated Column C (Expected Results)")
                            print(f"     Content: {expected_results.replace(chr(10), ' | ')}")  # Show on one line
                        
                        updates_made += 1
                    else:
                        print(f"  ⚠️  No valid steps found in description")
                else:
                    print(f"Row {idx + 1}: ✓ Already has data in columns B & C (skipped)")
            
            if updates_made > 0:
                # Save the workbook
                wb.save(self.file_path)
                print(f"\n✅ Excel file updated successfully!")
                print(f"   File: {self.file_path}")
                print(f"   Rows updated: {updates_made}")
            else:
                print(f"\n📋 No updates needed - all rows already have data in columns B & C")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating Excel file: {e}")
            return False
    
    def verify_results(self) -> bool:
        """
        Verify the results after processing.
        
        Returns:
            bool: True if verification was successful
        """
        try:
            print("\n🔍 Verifying Results")
            print("=" * 60)
            
            # Read the updated Excel file
            df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            
            print(f"Final data shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            
            print("\n📋 Final Results Summary:")
            print("-" * 40)
            
            for idx, row in df.iterrows():
                design_steps = row.get('Description (Design Steps)')
                expected_results = row.get('Description (Expected Result)')
                
                print(f"\nRow {idx + 1}:")
                if pd.notna(design_steps):
                    steps_preview = str(design_steps).replace('\n', ' | ')
                    print(f"  Column B: ✓ {steps_preview}")
                else:
                    print(f"  Column B: ✗ Empty")
                
                if pd.notna(expected_results):
                    results_preview = str(expected_results).replace('\n', ' | ')
                    print(f"  Column C: ✓ {results_preview}")
                else:
                    print(f"  Column C: ✗ Empty")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying results: {e}")
            return False
    
    def process(self, create_backup: bool = True) -> bool:
        """
        Main processing method that runs the complete workflow.
        
        Args:
            create_backup (bool): Whether to create a backup before processing
            
        Returns:
            bool: True if processing was successful
        """
        print("🚀 Excel Description Processor")
        print("=" * 60)
        print(f"File: {self.file_path}")
        print(f"Sheet: {self.sheet_name}")
        print("=" * 60)
        
        # Check if file exists
        if not os.path.exists(self.file_path):
            print(f"❌ Error: File '{self.file_path}' not found!")
            return False
        
        # Create backup if requested
        if create_backup:
            self.create_backup()
        
        # Step 1: Examine structure
        if not self.examine_excel_structure():
            return False
        
        # Step 2: Update columns
        if not self.update_excel_columns():
            return False
        
        # Step 3: Verify results
        if not self.verify_results():
            return False
        
        print("\n🎉 Processing completed successfully!")
        print("=" * 60)
        
        return True


def main():
    """Main function to run the Excel Description Processor."""
    
    # Use configuration variables from top of file, but allow command line override
    if len(sys.argv) > 1:
        file_path = sys.argv[1]  # Command line override
    else:
        file_path = EXCEL_FILE   # Use configuration variable
    
    if len(sys.argv) > 2:
        sheet_name = sys.argv[2] # Command line override
    else:
        sheet_name = SHEET_NAME  # Use configuration variable
    
    # Create processor instance
    processor = ExcelDescriptionProcessor(file_path, sheet_name)
    
    # Run the processing
    success = processor.process(create_backup=CREATE_BACKUP)
    
    if success:
        print("\n✅ All operations completed successfully!")
        print(f"📁 Updated file: {file_path}")
        if processor.backup_created:
            backup_path = f"{os.path.splitext(file_path)[0]}_backup.xlsx"
            print(f"💾 Backup available: {backup_path}")
    else:
        print("\n❌ Processing failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
