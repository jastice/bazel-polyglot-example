package com.example.core

/**
 * A complex looking generic Graph implementation with topological sorting
 * and cycle detection using purely functional state transitions.
 */
class Graph<T> {
    private val adjacencyList = mutableMapOf<T, MutableList<T>>()

    fun addEdge(source: T, destination: T) {
        adjacencyList.computeIfAbsent(source) { mutableListOf() }.add(destination)
        adjacencyList.computeIfAbsent(destination) { mutableListOf() } // Ensure destination exists
    }

    fun topologicalSort(): List<T> {
        val visited = mutableSetOf<T>()
        val stack = mutableListOf<T>()
        val currentPath = mutableSetOf<T>()

        fun dfs(vertex: T) {
            if (currentPath.contains(vertex)) throw IllegalStateException("Cycle detected in graph")
            if (visited.contains(vertex)) return

            currentPath.add(vertex)
            visited.add(vertex)

            adjacencyList[vertex]?.forEach { neighbor -> dfs(neighbor) }

            currentPath.remove(vertex)
            stack.add(vertex)
        }

        adjacencyList.keys.forEach { dfs(it) }
        return stack.reversed()
    }

    override fun toString(): String {
        return adjacencyList.entries.joinToString(separator = "\n") { (key, value) ->
            "$key -> ${value.joinToString()}"
        }
    }
}
