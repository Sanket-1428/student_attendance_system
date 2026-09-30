"""Command-line interface for the attendance system."""
import argparse
import logging
from datetime import date
from pathlib import Path
from .analytics import attendance_summary, below_threshold
from .database import connect
from .repository import AttendanceRepository

LOGGER = logging.getLogger("attendance_system")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="attendance", description="Student attendance manager")
    root.add_argument("--db", default="attendance.db", help="SQLite database path")
    root.add_argument("--verbose", action="store_true", help="Show diagnostic messages")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Create the database")
    add = commands.add_parser("add-student", help="Add a student")
    add.add_argument("name")
    commands.add_parser("list-students", help="List students")
    remove = commands.add_parser("remove-student", help="Remove a student by ID")
    remove.add_argument("student_id", type=int)
    subject = commands.add_parser("add-subject", help="Add a subject")
    subject.add_argument("name")
    commands.add_parser("list-subjects", help="List subjects")
    mark = commands.add_parser("mark", help="Mark one attendance record")
    mark.add_argument("student_id", type=int)
    mark.add_argument("subject_id", type=int)
    mark.add_argument("status", choices=("present", "absent"))
    mark.add_argument("--date", default=date.today().isoformat(), dest="session_date")
    records = commands.add_parser("records", help="Display attendance records")
    records.add_argument("--subject", type=int, dest="subject_id")
    report = commands.add_parser("report", help="Show attendance percentages")
    report.add_argument("--subject", type=int, dest="subject_id")
    threshold = commands.add_parser("below-threshold", help="List students below a percentage")
    threshold.add_argument("percentage", type=float)
    threshold.add_argument("--subject", type=int, dest="subject_id")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING,
                        format="%(levelname)s: %(message)s")
    db = None
    try:
        db = connect(Path(args.db).expanduser())
        repo = AttendanceRepository(db)
        if args.command == "init":
            print(f"Database ready: {args.db}")
        elif args.command == "add-student":
            print(f"Added student #{repo.add_student(args.name)}")
        elif args.command == "list-students":
            for row in repo.list_students(): print(f"{row['id']}\t{row['name']}")
        elif args.command == "remove-student":
            if not repo.remove_student(args.student_id): raise ValueError("Student ID not found.")
            print("Student removed.")
        elif args.command == "add-subject":
            print(f"Added subject #{repo.add_subject(args.name)}")
        elif args.command == "list-subjects":
            for row in repo.list_subjects(): print(f"{row['id']}\t{row['name']}")
        elif args.command == "mark":
            repo.record_attendance(args.student_id, args.subject_id, args.session_date, args.status)
            print("Attendance saved.")
        elif args.command == "records":
            for row in repo.records(args.subject_id):
                print(f"{row['session_date']}\t{row['subject']}\t{row['student']}\t{row['status']}")
        elif args.command == "report":
            for item in attendance_summary(db, args.subject_id):
                print(f"{item['id']}\t{item['name']}\t{item['present']}/{item['sessions']}\t{item['percentage']:.2f}%")
        elif args.command == "below-threshold":
            matches = below_threshold(db, args.percentage, args.subject_id)
            for item in matches: print(f"{item['name']}\t{item['percentage']:.2f}%")
            if not matches: print("No students below threshold.")
        return 0
    except (ValueError, OSError) as exc:
        LOGGER.error("%s", exc)
        print(f"Error: {exc}")
        return 2
    except Exception:
        LOGGER.exception("Unexpected failure")
        print("Error: unexpected failure; run with --verbose for details.")
        return 1
    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    raise SystemExit(main())
