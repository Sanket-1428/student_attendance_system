# Problem Statement

## Problem
Manual attendance registers are slow to summarize and make it difficult to identify students below a required attendance percentage. The supplied starter marks attendance but keeps students and statistics in memory, so information does not persist reliably between runs.

## Scope
This is a local, single-user CLI application. It manages student and subject lists, stores dated present/absent records in SQLite, and calculates session totals and attendance percentages. Records and reports can be filtered by subject.

## Target users
Teachers, instructors, and students building or demonstrating a small Python attendance project.

## High-level features
- Add, list, and remove student records.
- Add and list subjects.
- Record attendance for a student and subject on a date.
- View attendance records and percentage summaries.
- Find students below a configurable threshold.

Authentication, multi-user access, a GUI, and cloud synchronization are outside scope.
