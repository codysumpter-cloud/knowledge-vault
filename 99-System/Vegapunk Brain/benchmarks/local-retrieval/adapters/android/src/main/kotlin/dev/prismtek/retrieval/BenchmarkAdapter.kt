package dev.prismtek.retrieval

import java.security.MessageDigest
import kotlin.math.sqrt

private const val dimension = 256

private fun embedding(text: String): List<Double> {
    val vector = DoubleArray(dimension)
    val base = Regex("[a-z0-9_-]+").findAll(text.lowercase()).map { it.value }.toList()
    val features = base + base.zipWithNext { left, right -> "$left::$right" }
    for (feature in features) {
        val digest = MessageDigest.getInstance("SHA-256").digest(feature.toByteArray())
        val index = ((digest[0].toInt() and 0xff) shl 24 or
            ((digest[1].toInt() and 0xff) shl 16) or
            ((digest[2].toInt() and 0xff) shl 8) or
            (digest[3].toInt() and 0xff)).ushr(1) % dimension
        vector[index] += if ((digest[4].toInt() and 1) == 0) 1.0 else -1.0
    }
    val norm = sqrt(vector.sumOf { it * it }).takeIf { it > 0 } ?: 1.0
    return vector.map { it / norm }
}

// Minimal JSONL baseline without third-party JSON dependencies. Production LiteRT adapters should
// use a real JSON codec and preserve the documented metadata/embed protocol.
fun main() {
    generateSequence(::readLine).filter { it.isNotBlank() }.forEach { line ->
        when {
            line.contains("\"op\":\"metadata\"") || line.contains("\"op\": \"metadata\"") ->
                println("{\"metadata\":{\"name\":\"hash-ngram-android-baseline\",\"runtime\":\"kotlin-jvm\",\"model\":\"none\",\"model_download_mb\":0,\"offline\":true,\"native_acceleration\":false,\"browser_fallback\":false,\"dimension\":$dimension}}")
            line.contains("\"op\":\"embed\"") || line.contains("\"op\": \"embed\"") -> {
                System.err.println("The dependency-free Android baseline only proves metadata/build wiring; use the Python or web adapter for executable CI until a JSON codec/LiteRT adapter is selected.")
                kotlin.system.exitProcess(3)
            }
            else -> kotlin.system.exitProcess(2)
        }
    }
}
