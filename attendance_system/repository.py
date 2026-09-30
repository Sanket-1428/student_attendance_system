"""Persistence layer for student, subject, and attendance CRUD."""
import sqlite3
from datetime import date


class AttendanceRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.db = connection

    def add_student(self, name: str) -> int:
        name = name.strip()
        if not name:
            raise ValueError("Student name cannot be empty.")
        try:
            cursor = self.db.execute("INSERT INTO students(name) VALUES (?)", (name,))
            self.db.commit()
            return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Student already exists: {name}") from exc

    def list_students(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT id, name FROM students ORDER BY name COLLATE NOCASE"))

    def remove_student(self, student_id: int) -> bool:
        cursor = self.db.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.db.commit()
        return cursor.rowcount == 1

    def add_subject(self, name: str) -> int:
        name = name.strip()
        if not name:
            raise ValueError("Subject name cannot be empty.")
        try:
            cursor = self.db.execute("INSERT INTO subjects(name) VALUES (?)", (name,))
            self.db.commit()
            return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Subject already exists: {name}") from exc

    def list_subjects(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT id, name FROM subjects ORDER BY name COLLATE NOCASE"))

    def record_attendance(self, student_id: int, subject_id: int, session_date: str, status: str) -> None:
        try:
            date.fromisoformat(session_date)
        except ValueError as exc:
            raise ValueError("Date must use YYYY-MM-DD format.") from exc
        normalized = status.strip().lower()
        if normalized not in {"present", "absent"}:
            raise ValueError("Status must be 'present' or 'absent'.")
        try:
            self.db.execute(
                "INSERT INTO attendance(student_id, subject_id, session_date, status) VALUES (?, ?, ?, ?)",
                (student_id, subject_id, session_date, normalized),
            )
            self.db.commit()
        except sqlite3.IntegrityError as exc:
            self.db.rollback()
            raise ValueError("Invalid student/subject or attendance already exists for that date.") from exc

    def records(self, subject_id: int | None = None) -> list[sqlite3.Row]:
        query = """SELECT a.session_date, st.name AS student, su.name AS subject, a.status
                   FROM attendance a JOIN students st ON st.id=a.student_id
                   JOIN subjects su ON su.id=a.subject_id"""
        params: tuple = ()
        if subject_id is not None:
            query += " WHERE a.subject_id = ?"
            params = (subject_id,)
        query += " ORDER BY a.session_date DESC, st.name COLLATE NOCASE"
        return list(self.db.execute(query, params))
