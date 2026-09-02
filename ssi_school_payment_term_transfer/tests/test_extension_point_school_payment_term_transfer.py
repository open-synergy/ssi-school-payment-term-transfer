# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestExtensionPointSchoolPaymentTermTransfer(YamlTransactionCase):
    """Lock the return values of the five extension point methods.

    Pure Python -- trigger P1 (L-01: the ``call`` action discards the
    return value of a method, so YAML cannot assert what ``_get_
    owner_document``, ``_get_term_owner``, ``_get_destination_detail_
    model`` and ``_get_source_detail`` return; L-02: every assert's
    "actual" side is a dotted ``getattr`` on a record already in the
    registry, so YAML cannot assert a bare string return value like
    ``_get_destination_detail_model`` produces either). Builds one
    enrollment-side transfer document with a source term, a
    destination term and one line, then asserts each extension
    point's parent implementation returns exactly what the code it
    replaced used to read directly.
    """

    def _create_fixtures(self):
        """Build one transfer document with a source/destination term.

        Reused by every ``test_*`` method below so each one only has
        to call the extension point and assert its return value.

        :return: ``(transfer, line)`` tuple of the created
            ``school_payment_term_transfer`` and its single
            ``school_payment_term_transfer_line``.
        """
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type for Extension Point Test",
                "code": "GTEXTPT",
                "sequence": 10,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School for Extension Point Test",
                "code": "SCEXTPT",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "Academic Year for Extension Point Test",
                "code": "AYEXTPT",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Academic Term for Extension Point Test",
                "code": "ATEXTPT",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade for Extension Point Test",
                "code": "GREXTPT",
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Grade Class for Extension Point Test",
                "code": "GCEXTPT",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Extension Point Student Contact"}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student for Extension Point Test",
                "code": "STEXTPT",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = self.env["school_enrollment"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        income_type = self.env.ref("account.data_account_type_revenue")
        income_account = self.env["account.account"].create(
            {
                "name": "Extension Point Income Account",
                "code": "EXTPTIA",
                "user_type_id": income_type.id,
                "reconcile": False,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Extension Point Product",
                "type": "service",
            }
        )
        reason = self.env["school_payment_term_transfer_reason"].create(
            {
                "name": "Extension Point Reason",
                "code": "EXTPTRS",
            }
        )
        source_term = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "Extension Point Source Term",
            }
        )
        destination_term = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "Extension Point Destination Term",
            }
        )
        uom_unit = self.env.ref("uom.product_uom_unit")
        source_detail = self.env["school_enrollment_payment_term_detail"].create(
            {
                "term_id": source_term.id,
                "product_id": product.id,
                "name": "Extension Point Fee",
                "account_id": income_account.id,
                "uom_id": uom_unit.id,
                "uom_quantity": 1.0,
                "price_unit": 100000.0,
            }
        )
        transfer = self.env["school_payment_term_transfer"].create(
            {
                "enrollment_id": enrollment.id,
                "reason_id": reason.id,
                "source_term_id": source_term.id,
                "destination_term_id": destination_term.id,
            }
        )
        line = self.env["school_payment_term_transfer_line"].create(
            {
                "transfer_id": transfer.id,
                "source_detail_id": source_detail.id,
                "amount_before": 100000.0,
                "amount": 25000.0,
            }
        )
        return transfer, line

    def test_get_owner_document_returns_enrollment(self):
        """``_get_owner_document`` returns the document's ``enrollment_id``.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        transfer, _line = self._create_fixtures()
        self.assertEqual(transfer._get_owner_document(), transfer.enrollment_id)

    def test_get_term_owner_returns_enrollment_for_source_term(self):
        """``_get_term_owner`` on the source term returns its enrollment.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        transfer, _line = self._create_fixtures()
        owner = transfer._get_term_owner(transfer.source_term_id)
        self.assertEqual(owner, transfer.enrollment_id)

    def test_get_term_owner_returns_enrollment_for_destination_term(self):
        """``_get_term_owner`` on the destination term returns its enrollment.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        transfer, _line = self._create_fixtures()
        owner = transfer._get_term_owner(transfer.destination_term_id)
        self.assertEqual(owner, transfer.enrollment_id)

    def test_get_destination_detail_model_returns_model_name(self):
        """``_get_destination_detail_model`` returns the detail model name.

        Pure Python -- trigger P1 (L-01: the return value is a bare
        string, and L-02: YAML's assert can only read a dotted
        ``getattr`` on a record already in the registry, never a
        method's return value), see the class docstring.
        """
        transfer, _line = self._create_fixtures()
        self.assertEqual(
            transfer._get_destination_detail_model(),
            "school_enrollment_payment_term_detail",
        )

    def test_get_source_detail_returns_source_detail_id(self):
        """``_get_source_detail`` on the line returns its source detail.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        _transfer, line = self._create_fixtures()
        self.assertEqual(line._get_source_detail(), line.source_detail_id)
