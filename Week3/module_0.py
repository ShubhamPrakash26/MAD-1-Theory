import sys

arguments = sys.argv

courses = {'MAD 1': '1002', 'MAD-2': '2003', 'BDM': '205', 'SysCom': '304'}

def operate():
    arg_1 = arguments[1]
    arg_2 = courses[arg_1]
    return f"The function output is: {len(arg_1 + arg_2)}"

print(operate())