# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolPaymentTermTransferOperatingUnit(YamlTransactionCase):
    """Cover Operating Unit handling on ``school_payment_term_transfer``.

    Includes the derivation of ``operating_unit_id`` from
    ``enrollment_id`` on create/write, an explicit value winning over
    that derivation, the record rule restricting visibility to a
    user's own Operating Units -- exercised across two different
    Operating Units so the restriction is actually tested rather than
    passing by coincidence -- and the ``enrollment_id`` falsy branch
    of ``get_operating_unit_id_from_enrollment``, reached via a
    ``write()`` that clears ``enrollment_id`` on an existing document
    and is rejected by
    ``ssi_school_payment_term_transfer_admission``'s
    ``_check_single_source_term`` constraint.
    """

    def test_school_payment_term_transfer_operating_unit(self):
        """Run every Operating Unit scenario for the transfer document."""
        self.run_yaml_scenario(
            "test_data_school_payment_term_transfer_operating_unit.yaml"
        )
