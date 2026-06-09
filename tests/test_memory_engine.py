from pathlib import Path

from memory_engine.core import index_vault, search_index


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_index_vault_extracts_metadata_links_and_backlinks(tmp_path: Path) -> None:
    write(
        tmp_path / "A.md",
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
        tmp_path / "B.md",
        """# B

Beta body.
""",
    )

    index = index_vault(tmp_path, vault_name="TestVault")
    assert index.stats["records"] == 2
    alpha = next(record for record in index.records if record.path == "A.md")
    beta = next(record for record in index.records if record.path == "B.md")
    assert alpha.metadata["type"] == "project"
    assert "memory" in alpha.tags
    assert alpha.outgoing_paths == ["B.md"]
    assert beta.backlinks == ["A.md"]
    assert alpha.obsidian_uri.startswith("obsidian://open?vault=TestVault")


def test_search_scores_title_and_tags(tmp_path: Path) -> None:
    write(tmp_path / "Memory.md", "# Memory Engine\n\n#agent-memory\n")
    write(tmp_path / "Other.md", "# Other\n\nplain note\n")
    index = index_vault(tmp_path)
    results = search_index(index, "memory", limit=1)
    assert results[0][1].path == "Memory.md"
