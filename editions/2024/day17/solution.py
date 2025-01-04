

def parse_input():
    lines = open("input.txt").readlines()
    REGISTERS["A"] = int(lines[0].split(" ")[-1])
    REGISTERS["B"] = int(lines[1].split(" ")[-1])
    REGISTERS["C"] = int(lines[2].split(" ")[-1])
    p = lines[-1].split(" ")[-1].split(",")
    opcodes = p[0::2]
    operands = p[1::2]
    return p, list(zip(opcodes, operands))


def read_combo_operator(combo_op):
    if combo_op in [0, 1, 2, 3]:
        return combo_op
    if combo_op == 4:
        return REGISTERS["A"]
    if combo_op == 5:
        return REGISTERS["B"]
    if combo_op == 6:
        return REGISTERS["C"]
    if combo_op == 7:
        raise ValueError("Combo operator 7 is reserved and should not apper in valid programs.")


def division(inst_pointer, combo_op, output_register):
    numerator = REGISTERS["A"]
    denominator = 2**read_combo_operator(combo_op)
    result = numerator // denominator
    REGISTERS[output_register] = result
    return inst_pointer + 1, None


def adv(inst_pointer, combo_op):
    return division(inst_pointer, combo_op, "A")


def bxl(inst_pointer, literal_op):
    b = REGISTERS["B"]
    result = b ^ literal_op
    REGISTERS["B"] = result
    return inst_pointer + 1, None


def bst(inst_pointer, combo_op):
    result = read_combo_operator(combo_op) % 8
    REGISTERS["B"] = result
    return inst_pointer + 1, None


def jnz(inst_pointer, literal_op):
    a = REGISTERS["A"]
    if a != 0:
        return literal_op, None
    return inst_pointer + 1, None


def bxc(inst_pointer, _):
    b = REGISTERS["B"]
    result = b ^ REGISTERS["C"]
    REGISTERS["B"] = result
    return inst_pointer + 1, None


def out(inst_pointer, combo_op):
    result = read_combo_operator(combo_op) % 8
    return inst_pointer + 1, result


def bdv(inst_pointer, combo_op):
    return division(inst_pointer, combo_op, "B")


def cdv(inst_pointer, combo_op):
    return division(inst_pointer, combo_op, "C")


REGISTERS = {
    "A": 0,
    "B": 0,
    "C": 0
}

INSTRUCTIONS_SET = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}


def run_program(program):
    inst_pointer = 0
    run_output = []
    while inst_pointer < len(program):
        opcode, operand = parsed_program[inst_pointer]
        inst_pointer, result = INSTRUCTIONS_SET[int(opcode)](inst_pointer, int(operand))
        if result is not None:
            run_output.append(str(result))
    return run_output


if __name__ == "__main__":
    original_program, parsed_program = parse_input()
    output = run_program(parsed_program)
    print(f'(Part 1) Output: {",".join(output)}')
    A = 0
    j = 1
    istart = 0
    while 0 <= j <= len(original_program):
        A <<= 3
        for i in range(istart, 8):
            REGISTERS["A"] = A + i
            output = run_program(parsed_program)
            if original_program[-j:] == output:
                break
        else:
            j -= 1
            A >>= 3
            istart = A % 8 + 1
            A >>= 3
            continue
        j += 1
        A += i
        istart = 0
    print(f'(Part 2) Minimum register A value for copy output: {A}')
