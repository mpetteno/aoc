package editions.y2025.day11

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 11: Reactor.
 *
 * Models a directed connection graph of electrical devices running between a server rack and a reactor.
 * Part 1 finds the total number of distinct directed paths leading from the starting device "you" to the destination device "out".
 * Part 2 finds the total number of paths leading from the server rack "svr" to "out" that visit both key devices "dac" and "fft" in any order.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    /**
     * Parses the raw input into an adjacency list mapping each device ID to its list of connected output devices.
     */
    override fun parseInput(rawInput: String): Any {
        val rawLines = rawInput.lines().filter { it.isNotBlank() }
        val deviceConnectionDiagram = mutableMapOf<String, List<String>>()
        for (line in rawLines) {
            val colonIdx = line.indexOf(':')
            val deviceId = line.substring(0, colonIdx).trim()
            val connectedDevices = line.substring(colonIdx + 1).trim().split("\\s+".toRegex())
            deviceConnectionDiagram[deviceId] = connectedDevices
        }
        return deviceConnectionDiagram
    }

    /**
     * Calculates the total number of distinct directed paths from [start] to [target] using depth-first search (DFS) with memoization.
     */
    private fun countPathsBetween(start: String, target: String, graph: Map<String, List<String>>): Long {
        val memo = mutableMapOf<String, Long>()

        fun dfs(current: String): Long {
            if (current == target) return 1L
            return memo.getOrPut(current) {
                val neighbors = graph[current] ?: emptyList()
                neighbors.sumOf { dfs(it) }
            }
        }

        return dfs(start)
    }

    /**
     * Part 1: Calculates the total number of distinct data paths leading from "you" to "out".
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val devicesGraph = parsed as Map<String, List<String>>
        return countPathsBetween("you", "out", devicesGraph).toString()
    }

    /**
     * Part 2: Calculates the total number of distinct data paths leading from "svr" to "out" that visit both
     * "dac" and "fft" devices. Evaluates both sequential orderings ("dac" then "fft", and "fft" then "dac")
     * by multiplying independent path counts across intermediate target nodes.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val devicesGraph = parsed as Map<String, List<String>>
        val dacThenFft = countPathsBetween("svr", "dac", devicesGraph) *
                countPathsBetween("dac", "fft", devicesGraph) *
                countPathsBetween("fft", "out", devicesGraph)
        val fftThenDac = countPathsBetween("svr", "fft", devicesGraph) *
                countPathsBetween("fft", "dac", devicesGraph) *
                countPathsBetween("dac", "out", devicesGraph)
        val totalValidPaths = dacThenFft + fftThenDac
        return totalValidPaths.toString()
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}