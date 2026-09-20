package editions.y2025.day2

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 2: Gift Shop.
 *
 * GENERAL ALGORITHM OVERVIEW: DIRECT GENERATION
 *
 * Brute-force methods iterate through every number in a range (such as from 100,000 to 999,999),
 * convert each value to a string, and check for pattern properties. This causes millions of heap
 * allocations (from `toString()`, `substring()`, or `split()`) and wastes CPU cycles checking numbers that
 * are valid.
 *
 * Direct Generation reverses the problem:
 * Instead of checking if a number matches a pattern, we mathematically generate ONLY the numbers
 * that are guaranteed to follow the pattern, then use algebraic bounds to test only those that fall
 * within the given range bounds (`start` to `end`).
 *
 * MATHEMATICAL FOUNDATION:
 *
 * Let `X` be a pattern of length `k` (for instance, `X = 12`, so `k = 2`).
 * Repeating `X` across `R` repetitions can be expressed via a geometric series multiplier:
 *
 *     Candidate = X * Multiplier(k, R)
 *     Multiplier(k, R) = 1 + 10^k + 10^(2k) + ... + 10^((R-1)k)
 *
 * Examples:
 * - Part 1 (R = 2 repetitions only):
 *   - `k = 1` (for example `X = 7`) yields `Multiplier = 10^1 + 1 = 11`, producing `7 * 11 = 77`
 *   - `k = 2` (for example `X = 12`) yields `Multiplier = 10^2 + 1 = 101`, producing `12 * 101 = 1212`
 *   - `k = 3` (for example `X = 456`) yields `Multiplier = 10^3 + 1 = 1001`, producing `456 * 1001 = 456456`
 *
 * - Part 2 (R >= 2 repetitions):
 *   - `k = 3`, `R = 3` (for example `X = 123`) yields `Multiplier = 1 + 10^3 + 10^6 = 1001001`,
 *     producing `123 * 1001001 = 123123123`
 *
 * ALGEBRAIC RANGE SLICING:
 *
 * To find all valid `X` values such that `Candidate = X * Multiplier` falls within `[rangeStart..rangeEnd]`:
 *
 *     rangeStart <= X * Multiplier <= rangeEnd
 *     startX = ceil(rangeStart / Multiplier) = (rangeStart + Multiplier - 1) / Multiplier
 *     endX   = floor(rangeEnd / Multiplier)  = rangeEnd / Multiplier
 *
 * We only loop `X` strictly from `startX` to `endX`. This reduces loop iterations from billions to
 * a few thousand and eliminates string allocations entirely inside the loop.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    data class LongRangeBounds(val start: Long, val end: Long)

    override fun parseInput(rawInput: String): List<LongRangeBounds> {
        val ranges = rawInput.split(",")
        return ranges.map { range ->
            val dashIndex = range.indexOf('-')
            LongRangeBounds(
                start = range.substring(0, dashIndex).toLong(),
                end = range.substring(dashIndex + 1).toLong()
            )
        }
    }

    /**
     * Finds invalid IDs consisting of a digit sequence repeated EXACTLY TWICE (R = 2).
     * Examples: 11 (1, 2x), 22 (2, 2x), 1010 (10, 2x), 1188511885 (11885, 2x).
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val ranges = parsed as List<LongRangeBounds>
        val invalidIDs = HashSet<Long>()
        for ((rangeStart, rangeEnd) in ranges) {
            // Track half-length k using powers of 10
            // powerOf10ForK = 10^k
            // multiplier    = 10^k + 1  (For R = 2 repetitions)
            var powerOf10ForK = 10L
            var multiplier = 11L
            // Iterate through valid half-lengths k (1-digit half, 2-digit half, etc.)
            while (powerOf10ForK <= 10_000_000_000L) {
                // Bounds for a valid k-digit number X without leading zeros
                // e.g., for k=2: minHalf = 10, maxHalf = 99
                val minHalf = powerOf10ForK / 10
                val maxHalf = powerOf10ForK - 1
                // Algebraic Range Slicing
                val startX = maxOf(minHalf, (rangeStart + multiplier - 1) / multiplier)
                val endX = minOf(maxHalf, rangeEnd / multiplier)
                // Direct generation loop
                for (x in startX..endX) {
                    invalidIDs.add(x * multiplier)
                }
                // Advance to next pattern length k (e.g., 10^1 -> 10^2)
                powerOf10ForK *= 10
                multiplier = powerOf10ForK + 1
            }
        }
        return invalidIDs.sum().toString()
    }

    /**
     * Finds invalid IDs consisting of ANY sequence of digits repeated AT LEAST TWICE (R >= 2).
     * Examples: 12341234 (R=2), 123123123 (R=3), 1111111 (R=7).
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val ranges = parsed as List<LongRangeBounds>
        val invalidIDs = HashSet<Long>()
        for ((rangeStart, rangeEnd) in ranges) {
            // Iterate through pattern lengths k = 1, 2, 3...
            var powerOf10ForK = 10L // 10^k
            while (powerOf10ForK <= 10_000_000_000L) {
                val minHalf = powerOf10ForK / 10
                val maxHalf = powerOf10ForK - 1
                // Start with R = 2 repetitions: Multiplier = 10^k + 1
                var multiplier = powerOf10ForK + 1
                // Iterate through number of repetitions R >= 2
                // Continue as long as the minimum possible candidate (minHalf * multiplier) fits in rangeEnd
                while (multiplier > 0 && minHalf <= rangeEnd / multiplier) {
                    // Algebraic Range Slicing for current k and R
                    val startX = maxOf(minHalf, (rangeStart + multiplier - 1) / multiplier)
                    val endX = minOf(maxHalf, rangeEnd / multiplier)
                    // Direct generation loop
                    for (x in startX..endX) {
                        invalidIDs.add(x * multiplier)
                    }
                    // Compute multiplier for next repetition count (R + 1)
                    // Multiplier(k, R+1) = Multiplier(k, R) * 10^k + 1
                    val nextMultiplier = multiplier * powerOf10ForK + 1
                    // Stop if Long primitive overflows
                    if (nextMultiplier <= multiplier) break
                    multiplier = nextMultiplier
                }
                // Advance to next pattern length k
                powerOf10ForK *= 10
            }
        }
        return invalidIDs.sum().toString()
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}