package editions.y2025.day8

import solvers.Solver

/**
 * Solution for Advent of Code 2025 - Day 8: Playground.
 *
 * Models electrical connections between 3D spatial junction boxes using minimum squared Euclidean distances.
 * Part 1 uses a Union-Find data structure to make the 1,000 shortest pairwise connections and calculates
 * the product of the three largest circuit sizes.
 * Part 2 applies Kruskal's Minimum Spanning Tree (MST) algorithm to determine the final edge required to unite
 * all junction boxes into a single connected circuit, returning the product of the X coordinates of those endpoints.
 */
class Solution(inputData: String? = null) : Solver(inputData) {

    /**
     * Represents a 3D spatial coordinate for a junction box.
     */
    data class JunctionBoxCoord(val x: Long, val y: Long, val z: Long) {
        companion object {
            /**
             * Parses a comma-separated string into a [JunctionBoxCoord].
             */
            fun fromString(coordString: String): JunctionBoxCoord {
                val coordStringILong = coordString.split(",").map(String::toLong)
                return JunctionBoxCoord(coordStringILong[0], coordStringILong[1], coordStringILong[2])
            }
        }

        /**
         * Calculates the squared Euclidean distance to another [JunctionBoxCoord].
         * Avoids floating-point precision issues by working entirely with exact integer operations.
         */
        fun getSquaredEuclideanDistance(other: JunctionBoxCoord): Long {
            val dx = (this.x - other.x)
            val dy = (this.y - other.y)
            val dz = (this.z - other.z)
            return dx * dx + dy * dy + dz * dz
        }
    }

    /**
     * Represents an edge connecting two junction box indices [u] and [v] with a given squared [distance].
     */
    data class Edge(val u: Int, val v: Int, val distance: Long) : Comparable<Edge> {
        override fun compareTo(other: Edge): Int = this.distance.compareTo(other.distance)
    }

    /**
     * Disjoint-set data structure with path compression and union-by-size tracking.
     */
    class UnionFind(size: Int) {
        private val parent = IntArray(size) { it }
        private val componentSize = IntArray(size) { 1 }

        /**
         * The total number of disconnected components remaining.
         */
        var componentsRemaining: Int = size
            private set

        /**
         * Finds the representative root of element [i] with path compression.
         */
        fun find(i: Int): Int {
            var root = i
            while (root != parent[root]) root = parent[root]
            var curr = i
            while (curr != root) {
                val nxt = parent[curr]
                parent[curr] = root
                curr = nxt
            }
            return root
        }

        /**
         * Merges the components containing elements [i] and [j].
         * Returns `true` if a new union was formed, or `false` if they were already connected.
         */
        fun union(i: Int, j: Int): Boolean {
            val rootI = find(i)
            val rootJ = find(j)
            if (rootI != rootJ) {
                if (componentSize[rootI] < componentSize[rootJ]) {
                    parent[rootI] = rootJ
                    componentSize[rootJ] += componentSize[rootI]
                } else {
                    parent[rootJ] = rootI
                    componentSize[rootI] += componentSize[rootJ]
                }
                componentsRemaining--
                return true
            }
            return false
        }

        /**
         * Retrieves the sizes of the [topK] largest connected components (circuits).
         */
        fun getTopCircuitSizes(topK: Int): List<Long> {
            val sizes = mutableListOf<Long>()
            for (i in parent.indices) {
                if (parent[i] == i) sizes.add(componentSize[i].toLong())
            }
            return sizes.sortedDescending().take(topK)
        }
    }

    /**
     * Parses the raw coordinate lines into a list of [JunctionBoxCoord] objects and
     * generates all sorted pairwise [Edge] connections ordered by squared distance ascending.
     */
    override fun parseInput(rawInput: String): Any {
        // List of JunctionBoxCoord objects
        val junctionBoxesCoords = rawInput.lines()
            .filter { it.isNotEmpty() }
            .map { JunctionBoxCoord.fromString(it) }
            .toList()

        // List of Edge objects
        val n = junctionBoxesCoords.size
        val totalEdges = n * (n - 1) / 2
        val edges = ArrayList<Edge>(totalEdges)
        for (i in 0 until n) {
            for (j in i + 1 until n) {
                val distSq = junctionBoxesCoords[i].getSquaredEuclideanDistance(junctionBoxesCoords[j])
                edges.add(Edge(i, j, distSq))
            }
        }
        edges.sort()
        return Pair(junctionBoxesCoords, edges)
    }

    /**
     * Part 1: Connects the 1,000 shortest edges between junction boxes and returns
     * the product of the sizes of the three largest resulting circuits.
     */
    override fun solveFirstPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val (junctionBoxesCoords, sortedEdges) = parsed as Pair<List<JunctionBoxCoord>, List<Edge>>

        // Connect the first N shortest pairs
        val connectionsToMake = 1000
        val uf = UnionFind(junctionBoxesCoords.size)
        val connectionsCount = minOf(connectionsToMake, sortedEdges.size)
        for (k in 0 until connectionsCount) {
            val edge = sortedEdges[k]
            uf.union(edge.u, edge.v)
        }

        // Multiply sizes of the 3 largest circuits
        val topSizes = uf.getTopCircuitSizes(3)
        return topSizes.reduce { acc, size -> acc * size }.toString()
    }

    /**
     * Part 2: Connects pairs in order of increasing distance until all junction boxes belong to
     * a single circuit. Returns the product of the X coordinates of the final edge's endpoints.
     */
    override fun solveSecondPart(parsed: Any): String {
        @Suppress("UNCHECKED_CAST")
        val (junctionBoxesCoords, sortedEdges) = parsed as Pair<List<JunctionBoxCoord>, List<Edge>>

        // Kruskal's MST algorithm: keep merging until only 1 component remains
        val uf = UnionFind(junctionBoxesCoords.size)
        for ((u, v) in sortedEdges) {
            if (uf.union(u, v)) {
                if (uf.componentsRemaining == 1) {
                    val box1 = junctionBoxesCoords[u]
                    val box2 = junctionBoxesCoords[v]
                    return (box1.x * box2.x).toString()
                }
            }
        }
        error("Failed to merge all junction boxes into a single component.")
    }
}

fun main() {
    val solution = Solution()
    solution.run(part = null)
}