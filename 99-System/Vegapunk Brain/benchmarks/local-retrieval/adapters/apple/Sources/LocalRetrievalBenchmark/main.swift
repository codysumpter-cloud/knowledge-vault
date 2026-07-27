import CryptoKit
import Foundation

private let dimension = 256

private struct Request: Decodable {
    let op: String
    let texts: [String]?
}

private func tokens(_ text: String) -> [String] {
    text.lowercased().split { !$0.isLetter && !$0.isNumber && $0 != "-" && $0 != "_" }.map(String.init)
}

private func embedding(_ text: String) -> [Double] {
    var vector = Array(repeating: 0.0, count: dimension)
    let base = tokens(text)
    let bigrams = zip(base, base.dropFirst()).map { "\($0)::\($1)" }
    for feature in base + bigrams {
        let digest = SHA256.hash(data: Data(feature.utf8))
        let bytes = Array(digest)
        let index = bytes.prefix(4).reduce(0) { ($0 << 8) | Int($1) } % dimension
        vector[index] += bytes[4].isMultiple(of: 2) ? 1 : -1
    }
    let norm = sqrt(vector.reduce(0) { $0 + $1 * $1 })
    return norm == 0 ? vector : vector.map { $0 / norm }
}

private func write(_ value: Any) throws {
    let data = try JSONSerialization.data(withJSONObject: value, options: [.sortedKeys])
    print(String(decoding: data, as: UTF8.self))
}

while let line = readLine() {
    guard !line.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { continue }
    let request = try JSONDecoder().decode(Request.self, from: Data(line.utf8))
    switch request.op {
    case "metadata":
        try write(["metadata": [
            "name": "hash-ngram-apple-baseline",
            "runtime": "swift",
            "model": "none",
            "model_download_mb": 0,
            "offline": true,
            "native_acceleration": false,
            "browser_fallback": false,
            "dimension": dimension,
        ]])
    case "embed":
        try write(["vectors": (request.texts ?? []).map(embedding)])
    default:
        fputs("unsupported request\n", stderr)
        exit(2)
    }
}
