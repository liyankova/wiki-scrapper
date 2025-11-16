import json
from pathlib import Path
from typing import Iterable

def save_checkpoint(path: str, visited: Iterable[str], queue: Iterable[tuple]):
    checkpoint = {
        "visited": list(visited),
        "queue": list(queue),
    }
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=2)
    tmp.replace(p)

def load_checkpoint(path: str):
    p = Path(path)
    if not p.exists():
        return set(), []
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    visited = set(data.get("visited", []))
    queue = data.get("queue", [])
    return visited, queue
