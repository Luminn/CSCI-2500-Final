import forward_no_label
import input
import os
import sys

if len(sys.argv) != 3:
    print("Invalid Arguments.")

is_forwarding = True if sys.argv[1] == "F" else False
input_file = sys.argv[2]

