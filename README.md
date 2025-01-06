# Advent of Code

This repository contains my solutions for the [Advent of Code](https://adventofcode.com/) problems.

Each year, I will choose a programming language either randomly by running the script `select_language.sh` or 
deliberately if I wish to learn or explore a specific language.

There are two rules: no external help and no external libraries.
Also, the two parts of each challenge are considered independent, meaning part 2 will recompute part 1 if necessary.

Every day, I will attempt to solve the proposed challenge and publish a brief description of the solution on my 
[portfolio page](https://mpetteno.github.io/portfolio/en/projects/personal/aoc/) dedicated to AoC.
Additionally, I have implemented a web server that can be called from each day’s page on my portfolio: this server 
allows you to upload the input file for the current day’s challenge and returns the solution (see the next section).

## Webserver

The webserver implements a Flask-based application designed to solve Advent of Code (AoC) challenges by executing 
solution scripts in various programming languages. It exposes a single `/solve` endpoint that accepts a JSON 
payload containing the challenge’s year, day, part, and input file. The system locates the appropriate solution file 
based on the provided challenge details (note that the solution file name must start with `solution`), and determines 
the correct solver to use based on its extension. For example, if the solution file for a given day has a `.py` 
extension, the server will invoke the corresponding Python solver script `py_solver.py` in a subprocess. 
This script is then responsible for running the actual solution file. If a solver for a specific programming language 
is not already implemented, it will be added as part of that year’s AoC solutions and the implementation details will 
be provided in the edition page in my portfolio.