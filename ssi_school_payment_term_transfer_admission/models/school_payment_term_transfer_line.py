# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolPaymentTermTransferLine(models.Model):
    """Let a transfer line move an amount out of an Admission detail.

    Gives the line a second, mutually-exclusive source field,
    ``admission_source_detail_id``, alongside the base module's
    ``source_detail_id``. ``_get_source_detail`` is routed on the
    owning document's ``transfer_id.source_type`` -- not on whether
    ``admission_source_detail_id`` happens to be filled in -- so
    Enrollment-sourced lines keep working unmodified.
    ``_check_source_detail_consistency`` enforces that the field of
    the path NOT selected by ``transfer_id.source_type`` stays empty.

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
        """Return the Admission source detail on the Admission path.

        :return: ``admission_source_detail_id`` when
            ``transfer_id.source_type`` is ``"admission"``, otherwise
            whatever ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.transfer_id.source_type == "admission":
            return self.admission_source_detail_id
        return super()._get_source_detail()

    @api.constrains("source_detail_id", "admission_source_detail_id", "transfer_id")
    def _check_source_detail_consistency(self):
        """Require the source field of the OTHER path to stay empty.

        Mirrors ``school_payment_term_transfer._check_source_type_
        consistency`` at the line level: a line whose document is on
        the Admission path is rejected if ``source_detail_id`` is
        also set, and vice versa for a line whose document is on the
        Enrollment path against ``admission_source_detail_id``. A
        line not yet attached to a document (``transfer_id`` empty,
        e.g. a standalone line form still being filled in) is
        skipped -- there is no ``source_type`` to route on yet.

        :raises ValidationError: the source field of the path NOT
            selected by ``transfer_id.source_type`` is set.
        """
        for record in self.sudo():
            if not record.transfer_id:
                continue
            if (
                record.transfer_id.source_type == "admission"
                and record.source_detail_id
            ):
                error_message = (
                    _(
                        """
Context: Set payment term transfer line source detail
Database ID: %s
Problem: Source Type is Admission but Source Detail is also set
Solution: Clear Source Detail, or select Admission Source Detail instead
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
            if (
                record.transfer_id.source_type == "enrollment"
                and record.admission_source_detail_id
            ):
                error_message = (
                    _(
                        """
Context: Set payment term transfer line source detail
Database ID: %s
Problem: Source Type is Enrollment but Admission Source Detail is also set
Solution: Clear Admission Source Detail, or select Source Detail instead
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

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
