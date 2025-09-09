# Bril Control Flow Graph Builder

## Overview
This tool constructs basic blocks and builds control flow graphs from Bril JSON programs using an object-oriented design with dataclasses.

## Input
- **File Format**: Bril JSON format
- **Content**: Standard Bril program with instructions and labels

## Output
1. **Basic Blocks**: List of blocks with their instructions
2. **Control Flow Graph**: Block names and their successors

## Usage
```bash
python3 cfg_builder.py <bril_json_file>
```

## Example
```bash
python3 cfg_builder.py test/add.json
```

### Sample Output
```
Basic Blocks:
========================================

Block 'b1':
  v0 = const 1
  v1 = const 2
  v2 = add v0 v1
  print v2
  ret

Control Flow Graph (main):
========================================
b1 -> exit
```

## Algorithm
1. **Block Construction**: Identifies leaders (first instructions of blocks) and forms blocks
2. **CFG Building**: Adds terminators for fall-through and creates edges based on jumps/branches

## Testing
Run tests with:
```bash
cd test && turnt *.json
```