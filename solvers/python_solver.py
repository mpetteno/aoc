import argparse
import sys
import time
import logging
import importlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable


def timed_execution(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        execution_time = end - start
        execution_time_ms = execution_time * 1000
        logging.info(f"Execution Time: {execution_time_ms:.9f} ms")
        return result
    return wrapper


class Solver(ABC):

    def __init__(self, input_data: str = None):
        logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
        if input_data is not None:
            self.input_data = input_data
        else:
            with open("input.txt", 'r') as file:
                self.input_data = file.read()

    @abstractmethod
    def parse_input(self) -> Any:
        pass

    @abstractmethod
    def solve_first_part(self, parsed_input: Any) -> str:
        pass

    @abstractmethod
    def solve_second_part(self, parsed_input: Any) -> str:
        pass

    @timed_execution
    def timed_first_part_solution(self, parsed_input: Any) -> str:
        return self.solve_first_part(parsed_input)

    @timed_execution
    def timed_second_part_solution(self, parsed_input: Any) -> str:
        return self.solve_second_part(parsed_input)

    def run(self, part: int = None) -> None:
        parsed_input = self.parse_input()
        if part == 1:
            logging.info("------------- Part 1 -------------")
            output_message = self.timed_first_part_solution(parsed_input)
            logging.info(output_message)
        elif part == 2:
            logging.info("------------- Part 2 -------------")
            output_message = self.timed_second_part_solution(parsed_input)
            logging.info(output_message)
        elif part is None:
            logging.info("------------- Part 1 -------------")
            output_message = self.timed_first_part_solution(parsed_input)
            logging.info(output_message)
            logging.info("------------- Part 2 -------------")
            output_message = self.timed_second_part_solution(parsed_input)
            logging.info(output_message)
        else:
            raise ValueError("Invalid part specified. Use 1, 2, or leave empty for both parts.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AoC Python Solution Runner")
    parser.add_argument("year", type=int, help="The year of the AoC edition.")
    parser.add_argument("day", type=int, help="The day of the AoC challenge.")
    parser.add_argument("input_file", type=str, help="Content of the input file.", required=False)
    parser.add_argument("part", type=int, choices=[1, 2], required=False,
                        help="Specify the part to run (1 or 2). Run both parts if omitted.")
    vargs = parser.parse_args()
    # Dynamically load the day's solution module
    try:
        module_path = Path("../editions") / str(vargs.year) / f"day{vargs.day}" / "solution.py"
        module = importlib.import_module(module_path)
        solution_class = getattr(module, "Solution")
    except (ModuleNotFoundError, AttributeError):
        logging.error(f"Error: Solution for Day {vargs.day} not found.")
        sys.exit(1)
    # Create the solver and run
    solver = solution_class(input_data=vargs.input_file)
    solver.run(part=vargs.part)
