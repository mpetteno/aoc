"""
PART 2 Note
Here we need to make sure that the given input correctly implement the Full adder between two 45 bit number.

By using the following formula

Zn = (Xn ⊕ Yn) ⊕ Cn-1
Cn = (Xn * Yn) + (Cn-1 * (Xn ⊕ Yn)), with C0 = (Xn * Yn)

We can derive a series of rule.

1) AND (*):
    - AND gate can only be input to an OR gate
    - AND gate cannot take other AND gate as input
2) XOR (⊕):
    - XOR gate can only be input to an AND/XOR gate
    - XOR gate cannot take AND gate as input
3) OR (+):
    - OR gate can only be input of AND/XOR gate
    - OR gate can only take AND gate as input
4) (Xn ⊕ Yn) ⊕ (a + b) should always output a Zxx except for the last carry z45
5) A gate with Zxx as its output cannot directly use Xn or Yn as inputs.

Look for gates that does not follow those rules.
"""
from collections import defaultdict
from typing import Any

from solvers.python_solver import Solver

OP_MAP = {
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b
}


def run_circuit(init_state, operations):
    executed_operations = set()
    state = init_state.copy()
    while len(executed_operations) < len(operations):
        for operation in operations:
            if operation not in executed_operations:
                op_id, input_wire_a, input_wire_b, output_wire = operation
                input_wire_a_val = state[input_wire_a]
                input_wire_b_val = state[input_wire_b]
                if input_wire_a_val is None or input_wire_b_val is None:
                    continue
                state[output_wire] = OP_MAP[op_id](input_wire_a_val, input_wire_b_val)
                executed_operations.add(operation)
    return read_output(state)


def read_output(state):
    z_wires = [wire for wire in state.keys() if wire[0] == 'z']
    binary_output = "".join([str(state[z]) for z in list(sorted(z_wires, reverse=True))])
    decimal_output = int(binary_output, 2)
    return decimal_output


def validate_full_adder_circuit(operations, hsb_reg):
    usage = defaultdict(set)
    errors = []

    for (op_id, input_wire_a, input_wire_b, output_wire) in operations:
        usage[input_wire_a].add(op_id)
        usage[input_wire_b].add(op_id)

    for (operation_id, input_wire_a, input_wire_b, output_wire) in operations:
        input_wire_a_id, input_wire_b_id, output_wire_id = input_wire_a[0], input_wire_b[0], output_wire[0]

        # Special case for HSB
        if output_wire == hsb_reg:
            if input_wire_a_id in ["x", "y"] or input_wire_b_id in ["x", "y"] or operation_id != "OR":
                errors.append(output_wire)
            continue

        # Special case for LSB
        if output_wire == "z00":
            if sorted([input_wire_a, input_wire_b]) != ["x00", "y00"] or operation_id != "XOR":
                errors.append(output_wire)
            continue
        if input_wire_a in ["x00", "y00"] or input_wire_b in ["x00", "y00"]:
            if input_wire_a_id + input_wire_b_id in ["xy", "yx"] and operation_id not in ["XOR", "AND"]:
                errors.append(output_wire)
            continue

        # Validate rules for gate types
        if operation_id == "XOR":
            if input_wire_a_id in ["x", "y"]:
                if input_wire_b_id not in ["x", "y"]:
                    errors.append(output_wire)
                if output_wire_id == "z":
                    errors.append(output_wire)
                if "AND" not in usage[output_wire] or "XOR" not in usage[output_wire]:
                    errors.append(output_wire)
            elif output_wire_id != "z":
                errors.append(output_wire)
        elif operation_id == "OR":
            if input_wire_a_id in ["x", "y"] or input_wire_b_id in ["x", "y"] or output_wire_id == "z":
                errors.append(output_wire)
            if "AND" not in usage[output_wire] or "XOR" not in usage[output_wire]:
                errors.append(output_wire)
        elif operation_id == "AND":
            if input_wire_a_id in ["x", "y"]:
                if input_wire_a_id not in ["x", "y"]:
                    errors.append(output_wire)
            if "OR" not in usage[output_wire]:
                errors.append(output_wire)

    errors = sorted(list(set(errors)))
    assert len(errors) == 8, f"expected 8 values but got {len(errors)}"
    return errors


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        i = 0
        state = {}
        while lines[i] != "":
            wire_id, wire_value = lines[i].strip().split(": ")
            state[wire_id] = int(wire_value)
            i += 1
        operations = []
        for line in lines[i + 1:]:
            operation, output_wire = line.strip().split(" -> ")
            input_wire_a, operation_id, input_wire_b = operation.split(" ")
            operations.append((operation_id, input_wire_a, input_wire_b, output_wire))
            if input_wire_a not in state:
                state[input_wire_a] = None
            if input_wire_b not in state:
                state[input_wire_b] = None
            if output_wire not in state:
                state[output_wire] = None
        return state, operations

    def solve_first_part(self, parsed_input: Any) -> str:
        logic_state, logic_operations = parsed_input
        output = run_circuit(logic_state, logic_operations)
        return f'Z wires decimal output: {output}'

    def solve_second_part(self, parsed_input: Any) -> str:
        logic_state, logic_operations = parsed_input
        hsb_wire = list(sorted([wire for wire in logic_state.keys() if wire[0] == 'z']))[-1]
        wrong_wires = validate_full_adder_circuit(logic_operations, hsb_wire)
        return f'Wrong gates: {",".join(wrong_wires)}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
