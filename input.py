import re

re_none = re.compile(r"^\s*$")
single_instruction = re.compile(r"^\s*([a-z]+)\s*$")
re_label = re.compile(r"^\s*([A-Za-z]\w+)\s*:(.*)")
re_standard = re.compile(r"\s*([a-z]+)\s*\$([a-z]\d)\s*,\s*\$([a-z]\d|zero)\s*,\s*\$?([a-z]\d|-?\d+|zero)")
re_load_save = re.compile(r"\s*([a-z]+)\s*\$([a-z]\d)\s*,\s*(-?\d+)\s*\(\s*\$([a-z]\d|zero)\s*\)")
re_branch = re.compile(r"\s*([a-z]+)\s*\$([a-z]\d|zero)\s*,\s*[|$]([a-z]\d|-?\d+|zero)\s*,\s*([A-Za-z]\w+)")
re_invalid_var_num = re.compile(r"\$\d")

VALID_COMMANDS = {"add", "addi", "and", "andi", "or", "ori", "slt", "slti", "beq", "bne"}


class MipsError(BaseException):
    pass


def parse_line(line):
    label = None
    if re.match(re_none, line) is not None:
        return None, None
    if re.search(re_invalid_var_num, line):
        raise MipsError("Unknown Syntax: $number")
    if re.match(re_label, line) is not None:
        label = re.match(re_label, line).group(1)
        line = re.match(re_label, line).group(2)
        if re.match(re_none, line):
            return None, label
    if re.match(re_standard, line) is not None:
        result = [re.match(re_standard, line).group(i) for i in range(1, 5)]
    elif re.match(re_load_save, line) is not None:
        result = [re.match(re_load_save, line).group(i) for i in range(1, 5)]
    elif re.match(re_branch, line) is not None:
        result = [re.match(re_branch, line).group(i) for i in range(1, 5)]
    else:
        raise MipsError("Unknown Syntax.")
    return result, label


def jump_ref(parsed_data):
    ref_table = {}
    for i, v in enumerate(parsed_data):
        if v[1] is not None:
            ref_table[v[1]] = i
    return ref_table


def parse_file(file_name):
    result1 = []
    with open(file_name, "r") as file:
        data = file.read()
    last_label = None
    for line in data.split('\n'):
        line_data = parse_line(line)
        if line_data[0] is not None:
            if line_data[1] is None and last_label is not None:
                line_data = line_data[0], last_label
            result1.append(line_data)
            last_label = None
        elif line_data[0] is None and line_data[1] is not None:
            last_label = line_data[1]
    refs = jump_ref(result1)
    result = []
    for i, v in enumerate(result1):
        if v[0][0] in ("beq", "bne"):
            result.append([v[0][0], v[0][1], v[0][2], str(refs[v[0][3]])])
        else:
            result.append(v[0])
    return result


def is_var(item):
    return item[0].isalpha()


def list_labels(parsed_data):
    result = []
    for i, v in enumerate(parsed_data):
        if v[0] in ("beq", "bne"):
            result.append([i, int(v[3])])
    return result


a = parse_file("test.s")
print(list_labels(a))