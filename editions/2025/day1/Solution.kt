package editions.y2025.day1

import solvers.Solver

class Solution(inputData: String? = null) : Solver(inputData) {

    override fun parseInput(rawInput: String): List<String> {
        return rawInput.lines().filter { it.isNotBlank() }
    }

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

    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val rotations = parsed as List<String>
        var currentPosition = 50
        var zeroHits = 0L

        for (rotation in rotations) {
            val direction = rotation[0]
            val distance = rotation.substring(1).toInt()

            if (direction == 'R') {
                zeroHits += (currentPosition + distance) / 100
                currentPosition = (currentPosition + distance) % 100
            } else if (direction == 'L') {
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