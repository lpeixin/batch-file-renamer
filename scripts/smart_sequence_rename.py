import os
import argparse
import re
import sys
from pathlib import Path

def parse_rule(rule):
    """
    Parses the rule string (e.g., "IMG_1020") into a prefix and a starting number.
    Returns: (prefix, start_number, padding_length)
    """
    match = re.search(r'^(.*?)(\d+)$', rule)
    if not match:
        raise ValueError("Rule must end with a number (e.g., IMG_1020)")
    
    prefix = match.group(1)
    number_str = match.group(2)
    return prefix, int(number_str), len(number_str)

def main():
    parser = argparse.ArgumentParser(description="Batch rename files based on a sequence rule.")
    parser.add_argument("rule", help="Naming rule with starting number (e.g., IMG_1020)")
    parser.add_argument("path", help="Target folder path")
    parser.add_argument("ext", help="Target file extension (e.g., jpg)")
    
    args = parser.parse_args()
    
    target_dir = Path(args.path)
    if not target_dir.exists():
        print(f"Error: Directory '{args.path}' not found.")
        sys.exit(1)
        
    try:
        prefix, start_num, num_padding = parse_rule(args.rule)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    # Normalize extension (ensure it starts with dot and is lowercase for comparison)
    target_ext = args.ext.lower()
    if not target_ext.startswith('.'):
        target_ext = '.' + target_ext
        
    # Gather all files with the matching extension
    # We use case-insensitive matching for extension
    all_files = []
    for f in target_dir.iterdir():
        if f.is_file() and f.suffix.lower() == target_ext:
            all_files.append(f)
    
    if not all_files:
        print(f"No files with extension '{target_ext}' found in '{args.path}'.")
        sys.exit(0)

    # Identify existing matches to avoid collisions
    # Pattern: ^prefix + digits + ext$
    # We escape the prefix and ext to handle special regex characters safely
    pattern_str = f"^{re.escape(prefix)}(\\d+){re.escape(target_ext)}$"
    pattern = re.compile(pattern_str, re.IGNORECASE)
    
    existing_numbers = set()
    files_to_rename = []
    
    for f in all_files:
        match = pattern.match(f.name)
        if match:
            # File already matches the naming convention
            num_part = match.group(1)
            existing_numbers.add(int(num_part))
        else:
            # File needs renaming
            files_to_rename.append(f)
            
    # Sort files to rename to ensure deterministic order (e.g., alphabetical)
    files_to_rename.sort(key=lambda x: x.name)
    
    current_num = start_num
    renamed_count = 0
    
    print(f"Found {len(files_to_rename)} files to rename.")
    print(f"Found {len(existing_numbers)} files already matching the pattern '{prefix}XXX{target_ext}'.")
    
    for f in files_to_rename:
        # Find the next available number
        while current_num in existing_numbers:
            current_num += 1
            
        # Format new name
        new_num_str = str(current_num).zfill(num_padding)
        new_name = f"{prefix}{new_num_str}{target_ext}"
        new_path = target_dir / new_name
        
        # Final safety check for existence (though existing_numbers should cover it)
        if new_path.exists():
             print(f"Warning: Target '{new_name}' already exists. Skipping '{f.name}'.")
             existing_numbers.add(current_num)
             continue

        try:
            f.rename(new_path)
            print(f"Renamed: {f.name} -> {new_name}")
            existing_numbers.add(current_num)
            renamed_count += 1
            # Prepare for next iteration
            current_num += 1
        except OSError as e:
            print(f"Error renaming {f.name}: {e}")
            
    print(f"Done. Successfully renamed {renamed_count} files.")

if __name__ == "__main__":
    main()
