"""Attendance input validation and batch marking."""
from datetime import date
from .repository import AttendanceRepository


def mark_session(repo: AttendanceRepository, subject_id: int, session_date: str,
                 statuses: dict[int, str]) -> int:
    """Save one status per student in a single transaction."""
    try:
        date.fromisoformat(session_date)
    except ValueError as exc:
        raise ValueError("Date must use YYYY-MM-DD format.") from exc
    if not statuses:
        raise ValueError("At least one student's attendance is required.")
    normalized = {}
    for student_id, status in statuses.items():
        value = status.strip().lower()
        if value not in {"present", "absent"}:
            raise ValueError(f"Invalid status for student {student_id}: {status}")
        normalized[student_id] = value
    db = repo.db
    try:
        db.executemany(
            "INSERT INTO attendance(student_id, subject_id, session_date, status) VALUES (?, ?, ?, ?)",
            [(student_id, subject_id, session_date, status) for student_id, status in normalized.items()],
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    return len(normalized)
