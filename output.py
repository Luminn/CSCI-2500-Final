
def print_line_break():
    print("-" * 10)


def print_header():
    print("CPU Cycles ===>\t", end="")
    for i in range(1, 17):
        print("{}{}".format(i, "\t"if i != 16 else "\n"), end="")

