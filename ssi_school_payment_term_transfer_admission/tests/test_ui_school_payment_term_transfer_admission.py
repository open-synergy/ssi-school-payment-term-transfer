# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolPaymentTermTransferAdmission(HttpSavepointCase):
    """Tour tests for the Admission-path payment term transfer delta."""

    @classmethod
    def setUpClass(cls):
        """Create the admission and the Confirm-state fixture document.

        The admission is opened through its own ``action_open()``
        (``mixin.transaction_open``, ``_after_approved_method =
        "action_open"`` on ``school_admission``) with ``bypass_
        policy_check`` in the context, mirroring exactly how
        ``ssi_school_payment_term_transfer``'s own tour test opens its
        Enrollment fixture -- exercising the admission's own approval
        workflow is out of scope for this module's tours. The Approve
        fixture document is then confirmed the same way
        (``action_confirm`` with ``bypass_policy_check``), so the
        Approve tour starts from ``confirm`` without depending on the
        Confirm tour having run first.

        :return: None
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR PTTA Grade Type", "code": "TPTTAGT"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR PTTA School",
                "code": "TPTTASC",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR PTTA Academic Year",
                "code": "TPTTAAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR PTTA Term",
                "code": "TPTTATM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR PTTA Grade",
                "code": "TPTTAGR",
                "type_id": grade_type.id,
            }
        )
        student = cls.env["res.partner"].create({"name": "TOUR PTTA Student"})
        cls.tour_admission = cls.env["school_admission"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "student_id": student.id,
                "currency_id": cls.env.company.currency_id.id,
            }
        )
        cls.tour_admission.with_context(bypass_policy_check=True).action_open()

        account_type_income = cls.env.ref("account.data_account_type_revenue")
        income_account = cls.env["account.account"].create(
            {
                "name": "TOUR PTTA Income Account",
                "code": "TPTTAIA",
                "user_type_id": account_type_income.id,
                "reconcile": False,
            }
        )
        product = cls.env["product.product"].create(
            {"name": "TOUR PTTA Product", "type": "service"}
        )
        cls.tour_source_term = cls.env["school_admission_payment_term"].create(
            {
                "admission_id": cls.tour_admission.id,
                "name": "TOUR PTTA Source Term",
            }
        )
        cls.tour_destination_term = cls.env["school_admission_payment_term"].create(
            {
                "admission_id": cls.tour_admission.id,
                "name": "TOUR PTTA Destination Term",
            }
        )
        uom_unit = cls.env.ref("uom.product_uom_unit")
        detail = cls.env["school_admission_payment_term_detail"].create(
            {
                "term_id": cls.tour_source_term.id,
                "product_id": product.id,
                "name": "TOUR PTTA Detail Approve",
                "account_id": income_account.id,
                "uom_id": uom_unit.id,
                "uom_quantity": 1.0,
                "price_unit": 100000.0,
            }
        )
        reason = cls.env["school_payment_term_transfer_reason"].create(
            {"name": "TOUR PTTA Reason Approve", "code": "/"}
        )
        cls.tour_approve_doc = cls.env["school_payment_term_transfer"].create(
            {
                "user_id": admin.id,
                "source_type": "admission",
                "admission_id": cls.tour_admission.id,
                "reason_id": reason.id,
                "admission_source_term_id": cls.tour_source_term.id,
                "admission_destination_term_id": cls.tour_destination_term.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "admission_source_detail_id": detail.id,
                            "amount_before": 100000.0,
                            "amount": 25000.0,
                        },
                    )
                ],
            }
        )
        cls.tour_approve_doc.with_context(bypass_policy_check=True).action_confirm()

    def test_school_payment_term_transfer_admission_create(self):
        """Run the create tour, Admission path (Additional Fields delta).

        IK: docs/school_payment_term_transfer/01-create.md
        """
        self.start_tour(
            "/web", "ssi_school_payment_term_transfer_admission_create", login="admin"
        )

    def test_school_payment_term_transfer_admission_approve(self):
        """Run the approve tour, Admission path (Additional Post-Condition).

        IK: docs/school_payment_term_transfer/05-approve.md
        """
        self.start_tour(
            "/web", "ssi_school_payment_term_transfer_admission_approve", login="admin"
        )
