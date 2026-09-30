"""Attendance analytics and threshold reporting."""
import sqlite3


def attendance_summary(db: sqlite3.Connection, subject_id: int | None = None) -> list[dict]:
    """Return session totals and attendance percentages for each student."""
    query = """SELECT st.id, st.name, COUNT(a.id) AS sessions,
                      SUM(CASE WHEN a.status='present' THEN 1 ELSE 0 END) AS present
               FROM students st LEFT JOIN attendance a ON a.student_id=st.id"""
    params: tuple = ()
    if subject_id is not None:
        query += " AND a.subject_id = ?"
        params = (subject_id,)
    query += " GROUP BY st.id, st.name ORDER BY st.name COLLATE NOCASE"
    rows = db.execute(query, params).fetchall()
    result = []
    for row in rows:
        sessions = row["sessions"]
        present = row["present"] or 0
        result.append({"id": row["id"], "name": row["name"], "sessions": sessions,
                       "present": present, "percentage": (present / sessions * 100) if sessions else 0.0})
    return result


def below_threshold(db: sqlite3.Connection, threshold: float,
                    subject_id: int | None = None) -> list[dict]:
    if not 0 <= threshold <= 100:
        raise ValueError("Threshold must be between 0 and 100.")
    return [item for item in attendance_summary(db, subject_id)
            if item["sessions"] and item["percentage"] < threshold]
