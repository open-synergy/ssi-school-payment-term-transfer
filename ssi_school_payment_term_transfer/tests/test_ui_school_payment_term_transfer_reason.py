# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolPaymentTermTransferReason(HttpSavepointCase):
    """Tour tests for ``school_payment_term_transfer_reason`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records the edit/delete tours act on.

        The ``school_payment_term_transfer_reason_group`` group already
        grants ``base.user_admin`` membership by default (see
        ``security/res_groups/school_payment_term_transfer_reason.xml``),
        so no extra group setup is required for the ``admin`` user
        running these tours.
        """
        super().setUpClass()
        Reason = cls.env["school_payment_term_transfer_reason"]
        cls.reason_edit = Reason.create(
            {"name": "TOUR Payment Term Transfer Reason Edit", "code": "/"}
        )
        cls.reason_delete = Reason.create(
            {"name": "TOUR Payment Term Transfer Reason Delete", "code": "/"}
        )

    def test_create(self):
        """Run the create tour for ``school_payment_term_transfer_reason``.

        IK: docs/school_payment_term_transfer_reason/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_reason_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_payment_term_transfer_reason``.

        IK: docs/school_payment_term_transfer_reason/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_reason_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_payment_term_transfer_reason``.

        IK: docs/school_payment_term_transfer_reason/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_reason_delete",
            login="admin",
        )
