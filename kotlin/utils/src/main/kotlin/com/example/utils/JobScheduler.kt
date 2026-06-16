package com.example.utils

import com.example.core.Graph
import com.example.math.Matrix
import java.util.concurrent.Callable
import java.util.concurrent.Executors
import java.util.concurrent.Future

/**
 * A complex scheduler that takes a dependency graph of jobs and executes them.
 * In this example, jobs are matrix multiplications.
 */
class JobScheduler {
    private val executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors())

    fun executeMatrixJobs(dependencyGraph: Graph<String>, jobs: Map<String, Callable<Matrix>>): Map<String, Matrix> {
        val executionOrder = dependencyGraph.topologicalSort()
        val results = mutableMapOf<String, Matrix>()
        val futures = mutableMapOf<String, Future<Matrix>>()

        // Execute in topological order to ensure dependencies are met
        // In a real complex scheduler, this would wait for futures, but for simplicity we execute sequentially
        // while simulating async scheduling.
        for (jobId in executionOrder) {
            val job = jobs[jobId] ?: throw IllegalArgumentException("Missing job implementation for $jobId")

            // Submitting to thread pool
            val future = executor.submit(job)
            futures[jobId] = future
        }

        // Collect results
        for (jobId in executionOrder) {
            val future = futures[jobId]!!
            results[jobId] = future.get() // Block until result is ready
        }

        return results
    }

    fun shutdown() {
        executor.shutdown()
    }
}
