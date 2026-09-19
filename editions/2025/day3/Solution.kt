package editions.y2025.day3

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 3: Lobby.
 *
 * Solves both parts by finding the largest possible number formed by choosing
 * a fixed number of batteries (digits) from each bank string while preserving order.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    /**
     * Parses the raw puzzle input into a list of battery bank strings.
     * Filters out any blank lines.
     */
    override fun parseInput(rawInput: String): List<String> {
        return rawInput.lines().filter { it.isNotBlank() }
    }

    /**
     * Solves Part 1: Finds the total output joltage by picking 2 batteries (digits)
     * per bank to maximize each bank's value.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val batteryBanks = parsed as List<String>
        return batteryBanks.sumOf { maxJoltageForBank(it, k = 2) }.toString()
    }

    /**
     * Solves Part 2: Finds the total output joltage by picking 12 batteries (digits)
     * per bank to maximize each bank's value.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val batteryBanks = parsed as List<String>
        return batteryBanks.sumOf { maxJoltageForBank(it, k = 12) }.toString()
    }

    /**
     * Calculates the maximum joltage for a given battery bank by selecting exactly [k] digits
     * using a monotonic stack (greedy) approach.
     *
     * @param bank The string of digits representing battery joltages in a single bank.
     * @param k The number of batteries (digits) to select.
     * @return The largest [k]-digit number formed as a [Long].
     */
    private fun maxJoltageForBank(bank: String, k: Int): Long {
        val result = StringBuilder()
        val digitsToDrop = bank.length - k
        var dropped = 0
        for (battery in bank) {
            while (result.isNotEmpty() && dropped < digitsToDrop && result.last() < battery) {
                result.deleteAt(result.length - 1)
                dropped++
            }
            result.append(battery)
        }
        return result.substring(0, k).toLong()
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}