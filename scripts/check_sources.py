"""Validate notebook structure and Python syntax without executing analysis."""
import ast
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in root.rglob("*.py"):
    if not any(part.startswith(".") for part in path.relative_to(root).parts):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
for path in root.rglob("*.ipynb"):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4, path
    language = notebook.get("metadata", {}).get("kernelspec", {}).get("language", "python").lower()
    source = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell.get("outputs") == [], path
            assert cell.get("execution_count") is None, path
            assert not any(key in cell.get("metadata", {}) for key in ("execution", "ExecuteTime", "widgets", "trusted")), path
            source.append("".join(cell["source"]))
    if language == "python":
        ast.parse("\n\n".join(source), filename=str(path))
for path in root.glob("config*.json"):
    json.loads(path.read_text(encoding="utf-8"))
print("Notebook structure and Python syntax are valid. No analysis was executed.")
