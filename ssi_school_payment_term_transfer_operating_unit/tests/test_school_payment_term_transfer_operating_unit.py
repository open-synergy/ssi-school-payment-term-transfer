# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestSchoolPaymentTermTransferOperatingUnit(YamlTransactionCase):
    """Cover Operating Unit handling on ``school_payment_term_transfer``.

    Includes the derivation of ``operating_unit_id`` from
    ``enrollment_id`` on create/write, an explicit value winning over
    that derivation, the record rule restricting visibility to a
    user's own Operating Units -- exercised across two different
    Operating Units so the restriction is actually tested rather than
    passing by coincidence -- and the ``enrollment_id`` falsy branch
    of ``get_operating_unit_id_from_enrollment``, only reachable via a
    ``write()`` that is itself rejected by a database constraint.
    """

    def test_school_payment_term_transfer_operating_unit(self):
        """Run every Operating Unit scenario for the transfer document."""
        self.run_yaml_scenario(
            "test_data_school_payment_term_transfer_operating_unit.yaml"
        )

    def _create_transfer(self, suffix):
        """Build one ``school_payment_term_transfer`` from scratch.

        Mirrors the fixture chain used by the YAML scenarios, built
        directly through the ORM instead: per
        ``python-escape-hatch.md`` rule 6, a pure Python method's
        fixtures are created in the method itself (or here, a private
        helper it calls), never taken from the YAML registry, which
        only lives for the duration of ``run_yaml_scenario``.

        :param suffix: short unique string appended to every fixture
            ``code``/``name``, keeping this helper safe to call more
            than once in the same test method
        :return: the created ``school_payment_term_transfer`` record
        """
        grade_type = self.env["school_grade_type"].create(
            {
                "name": "PTTOU Py Grade Type %s" % suffix,
                "code": "PTTOUPYGT%s" % suffix,
            }
        )
        school = self.env["school"].create(
            {
                "name": "PTTOU Py School %s" % suffix,
                "code": "PTTOUPYSC%s" % suffix,
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "PTTOU Py Academic Year %s" % suffix,
                "code": "PTTOUPYAY%s" % suffix,
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "PTTOU Py Academic Term %s" % suffix,
                "code": "PTTOUPYTM%s" % suffix,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "PTTOU Py Grade %s" % suffix,
                "code": "PTTOUPYGR%s" % suffix,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "PTTOU Py Class %s" % suffix,
                "code": "PTTOUPYCL%s" % suffix,
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "PTTOU Py Contact %s" % suffix}
        )
        student = self.env["school_student"].create(
            {
                "name": "PTTOU Py Student %s" % suffix,
                "code": "PTTOUPYST%s" % suffix,
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
        reason = self.env["school_payment_term_transfer_reason"].create(
            {"name": "PTTOU Py Reason %s" % suffix, "code": "/"}
        )
        source_term = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "PTTOU Py Source Term %s" % suffix,
            }
        )
        destination_term = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "PTTOU Py Destination Term %s" % suffix,
            }
        )
        return self.env["school_payment_term_transfer"].create(
            {
                "enrollment_id": enrollment.id,
                "reason_id": reason.id,
                "source_term_id": source_term.id,
                "destination_term_id": destination_term.id,
            }
        )

    @mute_logger("odoo.sql_db")
    def test_write_enrollment_id_false_raises_integrity_error(self):
        """``write({"enrollment_id": False})`` hits the NOT NULL column.

        Pure Python -- trigger P5 (L-22: ``psycopg2.IntegrityError`` is
        outside the 12 error types ``expect_error`` understands). This
        is the only production path into
        ``get_operating_unit_id_from_enrollment``'s ``if not
        enrollment_id: return None`` (lines 27-28): reaching it
        requires ``vals["enrollment_id"]`` to be present as a key but
        falsy, which only happens through a ``write()`` that sets
        ``enrollment_id`` to ``False`` on an existing record -- a
        missing key stops earlier, at the already-covered
        ``"enrollment_id" not in vals`` check (lines 48-49).
        ``enrollment_id`` is ``required=True``
        (``ssi_school_payment_term_transfer/models/
        school_payment_term_transfer.py:100-103``), so the
        ``super().write(vals)`` called by the override after the
        helper finishes raises ``psycopg2.IntegrityError`` on the NOT
        NULL column -- but only after lines 27-28 already ran, so
        their coverage is recorded regardless of the write failing.
        ``mute_logger("odoo.sql_db")`` silences the PostgreSQL ERROR
        line this deliberately triggers; without it
        ``oca_checklog_odoo`` fails the CI even though the test
        itself passes.
        """
        doc = self._create_transfer("A")
        with self.assertRaises(IntegrityError):
            doc.write({"enrollment_id": False})
