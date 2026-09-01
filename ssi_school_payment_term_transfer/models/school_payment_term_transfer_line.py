# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero


class SchoolPaymentTermTransferLine(models.Model):
    """Represents one fee line being moved by a payment term transfer.

    Each line snapshots the originating detail line's billed amount
    (``amount_before``) the moment it is selected, records how much of
    it is being moved (``amount``), and derives what stays behind on
    the source term (``amount_after``) and whether the whole line was
    moved (``full_transfer``). ``amount_before`` is a plain stored
    field filled once by onchange -- not related/compute -- so this
    snapshot never drifts if the source detail's own amount changes
    afterwards; that stability is the entire reason this document
    keeps a trace of where an amount came from.
    """

    _name = "school_payment_term_transfer_line"
    _description = "School Payment Term Transfer Line"
    _order = "id"

    transfer_id = fields.Many2one(
        string="Transfer",
        comodel_name="school_payment_term_transfer",
        required=True,
        ondelete="cascade",
        help="The payment term transfer document that owns this line.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="transfer_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, taken from the transfer document.",
    )
    allowed_source_detail_ids = fields.Many2many(
        string="Allowed Source Details",
        comodel_name="school_enrollment_payment_term_detail",
        compute="_compute_allowed_source_detail_ids",
        store=False,
        compute_sudo=True,
        help=(
            "Detail lines of the transfer's Source Term that are not "
            "yet invoiced and not already voided, eligible to be "
            "selected on this line."
        ),
    )
    source_detail_id = fields.Many2one(
        string="Source Detail",
        comodel_name="school_enrollment_payment_term_detail",
        required=True,
        help=(
            "The original fee line the amount is being moved from. "
            "Selecting it fills Amount Before automatically."
        ),
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        related="source_detail_id.product_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The product of the source detail line, shown for reference.",
    )
    amount_before = fields.Monetary(
        string="Amount Before",
        currency_field="currency_id",
        readonly=True,
        copy=False,
        help=(
            "Snapshot of the source detail line's billed amount at "
            "the moment it was selected, filled automatically by "
            "onchange. Never changes afterwards, even if the source "
            "detail's own amount is later modified -- this is what "
            "keeps this line a reliable trace of where the amount "
            "moved from."
        ),
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        required=True,
        help="The portion of Amount Before being moved to the destination term.",
    )
    amount_after = fields.Monetary(
        string="Amount After",
        currency_field="currency_id",
        compute="_compute_amount_after",
        store=True,
        compute_sudo=True,
        help="Amount Before minus Amount: what stays on the source term.",
    )
    full_transfer = fields.Boolean(
        string="Full Transfer",
        compute="_compute_amount_after",
        store=True,
        compute_sudo=True,
        help="Whether Amount After is zero: the entire line was moved.",
    )
    destination_detail_id = fields.Many2one(
        string="Destination Detail",
        comodel_name="school_enrollment_payment_term_detail",
        readonly=True,
        copy=False,
        help=(
            "The fee line created on the Destination Term to hold "
            "the moved amount. Left empty by this item -- it is only "
            "filled once the actual transfer is applied, added by a "
            "later item in this repository."
        ),
    )

    @api.depends("transfer_id.source_term_id")
    def _compute_allowed_source_detail_ids(self):
        """Compute the source details selectable on this line.

        Nothing is proposed until the owning document's
        ``source_term_id`` is set; otherwise the
        ``school_enrollment_payment_term_detail`` records matching
        ``_get_allowed_source_detail_criteria`` are collected. The
        view uses this field to restrict ``source_detail_id``.

        :return: None
        """
        for record in self:
            result = False
            term = record.transfer_id.source_term_id
            if term:
                criteria = record._get_allowed_source_detail_criteria()
                result = (
                    self.env["school_enrollment_payment_term_detail"]
                    .search(criteria)
                    .ids
                )
            record.allowed_source_detail_ids = result

    def _get_allowed_source_detail_criteria(self):
        """Return the domain of source detail lines eligible for transfer.

        Extension point of ``_compute_allowed_source_detail_ids``:
        override it to widen or narrow the selection. Matches the
        detail lines of the owning document's Source Term that have
        no customer invoice line yet and are not already voided.

        :return: search domain for ``school_enrollment_payment_term_detail``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return [
            ("term_id", "=", self.transfer_id.source_term_id.id),
            ("customer_invoice_line_id", "=", False),
            ("voided", "=", False),
        ]

    @api.onchange("source_detail_id")
    def onchange_amount_before(self):
        """Snapshot the source detail line's billed amount.

        Fired when ``source_detail_id`` changes. Fills
        ``amount_before`` with the selected detail's untaxed amount
        (``price_subtotal``) so amounts can be compared and summed
        without pulling tax into this document -- the worked example
        this document is built around is deliberately untaxed. Clears
        it back to zero when the source detail is unset.
        """
        self.amount_before = (
            self.source_detail_id.price_subtotal if self.source_detail_id else 0.0
        )

    @api.depends("amount_before", "amount", "currency_id")
    def _compute_amount_after(self):
        """Derive what stays on the source term after the transfer.

        ``amount_after`` is ``amount_before`` minus ``amount``.
        ``full_transfer`` is ``True`` exactly when ``amount_after`` is
        zero within the document currency's rounding -- compared with
        ``float_is_zero`` rather than ``== 0`` so rounding never
        leaves a line that looks fully transferred but technically
        is not, or vice versa.

        :return: None
        """
        for record in self:
            amount_after = record.amount_before - record.amount
            record.amount_after = amount_after
            record.full_transfer = float_is_zero(
                amount_after,
                precision_rounding=record.currency_id.rounding,
            )

    @api.constrains("amount")
    def _check_amount_positive(self):
        """Enforce a strictly positive transfer amount.

        Runs on every create or write touching ``amount``: a transfer
        line moving zero or a negative amount is not a transfer.

        :raises ValidationError: ``amount`` is not strictly positive.
        """
        for record in self.sudo():
            if record.amount <= 0:
                error_message = (
                    _(
                        """
Context: Set payment term transfer line amount
Database ID: %s
Problem: Amount %s is not greater than zero
Solution: Enter an amount greater than zero
"""
                    )
                    % (
                        record.id,
                        record.amount,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("amount", "amount_before")
    def _check_amount_not_exceeding(self):
        """Enforce that the moved amount never exceeds the source line.

        Runs on every create or write touching ``amount`` or
        ``amount_before``: a line can never move more than what the
        source detail line was actually billed for.

        :raises ValidationError: ``amount`` is greater than
            ``amount_before``.
        """
        for record in self.sudo():
            if record.amount > record.amount_before:
                error_message = (
                    _(
                        """
Context: Set payment term transfer line amount
Database ID: %s
Problem: Amount %s exceeds Amount Before %s
Solution: Enter an amount no greater than Amount Before
"""
                    )
                    % (
                        record.id,
                        record.amount,
                        record.amount_before,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("source_detail_id", "transfer_id")
    def _check_source_detail_unique(self):
        """Enforce a source detail line is used at most once per document.

        Runs on every create or write touching ``source_detail_id`` or
        ``transfer_id``: two lines of the same document moving amounts
        out of the same source detail line would double-count how
        much of it has been moved.

        :raises ValidationError: another line of the same document
            already uses this ``source_detail_id``.
        """
        for record in self.sudo():
            if not record.source_detail_id or not record.transfer_id:
                continue
            sibling = record.transfer_id.line_ids.filtered(
                lambda line, record=record: (
                    line.id != record.id
                    and line.source_detail_id == record.source_detail_id
                )
            )
            if sibling:
                error_message = (
                    _(
                        """
Context: Set payment term transfer line source detail
Database ID: %s
Problem: Source Detail '%s' is already used by another line of this document
Solution: Select a different Source Detail, or edit the existing line instead
"""
                    )
                    % (
                        record.id,
                        record.source_detail_id.display_name,
                    )
                )
                raise ValidationError(error_message)
