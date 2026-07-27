// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "LocalRetrievalBenchmark",
    platforms: [.macOS(.v14)],
    products: [.executable(name: "local-retrieval-apple", targets: ["LocalRetrievalBenchmark"])],
    targets: [.executableTarget(name: "LocalRetrievalBenchmark")]
)
