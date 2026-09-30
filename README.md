# Student Attendance System

A lightweight CLI attendance app based on the supplied Tkinter starter. It manages students and subjects, records dated attendance in SQLite, and reports percentages.

## Features
- Student and subject create/list operations, plus student removal.
- Dated attendance with duplicate-session protection.
- Attendance summaries and below-threshold reports.
- SQLite persistence, validation, transaction rollback, and diagnostic logging.
- Python standard-library runtime; no third-party dependencies.

## Technologies
Python 3.10+, SQLite (`sqlite3`), `argparse`, and `unittest`.

## Setup and run

```sh
python -m attendance_system.cli init
```

Example workflow:

```sh
python -m attendance_system.cli add-student "Asha Rao"
python -m attendance_system.cli add-subject "Python Essentials"
python -m attendance_system.cli list-students
python -m attendance_system.cli list-subjects
python -m attendance_system.cli mark 1 1 present --date 2026-09-30
python -m attendance_system.cli records
python -m attendance_system.cli report
python -m attendance_system.cli below-threshold 75
```

Use IDs printed during creation. Put `--db path/to/file.db` before the command to select a database. Run `python -m attendance_system.cli --help` for all commands. The default database is `attendance.db` in the current directory.

Optional editable install exposes `attendance`:

```sh
python -m pip install -e .
attendance --help
```

## Testing

```sh
python -m unittest discover -v
```

## GitHub deployment
The intended public repository is `https://github.com/Sanket-1428/student_attendance_system` (inferred from the supplied URL). Create that empty repository first, then run from the project root:

```sh
git init
git branch -M main
git add .
git commit -m "Create student attendance system"
git remote add origin https://github.com/Sanket-1428/student_attendance_system.git
git push -u origin main
```

Authenticate with `gh auth login` or Git Credential Manager. Never put an access token in source files.
