# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestExtensionPointSchoolPaymentTermTransferAdmission(YamlTransactionCase):
    """Lock the Admission-path override of each extension point.

    Pure Python -- trigger P1 (L-01: the ``call`` action discards the
    return value of a method, so YAML cannot assert what
    ``_get_source_term``, ``_get_destination_term``, ``_get_owner_
    document``, ``_get_term_owner``, and ``_get_source_detail``
    return; L-02: every assert's "actual" side is a dotted
    ``getattr`` on a record already in the registry, so YAML cannot
    assert a bare string return value like ``_get_destination_detail_
    model`` produces either). Builds one Admission-side transfer
    document with a source term, a destination term and one line,
    then asserts each extension point's Admission override returns
    exactly what the code it replaces would otherwise read directly.
    """

    def _create_fixtures(self):
        """Build one Admission-path transfer document with one line.

        Reused by every ``test_*`` method below so each one only has
        to call the extension point and assert its return value.

        :return: ``(transfer, line)`` tuple of the created
            ``school_payment_term_transfer`` and its single
            ``school_payment_term_transfer_line``.
        """
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "Grade Type for Admission Extension Point Test",
                "code": "GTAEPT",
                "sequence": 10,
            }
        )
        school = self.env["school"].create(
            {
                "name": "School for Admission Extension Point Test",
                "code": "SCAEPT",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "Academic Year for Admission Extension Point Test",
                "code": "AYAEPT",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Academic Term for Admission Extension Point Test",
                "code": "ATAEPT",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade for Admission Extension Point Test",
                "code": "GRAEPT",
                "type_id": grade_type.id,
            }
        )
        student = self.env["res.partner"].create(
            {"name": "Admission Extension Point Student"}
        )
        admission = self.env["school_admission"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "student_id": student.id,
                "currency_id": self.env.company.currency_id.id,
            }
        )
        income_type = self.env.ref("account.data_account_type_revenue")
        income_account = self.env["account.account"].create(
            {
                "name": "Admission Extension Point Income Account",
                "code": "AEXTPTIA",
                "user_type_id": income_type.id,
                "reconcile": False,
            }
        )
        product = self.env["product.product"].create(
            {
                "name": "Admission Extension Point Product",
                "type": "service",
            }
        )
        reason = self.env["school_payment_term_transfer_reason"].create(
            {
                "name": "Admission Extension Point Reason",
                "code": "AEXTPTRS",
            }
        )
        source_term = self.env["school_admission_payment_term"].create(
            {
                "admission_id": admission.id,
                "name": "Admission Extension Point Source Term",
            }
        )
        destination_term = self.env["school_admission_payment_term"].create(
            {
                "admission_id": admission.id,
                "name": "Admission Extension Point Destination Term",
            }
        )
        uom_unit = self.env.ref("uom.product_uom_unit")
        source_detail = self.env["school_admission_payment_term_detail"].create(
            {
                "term_id": source_term.id,
                "product_id": product.id,
                "name": "Admission Extension Point Fee",
                "account_id": income_account.id,
                "uom_id": uom_unit.id,
                "uom_quantity": 1.0,
                "price_unit": 100000.0,
            }
        )
        transfer = self.env["school_payment_term_transfer"].create(
            {
                "admission_id": admission.id,
                "reason_id": reason.id,
                "admission_source_term_id": source_term.id,
                "admission_destination_term_id": destination_term.id,
            }
        )
        line = self.env["school_payment_term_transfer_line"].create(
            {
                "transfer_id": transfer.id,
                "admission_source_detail_id": source_detail.id,
                "amount_before": 100000.0,
                "amount": 25000.0,
            }
        )
        return transfer, line

    def test_get_source_term_returns_admission_source_term(self):
        """``_get_source_term`` returns ``admission_source_term_id``.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        transfer, _line = self._create_fixtures()
        self.assertEqual(transfer._get_source_term(), transfer.admission_source_term_id)

    def test_get_destination_term_returns_admission_destination_term(self):
        """``_get_destination_term`` returns ``admission_destination_term_id``.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        transfer, _line = self._create_fixtures()
        self.assertEqual(
            transfer._get_destination_term(),
            transfer.admission_destination_term_id,
        )

    def test_get_owner_document_returns_admission(self):
        """``_get_owner_document`` returns the document's ``admission_id``.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        transfer, _line = self._create_fixtures()
        self.assertEqual(transfer._get_owner_document(), transfer.admission_id)

    def test_get_term_owner_returns_admission_for_source_term(self):
        """``_get_term_owner`` on the Admission source term returns its Admission.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        transfer, _line = self._create_fixtures()
        owner = transfer._get_term_owner(transfer.admission_source_term_id)
        self.assertEqual(owner, transfer.admission_id)

    def test_get_destination_detail_model_returns_admission_model_name(self):
        """``_get_destination_detail_model`` returns the Admission detail model.

        Pure Python -- trigger P1 (L-01: the return value is a bare
        string, and L-02: YAML's assert can only read a dotted
        ``getattr`` on a record already in the registry, never a
        method's return value), see the class docstring.
        """
        transfer, _line = self._create_fixtures()
        self.assertEqual(
            transfer._get_destination_detail_model(),
            "school_admission_payment_term_detail",
        )

    def test_get_source_detail_returns_admission_source_detail_id(self):
        """``_get_source_detail`` on the line returns the Admission detail.

        Pure Python -- trigger P1 (L-01, L-02), see the class
        docstring.
        """
        _transfer, line = self._create_fixtures()
        self.assertEqual(line._get_source_detail(), line.admission_source_detail_id)

    def test_prepare_destination_detail_vals_targets_admission_term(self):
        """``_prepare_destination_detail_vals`` targets the Admission term.

        Pure Python -- trigger P1 (L-01, L-02): the return value is a
        plain ``dict``, which YAML's ``assert`` action cannot inspect
        at all.
        """
        transfer, line = self._create_fixtures()
        vals = transfer._prepare_destination_detail_vals(line)
        self.assertEqual(vals["term_id"], transfer.admission_destination_term_id.id)
        self.assertEqual(vals["price_unit"], line.amount)
        self.assertEqual(vals["uom_quantity"], 1.0)
        self.assertTrue(vals["locked"])
