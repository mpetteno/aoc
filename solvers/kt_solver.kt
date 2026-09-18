@file:JvmName("SolverMain")

package solvers
import java.io.File
import kotlin.system.exitProcess

abstract class Solver(protected val inputData: String? = null) {

    abstract fun parseInput(rawInput: String): Any

    abstract fun solveFirstPart(parsed: Any): String

    abstract fun solveSecondPart(parsed: Any): String

    protected fun readFile(): Any {
        val rawInput = if (this.inputData == null) {
            val pkg = this.javaClass.`package`.name
            val parts = pkg.split(".").map { it.removePrefix("y") }
            val path = parts.joinToString("/") + "/input.txt"
            File(path).readText()
        } else {
            this.inputData
        }
        return parseInput(rawInput)
    }

    fun run(part: Int?) {
        val parsed = readFile()
        when (part) {
            1 -> runPart("Part 1") { solveFirstPart(parsed) }
            2 -> runPart("Part 2") { solveSecondPart(parsed) }
            null -> {
                runPart("Part 1") { solveFirstPart(parsed) }
                runPart("Part 2") { solveSecondPart(parsed) }
            }
            else -> throw IllegalArgumentException("Invalid part specified. Use 1, 2, or omit for both.")
        }
    }

    private fun runPart(label: String, block: () -> String) {
        println("------------- $label -------------")
        val start = System.nanoTime()
        val result = block()
        val ms = (System.nanoTime() - start) / 1_000_000.0
        println("Execution Time: %.9f ms".format(ms))
        println(result)
    }
}

private fun parseArgs(args: Array<String>): Map<String, String> {
    val map = mutableMapOf<String, String>()
    var i = 0
    while (i < args.size) {
        val key = args[i].removePrefix("--")
        if (i + 1 < args.size && !args[i + 1].startsWith("--")) {
            map[key] = args[i + 1]; i += 2
        } else { map[key] = "true"; i += 1 }
    }
    return map
}

fun main(args: Array<String>) {
    val argMap = parseArgs(args)
    val year = argMap["year"]
    val day = argMap["day"]
    val part = argMap["part"]?.toIntOrNull()

    if (year == null || day == null) {
        System.err.println("--year and --day are required")
        exitProcess(1)
    }
    if (!year.matches(Regex("\\d{4}")) || !day.matches(Regex("\\d{1,2}"))) {
        System.err.println("Invalid year/day")
        exitProcess(1)
    }

    val inputData = System.`in`.bufferedReader().readText()
    println(inputData)
    val className = "editions.y$year.day$day.Solution"

    try {
        val clazz = Class.forName(className)
        val ctor = clazz.getDeclaredConstructor(String::class.java)
        val instance = ctor.newInstance(inputData) as Solver
        instance.run(part)
    } catch (e: ClassNotFoundException) {
        System.err.println("Failed to load solution module: $className")
        exitProcess(1)
    }
}