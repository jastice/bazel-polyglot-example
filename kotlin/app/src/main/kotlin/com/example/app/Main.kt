package com.example.app

import com.example.core.Graph
import com.example.math.Matrix
import com.example.utils.JobScheduler

fun main() {
    println("Initializing Complex Kotlin Application...")

    val graph = Graph<String>()
    graph.addEdge("JobA", "JobC")
    graph.addEdge("JobB", "JobC")
    graph.addEdge("JobC", "JobD")

    println("Dependency Graph:")
    println(graph)
    println()

    val scheduler = JobScheduler()

    val matrixA = Matrix(arrayOf(doubleArrayOf(1.0, 2.0), doubleArrayOf(3.0, 4.0)))
    val matrixB = Matrix(arrayOf(doubleArrayOf(5.0, 6.0), doubleArrayOf(7.0, 8.0)))
    val matrixC = Matrix(arrayOf(doubleArrayOf(2.0, 0.0), doubleArrayOf(1.0, 2.0)))

    val jobs = mapOf(
        "JobA" to java.util.concurrent.Callable {
            println("Executing JobA...")
            matrixA * matrixB
        },
        "JobB" to java.util.concurrent.Callable {
            println("Executing JobB...")
            matrixB.transpose()
        },
        "JobC" to java.util.concurrent.Callable {
            println("Executing JobC...")
            matrixA + matrixC
        },
        "JobD" to java.util.concurrent.Callable {
            println("Executing JobD...")
            matrixC * matrixC
        }
    )

    try {
        val results = scheduler.executeMatrixJobs(graph, jobs)
        println("\nExecution Results:")
        results.forEach { (jobId, result) ->
            println("Result of $jobId:")
            println(result)
            println()
        }
    } finally {
        scheduler.shutdown()
    }

    println("Application Finished Successfully!")
}
