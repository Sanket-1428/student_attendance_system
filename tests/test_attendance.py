"""Unit tests for repository and reporting behavior."""
import unittest
from attendance_system.analytics import attendance_summary, below_threshold
from attendance_system.database import connect
from attendance_system.processing import mark_session
from attendance_system.repository import AttendanceRepository


class AttendanceTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(":memory:")
        self.repo = AttendanceRepository(self.db)
        self.student = self.repo.add_student("Asha Rao")
        self.subject = self.repo.add_subject("Python")

    def tearDown(self):
        self.db.close()

    def test_crud_rejects_duplicates_and_removes_student(self):
        with self.assertRaises(ValueError):
            self.repo.add_student("asha rao")
        self.assertTrue(self.repo.remove_student(self.student))
        self.assertFalse(self.repo.remove_student(self.student))

    def test_mark_and_percentage_report(self):
        second = self.repo.add_student("Dev Kumar")
        self.assertEqual(mark_session(self.repo, self.subject, "2026-09-30",
                                      {self.student: "present", second: "absent"}), 2)
        result = attendance_summary(self.db, self.subject)
        self.assertEqual(result[0]["percentage"], 100.0)
        self.assertEqual([x["name"] for x in below_threshold(self.db, 75, self.subject)], ["Dev Kumar"])

    def test_duplicate_date_rolls_back_whole_session(self):
        self.repo.record_attendance(self.student, self.subject, "2026-09-30", "present")
        second = self.repo.add_student("Dev Kumar")
        with self.assertRaises(Exception):
            mark_session(self.repo, self.subject, "2026-09-30",
                         {second: "present", self.student: "absent"})
        self.assertEqual(len(self.repo.records()), 1)

    def test_validation(self):
        with self.assertRaises(ValueError):
            self.repo.record_attendance(self.student, self.subject, "30-09-2026", "present")
        with self.assertRaises(ValueError):
            below_threshold(self.db, 101)


if __name__ == "__main__":
    unittest.main()
