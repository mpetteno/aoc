import re

if __name__ == '__main__':
    with open("input.txt") as f:
        program = f.read()
        # Part 1
        mul_factors = re.findall(r"mul\((\d+),(\d+)\)", program)
        result = 0
        for x, y in mul_factors:
            result += int(x) * int(y)
        print(f'(Part 1) Multiplication result is {result}')
        # Part 2
        # Use re.DOTALL to match newline characters too
        enabled_ops = re.findall(r"do\(\)(.*?)don't\(\)", program, re.DOTALL)
        enabled_ops.append(program[:min(program.index("don't()"), program.index("do()"))])
        result = 0
        for p in enabled_ops:
            enabled_mul_factors = re.findall(r"mul\((\d+),(\d+)\)", p)
            for x, y in enabled_mul_factors:
                result += int(x) * int(y)
        print(f'(Part 2) Multiplication result is {result}')
