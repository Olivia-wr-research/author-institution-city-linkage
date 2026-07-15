"""Request manifest and SQLite-backed resume state."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from ..schemas import RequestTask


class SQLiteTaskStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            "create table if not exists tasks (task_id text primary key, query text not null, status text not null, attempts integer not null, checkpoint text, error text)"
        )
        self.connection.commit()

    def upsert_pending(self, task: RequestTask) -> None:
        self.connection.execute(
            "insert or ignore into tasks(task_id, query, status, attempts, checkpoint, error) values (?, ?, ?, ?, ?, ?)",
            (task.task_id, task.query, task.status, task.attempts, task.checkpoint, task.error),
        )
        self.connection.commit()

    def mark(self, task_id: str, status: str, attempts: int, checkpoint: str = "", error: str = "") -> None:
        self.connection.execute(
            "update tasks set status=?, attempts=?, checkpoint=?, error=? where task_id=?",
            (status, attempts, checkpoint, error, task_id),
        )
        self.connection.commit()

    def pending(self) -> list[RequestTask]:
        rows = self.connection.execute(
            "select task_id, query, status, attempts, coalesce(checkpoint,''), coalesce(error,'') from tasks where status in ('pending','retryable') order by task_id"
        ).fetchall()
        return [RequestTask(*row) for row in rows]

    def all(self) -> list[RequestTask]:
        rows = self.connection.execute(
            "select task_id, query, status, attempts, coalesce(checkpoint,''), coalesce(error,'') from tasks order by task_id"
        ).fetchall()
        return [RequestTask(*row) for row in rows]

    def close(self) -> None:
        self.connection.close()
