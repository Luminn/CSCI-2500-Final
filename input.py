import re

re_none = re.compile(r"^\s*$")
single_instruction = re.compile(r"^\s*([a-z]+)\s*$")
re_label = re.compile(r"^\s*([A-Za-z]\w+)\s*:(.*)")
re_standard = re.compile(r"\s*([a-z]+)\s*\$([a-z]\d)\s*,\s*\$([a-z]\d|zero)\s*,\s*[|$]([a-z]\d|-?\d+|zero)")
re_load_save = re.compile(r"\s*([a-z]+)\s*\$([a-z]\d)\s*,\s*(-?\d+)\s*\(\s*\$([a-z]\d|zero)\s*\)")
re_branch = re.compile(r"\s*([a-z]+)\s*\$([a-z]\d|zero)\s*,\s*[|$]([a-z]\d|-?\d+|zero)\s*,\s*([A-Za-z]\w+)")


def parse_line(line):
    label = None
    if re.match(re_none, line) is not None:
        return None
    if re.match(re_label, line) is not None:
        label = re.match(re_label, line).group(1)
        line = re.match(re_label, line).group(2)
    if re.match(re_standard, line) is not None:
        result = [re.match(re_standard, line).group(i) for i in range(1, 4)]
    elif re.match(re_load_save, line) is not None:
        result = [re.match(re_load_save, line).group() for i in range(1, 4)]
    elif re.match(re_branch, line) is not None:
        result = [re.match(re_branch, line).group() for i in range(1, 4)]
    else:
        result = None
    return result, label


def parse_file(file_name):
    result = []
    with open(file_name, "r") as file:
        data = file.read()
    for line in data:
        line_data = parse_line(line)
        if line_data is not None:
            if line_data[0] is None:
                raise ValueError("Invalid mips code.")
            result.append(result)


def jump_ref(parsed_data):
    ref_table = {}
    for i, v in enumerate(parsed_data):
        if parsed_data[1] is not None:
            ref_table[v] = i
    return ref_table




