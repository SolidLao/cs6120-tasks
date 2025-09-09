#!/usr/bin/env python3
"""
Bril Instruction Distribution Analyzer

Analyzes Bril JSON programs and reports instruction frequency distribution.
"""

import json
import sys
from collections import Counter


def analyze_instruction_distribution(bril_program):
    """Count frequency of each instruction type in the Bril program."""
    instruction_counter = Counter()
    
    for function in bril_program.get("functions", []):
        for instruction in function.get("instrs", []):
            op = instruction.get("op")
            if op:
                instruction_counter[op] += 1
    
    return instruction_counter


def print_instruction_distribution(counter, total_instructions):
    """Print formatted instruction distribution results."""
    print("Instruction Distribution Analysis")
    print("=" * 40)
    print(f"Total instructions: {total_instructions}")
    print("-" * 40)
    
    # Sort by frequency (descending) then by name
    sorted_instructions = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    
    for instruction, count in sorted_instructions:
        percentage = (count / total_instructions) * 100 if total_instructions > 0 else 0
        print(f"{instruction:12} | {count:4} | {percentage:6.2f}%")


def main():
    if len(sys.argv) != 2:
        print("Usage: python instruction_analyzer.py <bril_json_file>", file=sys.stderr)
        print("Example: python instruction_analyzer.py test/add.json", file=sys.stderr)
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    try:
        with open(json_file, 'r') as f:
            bril_program = json.load(f)
        
        instruction_counter = analyze_instruction_distribution(bril_program)
        total_instructions = sum(instruction_counter.values())
        
        print_instruction_distribution(instruction_counter, total_instructions)
        
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{json_file}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()