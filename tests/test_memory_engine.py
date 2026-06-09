import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from memory_engine.core import index_vault, search_index


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class MemoryEngineTests(unittest.TestCase):
    def test_index_vault_extracts_metadata_links_and_backlinks(self) -> None:
        with TemporaryDirectory() as raw:
            root = Path(raw)
            write(
                root / "A.md",
                """---
type: project
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-09
risk_level: low
privacy: public
tags: [alpha, memory]
---

# Alpha Note

> Alpha summary.

Links to [[B]].
""",
            )
            write(
                root / "B.md",
                """# B

Beta body.
""",
            )

            index = index_vault(root, vault_name="TestVault")
            self.assertEqual(index.stats["records"], 2)
            alpha = next(record for record in index.records if record.path == "A.md")
            beta = next(record for record in index.records if record.path == "B.md")
            self.assertEqual(alpha.metadata["type"], "project")
            self.assertIn("memory", alpha.tags)
            self.assertEqual(alpha.outgoing_paths, ["B.md"])
            self.assertEqual(beta.backlinks, ["A.md"])
            self.assertTrue(alpha.obsidian_uri.startswith("obsidian://open?vault=TestVault"))

    def test_search_scores_title_and_tags(self) -> None:
        with TemporaryDirectory() as raw:
            root = Path(raw)
            write(root / "Memory.md", "# Memory Engine\n\n#agent-memory\n")
            write(root / "Other.md", "# Other\n\nplain note\n")
            index = index_vault(root)
            results = search_index(index, "memory", limit=1)
            self.assertEqual(results[0][1].path, "Memory.md")


if __name__ == "__main__":
    unittest.main()
