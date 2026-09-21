package editions.y2025.day9

import solvers.Solver
import kotlin.math.max
import kotlin.math.min

/**
 * Solution for Advent of Code 2025 - Day 9: Movie Theater.
 *
 * Models a grid of tile coordinates representing red tiles in a movie theater floor pattern.
 * Part 1 finds the largest axis-aligned rectangular tile area formed by choosing any two red tiles as opposite corners.
 * Part 2 finds the largest axis-aligned rectangle formed by two red tiles such that no boundary segment of the closed
 * polygon formed by sequential red tiles pierces through the strict interior of the candidate rectangle.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    /**
     * Represents a 2D spatial grid coordinate for a red tile.
     */
    data class RedTileCoord(val x: Long = 0, val y: Long = 0)

    /**
     * Represents a straight boundary line segment connecting two sequential [RedTileCoord] vertices of the polygon.
     */
    data class LineSegment(val p1: RedTileCoord, val p2: RedTileCoord) {
        val minX = min(p1.x, p2.x)
        val maxX = max(p1.x, p2.x)
        val minY = min(p1.y, p2.y)
        val maxY = max(p1.y, p2.y)

        /**
         * Indicates whether this line segment runs horizontally ([p1].y == [p2].y).
         */
        val isHorizontal = p1.y == p2.y
    }

    /**
     * Represents an axis-aligned rectangle defined by two opposing red tile vertices.
     */
    class RedTileRectangle(firstVertex: RedTileCoord, secondVertex: RedTileCoord) {

        val minX = min(firstVertex.x, secondVertex.x)
        val maxX = max(firstVertex.x, secondVertex.x)
        val minY = min(firstVertex.y, secondVertex.y)
        val maxY = max(firstVertex.y, secondVertex.y)

        /**
         * Calculates the total number of discrete grid tiles enclosed by this rectangle.
         * Includes both starting and ending boundary tile coordinates.
         */
        val area: Long
            get() = (maxX - minX + 1) * (maxY - minY + 1)

        /**
         * Checks whether a given [redTile] coordinate lies within or on the boundary of this rectangle.
         */
        fun contains(redTile: RedTileCoord): Boolean {
            return redTile.x in minX..maxX && redTile.y in minY..maxY
        }

        /**
         * Checks if a polygon boundary edge crosses through the strict interior of this rectangle.
         *
         * An edge is considered to cross the interior if it cuts through the open region strictly
         * between the rectangle's boundary bounds.
         */
        fun crossesInterior(edge: LineSegment): Boolean {
            return if (edge.isHorizontal) {
                // Horizontal edge crossing vertical span
                edge.minY in (minY + 1 until maxY) &&
                        max(minX, edge.minX) < min(maxX, edge.maxX)
            } else {
                // Vertical edge crossing horizontal span
                edge.minX in (minX + 1 until maxX) &&
                        max(minY, edge.minY) < min(maxY, edge.maxY)
            }
        }
    }

    /**
     * Parses the raw coordinate lines into a list of [RedTileCoord] objects.
     */
    override fun parseInput(rawInput: String): Any {
        return rawInput.lines().filter { it.isNotBlank() }.map { line ->
            val (x, y) = line.split(",").map(String::toLong)
            RedTileCoord(x, y)
        }
    }

    /**
     * Part 1: Evaluates all pairs of red tiles as opposing rectangle corners and returns
     * the maximum possible discrete tile area.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val redTiles = parsed as List<RedTileCoord>
        var maxArea = 0L
        for (i in redTiles.indices) {
            for (j in i + 1 until redTiles.size) {
                val rect = RedTileRectangle(redTiles[i], redTiles[j])
                if (rect.area > maxArea) {
                    maxArea = rect.area
                }
            }
        }
        return maxArea.toString()
    }

    /**
     * Part 2: Connects sequential red tiles into a closed polygon boundary, generates all possible
     * pair rectangle candidates sorted by descending area, and returns the area of the first rectangle
     * whose interior is not crossed by any polygon edge.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val redTiles = parsed as List<RedTileCoord>
        val polygonBoundaries = redTiles.indices.map { i ->
            LineSegment(redTiles[i], redTiles[(i + 1) % redTiles.size])
        }
        val allRedRectangles = mutableListOf<RedTileRectangle>()
        for (i in redTiles.indices) {
            for (j in i + 1 until redTiles.size) {
                allRedRectangles.add(RedTileRectangle(redTiles[i], redTiles[j]))
            }
        }
        allRedRectangles.sortByDescending { it.area }
        for (rect in allRedRectangles) {
            if (polygonBoundaries.none { polygonBoundary -> rect.crossesInterior(polygonBoundary) }) {
                return rect.area.toString()
            }
        }
        return "0"
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}