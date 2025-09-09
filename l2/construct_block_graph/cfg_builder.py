import json
import sys
from dataclasses import dataclass
from typing import List, Dict, Set

TERMINATORS = {"br", "jmp", "ret"}

@dataclass
class BasicBlock:
    name: str
    instructions: List[dict]
    successors: Set[str]
    
    def __post_init__(self):
        self.successors = set()
    
    def add_successor(self, block_name: str):
        self.successors.add(block_name)

class CFGBuilder:
    def __init__(self, instrs: List[dict]):
        self.instructions = instrs
        self.blocks: Dict[str, BasicBlock] = {}
        self.block_counter = 1
        
    def build(self):
        self._form_blocks()
        self._add_terminators()
        self._build_cfg()
        return self.blocks
    
    def _form_blocks(self):
        current_block = []
        
        for instr in self.instructions:
            if "op" in instr:
                current_block.append(instr)
                if instr["op"] in TERMINATORS:
                    self._create_block(current_block)
                    current_block = []
            else:  # label
                if current_block:
                    self._create_block(current_block)
                current_block = [instr]
        
        if current_block:
            self._create_block(current_block)
    
    def _create_block(self, instrs: List[dict]):
        if "label" in instrs[0]:
            name = instrs[0]["label"]
            content = instrs[1:]
        else:
            name = f"b{self.block_counter}"
            self.block_counter += 1
            content = instrs
        
        self.blocks[name] = BasicBlock(name, content, set())
    
    def _add_terminators(self):
        block_names = list(self.blocks.keys())
        
        for i, block in enumerate(self.blocks.values()):
            if not block.instructions or block.instructions[-1]["op"] not in TERMINATORS:
                if i == len(block_names) - 1:
                    block.instructions.append({"op": "ret", "args": []})
                else:
                    next_block = block_names[i + 1]
                    block.instructions.append({"op": "jmp", "labels": [next_block]})
    
    def _build_cfg(self):
        for block in self.blocks.values():
            if block.instructions:
                last_instr = block.instructions[-1]
                if last_instr["op"] in ("jmp", "br"):
                    for label in last_instr["labels"]:
                        block.add_successor(label)
                elif last_instr["op"] == "ret":
                    block.add_successor("exit")

def format_instruction(instr):
    op = instr["op"]
    
    if op == "const":
        return f"{instr['dest']} = const {instr['value']}"
    elif op in ("add", "sub", "mul", "div"):
        args = " ".join(instr["args"])
        return f"{instr['dest']} = {op} {args}"
    elif op == "print":
        return f"print {' '.join(instr['args'])}"
    elif op == "ret":
        if "args" in instr and instr["args"]:
            return f"ret {' '.join(instr['args'])}"
        return "ret"
    elif op == "jmp":
        return f"jmp {instr['labels'][0]}"
    elif op == "br":
        return f"br {instr['args'][0]} {instr['labels'][0]} {instr['labels'][1]}"
    else:
        return op

def main():
    if len(sys.argv) != 2:
        print("Usage: python cfg_builder.py <bril_json_file>", file=sys.stderr)
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        prog = json.load(f)
    
    func = prog["functions"][0]
    builder = CFGBuilder(func["instrs"])
    blocks = builder.build()
    
    print("Basic Blocks:")
    print("=" * 40)
    print()
    
    for block in blocks.values():
        print(f"Block '{block.name}':")
        for instr in block.instructions:
            print(f"  {format_instruction(instr)}")
        print()
    
    print(f"Control Flow Graph ({func['name']}):")
    print("=" * 40)
    for block in blocks.values():
        for successor in sorted(block.successors):
            print(f"{block.name} -> {successor}")

if __name__ == "__main__":
    main()