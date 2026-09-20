package editions.y2025.day5

import solvers.Solver
import kotlin.math.max
import kotlin.text.indexOf
import kotlin.text.substring

/**
 * Solution for Advent of Code 2025 - Day 5: Cafeteria.
 *
 * Solves both parts by parsing fresh ingredient ID ranges and individual available ingredient IDs,
 * checking individual IDs against valid ranges in Part 1 and calculating the total unique coverage
 * of merged ID ranges in Part 2.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    data class LongRangeBounds(val start: Long, val end: Long) {
        val count: Long get() = end - start + 1
    }

    /**
     * Parses the raw puzzle input into a Pair containing a list of inclusive fresh ID ranges
     * and a list of available ingredient IDs to check.
     */
    override fun parseInput(rawInput: String): Any {
        val rawInputLines = rawInput.lines()
        // Parse ingredients ranges
        val rawRanges = rawInputLines.takeWhile { it.isNotBlank() }
        val ingredientsRanges = rawRanges.map { line ->
            val dashIndex = line.indexOf('-')
            LongRangeBounds(
                start = line.substring(0, dashIndex).toLong(),
                end = line.substring(dashIndex + 1).toLong()
            )
        }
        // Parse ingredients IDs
        val ingredientIds = rawInputLines.takeLastWhile { it.isNotBlank() }.map { it.toLong() }
        return Pair(ingredientsRanges, ingredientIds)
    }

    /**
     * Solves Part 1: Counts how many of the available ingredient IDs fall within at least one
     * of the fresh ingredient ID ranges.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val (ingredientsRanges, ingredientsIDs) = parsed as Pair<MutableList<LongRangeBounds>, MutableList<Long>>
        var freshIngredientsCount = 0
        outer@ for (ingredientsID in ingredientsIDs) {
            for ((start, end) in ingredientsRanges) {
                if (ingredientsID in start..end) {
                    freshIngredientsCount++
                    continue@outer
                }
            }
        }
        return freshIngredientsCount.toString()
    }

    /**
     * Solves Part 2: Merges overlapping or contiguous ingredient ID ranges and calculates
     * the total count of unique ingredient IDs considered fresh across all ranges.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val (ingredientsRanges, _) = parsed as Pair<MutableList<LongRangeBounds>, *>
        val sortedRanges = ingredientsRanges.sortedBy { it.start }
        val merged = mutableListOf<LongRangeBounds>()
        var current = sortedRanges.first()
        for (i in 1 until sortedRanges.size) {
            val next = sortedRanges[i]
            if (next.start <= current.end + 1) {
                current = LongRangeBounds(current.start, max(current.end, next.end))
            } else {
                merged.add(current)
                current = next
            }
        }
        merged.add(current)
        return merged.sumOf { it.count }.toString()
    }

}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}