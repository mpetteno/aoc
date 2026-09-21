package editions.y2025.day7

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 7: Laboratories.
 *
 * Solves both parts by simulating downward tachyon beam propagation through a splitters grid.
 * Part 1 tracks active beam indices via unique set states to count split events, while
 * Part 2 uses dynamic programming frequency maps to track total quantum timelines across all paths.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    /**
     * Parses the raw input string by filtering out empty lines into a grid of strings.
     */
    override fun parseInput(rawInput: String): Any {
        return rawInput.lines().filter { it.isNotEmpty() }
    }

    /**
     * Part 1: Count the total number of split events.
     * Multiple beams hitting the same splitter on the same row count as 1 split event.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val tachyonManifoldDiagram = parsed as List<String>
        val cols = tachyonManifoldDiagram[0].length
        val rayStartIdx = tachyonManifoldDiagram[0].indexOf('S')
        var splitCount = 0
        var activeRayIdxs = setOf(rayStartIdx)
        for (r in tachyonManifoldDiagram.indices) {
            val nextRayIdxs = mutableSetOf<Int>()
            for (c in activeRayIdxs) {
                if (tachyonManifoldDiagram[r][c] == '^') {
                    splitCount++
                    if (c - 1 >= 0) nextRayIdxs.add(c - 1)
                    if (c + 1 < cols) nextRayIdxs.add(c + 1)
                } else {
                    nextRayIdxs.add(c)
                }
            }
            activeRayIdxs = nextRayIdxs
            if (activeRayIdxs.isEmpty()) break
        }
        return splitCount.toString()
    }

    /**
     * Part 2: Count total quantum timelines (distinct paths).
     * Uses dynamic programming / frequency counts (Long) to handle exponential path growth.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val tachyonManifoldDiagram = parsed as List<String>
        val cols = tachyonManifoldDiagram[0].length
        val rayStartIdx = tachyonManifoldDiagram[0].indexOf('S')
        var currentCounts = mapOf(rayStartIdx to 1L)
        for (r in tachyonManifoldDiagram.indices) {
            val nextCounts = mutableMapOf<Int, Long>().withDefault { 0L }
            for ((c, count) in currentCounts) {
                if (tachyonManifoldDiagram[r][c] == '^') {
                    if (c - 1 >= 0) nextCounts[c - 1] = nextCounts.getValue(c - 1) + count
                    if (c + 1 < cols) nextCounts[c + 1] = nextCounts.getValue(c + 1) + count
                } else {
                    nextCounts[c] = nextCounts.getValue(c) + count
                }
            }
            currentCounts = nextCounts
            if (currentCounts.isEmpty()) break
        }
        return currentCounts.values.sum().toString()
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}