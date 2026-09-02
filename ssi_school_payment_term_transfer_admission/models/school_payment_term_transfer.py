# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolPaymentTermTransfer(models.Model):
    """Let a payment term transfer target an Admission instead.

    Gives the document a second, mutually-exclusive billing source:
    ``admission_id`` alongside the base module's ``enrollment_id``.
    Every ``_get_source_term``/``_get_destination_term``/
    ``_get_owner_document``/``_get_term_owner``/``_get_destination_
    detail_model``/``_recompute_owner_summaries`` extension point is
    overridden to resolve the Admission path when ``admission_id`` is
    set, falling back to ``super()`` (the Enrollment path) otherwise
    -- so every gate and the transfer application itself run
    unmodified for both paths. ``_10_apply_transfer`` is the one
    exception: its own ``line.write({"destination_detail_id": ...})``
    is hard-coded to a field whose comodel is the Enrollment-side
    detail model, so it is fully re-implemented for the Admission
    path (writing ``admission_destination_detail_id`` instead) rather
    than merely extended, see ``school_payment_term_transfer_line``.
    """

    _name = "school_payment_term_transfer"
    _inherit = [
        "school_payment_term_transfer",
    ]

    enrollment_id = fields.Many2one(
        required=False,
    )
    source_term_id = fields.Many2one(
        required=False,
    )
    destination_term_id = fields.Many2one(
        required=False,
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
            "between payment terms. Mutually exclusive with "
            "Enrollment -- exactly one of the two must be set."
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
            "out of. Only shown when Admission is set."
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
            "into. Only shown when Admission is set."
        ),
    )

    @api.constrains("enrollment_id", "admission_id")
    def _check_single_source_term(self):
        """Require exactly one of Enrollment / Admission.

        Both fields identify the document's billing source in a
        different domain; leaving both set or both empty makes
        ``_get_owner_document()`` ambiguous or empty. Message format
        copied from ``ssi_school_fee_waiver_admission``'s
        ``_check_single_source_term``.

        :raises ValidationError: when both are set, or neither is
            set.
        """
        for record in self:
            if bool(record.enrollment_id) == bool(record.admission_id):
                error_message = """
Document Type: %s
Context: Configure payment term transfer
Database ID: %s
Problem: Exactly one of Enrollment or Admission must be set
Solution: Select either an Enrollment or an Admission, not both and not neither
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _get_source_term(self):
        """Return the Admission source term when one is set.

        :return: ``admission_source_term_id`` when set, otherwise
            whatever ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.admission_source_term_id:
            return self.admission_source_term_id
        return super()._get_source_term()

    def _get_destination_term(self):
        """Return the Admission destination term when one is set.

        :return: ``admission_destination_term_id`` when set,
            otherwise whatever ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.admission_destination_term_id:
            return self.admission_destination_term_id
        return super()._get_destination_term()

    def _get_owner_document(self):
        """Return the Admission owning this transfer, when set.

        :return: ``admission_id`` when set, otherwise whatever
            ``super()`` returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.admission_id:
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
        """Return the Admission detail model when it is the target.

        :return: ``"school_admission_payment_term_detail"`` when
            ``admission_id`` is set, otherwise whatever ``super()``
            returns.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        if self.admission_id:
            return "school_admission_payment_term_detail"
        return super()._get_destination_detail_model()

    def _recompute_owner_summaries(self):
        """Refresh the Admission's product summary, when it is the owner.

        ``school_admission`` exposes ``_recompute_product_summary``
        (singular) rather than the Enrollment's
        ``_recompute_product_summaries`` (plural) -- ``super()``'s
        implementation calls the wrong name for an Admission owner,
        so this is overridden instead of left to ``_get_owner_
        document()`` alone.

        :return: None
        """
        # pylint: disable=protected-access
        if self.admission_id:
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
            create values when ``admission_id`` is set, otherwise
            whatever ``super()`` returns.
        """
        self.ensure_one()
        if not self.admission_id:
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
            when ``admission_id`` is not set.
        """
        self.ensure_one()
        if not self.admission_id:
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
