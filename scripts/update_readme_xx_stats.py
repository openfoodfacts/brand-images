"""Update the README stats section with per-folder counts from xx/.

Usage:
    python3 scripts/update_readme_xx_stats.py
"""

from __future__ import annotations

import datetime
from pathlib import Path

README_HEADING = "## Stats"


def count_files(folder: Path) -> int:
    return sum(1 for path in folder.rglob("*") if path.is_file())


def build_table(xx_dir: Path) -> str:
    today = datetime.date.today().strftime("%Y-%m-%d")
    subdirs = sorted(path for path in xx_dir.iterdir() if path.is_dir())
    rows = [(subdir.name, count_files(subdir)) for subdir in subdirs]

    lines = [
        "| Folder | Items |",
        "|--------|------:|",
    ]
    for name, count in rows:
        folder_path = f"xx/{name}"
        lines.append(f"| `{folder_path}` | {count} |")
    lines.append("")
    lines.append(f"Last updated: {today}")
    return "\n".join(lines)


def find_section_bounds(lines: list[str], heading: str) -> tuple[int, int]:
    start = next((idx for idx, line in enumerate(lines) if line.strip() == heading), -1)
    if start == -1:
        raise RuntimeError(f"Could not find heading: {heading}")

    end = len(lines)
    for idx in range(start + 1, len(lines)):
        if lines[idx].startswith("## "):
            end = idx
            break

    return start, end


def update_readme(readme_path: Path, table: str) -> None:
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    start, end = find_section_bounds(lines, README_HEADING)

    new_section = [
        lines[start],
        "",
        "<!-- AUTO-GENERATED: XX_STATS_START -->",
        table,
        "<!-- AUTO-GENERATED: XX_STATS_END -->",
        "",
    ]

    updated = lines[:start] + new_section + lines[end:]
    readme_path.write_text("\n".join(updated).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    readme_path = repo_root / "README.md"
    xx_dir = repo_root / "xx"

    if not xx_dir.exists() or not xx_dir.is_dir():
        raise RuntimeError(f"Missing xx directory: {xx_dir}")

    table = build_table(xx_dir)
    update_readme(readme_path, table)
    print(f"Updated {readme_path}")


if __name__ == "__main__":
    main()
