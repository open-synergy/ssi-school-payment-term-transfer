# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolPaymentTermTransferReason(YamlTransactionCase):
    """Scenario tests for ``school_payment_term_transfer_reason``."""

    def test_school_payment_term_transfer_reason(self):
        """Run the CRUD scenario for ``school_payment_term_transfer_reason``."""
        self.run_yaml_scenario("test_data_school_payment_term_transfer_reason.yaml")
