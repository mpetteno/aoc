"""
This module, `runners.py`, provides utility functions to execute solutions written in various programming languages.

The primary purpose of this module is to facilitate the execution of external programs or scripts
by wrapping their invocation logic within Python functions. It supports the following types of solutions:
- Generic commands: Using `generic_runner` for general-purpose command-line executions.
- Java solutions: Managed by `java_runner`, which handles compilation and execution of Java programs.
- C++ solutions: Handled by `cpp_runner`, which compiles and then executes C++ source files.
- Rust solutions: Executed using `rust_runner`, designed for Rust binaries.

Each runner function is designed to:
1. Receive the solution file path, input data, and task part identifier.
2. Compile or prepare the solution (if required).
3. Execute the solution with specified inputs and return the resulting process output as a CompletedProcess object.

Dependencies:
- Python `subprocess` module: Used for executing commands and capturing outputs.
- Python `pathlib.Path` class: Handles file paths in a cross-platform manner.
"""
from pathlib import Path
import subprocess


def generic_runner(command: str, solution_path: Path, input_data: str, part: str):
    """
    Executes a subprocess to run a specified command with provided parameters and input data.

    This function facilitates the execution of an external command-line program by running
    it as a subprocess. It passes the necessary command, the path to the solution,
    the input data, and the part to execute. This utility is useful for executing
    external scripts, binaries, or any solution needing specific arguments and an input
    data stream.

    :param command: The executable command that needs to be run as a subprocess.
    :param solution_path: The file path to the solution or script to be used for the command.
    :param input_data: The input data to be fed to the subprocess as a standard input stream.
    :param part: Indicates the type of execution or a specific task/part that the solution should process.
    :return: A CompletedProcess instance containing the results of the subprocess execution.
    """
    return subprocess.run(
        [command, str(solution_path), part],
        cwd=solution_path.parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )


def java_runner(command: str, solution_path: Path, input_data: str, part: str):
    """
    Executes a Java solution for a given input and command by compiling and running the Java code in
    a specified file path. The function first compiles the Java program and then runs the generated 
    class file with the provided parameters. It is designed to handle input data, specific solution 
    paths, and processing based on the specified "part" of the task.

    :param command: Command to run the Java program, typically the `java` executable.
    :param solution_path: File path to the Java solution file to be compiled and executed.
    :param input_data: Input data to be processed by the Java program; passed to the program during execution.
    :param part: Specifies which part of the task to solve; used as an argument when running the program.
    :return: The result of the `subprocess.run` function call used to execute the compiled Java program.
    :raises subprocess.CalledProcessError: If the compilation or execution of the Java program fails.
    """
    subprocess.run(["javac", str(solution_path)], check=True)
    return subprocess.run(
        [command, solution_path.suffix[:-5], part],
        cwd=solution_path.parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )


def cpp_runner(command: str, solution_path: Path, input_data: str, part: str):
    """
    Compiles and executes a C++ solution, passing the specified input data and returning
    the result. The function compiles the provided solution file using the given command
    and then runs the compiled executable with the specified part identifier and 
    input data. The compilation ensures that the executable is created in the same
    location as the original solution file but with a `.out` extension.

    :param command: The command used to compile the C++ source file.
    :param solution_path: The path of the C++ solution file to be compiled and executed.
    :param input_data: Input data to be passed to the executable during execution.
    :param part: Identifier string that specifies which part of the solution or
        functionality to execute.
    :return: The result of executing the compiled C++ solution, as a CompletedProcess object.
    """
    executable = str(solution_path.with_suffix(".out"))
    subprocess.run([command, str(solution_path), "-o", executable], check=True)
    return subprocess.run(
        [executable, part],
        cwd=solution_path.parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )


def rust_runner(command: str, solution_path: Path, input_data: str, part: str):
    """
    Executes a Rust command to run a solution with provided input data and captures
    the output. This utility function simplifies the process of interacting with
    Rust binaries that solve specific programming challenges or tasks.

    :param command: The Rust binary command to be executed.
    :param solution_path: A Path object pointing to the solution file's directory.
    :param input_data: The input string to be passed to the solution program.
    :param part: A string specifying which part of the solution to execute.
    :return: A CompletedProcess instance containing the executed process's output
        and metadata.
    """
    return subprocess.run(
        [command, "--", part],
        cwd=solution_path.parent,
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )
