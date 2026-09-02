# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolPaymentTermTransferAdmissionOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover Operating Unit derivation from ``admission_id``.

    Includes the derivation of ``operating_unit_id`` from the
    targeted Admission's own Operating Unit on create/write, an
    explicit value winning over that derivation, the write() re-
    derivation when ``admission_id`` changes, the Enrollment path
    still deriving as before, and the record rule restricting
    visibility to a user's own Operating Units -- exercised across
    two different Operating Units so the restriction is actually
    tested rather than passing by coincidence.
    """

    def test_school_payment_term_transfer_admission_operating_unit(self):
        """Run every Admission-path Operating Unit derivation scenario."""
        self.run_yaml_scenario(
            "test_data_school_payment_term_transfer_admission_operating_unit.yaml"
        )
