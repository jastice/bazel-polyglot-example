package com.example.math

import kotlin.math.abs

/**
 * A complex class for matrix operations with immutable state.
 */
class Matrix(val data: Array<DoubleArray>) {
    val rows: Int = data.size
    val cols: Int = if (data.isNotEmpty()) data[0].size else 0

    init {
        require(data.all { it.size == cols }) { "All rows must have the same number of columns" }
    }

    operator fun plus(other: Matrix): Matrix {
        require(this.rows == other.rows && this.cols == other.cols) { "Matrix dimensions must match for addition" }
        return Matrix(Array(rows) { i ->
            DoubleArray(cols) { j -> this.data[i][j] + other.data[i][j] }
        })
    }

    operator fun times(other: Matrix): Matrix {
        require(this.cols == other.rows) { "Incompatible matrices for multiplication" }
        val result = Array(this.rows) { DoubleArray(other.cols) }
        for (i in 0 until this.rows) {
            for (j in 0 until other.cols) {
                var sum = 0.0
                for (k in 0 until this.cols) {
                    sum += this.data[i][k] * other.data[k][j]
                }
                result[i][j] = sum
            }
        }
        return Matrix(result)
    }

    fun transpose(): Matrix {
        return Matrix(Array(cols) { i ->
            DoubleArray(rows) { j -> this.data[j][i] }
        })
    }

    override fun toString(): String {
        return data.joinToString(separator = "\n") { row -> row.joinToString(separator = "\t") { String.format("%.2f", it) } }
    }
}
