# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolPaymentTermTransferAdmissionOperatingUnit(HttpSavepointCase):
    """Tour test for the Admission-path Operating Unit IK extension.

    ``base.user_admin`` is already a member of
    ``operating_unit.group_manager_operating_unit`` (see
    ``operating_unit/security/operating_unit_security.xml``), which
    implies ``group_multi_operating_unit`` -- so the Operating Unit
    field is visible to the tour's ``admin`` login without any extra
    group setup here.
    """

    @classmethod
    def setUpClass(cls):
        """Create an open Admission whose School has one Operating Unit.

        The tour stops right after selecting Admission, so the
        transfer document is never saved -- payment terms and lines
        are never reached and are not created here.
        ``admission_id``'s field domain on the transfer form is
        ``[("state", "=", "open")]``, so the fixture is confirmed and
        approved -- mirroring
        ``ssi_school_payment_term_transfer_admission``'s own
        ``test_data_school_payment_term_transfer_admission.yaml``
        fixture -- rather than written directly to ``state`` (see
        ``odoo-development-ui-test`` skill, "Prasyarat state fixture
        dicapai lewat action method").
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        partner = cls.env["res.partner"].create(
            {"name": "TOUR PTTAOU Operating Unit Partner"}
        )
        operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR PTTAOU Operating Unit",
                "code": "TPTTAOU",
                "partner_id": partner.id,
            }
        )
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR PTTAOU Grade Type", "code": "TPTTAOUGT"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR PTTAOU School",
                "code": "TPTTAOUSC",
                "grade_type_id": grade_type.id,
                "operating_unit_ids": [(6, 0, [operating_unit.id])],
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR PTTAOU Academic Year",
                "code": "TPTTAOUAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR PTTAOU Term",
                "code": "TPTTAOUTM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR PTTAOU Grade",
                "code": "TPTTAOUGR",
                "type_id": grade_type.id,
            }
        )
        # Admission's Student is res.partner, not school_student.
        student = cls.env["res.partner"].create({"name": "TOUR PTTAOU Student"})
        admission = (
            cls.env["school_admission"]
            .with_user(admin)
            .create(
                {
                    "academic_year_id": academic_year.id,
                    "academic_term_id": academic_term.id,
                    "school_id": school.id,
                    "grade_id": grade.id,
                    "student_id": student.id,
                }
            )
        )
        # bypass_policy_check -- pure fixture setup, not testing the
        # confirm/approve transition itself. Without it, approve_ok's
        # non-stored compute reads a stale pre-confirm cache and the
        # approval fails nondeterministically (T-04, Python jalur).
        admission_setup = admission.with_context(bypass_policy_check=True)
        admission_setup.action_confirm()
        admission_setup.action_approve_approval()
        admission.write({"name": "TOUR PTTAOU Admission"})
        cls.tour_admission = admission

    def test_create(self):
        """Run the create-delta tour for the Admission-path OU field.

        IK: docs/school_payment_term_transfer/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_admission_operating_unit_create",
            login="admin",
        )
