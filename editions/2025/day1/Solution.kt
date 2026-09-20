package editions.y2025.day1

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 1: Secret Entrance.
 *
 * PROBLEM SUMMARY:
 * A circular dial numbered 0 through 99 (100 positions total) starts at position 50.
 * A sequence of rotation commands is processed, where each command specifies a direction
 * ('L' for toward lower numbers / counter-clockwise, 'R' for toward higher numbers / clockwise)
 * and a distance (number of clicks).
 *
 * SIMULATION OVERVIEW:
 *
 * 1. Dial Topology:
 *    - The dial wraps around modularly at boundary 100:
 *      - Right turns increase position: `(pos + distance) mod 100`
 *      - Left turns decrease position: `(pos - distance) mod 100`
 *
 * 2. Part 1 (Final Position Zero Checks):
 *    - Evaluates the dial's landing position *after* each complete rotation command.
 *    - Increments the count whenever `currentPosition == 0` at the end of a rotation step.
 *
 * 3. Part 2 (All Intermediate Zero Crossings):
 *    - Counts every time any single click causes the dial to point at 0, including full revolutions
 *      and landing positions during a rotation.
 *    - Right Turns (`R`):
 *      - Moving right from `currentPosition` by `distance` steps reaches position `currentPosition + distance`.
 *      - Every multiple of 100 hit along the way represents reaching 0. The total zero hits equal `(currentPosition + distance) / 100`.
 *    - Left Turns (`L`):
 *      - Moving left from `currentPosition`, the distance required to reach 0 for the first time is `currentPosition`
 *        (or 100 if already at 0, as a left turn from 0 immediately moves to 99 before completing a full lap to hit 0 again).
 *      - If `distance >= effectivePosition`, the dial hits 0 once at `effectivePosition`, plus `(distance - effectivePosition) / 100`
 *        additional times for full extra loops.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    override fun parseInput(rawInput: String): List<String> {
        return rawInput.lines().filter { it.isNotBlank() }
    }

    /**
     * Solves Part 1: Counts the number of times the dial lands EXACTLY on position 0
     * at the end of a rotation command.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val rotations = parsed as List<String>
        var currentPosition = 50
        var zeroCount = 0
        for (rotation in rotations) {
            val direction = rotation[0]
            val distance = rotation.substring(1).toInt()
            currentPosition = when (direction) {
                'L' -> (currentPosition - distance).mod(100)
                'R' -> (currentPosition + distance).mod(100)
                else -> currentPosition
            }
            if (currentPosition == 0) {
                zeroCount++
            }
        }
        return zeroCount.toString()
    }

    /**
     * Solves Part 2: Counts ALL times position 0 is passed or landed on (every click)
     * during and at the end of all rotation commands.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val rotations = parsed as List<String>
        var currentPosition = 50
        var zeroHits = 0L
        for (rotation in rotations) {
            val direction = rotation[0]
            val distance = rotation.substring(1).toInt()
            if (direction == 'R') {
                // Moving right: count full multi-wrap cycles past position 0
                zeroHits += (currentPosition + distance) / 100
                currentPosition = (currentPosition + distance) % 100
            } else if (direction == 'L') {
                // Moving left: distance to reach 0 for the first time (if starting at 0, 100 steps needed for a full loop)
                val effectivePosition = if (currentPosition == 0) 100 else currentPosition
                if (distance >= effectivePosition) {
                    zeroHits += 1 + (distance - effectivePosition) / 100
                }
                currentPosition = (currentPosition - distance).mod(100)
            }
        }
        return zeroHits.toString()
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}