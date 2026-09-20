package editions.y2025.day4

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 4: Printing Department.
 *
 * Solves both parts by identifying accessible paper rolls (those with fewer than four adjacent rolls)
 * and iteratively removing them until no more rolls can be removed.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    companion object {
        val SEARCH_DIRECTIONS = listOf<Pair<Int, Int>>(
            -1 to -1, -1 to 0, -1 to 1,
            0 to -1,          0 to 1,
            1 to -1,  1 to 0,  1 to 1
        )
    }

    /**
     * Parses the raw puzzle input into a 2D grid represented as a list of character arrays.
     * Filters out any blank lines.
     */
    override fun parseInput(rawInput: String): Any {
        return rawInput.lines().filter { it.isNotBlank() }.map { it.toCharArray() }
    }

    /**
     * Solves Part 1: Counts the number of paper rolls that are initially accessible
     * by having fewer than four neighboring paper rolls in the 8 adjacent directions.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val paperRollsMap = parsed as List<CharArray>
        val accessiblePaperRolls = findAccessiblePaperRolls(paperRollsMap)
        return accessiblePaperRolls.size.toString()
    }

    /**
     * Solves Part 2: Counts the total number of paper rolls removed by repeatedly identifying
     * accessible rolls, removing them, and continuing until no more accessible rolls remain.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val paperRollsMap = parsed as List<CharArray>
        var totalRemoved = 0
        while (true) {
            val toRemove = findAccessiblePaperRolls(paperRollsMap)
            if (toRemove.isEmpty()) { break }
            for ((r, c) in toRemove) { paperRollsMap[r][c] = '.' }
            totalRemoved += toRemove.size
        }
        return totalRemoved.toString()
    }

    /**
     * Finds all positions in the grid containing a paper roll ('@') that have fewer than 4 neighboring
     * paper rolls in the 8 surrounding cardinal and diagonal directions.
     *
     * @param paperRollsMap The 2D grid of paper rolls.
     * @return A list of (row, column) coordinate pairs representing accessible paper rolls.
     */
    private fun findAccessiblePaperRolls(paperRollsMap: List<CharArray>): List<Pair<Int, Int>> {
        val rows = paperRollsMap.size
        val cols = paperRollsMap[0].size
        val accessiblePaperRolls = mutableListOf<Pair<Int, Int>>()
        for (r in 0 until rows) {
            for (c in 0 until cols) {
                val currentPaperRoll = paperRollsMap[r][c]
                if (currentPaperRoll == '@') {
                    var neighborPaperRolls = 0
                    for ((dr, dc) in SEARCH_DIRECTIONS) {
                        val nr = r + dr
                        val nc = c + dc
                        if (nr in 0 until rows && nc in 0 until cols && paperRollsMap[nr][nc] == '@') {
                            neighborPaperRolls++
                        }
                    }
                    if (neighborPaperRolls < 4) { accessiblePaperRolls.add(Pair(r, c)) }
                }
            }
        }
        return accessiblePaperRolls
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}