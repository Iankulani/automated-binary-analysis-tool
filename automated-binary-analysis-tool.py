# -*- coding: utf-8 -*-
"""
Created on Thurs Jan  1 11:42:47 2025

@author: IAN CARTER KULANI
"""
from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("BINARY TOOL")
print(Fore.GREEN+font)

import re

# Function to read the assembly file
def read_file(file_path):
    """Reads the content of an assembly file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

# Function to save the modified assembly code to a file
def save_file(file_path, content):
    """Saves the modified assembly content to a new file."""
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"File saved as {file_path}")

# Function to analyze and fix common issues in the assembly code
def analyze_and_fix(code):
    """Analyze and fix common assembly code issues."""
    
    fixes = []

    # Example 1: Check for 'MOV' to 'LOAD' replacement (this is just an example fix)
    # Some systems might use 'MOV' for moving data, but we might want to replace it for compatibility or standards.
    if "MOV" in code:
        code = code.replace("MOV", "LOAD")
        fixes.append("Replaced 'MOV' with 'LOAD' for standardization.")
    
    # Example 2: Check for missing labels (e.g., missing 'LABEL' before jumps)
    # We will assume that jumps (like 'JMP') should always be preceded by a label.
    missing_labels = re.findall(r'\bJMP\b(?!\s+[A-Za-z_][A-Za-z0-9_]*)', code)
    if missing_labels:
        for _ in missing_labels:
            code = code.replace("JMP", "JMP DEFAULT_LABEL")  # Add a default label for simplicity
        fixes.append("Added default labels for 'JMP' statements.")
    
    # Example 3: Fixing redundant instructions (e.g., 'NOP' instructions)
    code = re.sub(r'\bNOP\s*\n', '', code)  # Remove redundant NOPs
    if "NOP" in code:
        fixes.append("Removed redundant 'NOP' instructions.")
    
    # Example 4: Replace hardcoded values with registers (e.g., 'MOV AX, 0' -> 'MOV AX, [REGISTER]')
    if re.search(r'MOV\s+[A-Za-z]+\s*,\s*\d+', code):
        code = re.sub(r'MOV\s+([A-Za-z]+)\s*,\s*(\d+)', r'MOV \1, [REGISTER]', code)
        fixes.append("Replaced hardcoded values with register references.")
    
    # Example 5: Ensure correct register use (e.g., using AX where BX is used incorrectly)
    if re.search(r'\bBX\b', code):
        code = code.replace("BX", "AX")
        fixes.append("Replaced 'BX' with 'AX' for consistency.")
    
    return code, fixes

# Function to prompt user for file path, read file, analyze, fix, and save
def main():
    print("Welcome to the Automated Binary Analysis Tool!")

    # Prompt user for the path to the assembly file
    file_path = input("Enter the path to the assembly file:").strip()

    # Read the file content
    code = read_file(file_path)
    
    if code:
        # Analyze and fix the assembly code
        modified_code, fixes = analyze_and_fix(code)
        
        # Show the applied fixes to the user
        if fixes:
            print("\nApplied fixes:")
            for fix in fixes:
                print(f"- {fix}")
        else:
            print("\nNo fixes applied. The code appears to be fine.")
        
        # Prompt the user for the path to save the modified file
        save_path = input("Enter the path to save the modified file: ").strip()
        save_file(save_path, modified_code)

if __name__ == "__main__":
    main()
