package editions.y2025.day6

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 6: Trash Compactor.
 *
 * Solves both parts by parsing operator symbols and transposed operand grids. Part 1 applies
 * operations left-to-right across rows, while Part 2 reads Cephalopod math right-to-left
 * column-by-column, constructing numbers top-to-bottom before reducing them.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    private val operations: Map<String, (Long, Long) -> Long> = mapOf(
        "+" to { a, b -> a + b },
        "*" to { a, b -> a * b }
    )

    /**
     * Parses the raw puzzle input into a Pair containing a transposed 2D list of operand strings
     * and a list of operator symbols from the bottom row.
     */
    override fun parseInput(rawInput: String): Any {
        val lines = rawInput.lines().filter { it.isNotEmpty() }
        val operators = lines.last().trim().split(Regex("\\s+"))
        val operandLines = lines.dropLast(1).map { row -> row.trim().split(Regex("\\s+")) }
        val rows = operandLines.size
        val cols = operandLines[0].size
        val operandsTransposed = List(cols) { col -> List(rows) { row -> operandLines[row][col] } }
        return Pair(operandsTransposed, operators)
    }

    /**
     * Solves Part 1: Converts transposed string operands directly into numbers and evaluates
     * each problem left-to-right using its assigned operator, returning the grand total sum.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val (operands, operators) = parsed as Pair<List<List<String>>, List<String>>
        return operands.zip(operators) { row, opSymbol ->
            val operator = operations[opSymbol] ?: error("Unsupported operator: $opSymbol")
            row.map { it.toLong() }.reduce { acc, number -> operator(acc, number) }
        }.sum().toString()
    }

    /**
     * Solves Part 2: Processes problems right-to-left by reconstructing vertical numbers
     * top-to-bottom from the transposed grid, applying the operation to each column block,
     * and summing the total.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val (operands, operators) = parsed as Pair<List<List<String>>, List<String>>
        // Reversing for right-to-left order
        val reversedOperands = operands.asReversed()
        val reversedOperators = operators.asReversed()
        return reversedOperands.zip(reversedOperators) { problemMatrix, opSymbol ->
            val operator = operations[opSymbol] ?: error("Unsupported operator: $opSymbol")
            // Determine maximum digit height across the strings in this problem block
            val maxDigits = problemMatrix.maxOf { it.length }
            // Read digits column-by-column right-to-left, top-to-bottom
            val newOperands = mutableListOf<Long>()
            for (colIdx in maxDigits - 1 downTo 0) {
                val digitCol = problemMatrix
                    .map { str -> str.getOrNull(colIdx) }
                    .filter { it != null && it.isDigit() }
                    .joinToString("")
                if (digitCol.isNotEmpty()) {
                    newOperands.add(digitCol.toLong())
                }
            }
            newOperands.reduce { acc, number -> operator(acc, number) }
        }.sum().toString()
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}