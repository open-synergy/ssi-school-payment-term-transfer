# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolPaymentTermTransfer(HttpSavepointCase):
    """Tour tests for ``school_payment_term_transfer`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the enrollment, terms, and fixture documents for the tours.

        The enrollment is forced to ``open`` directly through the ORM --
        exercising its own approval workflow is out of scope for this
        module's tours. The edit/delete fixture documents get
        ``user_id`` set explicitly to ``base.user_admin``: ``cls.env``
        runs as superuser, and
        ``school_payment_term_transfer_internal_user_rule`` would
        otherwise hide them from the ``admin`` session the tours log
        in as.
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR PTT Grade Type", "code": "TPTTGT"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR PTT School",
                "code": "TPTTSC",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR PTT Academic Year",
                "code": "TPTTAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR PTT Term",
                "code": "TPTTTM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR PTT Grade",
                "code": "TPTTGR",
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR PTT Class",
                "code": "TPTTCL",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR PTT Contact"})
        student = cls.env["school_student"].create(
            {
                "name": "TOUR PTT Student",
                "code": "TPTTST",
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
        cls.tour_enrollment.write({"state": "open"})
        account_type_income = cls.env.ref("account.data_account_type_revenue")
        income_account = cls.env["account.account"].create(
            {
                "name": "TOUR PTT Income Account",
                "code": "TPTTIA",
                "user_type_id": account_type_income.id,
                "reconcile": False,
            }
        )
        product = cls.env["product.product"].create(
            {"name": "TOUR PTT Product", "type": "service"}
        )
        cls.tour_source_term = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.tour_enrollment.id,
                "name": "TOUR PTT Source Term",
            }
        )
        cls.tour_destination_term = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.tour_enrollment.id,
                "name": "TOUR PTT Destination Term",
            }
        )
        uom_unit = cls.env.ref("uom.product_uom_unit")
        detail_vals = {
            "term_id": cls.tour_source_term.id,
            "product_id": product.id,
            "account_id": income_account.id,
            "uom_id": uom_unit.id,
            "uom_quantity": 1.0,
            "price_unit": 100000.0,
        }
        cls.tour_detail_create = cls.env[
            "school_enrollment_payment_term_detail"
        ].create(dict(detail_vals, name="TOUR PTT Detail Create"))
        detail_edit = cls.env["school_enrollment_payment_term_detail"].create(
            dict(detail_vals, name="TOUR PTT Detail Edit")
        )
        detail_delete = cls.env["school_enrollment_payment_term_detail"].create(
            dict(detail_vals, name="TOUR PTT Detail Delete")
        )
        cls.tour_reason_create = cls.env["school_payment_term_transfer_reason"].create(
            {"name": "TOUR PTT Reason Create", "code": "/"}
        )
        reason_edit = cls.env["school_payment_term_transfer_reason"].create(
            {"name": "TOUR PTT Reason Edit", "code": "/"}
        )
        reason_delete = cls.env["school_payment_term_transfer_reason"].create(
            {"name": "TOUR PTT Reason Delete", "code": "/"}
        )
        cls.tour_edit_doc = cls.env["school_payment_term_transfer"].create(
            {
                "user_id": admin.id,
                "enrollment_id": cls.tour_enrollment.id,
                "reason_id": reason_edit.id,
                "source_term_id": cls.tour_source_term.id,
                "destination_term_id": cls.tour_destination_term.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "source_detail_id": detail_edit.id,
                            "amount_before": 100000.0,
                            "amount": 25000.0,
                        },
                    )
                ],
            }
        )
        cls.tour_delete_doc = cls.env["school_payment_term_transfer"].create(
            {
                "user_id": admin.id,
                "enrollment_id": cls.tour_enrollment.id,
                "reason_id": reason_delete.id,
                "source_term_id": cls.tour_source_term.id,
                "destination_term_id": cls.tour_destination_term.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "source_detail_id": detail_delete.id,
                            "amount_before": 100000.0,
                            "amount": 10000.0,
                        },
                    )
                ],
            }
        )

    def test_create(self):
        """Run the create tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_delete",
            login="admin",
        )
