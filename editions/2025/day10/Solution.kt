package editions.y2025.day10

import solvers.Solver
import kotlin.math.roundToInt

/**
 * Solution for Advent of Code 2025 - Day 10: Factory.
 *
 * Models machine initialization as linear systems of equations:
 * Part 1 finds the minimum button presses required to configure indicator lights using a linear system over GF(2)
 * (modulo 2 arithmetic) solved via bitwise Gaussian Elimination.
 * Part 2 finds the minimum button presses required to reach exact target joltage requirements using an Integer
 * Linear Program (ILP) over non-negative integers solved via floating-point Gaussian Elimination with depth-first
 * search over free variable bounds.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    /**
     * Represents a single factory machine configuration.
     */
    data class FactoryMachine(
        val indicatorLightDiagram: List<Boolean>,
        val buttonWiringSchematics: List<List<Int>>,
        val joltageRequirements: List<Int>
    ) {

        /**
         * Calculates the minimum button presses to reach the target indicator light configuration (Part 1).
         *
         * Performs Gaussian Elimination over GF(2) to find pivot and free variables. Iterates over
         * all binary combinations of free variables to minimize total button presses (Hamming weight).
         */
        fun solveMinPresses(): Int {
            val numLights = indicatorLightDiagram.size
            val numButtons = buttonWiringSchematics.size
            if (numButtons == 0) return if (indicatorLightDiagram.all { !it }) 0 else Int.MAX_VALUE
            // Build Augmented Matrix (numLights x (numButtons + 1))
            val augmented = Array(numLights) { IntArray(numButtons + 1) }
            buttonWiringSchematics.forEachIndexed { col, button ->
                for (lightIdx in button) {
                    if (lightIdx in 0 until numLights) {
                        augmented[lightIdx][col] = 1
                    }
                }
            }
            // Target vector as last column
            for (i in 0 until numLights) {
                augmented[i][numButtons] = if (indicatorLightDiagram[i]) 1 else 0
            }
            // Gaussian Elimination over GF(2)
            val pivotCols = mutableListOf<Pair<Int, Int>>()
            var pivotRow = 0
            for (col in 0 until numButtons) {
                var rowWithPivot = -1
                for (r in pivotRow until numLights) {
                    if (augmented[r][col] == 1) {
                        rowWithPivot = r
                        break
                    }
                }
                if (rowWithPivot == -1) continue
                // Swap pivot row
                val temp = augmented[pivotRow]
                augmented[pivotRow] = augmented[rowWithPivot]
                augmented[rowWithPivot] = temp
                pivotCols.add(pivotRow to col)
                // Eliminate 1s in current column
                for (r in 0 until numLights) {
                    if (r != pivotRow && augmented[r][col] == 1) {
                        for (c in col..numButtons) {
                            augmented[r][c] = augmented[r][c] xor augmented[pivotRow][c]
                        }
                    }
                }
                pivotRow++
            }
            // Check for impossibility (row like [0 0 ... 0 | 1])
            for (r in pivotRow until numLights) {
                if (augmented[r][numButtons] == 1) {
                    return Int.MAX_VALUE
                }
            }
            // Identify free variables
            val pivotColIndices = pivotCols.map { it.second }.toSet()
            val freeCols = (0 until numButtons).filter { it !in pivotColIndices }
            val numFree = freeCols.size
            var minPresses = Int.MAX_VALUE
            val totalCombinations = 1 shl numFree
            // Search across free variable choices
            for (mask in 0 until totalCombinations) {
                val x = IntArray(numButtons)
                for (i in freeCols.indices) {
                    x[freeCols[i]] = (mask shr i) and 1
                }
                for ((r, col) in pivotCols) {
                    var valBit = augmented[r][numButtons]
                    for (freeCol in freeCols) {
                        if (augmented[r][freeCol] == 1) { valBit = valBit xor x[freeCol] }
                    }
                    x[col] = valBit
                }
                minPresses = minOf(minPresses, x.sum())
            }
            return minPresses
        }

        /**
         * Calculates the minimum button presses to reach exact target joltage requirements (Part 2).
         *
         * Reduces the linear system over real numbers, then performs depth-first search over bounded
         * non-negative integer choices for free variables to find valid non-negative integer solutions.
         */
        fun solveMinJoltagePresses(): Long {
            val numCounters = joltageRequirements.size
            val numButtons = buttonWiringSchematics.size
            if (numCounters == 0) return 0L
            if (numButtons == 0) return if (joltageRequirements.all { it == 0 }) 0L else Long.MAX_VALUE
            // Build system matrix A (numCounters x numButtons) and target b
            val matrix = Array(numCounters) { DoubleArray(numButtons) }
            val target = DoubleArray(numCounters)
            buttonWiringSchematics.forEachIndexed { col, button ->
                for (counterIdx in button) {
                    if (counterIdx in 0 until numCounters) {
                        matrix[counterIdx][col] = 1.0
                    }
                }
            }
            for (i in 0 until numCounters) {
                target[i] = joltageRequirements[i].toDouble()
            }
            // Augmented matrix [A | b]
            val aug = Array(numCounters) { r ->
                DoubleArray(numButtons + 1) { c ->
                    if (c < numButtons) matrix[r][c] else target[r]
                }
            }
            // Row reduction / Gaussian Elimination
            val pivotCols = mutableListOf<Pair<Int, Int>>() // (row, col)
            var pivotRow = 0
            val epsilon = 1e-9

            for (col in 0 until numButtons) {
                // Find pivot with largest absolute value for numerical stability
                var maxRow = -1
                var maxVal = epsilon
                for (r in pivotRow until numCounters) {
                    val absVal = kotlin.math.abs(aug[r][col])
                    if (absVal > maxVal) {
                        maxVal = absVal
                        maxRow = r
                    }
                }
                if (maxRow == -1) continue // Free variable column
                // Swap pivot row
                val temp = aug[pivotRow]
                aug[pivotRow] = aug[maxRow]
                aug[maxRow] = temp
                // Scale pivot row so pivot element is 1.0
                val pivotVal = aug[pivotRow][col]
                for (c in col..numButtons) {
                    aug[pivotRow][c] /= pivotVal
                }
                pivotCols.add(pivotRow to col)
                // Eliminate column entries in other rows
                for (r in 0 until numCounters) {
                    if (r != pivotRow && kotlin.math.abs(aug[r][col]) > epsilon) {
                        val factor = aug[r][col]
                        for (c in col..numButtons) {
                            aug[r][c] -= factor * aug[pivotRow][c]
                        }
                    }
                }
                pivotRow++
            }
            // Check for impossible rows (e.g. [0 0 ... 0 | nonzero])
            for (r in pivotRow until numCounters) {
                if (kotlin.math.abs(aug[r][numButtons]) > epsilon) {
                    return Long.MAX_VALUE // No solution
                }
            }
            // Separate pivot and free variables
            val pivotColSet = pivotCols.map { it.second }.toSet()
            val freeCols = (0 until numButtons).filter { it !in pivotColSet }
            val maxJoltage = joltageRequirements.maxOrNull() ?: 0
            var minPresses = Long.MAX_VALUE

            // Depth-First Search over integer choices for free variables
            fun searchFreeVars(freeIdx: Int, currentFreeValues: IntArray) {
                if (freeIdx == freeCols.size) {
                    // Compute pivot variable values
                    val x = LongArray(numButtons)
                    for (i in freeCols.indices) {
                        x[freeCols[i]] = currentFreeValues[i].toLong()
                    }
                    var isValid = true
                    for ((r, col) in pivotCols) {
                        var valDouble = aug[r][numButtons]
                        for (i in freeCols.indices) {
                            val freeCol = freeCols[i]
                            valDouble -= aug[r][freeCol] * currentFreeValues[i]
                        }
                        val rounded = valDouble.roundToInt()
                        // Must be an integer >= 0 within epsilon margin
                        if (kotlin.math.abs(valDouble - rounded) > epsilon || rounded < 0) {
                            isValid = false
                            break
                        }
                        x[col] = rounded.toLong()
                    }

                    if (isValid) minPresses = minOf(minPresses, x.sum())
                    return
                }
                // Branch on possible integer values for the current free variable
                for (v in 0..maxJoltage) {
                    currentFreeValues[freeIdx] = v
                    searchFreeVars(freeIdx + 1, currentFreeValues)
                }
            }

            searchFreeVars(0, IntArray(freeCols.size))
            return minPresses
        }
    }

    /**
     * Parses the raw input lines into a list of [FactoryMachine] instances.
     */
    override fun parseInput(rawInput: String): Any {
        val regex = Regex("""^\[([^]]+)]\s+(.*?)\s+\{([^}]+)}$""")
        return rawInput.lines().filter { it.isNotBlank() }.map { line ->
            val match = regex.find(line)
            if (match != null) {
                val (indicatorRaw, buttonsRaw, joltageRaw) = match.destructured
                val indicatorLightDiagram: List<Boolean> = indicatorRaw.map { if (it == '#') true else false }
                val btnWiringSchematics: List<List<Int>> = Regex("""\(([^)]+)\)""").findAll(buttonsRaw)
                    .map { result -> result.groupValues[1].split(",").map { it.trim().toInt() } }.toList()
                val joltageRequirements: List<Int> = joltageRaw.split(",").map { it.trim().toInt() }
                return@map FactoryMachine(indicatorLightDiagram, btnWiringSchematics, joltageRequirements)
            }
        }
    }

    /**
     * Part 1: Computes the sum of minimum button presses to configure indicator lights across all machines.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val machines = parsed as List<FactoryMachine>
        val totalPresses = machines.sumOf { machine ->
            val presses = machine.solveMinPresses()
            if (presses == Int.MAX_VALUE) 0 else presses
        }
        return totalPresses.toString()
    }

    /**
     * Part 2: Computes the sum of minimum button presses to reach exact target joltages across all machines.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val machines = parsed as List<FactoryMachine>

        val totalPresses = machines.sumOf { machine ->
            val presses = machine.solveMinJoltagePresses()
            if (presses == Long.MAX_VALUE) 0L else presses
        }

        return totalPresses.toString()
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}