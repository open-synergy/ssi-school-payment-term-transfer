# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmission(models.Model):
    """Adds the Transfers smart button to School Admission.

    Pure navigation: ``transfer_ids`` lists the payment term transfer
    documents that target this admission, and ``transfer_count``
    backs the smart button opening them -- mirrors the smart button
    ``ssi_school_payment_term_transfer`` adds on School Enrollment.
    No new action is added on the admission itself, so no policy
    field is added here and the admission's own Instruction Kit is
    unchanged.
    """

    _name = "school_admission"
    _inherit = [
        "school_admission",
    ]

    transfer_ids = fields.One2many(
        string="Payment Term Transfers",
        comodel_name="school_payment_term_transfer",
        inverse_name="admission_id",
        help="Payment term transfer documents that target this admission.",
    )
    transfer_count = fields.Integer(
        string="Payment Term Transfer Count",
        compute="_compute_transfer_count",
        help="Number of payment term transfer documents targeting this "
        "admission, backing the Transfers smart button.",
    )

    @api.depends("transfer_ids")
    def _compute_transfer_count(self):
        """Count the payment term transfer documents of this admission.

        :return: None
        """
        for record in self:
            record.transfer_count = len(record.transfer_ids)
