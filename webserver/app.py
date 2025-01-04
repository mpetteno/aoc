import functools
import logging
import subprocess
from pathlib import Path

from flask import Flask, request, jsonify

import webserver.runners as runners

app = Flask(__name__)

EXT_SOLVER_RUNNER_MAP = {
    "py": functools.partial(runners.python_runner, command="python"),
    "js": functools.partial(runners.generic_runner, command="node"),
    "ts": functools.partial(runners.generic_runner, command="ts-node"),
    "java": functools.partial(runners.java_runner, command="java"),
    "rs": functools.partial(runners.rust_runner, command="cargo run"),
    "cpp": functools.partial(runners.cpp_runner, command="g++"),
    "scala": functools.partial(runners.generic_runner, command="scala"),
    "kt": functools.partial(runners.generic_runner, command="kotlin"),
    "pl": functools.partial(runners.generic_runner, command="perl"),
    "lua": functools.partial(runners.generic_runner, command="lua"),
    "rb": functools.partial(runners.generic_runner, command="ruby"),
    "go": functools.partial(runners.generic_runner, command="go run"),
    "swift": functools.partial(runners.generic_runner, command="swift"),
    "m": functools.partial(runners.generic_runner, command="clang"),
}
AOC_EDITIONS_DIR = Path("../editions/")
AOC_SOLVERS_DIR = Path("../solvers/")
AVAILABLE_EDITIONS = list(d.name for d in AOC_EDITIONS_DIR.iterdir() if d.is_dir())


@app.route('/solve', methods=['POST'])
def solve():
    """
    Handles solving Advent of Code (AoC) challenges by executing the corresponding
    solution file based on the provided year, day, and part.

    Parameters (via JSON request payload):
    - year: The AoC edition year (must be a directory in `AOC_EDITIONS_DIR`).
    - day: The day of the challenge (must be between 1 and 25 and correspond to an available directory).
    - part: The part of the challenge to execute (must be either "1" or "2").
    - input_file: Input data passed to the solution script.

    Returns:
    - JSON response with the output of the executed solution file on success.
    - JSON error response with an appropriate status code on failure.
    """
    data = request.json

    # Get and validate parameters
    year = str(data.get("year"))
    if not (year.isdigit() and year in AVAILABLE_EDITIONS):
        return jsonify({"error": "The given edition year is not available."}), 400
    day = str(data.get("day"))
    if not (day.isdigit() and 1 <= int(day) <= 25 and (AOC_EDITIONS_DIR / year / f"day{day}").is_dir()):
        return jsonify({"error": "The given day is not available for the given edition year."}), 400
    solution_dir = AOC_EDITIONS_DIR / year / f"day{day}"
    part = str(data.get("part"))
    if not (part.isdigit() and part in ["1", "2"]):
        return jsonify({"error": "Part must be 1 or 2."}), 400

    # Locate the solution file and get the associated solver from its extension
    solution_files = [f for f in solution_dir.iterdir() if f.is_file() and f.name.startswith("solution")]
    if not solution_files or len(solution_files) > 1:
        return jsonify({"error": "Solution not found for given edition year and day."}), 404
    solution_file = solution_files[0]
    ext = solution_file.suffix[1:]
    if ext not in EXT_SOLVER_RUNNER_MAP:
        return jsonify({"error": f"Unsupported file extension: {ext}"}), 400
    runner = EXT_SOLVER_RUNNER_MAP[ext]
    solver_name = f"{ext}_solver.{ext}"
    solver = AOC_SOLVERS_DIR / solver_name

    # Run the solution
    input_file = data.get("input_file", "")
    try:
        result = runner(solver_path=solver, input_data=input_file, year=year, day=day, part=part)
        return jsonify({"output": result.stdout.strip()})
    except subprocess.CalledProcessError as e:
        logging.error(f"Command Execution Error: {e.stderr.strip()}")
        return jsonify({"error": "An internal error occurred while executing the solution."}), 500
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": "An internal server error occurred."}), 500


if __name__ == '__main__':
    app.run(debug=True)
