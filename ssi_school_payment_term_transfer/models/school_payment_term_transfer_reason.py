# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolPaymentTermTransferReason(
    models.Model
):  # pylint: disable=too-few-public-methods
    """Represents the reason behind a payment term transfer.

    A payment term transfer moves an already-approved but not-yet-invoiced
    billing amount from one payment term to another on an enrollment or
    admission document, while the total billed amount stays unchanged.
    This model only carries the reason (e.g. renegotiation with the
    parent, scheduling mistake); it is shared by both the enrollment and
    admission sides so that reporting per reason stays consistent across
    both. The transfer document itself, which records which reason was
    used for a given transfer, is added later by the transactional
    module.

    All fields (``name``, ``code``, ``active``, ``note``) are provided by
    ``mixin.master_data``; this model does not redeclare any of them.
    """

    _name = "school_payment_term_transfer_reason"
    _inherit = ["mixin.master_data"]
    _description = "School Payment Term Transfer Reason"
    _order = "name, id"
