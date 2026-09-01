# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolPaymentTermTransfer(YamlTransactionCase):
    """Scenario tests for ``school_payment_term_transfer``."""

    def test_school_payment_term_transfer(self):
        """Run the field/compute/constraint scenario for the transfer."""
        self.run_yaml_scenario("test_data_school_payment_term_transfer.yaml")
