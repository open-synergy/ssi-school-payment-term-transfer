# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolPaymentTermTransferLine(models.Model):
    """Let a transfer line move an amount out of an Admission detail.

    Gives the line a second, mutually-exclusive source field,
    ``admission_source_detail_id``, alongside the base module's
    ``source_detail_id``. ``_get_source_detail`` falls back to
    ``super()`` whenever ``admission_source_detail_id`` is empty, so
    Enrollment-sourced lines keep working unmodified.

    ``admission_destination_detail_id`` is the Admission-path mirror
    of ``destination_detail_id``: the base field's comodel is fixed
    to ``school_enrollment_payment_term_detail``, so it cannot hold
    an Admission detail's id without violating its own foreign key.
    ``school_payment_term_transfer._10_apply_transfer`` writes this
    field instead for an Admission-path line -- see that method's
    docstring.
    """

    _name = "school_payment_term_transfer_line"
    _inherit = [
        "school_payment_term_transfer_line",
    ]

    source_detail_id = fields.Many2one(
        required=False,
    )
    admission_source_detail_id = fields.Many2one(
        string="Admission Source Detail",
        comodel_name="school_admission_payment_term_detail",
        domain=(
            "[('term_id', '=', parent.admission_source_term_id), "
            "('customer_invoice_line_id', '=', False), "
            "('voided', '=', False)]"
        ),
        help=(
            "The original Admission fee line the amount is being "
            "moved from. Selecting it fills Amount Before "
            "automatically. Mutually exclusive with Source Detail."
        ),
    )
    admission_destination_detail_id = fields.Many2one(
        string="Admission Destination Detail",
        comodel_name="school_admission_payment_term_detail",
        readonly=True,
        copy=False,
        help=(
            "The Admission fee line created on the Admission "
            "Destination Term to hold the moved amount. Left empty "
            "until the actual transfer is applied on Done -- the "
            "Admission-path mirror of Destination Detail."
        ),
    )

    def _get_source_detail(self):
        """Return the Admission source detail when one is set.

        :return: ``admission_source_detail_id`` when set, otherwise
            whatever ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.admission_source_detail_id:
            return self.admission_source_detail_id
        return super()._get_source_detail()

    @api.onchange("admission_source_detail_id")
    def onchange_admission_amount_before(self):
        """Snapshot the Admission source detail line's billed amount.

        Fired when ``admission_source_detail_id`` changes. Mirrors
        ``onchange_amount_before`` (base module), filling ``amount_
        before`` with the selected detail's untaxed amount
        (``price_subtotal``); clears it back to zero when the
        Admission source detail is unset.

        :return: None
        """
        self.amount_before = (
            self.admission_source_detail_id.price_subtotal
            if self.admission_source_detail_id
            else 0.0
        )
