# Android adapter

This Kotlin/JVM scaffold reserves the JSONL adapter boundary for an Android LiteRT implementation and proves that the baseline package can be built without committing a model.

The dependency-free baseline currently implements metadata only. That limitation is explicit: embedding is blocked until the chosen LiteRT model and JSON dependency are pinned and tested on an Android device. Do not claim native acceleration or retrieval quality from this scaffold alone.
