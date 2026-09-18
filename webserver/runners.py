from pathlib import Path
import subprocess


def generic_runner(command: str, solver_path: Path, input_data: str, year: str, day: str, part: str):
    return subprocess.run(
        [command, str(solver_path), year, day, part],
        cwd=solver_path.resolve().parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )


def python_runner(command: str, solver_path: Path, input_data: str, year: str, day: str, part: str):
    return subprocess.run(
        [command, str(solver_path), "--year", year, "--day", day, "--part", part],
        cwd=solver_path.resolve().parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )


def java_runner(command: str, solver_path: Path, input_data: str, year: str, day: str, part: str):
    subprocess.run(["javac", str(solver_path)], check=True)
    return subprocess.run(
        [command, solver_path.suffix[:-5], year, day, part],
        cwd=solver_path.resolve().parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )


def cpp_runner(command: str, solver_path: Path, input_data: str, year: str, day: str, part: str):
    executable = str(solver_path.with_suffix(".out"))
    subprocess.run([command, str(solver_path), "-o", executable], check=True)
    return subprocess.run(
        [executable, year, day, part],
        cwd=solver_path.resolve().parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )


def rust_runner(command: str, solver_path: Path, input_data: str, year: str, day: str, part: str):
    return subprocess.run(
        [command, "--", year, day, part],
        cwd=solver_path.resolve().parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )


def kotlin_runner(command: str, solver_path: Path, input_data: str, year: str, day: str, part: str):
    jar_path = solver_path.resolve().parent.parent / "build" / "libs" / "aoc-solver.jar"
    if not jar_path.is_file():
        raise FileNotFoundError(
            f"Kotlin solver jar not found at {jar_path}. Run './gradlew shadowJar' first."
        )
    return subprocess.run(
        [command, "-jar", str(jar_path), "--year", year, "--day", day, "--part", part],
        cwd=jar_path.parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True,
    )
