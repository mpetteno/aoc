package editions.y2025.day12

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 12: Christmas Tree Farm.
 *
 * Models present packing under Christmas trees as 2D spatial arrangement / polyomino packing.
 * Evaluates whether required quantities of various custom present shapes (allowing rotations
 * and reflections) can fit into given rectangular tree regions without overlapping using
 * recursive backtracking.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    /**
     * Represents a standard present shape in 2D space.
     *
     * @property id The unique identifier/index of the present shape.
     * @property originalGrid Visual string grid representation of the present shape (`#` = occupied, `.` = empty).
     */
    data class PresentShape(val id: Int, val originalGrid: List<String>) {

        /**
         * Precomputed set of all unique 2D coordinate orientations (rotations + reflections).
         * Each orientation is normalized so its top-leftmost occupied cell starts at offset relative `(0, 0)`.
         */
        val orientations: List<List<Pair<Int, Int>>> = generateUniqueOrientations(originalGrid)

        /**
         * Total area occupied by this present (number of `#` cells).
         */
        val area = originalGrid.sumOf { r -> r.count { it == '#' } }

        /**
         * Generates up to 8 unique orientations (4 rotations x 2 reflections) normalized to offset coordinates.
         */
        private fun generateUniqueOrientations(grid: List<String>): List<List<Pair<Int, Int>>> {

            fun rotateGrid(grid: List<String>): List<String> {
                val h = grid.size
                val w = grid[0].length
                val rotated = Array(w) { CharArray(h) }
                for (r in 0 until h) {
                    for (c in 0 until w) {
                        rotated[c][h - 1 - r] = grid[r][c]
                    }
                }
                return rotated.map { String(it) }
            }

            fun flipGrid(grid: List<String>): List<String> {
                return grid.map { it.reversed() }
            }

            fun toNormalizedCoords(grid: List<String>): List<Pair<Int, Int>> {
                val coords = mutableListOf<Pair<Int, Int>>()
                for (r in grid.indices) {
                    for (c in grid[r].indices) {
                        if (grid[r][c] == '#') {
                            coords.add(Pair(r, c))
                        }
                    }
                }
                val minR = coords.minOf { it.first }
                val minC = coords.minOf { it.second }
                return coords.map { Pair(it.first - minR, it.second - minC) }.sortedWith(compareBy({ it.first }, { it.second }))
            }

            val rawOrientations = mutableListOf<List<Pair<Int, Int>>>()
            var current = grid
            repeat(4) {
                rawOrientations.add(toNormalizedCoords(current))
                rawOrientations.add(toNormalizedCoords(flipGrid(current)))
                current = rotateGrid(current)
            }
            return rawOrientations.distinct()
        }
    }

    /**
     * Represents a rectangular region beneath a tree and the required quantities of present shapes.
     *
     * @property width Width of the tree region in grid units.
     * @property height Length/Height of the tree region in grid units.
     * @property quantities List where index `i` specifies how many presents of shape `i` must fit in this region.
     */
    data class TreeRegion(val width: Int, val height: Int, val quantities: List<Int>) {

        /**
         * Total grid area of the tree region.
         */
        val area: Int = width * height

        /**
         * Determines if all required present shapes can fit into this region using depth-first search with backtracking.
         *
         * @param shapes Master list of available present shapes.
         * @return `true` if a non-overlapping arrangement exists, `false` otherwise.
         */
        fun canFitAllPresents(shapes: List<PresentShape>): Boolean {

            fun canPlace(
                orientation: List<Pair<Int, Int>>,
                startR: Int,
                startC: Int,
                grid: Array<BooleanArray>,
                width: Int,
                height: Int
            ): Boolean {
                for ((dr, dc) in orientation) {
                    val r = startR + dr
                    val c = startC + dc
                    if (r !in 0 until height || c !in 0 until width || grid[r][c]) {
                        return false
                    }
                }
                return true
            }

            fun place(
                orientation: List<Pair<Int, Int>>,
                startR: Int,
                startC: Int,
                grid: Array<BooleanArray>,
                value: Boolean
            ) {
                for ((dr, dc) in orientation) {
                    grid[startR + dr][startC + dc] = value
                }
            }

            fun backtrack(
                presentIdx: Int,
                presents: List<PresentShape>,
                grid: Array<BooleanArray>,
                width: Int,
                height: Int
            ): Boolean {
                if (presentIdx == presents.size) return true
                val shape = presents[presentIdx]

                // Find the first empty cell on the grid
                var firstEmptyR = -1
                outer@ for (r in 0 until height) {
                    for (c in 0 until width) {
                        if (!grid[r][c]) {
                            firstEmptyR = r
                            break@outer
                        }
                    }
                }
                if (firstEmptyR == -1) return false

                // Try placing the current present shape in valid locations
                for (orientation in shape.orientations) {
                    for (r in 0 until height) {
                        for (c in 0 until width) {
                            if (canPlace(orientation, r, c, grid, width, height)) {
                                place(orientation, r, c, grid, true)
                                if (backtrack(presentIdx + 1, presents, grid, width, height)) {
                                    return true
                                }
                                place(orientation, r, c, grid, false)
                            }
                        }
                    }
                }
                return false
            }

            val presentsToPlace = mutableListOf<PresentShape>()
            for ((shapeIdx, count) in this.quantities.withIndex()) {
                repeat(count) { presentsToPlace.add(shapes[shapeIdx]) }
            }

            val totalAreaNeeded = presentsToPlace.sumOf { it.area }
            if (totalAreaNeeded > this.area) return false
            if (presentsToPlace.isEmpty()) return true

            // Sort present shapes by area descending to prune search tree earlier
            presentsToPlace.sortByDescending { it.area }
            val grid = Array(this.height) { BooleanArray(this.width) }
            return backtrack(0, presentsToPlace, grid, this.width, this.height)
        }
    }

    /**
     * Parses the puzzle input into a pair containing:
     * 1. A list of available [PresentShape] definitions.
     * 2. A list of [TreeRegion] queries to validate.
     */
    override fun parseInput(rawInput: String): Any {
        val lines = rawInput.lines()
        val shapes = mutableListOf<PresentShape>()
        val queries = mutableListOf<TreeRegion>()
        var idx = 0
        while (idx < lines.size) {
            val line = lines[idx].trim()
            if (line.isEmpty()) {
                idx++
                continue
            }
            // Region query lines start with dimensions formatted as "12x5: ..."
            if (line.contains("x") && line.contains(":")) {
                val parts = line.split(":")
                val dims = parts[0].trim().split("x")
                val width = dims[0].toInt()
                val height = dims[1].toInt()
                val quantities = parts[1].trim().split("\\s+".toRegex()).map { it.toInt() }
                queries.add(TreeRegion(width, height, quantities))
                idx++
            } else if (line.endsWith(":")) {
                // Present shape header "0:"
                val shapeId = line.dropLast(1).trim().toInt()
                idx++
                val gridLines = mutableListOf<String>()
                while (idx < lines.size && lines[idx].trim().let { it.isNotBlank() && !it.endsWith(":") && !it.contains("x") }) {
                    gridLines.add(lines[idx].trim())
                    idx++
                }
                val originalGrid = gridLines.filter { it.isNotEmpty() }
                shapes.add(PresentShape(shapeId, originalGrid))
            } else {
                idx++
            }
        }
        return Pair(shapes, queries)
    }

    /**
     * Part 1: Counts how many tree regions can successfully fit all required presents.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val (shapes, regions) = parsed as Pair<List<PresentShape>, List<TreeRegion>>
        val validCount = regions.count { it.canFitAllPresents(shapes) }
        return validCount.toString()
    }

    /**
     * Part 2: Merry Christmas!
     */
    override fun solveSecondPart(parsed: Any): String {
        return "Merry Christmas!"
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}