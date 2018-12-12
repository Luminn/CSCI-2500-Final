"""
This module provides the input of the program. Provides parsing of mips code.
"""

import re

"""Regex representing various MIPS commands"""
re_none = re.compile(r"^\s*$")
single_instruction = re.compile(r"^\s*([a-z]+)\s*$")
re_label = re.compile(r"^\s*([A-Za-z]\w+)\s*:(.*)")
re_standard = re.compile(r"\s*([a-z]+)\s*\$([a-z]\d)\s*,\s*\$([a-z]\d|zero)\s*,\s*\$?([a-z]\d|-?\d+|zero)")
re_load_save = re.compile(r"\s*([a-z]+)\s*\$([a-z]\d)\s*,\s*(-?\d+)\s*\(\s*\$([a-z]\d|zero)\s*\)")
re_branch = re.compile(r"\s*([a-z]+)\s*\$?([a-z]\d|-?\d+|zero)\s*,\s*\$?([a-z]\d|-?\d+|zero)\s*,\s*([A-Za-z]\w*)")
re_invalid_var_num = re.compile(r"\$\d")

"""Commands supported by this project."""
VALID_COMMANDS = {"add", "addi", "and", "andi", "or", "ori", "slt", "slti", "beq", "bne"}


class MipsError(BaseException):
    """An error class representing MIPS syntax error."""
    pass


def parse_line(line):
    """Parse a line of mips code into separate arguments."""
    label = None
    # match the empty line case
    if re.match(re_none, line) is not None:
        return None, None
    # match syntax like $10 that can bypass regex check
    if re.search(re_invalid_var_num, line):
        raise MipsError("Unknown Syntax: $number")
    # match and remove labels from the string
    if re.match(re_label, line) is not None:
        label = re.match(re_label, line).group(1)
        line = re.match(re_label, line).group(2)
        # terminate if only a label is found
        if re.match(re_none, line):
            return None, label
    # match the standard instructions
    if re.match(re_standard, line) is not None:
        result = [re.match(re_standard, line).group(i) for i in range(1, 5)]
    # match the syntax of lw and sw
    elif re.match(re_load_save, line) is not None:
        result = [re.match(re_load_save, line).group(i) for i in range(1, 5)]
    # match the syntax of branch instructions
    elif re.match(re_branch, line) is not None:
        result = [re.match(re_branch, line).group(i) for i in range(1, 5)]
    # invalid syntax
    else:
        raise MipsError("Unknown Syntax.")
    return result, label


def jump_ref(parsed_data):
    """Returns a reference table of labels and their location in the list."""
    ref_table = {}
    for i, v in enumerate(parsed_data):
        if v[1] is not None:
            ref_table[v[1]] = i
    return ref_table


def translation_dict(parsed_data):
    """Returns a reference table of labels and their location in the list."""
    ref_table = {}
    for i, v in enumerate(parsed_data):
        if v[1] is not None:
            ref_table[i] = v[1]
    return ref_table


def parse_file(file_name):
    """Parse a file containing mips code."""
    result1 = []
    with open(file_name, "r") as file:
        data = file.read()
    last_label = None
    for line in data.split('\n'):
        line_data = parse_line(line)
        # remove lines containing only a label and apply the label to subsequent lines.
        if line_data[0] is not None:
            if line_data[1] is None and last_label is not None:
                line_data = line_data[0], last_label
            result1.append(line_data)
            last_label = None
        elif line_data[0] is None and line_data[1] is not None:
            last_label = line_data[1]
    # convert jump labels to line numbers
    refs = jump_ref(result1)
    result = []
    for i, v in enumerate(result1):
        if v[0][0] in ("beq", "bne"):
            result.append([v[0][0], v[0][1], v[0][2], str(refs[v[0][3]])])
        else:
            result.append(v[0])
    translation = translation_dict(result1)
    return result, translation


def is_var(item):
    """Returns true a string represents a variable."""
    return item[0].isalpha()


def list_labels(parsed_data):
    """Get a list of all possible jumps from the instructions"""
    result = []
    for i, v in enumerate(parsed_data):
        if v[0] in ("beq", "bne"):
            result.append([i, int(v[3])])
    return result


def item_to_string(item):
    if is_var(item):
        return "$" + item
    else:
        return item


def instruction_to_string(instruction):
    result = ""
    result += instruction[0] + " " + item_to_string(instruction[1]) + "," + item_to_string(instruction[2])
    if instruction[0] in ("lw", "sw"):
        result += "(" + item_to_string(instruction[3]) + ")"
    else:
        result += "," + item_to_string(instruction[3])
    return result