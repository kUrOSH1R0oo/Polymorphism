"""
Polymorphic Code Implementation in Python
Author: Ivan/KuroSh1r0

This project demonstrates the implementation of polymorphic self-modifying code in Python. 
The script modifies its own source code on each execution, introducing random variations while preserving its core functionality. 
The purpose of this implementation is to explore techniques used in obfuscation, anti-analysis, and 
dynamic code mutation, commonly seen in malware evasion strategies.
"""

import os
import random
import string
import re
import sys

def transform_source(source):
    # Apply polymorphic changes to the source code.
    def rename_functions(match):
        old_name = match.group(1)
        first_char = random.choice(string.ascii_letters)
        rest_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        new_name = first_char + rest_chars
        return f"def {new_name}("
    # Rename the dummy function
    new_source = re.sub(r'def (\w+)\(', rename_functions, source)
    # Split into lines and add junk code carefully
    lines = new_source.split('\n')
    new_lines = []  # Remove gibberish header
    in_function = False  # Track if we're inside a function body
    
    for line in lines:
        stripped_line = line.strip()
        
        # Detect function start
        if stripped_line.startswith('def '):
            new_lines.append(line)
            in_function = True
            continue
        
        # Skip adding junk right after def unless indented
        if in_function and not stripped_line:  # Empty line after def
            new_lines.append(line)
            continue
        elif in_function and stripped_line and not line.startswith(' '):  # End of function scope
            in_function = False

        # Add junk code only outside function starts or in indented blocks
        if random.random() > 0.7 and not stripped_line.startswith('def '):
            junk_var = 'x' + ''.join(random.choices(string.ascii_letters, k=random.randint(8, 16)))
            junk_value = '"' + ''.join(random.choices(string.ascii_letters, k=random.randint(5, 12))) + '"'
            junk = f"{junk_var} = {junk_value}"
            # Match indentation of current line if it’s indented
            indent = ' ' * (len(line) - len(stripped_line))
            new_lines.append(indent + junk)
        new_lines.append(line)
    return '\n'.join(new_lines)

# Sample Functions for renaming
def pixieeee():
    print("She so pretty!!!")
    
def pixxxx():
    print("She so pretty with her braces!!!")
    
def pixieeeeeeeee():
    print("She was in the same group as me earlier! She's so beautiful!!!!!")

# Recursions
if 'RUN_COUNT' not in os.environ:
    os.environ['RUN_COUNT'] = '0'
count = int(os.environ['RUN_COUNT'])
if count >= 10:
    sys.exit(0)

# Self-modify
with open(__file__, 'r') as f:
    source = f.read()

# Preserve the transform_source function in the new source
transform_source_def = re.search(r'def transform_source\(.*?\):.*?(?=\n\S|\Z)', source, re.DOTALL).group()
new_source = transform_source(source.replace(transform_source_def, ''))  # Remove the original definition
new_source = transform_source_def + '\n' + new_source  # Add it back at the top

# Generate a filename for each iteration
new_filename = f"polymorphic_{count}.py"
with open(new_filename, 'w') as f:
    f.write(new_source)

print(f"New version created as '{new_filename}'. Running it...")

os.environ['RUN_COUNT'] = str(count + 1)
os.system(f"python3 {new_filename}")
