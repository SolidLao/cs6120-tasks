# Bril Instruction Distribution Analyzer

## Overview
This tool analyzes Bril JSON programs and reports the frequency distribution of instructions used in the program.

## Input
- **File Format**: Bril JSON format (e.g., `add.json`)
- **Content**: Standard Bril program represented as JSON with functions and instructions

## Function
The analyzer:
1. Parses the Bril JSON program
2. Counts the frequency of each instruction type (`op` field)
3. Calculates percentages and sorts results by frequency

## Output
Formatted table showing:
- Total number of instructions
- Each instruction type with count and percentage
- Results sorted by frequency (descending), then alphabetically

## Usage
```bash
python instruction_analyzer.py <bril_json_file>
```

## Example
```bash
python instruction_analyzer.py add.json
```

### Sample Output
```
Instruction Distribution Analysis
========================================
Total instructions: 4
----------------------------------------
const        |    2 |  50.00%
add          |    1 |  25.00%
print        |    1 |  25.00%
```