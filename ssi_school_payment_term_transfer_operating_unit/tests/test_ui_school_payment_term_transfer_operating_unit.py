# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolPaymentTermTransferOperatingUnit(HttpSavepointCase):
    """Tour test for the Operating Unit IK extension.

    ``base.user_admin`` is already a member of
    ``operating_unit.group_manager_operating_unit`` (see
    ``operating_unit/security/operating_unit_security.xml``), which
    implies ``group_multi_operating_unit`` -- so the Operating Unit
    field is visible to the tour's ``admin`` login without any extra
    group setup here.
    """

    @classmethod
    def setUpClass(cls):
        """Create an Enrollment whose School has exactly one Operating Unit.

        Mirrors ``ssi_school_payment_term_transfer``'s own
        ``test_ui_school_payment_term_transfer.py`` fixture, minus the
        parts this delta tour never reaches (payment terms, lines) --
        the tour stops right after selecting Enrollment, so the
        document is never saved. The enrollment still needs to reach
        ``open``: ``enrollment_id``'s field domain on the transfer form
        is ``[("state", "=", "open")]``, so a draft enrollment would
        never appear in the Select step's dropdown. See that sibling
        file's docstring for why ``action_open_enrollment()`` then
        ``action_open()`` are used instead of ``write({"state": ...})``.
        """
        super().setUpClass()
        partner = cls.env["res.partner"].create(
            {"name": "TOUR PTTOU Operating Unit Partner"}
        )
        operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR PTTOU Operating Unit",
                "code": "TPTTOU",
                "partner_id": partner.id,
            }
        )
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR PTTOU Grade Type", "code": "TPTTOUGT"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR PTTOU School",
                "code": "TPTTOUSC",
                "grade_type_id": grade_type.id,
                "operating_unit_ids": [(6, 0, [operating_unit.id])],
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR PTTOU Academic Year",
                "code": "TPTTOUAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR PTTOU Term",
                "code": "TPTTOUTM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR PTTOU Grade",
                "code": "TPTTOUGR",
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR PTTOU Class",
                "code": "TPTTOUCL",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR PTTOU Contact"})
        student = cls.env["school_student"].create(
            {
                "name": "TOUR PTTOU Student",
                "code": "TPTTOUST",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        cls.tour_enrollment = cls.env["school_enrollment"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        academic_term.action_open_enrollment()
        cls.tour_enrollment.write({"name": "TOUR PTTOU Enrollment"})
        cls.tour_enrollment.with_context(bypass_policy_check=True).action_open()

    def test_create(self):
        """Run the create-delta tour for the Operating Unit IK extension.

        IK: docs/school_payment_term_transfer/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_operating_unit_create",
            login="admin",
        )
