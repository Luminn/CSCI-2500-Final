class menv:
    def __init__(self):
        self.vars = {**{"s{}".format(i): 0 for i in range(8)}, **{"t{}".format(i): 0 for i in range(10)}}

    def __getitem__(self, item):
        if item == "zero":
            return 0
        if item not in self.vars:
            raise KeyError
        return self.vars[item]

    def __setitem__(self, key, value):
        if not isinstance(value, int):
            raise ValueError
        if key not in self.vars:
            raise KeyError
        self.vars[key] = value

    def __str__(self):
        result = ""
        line_count = 0
        for i in self.vars:
            line_count += 1
            temp = "${} = {}".format(i, self.vars[i])
            result += temp + (" " * (20 - len(temp)) if line_count % 4 != 0 else "\n")
        return result


def apply_instruction(inst, env):
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
        env[inst[1]] = env[inst[2]] << env[inst[3]]
    elif inst[0] == "slti":
        env[inst[1]] = env[inst[2]] << int(inst[3])
