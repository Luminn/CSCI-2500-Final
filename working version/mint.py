"""
This module provides the functions of a simple MIPS interpreter, allowing the user to execute mips instructions and
store register values.
"""


class menv:
    """MIPS environment, representing all mips registers"""

    def __init__(self):
        self.vars = {**{"s{}".format(i): 0 for i in range(8)}, **{"t{}".format(i): 0 for i in range(10)}}

    def __getitem__(self, item):
        """dict styled access to the mips registers"""
        try:
            return int(item)
        except ValueError:
            pass
        if item == "zero":
            return 0
        if item not in self.vars:
            raise KeyError
        return self.vars[item]

    def __setitem__(self, key, value):
        """dict styled access to the mips registers"""
        if not isinstance(value, int):
            raise ValueError
        if key not in self.vars:
            raise KeyError
        self.vars[key] = value

    def __str__(self):
        """Convert the data into output"""
        result = ""
        line_count = 0
        for i in self.vars:
            line_count += 1
            temp = "${} = {}".format(i, self.vars[i])
            result += temp + (" " * (20 - len(temp)) if line_count % 4 != 0 else "\n")
        return result.rstrip()


def apply_instruction(inst, env):
    """Apply a formatted mips instruction to a MIPS environment."""
    if inst[0] == "add":
        env[inst[1]] = env[inst[2]] + env[inst[3]]
    elif inst[0] == "addi":
        env[inst[1]] = env[inst[2]] + int(inst[3])
    elif inst[0] == "and":
        env[inst[1]] = env[inst[2]] & env[inst[3]]
    elif inst[0] == "andi":
        env[inst[1]] = env[inst[2]] & int(inst[3])
    elif inst[0] == "or":
        env[inst[1]] = env[inst[2]] | env[inst[3]]
    elif inst[0] == "ori":
        env[inst[1]] = env[inst[2]] | int(inst[3])
    elif inst[0] == "slt":
        env[inst[1]] = 1 if env[inst[2]] < env[inst[3]] else 0
    elif inst[0] == "slti":
        env[inst[1]] = 1 if env[inst[2]] < int(inst[3]) else 0