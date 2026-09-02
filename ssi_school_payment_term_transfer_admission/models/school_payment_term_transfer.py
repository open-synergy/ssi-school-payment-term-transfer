# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolPaymentTermTransfer(models.Model):
    """Let a payment term transfer target an Admission instead.

    Adds ``"admission"`` to ``source_type`` and gives the document a
    second, mutually-exclusive billing source: ``admission_id``
    alongside the base module's ``enrollment_id``. Every extension
    point is routed on ``self.source_type == "admission"`` -- not on
    whether ``admission_id`` happens to be filled in -- so a document
    whose Source Type is Enrollment never picks up a stray Admission
    value, and vice versa; ``_check_source_type_consistency`` below
    enforces that the two paths' fields never mix.
    ``_10_apply_transfer`` is the one exception routed the same way
    but not merely delegating to ``super()``: its own
    ``line.write({"destination_detail_id": ...})`` is hard-coded to a
    field whose comodel is the Enrollment-side detail model, so it is
    fully re-implemented for the Admission path (writing
    ``admission_destination_detail_id`` instead), see
    ``school_payment_term_transfer_line``.
    """

    _name = "school_payment_term_transfer"
    _inherit = [
        "school_payment_term_transfer",
    ]

    source_type = fields.Selection(
        selection_add=[
            ("admission", "Admission"),
        ],
        ondelete={"admission": "set default"},
    )
    admission_id = fields.Many2one(
        string="Admission",
        comodel_name="school_admission",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        domain=[("state", "=", "open")],
        help=(
            "The open admission whose billed amount is being moved "
            "between payment terms. Shown, and required, only when "
            "Source Type is Admission -- enforced by "
            "``_check_source_type_consistency``, not by this field "
            "itself."
        ),
    )
    admission_source_term_id = fields.Many2one(
        string="Admission Source Term",
        comodel_name="school_admission_payment_term",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        domain="[('admission_id', '=', admission_id), "
        "('customer_invoice_id', '=', False)]",
        help=(
            "The Admission payment term the amount is being moved "
            "out of. Shown, and required, only when Source Type is "
            "Admission."
        ),
    )
    admission_destination_term_id = fields.Many2one(
        string="Admission Destination Term",
        comodel_name="school_admission_payment_term",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        domain="[('admission_id', '=', admission_id), "
        "('customer_invoice_id', '=', False)]",
        help=(
            "The Admission payment term the amount is being moved "
            "into. Shown, and required, only when Source Type is "
            "Admission."
        ),
    )

    @api.constrains(
        "source_type",
        "enrollment_id",
        "source_term_id",
        "destination_term_id",
        "admission_id",
        "admission_source_term_id",
        "admission_destination_term_id",
    )
    def _check_source_type_consistency(self):
        """Require the fields of the OTHER path to stay empty.

        Replaces the base pair's old ``_check_single_source_term``
        (an XOR on truthiness): routing is now keyed on
        ``source_type`` alone, so a document whose Source Type is
        Admission is rejected if any Enrollment-path field
        (``enrollment_id``, ``source_term_id``,
        ``destination_term_id``) is also set, and vice versa for a
        document whose Source Type is Enrollment against the three
        Admission-path fields. Admission field requiredness itself
        is left to a later item; this only enforces exclusivity.

        :raises ValidationError: a field belonging to the path NOT
            selected by ``source_type`` is set.
        """
        for record in self.sudo():
            if record.source_type == "admission":
                stray = (
                    record.enrollment_id
                    or record.source_term_id
                    or record.destination_term_id
                )
                if stray:
                    error_message = (
                        _(
                            """
Context: Set payment term transfer source/destination
Database ID: %s
Problem: Source Type is Admission but an Enrollment-path field is also set
Solution: Clear Enrollment, Source Term and Destination Term
"""
                        )
                        % (record.id,)
                    )
                    raise ValidationError(error_message)
            elif record.source_type == "enrollment":
                stray = (
                    record.admission_id
                    or record.admission_source_term_id
                    or record.admission_destination_term_id
                )
                if stray:
                    error_message = (
                        _(
                            """
Context: Set payment term transfer source/destination
Database ID: %s
Problem: Source Type is Enrollment but an Admission-path field is also set
Solution: Clear Admission, Admission Source Term and Admission
Destination Term
"""
                        )
                        % (record.id,)
                    )
                    raise ValidationError(error_message)

    @api.depends("source_type", "enrollment_id", "enrollment_id.name")
    def _compute_source_document(self):
        """Widen the base compute's trigger with Admission fields.

        ``self.admission_id``/``.name`` are added so the Admission
        path recomputes too; the base implementation already reads
        through ``_get_owner_document()``, which this module's
        override resolves for the Admission path, so the body is
        just ``super()``.

        :return: None
        """
        return super()._compute_source_document()

    @api.depends("source_type", "source_term_id", "source_term_id.name")
    def _compute_source_term_name(self):
        """Widen the base compute's trigger with Admission fields.

        See ``_compute_source_document`` -- the body is
        unmodified, ``@api.depends`` widened with
        ``admission_source_term_id``/``.name``.

        :return: None
        """
        return super()._compute_source_term_name()

    @api.depends(
        "source_type",
        "destination_term_id",
        "destination_term_id.name",
    )
    def _compute_destination_term_name(self):
        """Widen the base compute's trigger with Admission fields.

        See ``_compute_source_document`` -- the body is
        unmodified, ``@api.depends`` widened with
        ``admission_destination_term_id``/``.name``.

        :return: None
        """
        return super()._compute_destination_term_name()

    @api.constrains("enrollment_id", "admission_id", "source_type")
    def _check_source_document(self):
        """Widen the base constraint's trigger with Admission fields.

        ``admission_id`` is added so the Admission path is checked
        too; ``source_type`` is added so a ``create()`` naming
        neither ``enrollment_id`` nor ``admission_id`` -- Source Type
        left at its default -- still triggers this check and is
        rejected by ``_get_owner_document()`` being empty, instead of
        silently passing (see the base module's docstring for why
        ``source_type`` was deliberately NOT a trigger there). The
        body is unmodified.

        :raises ValidationError: forwarded from ``super()``.
        """
        return super()._check_source_document()

    @api.constrains(
        "source_type",
        "source_term_id",
        "destination_term_id",
        "admission_source_term_id",
        "admission_destination_term_id",
    )
    def _check_term_distinct(self):
        """Widen the base constraint's trigger with Admission fields.

        See ``_check_source_document`` -- the body is unmodified,
        ``@api.constrains`` widened with
        ``admission_source_term_id``/``admission_destination_term_id``.

        :raises ValidationError: forwarded from ``super()``.
        """
        return super()._check_term_distinct()

    @api.onchange("source_type")
    def onchange_admission_id(self):
        """Clear Admission when Source Type moves away from Admission."""
        if self.source_type != "admission":
            self.admission_id = False

    @api.onchange("source_type")
    def onchange_admission_source_term_id(self):
        """Clear Admission Source Term when Source Type leaves Admission."""
        if self.source_type != "admission":
            self.admission_source_term_id = False

    @api.onchange("source_type")
    def onchange_admission_destination_term_id(self):
        """Clear Admission Destination Term, Source Type leaves Admission."""
        if self.source_type != "admission":
            self.admission_destination_term_id = False

    def _get_source_term(self):
        """Return the Admission source term on the Admission path.

        :return: ``admission_source_term_id`` when ``source_type`` is
            ``"admission"``, otherwise whatever ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.source_type == "admission":
            return self.admission_source_term_id
        return super()._get_source_term()

    def _get_destination_term(self):
        """Return the Admission destination term on the Admission path.

        :return: ``admission_destination_term_id`` when
            ``source_type`` is ``"admission"``, otherwise whatever
            ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.source_type == "admission":
            return self.admission_destination_term_id
        return super()._get_destination_term()

    def _get_owner_document(self):
        """Return the Admission owning this transfer, on the Admission path.

        :return: ``admission_id`` when ``source_type`` is
            ``"admission"``, otherwise whatever ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.source_type == "admission":
            return self.admission_id
        return super()._get_owner_document()

    def _get_term_owner(self, term):
        """Return the Admission owning a given Admission payment term.

        :param term: ``school_admission_payment_term`` or
            ``school_enrollment_payment_term`` record.
        :return: ``term.admission_id`` when ``term`` is an Admission
            payment term, otherwise whatever ``super()`` returns.
        """
        if term._name == "school_admission_payment_term":
            return term.admission_id
        return super()._get_term_owner(term)

    def _get_destination_detail_model(self):
        """Return the Admission detail model on the Admission path.

        :return: ``"school_admission_payment_term_detail"`` when
            ``source_type`` is ``"admission"``, otherwise whatever
            ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.source_type == "admission":
            return "school_admission_payment_term_detail"
        return super()._get_destination_detail_model()

    def _recompute_owner_summaries(self):
        """Refresh the Admission's product summary on the Admission path.

        ``school_admission`` exposes ``_recompute_product_summary``
        (singular) rather than the Enrollment's
        ``_recompute_product_summaries`` (plural) -- ``super()``'s
        implementation calls the wrong name for an Admission owner,
        so this is overridden instead of left to ``_get_owner_
        document()`` alone.

        :return: None
        """
        # pylint: disable=protected-access
        if self.source_type == "admission":
            self._get_owner_document()._recompute_product_summary()
            return
        super()._recompute_owner_summaries()

    def _prepare_destination_detail_vals(self, line):
        """Build the destination detail's create values, Admission path.

        Mirrors ``super()``'s Enrollment-side values exactly --
        ``uom_quantity`` is always 1, ``price_unit`` is the moved
        ``amount``, ``tax_ids`` is copied from the source detail, and
        the new detail is locked immediately -- only the target
        model differs (``school_admission_payment_term_detail``,
        via ``_get_destination_detail_model``).

        :param line: ``school_payment_term_transfer_line`` record
            being applied.
        :return: dict of ``school_admission_payment_term_detail``
            create values when ``source_type`` is ``"admission"``,
            otherwise whatever ``super()`` returns.
        """
        self.ensure_one()
        if self.source_type != "admission":
            return super()._prepare_destination_detail_vals(line)
        detail = line._get_source_detail()
        return {
            "term_id": self._get_destination_term().id,
            "product_id": detail.product_id.id,
            "name": detail.name,
            "account_id": detail.account_id.id,
            "uom_id": detail.uom_id.id,
            "uom_quantity": 1.0,
            "price_unit": line.amount,
            "tax_ids": [(6, 0, detail.tax_ids.ids)],
            "locked": True,
        }

    @ssi_decorator.post_done_action()
    def _10_apply_transfer(self):
        """Apply the transfer once Done is reached, Admission path.

        Re-implements ``super()``'s loop instead of extending it:
        the base method's own ``line.write({"destination_detail_id":
        ...})`` is hard-coded to a field whose comodel is the
        Enrollment-side detail model
        (``school_enrollment_payment_term_detail``) -- writing an
        Admission detail's id there would violate that field's
        foreign key. This override writes ``admission_destination_
        detail_id`` instead, added on the line model for exactly
        this purpose. Every other step -- ``sudo()``,
        ``bypass_addendum_lock``, voiding/reducing the source detail,
        the closing ``_recompute_owner_summaries``/``message_post``
        -- mirrors ``super()`` exactly.

        :return: whatever ``super()._10_apply_transfer()`` returns
            when ``source_type`` is not ``"admission"``.
        """
        self.ensure_one()
        if self.source_type != "admission":
            return super()._10_apply_transfer()
        context_self = self.sudo().with_context(bypass_addendum_lock=True)
        for line in context_self.line_ids:
            detail = line._get_source_detail()
            destination_detail = context_self.env[
                context_self._get_destination_detail_model()
            ].create(context_self._prepare_destination_detail_vals(line))
            if line.full_transfer:
                detail.write({"voided": True})
            else:
                detail.write({"price_unit": line.amount_after})
            line.write({"admission_destination_detail_id": destination_detail.id})
        context_self._recompute_owner_summaries()
        context_self._get_owner_document().message_post(
            body=context_self._prepare_transfer_notification(),
            message_type="notification",
            subtype_xmlid="mail.mt_note",
        )
        return None
