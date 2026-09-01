# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolEnrollment(models.Model):
    """Adds the Transfers smart button to School Enrollment.

    Pure navigation: ``transfer_ids`` lists the payment term transfer
    documents that target this enrollment, and ``transfer_count``
    backs the smart button opening them. No new action is added on
    the enrollment itself, so no policy field is added here and the
    enrollment's own Instruction Kit is unchanged.
    """

    _name = "school_enrollment"
    _inherit = [
        "school_enrollment",
    ]

    transfer_ids = fields.One2many(
        string="Payment Term Transfers",
        comodel_name="school_payment_term_transfer",
        inverse_name="enrollment_id",
        help="Payment term transfer documents that target this enrollment.",
    )
    transfer_count = fields.Integer(
        string="Payment Term Transfer Count",
        compute="_compute_transfer_count",
        help="Number of payment term transfer documents targeting this "
        "enrollment, backing the Transfers smart button.",
    )

    @api.depends("transfer_ids")
    def _compute_transfer_count(self):
        """Count the payment term transfer documents of this enrollment.

        :return: None
        """
        for record in self:
            record.transfer_count = len(record.transfer_ids)
