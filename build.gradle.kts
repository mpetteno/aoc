plugins {
    kotlin("jvm") version "2.4.20"
    id("com.gradleup.shadow") version "8.3.5"
    application
}

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(21)
}

application {
    mainClass.set("solvers.SolverMain")
}

sourceSets {
    main {
        kotlin.srcDirs("solvers", "editions/2025")
    }
}

tasks.shadowJar {
    archiveBaseName.set("aoc-solver")
    archiveClassifier.set("")
    archiveVersion.set("")
}
