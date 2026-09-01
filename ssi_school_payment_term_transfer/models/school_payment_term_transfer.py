# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolPaymentTermTransfer(models.Model):
    """Represents a payment term transfer document.

    A payment term transfer moves an already-approved but not-yet-
    invoiced billing amount from one payment term
    (``source_term_id``) to another (``destination_term_id``) on the
    same enrollment, while the enrollment's total billed amount stays
    unchanged -- e.g. moving 25,000 of a 100,000 Computer Fee line
    from Term 2 to Term 3 leaves Term 2 with 75,000 and adds a
    25,000 Computer Fee line to Term 3. Reducing the billed amount is
    not this document's concern; that is handled by
    ``ssi_school_fee_waiver``.

    Confirm/Approve/Reject/Restart Approval/Cancel/Restart are gated by
    a ``policy.template`` (``policy_template/
    school_payment_term_transfer.xml``); there is no manual Done
    button (``_automatically_insert_done_button = False``) because
    ``_after_approved_method = "action_done"`` reaches ``done``
    automatically once approval completes. The prerequisites checked
    before Confirm and again before Done, and the transfer applied on
    Done, live in ``_check_transfer_prerequisites`` and
    ``_apply_transfer`` below.
    """

    _name = "school_payment_term_transfer"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.company_currency",
    ]
    _description = "School Payment Term Transfer"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Date this payment term transfer document was created.",
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        domain=[("state", "=", "open")],
        help=(
            "The open enrollment whose billed amount is being moved "
            "between payment terms."
        ),
    )
    reason_id = fields.Many2one(
        string="Reason",
        comodel_name="school_payment_term_transfer_reason",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Why this amount is being moved between payment terms.",
    )
    note = fields.Text(
        string="Note",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Optional free-form explanation for this transfer.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        related="enrollment_id.student_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The student being billed, taken from the enrollment.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        related="enrollment_id.academic_year_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The academic year of the enrollment.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="enrollment_id.academic_term_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The academic term of the enrollment.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="enrollment_id.currency_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The billing currency, taken from the enrollment.",
    )
    allowed_term_ids = fields.Many2many(
        string="Allowed Payment Terms",
        comodel_name="school_enrollment_payment_term",
        compute="_compute_allowed_term_ids",
        store=False,
        compute_sudo=True,
        help=(
            "Payment terms of the selected enrollment that have no "
            "customer invoice yet, eligible as the source or "
            "destination of this transfer."
        ),
    )
    source_term_id = fields.Many2one(
        string="Source Term",
        comodel_name="school_enrollment_payment_term",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The payment term the amount is being moved out of.",
    )
    destination_term_id = fields.Many2one(
        string="Destination Term",
        comodel_name="school_enrollment_payment_term",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The payment term the amount is being moved into.",
    )
    line_ids = fields.One2many(
        string="Line",
        comodel_name="school_payment_term_transfer_line",
        inverse_name="transfer_id",
        copy=True,
        help="The individual fee lines being moved by this transfer.",
    )
    amount_total = fields.Monetary(
        string="Total",
        currency_field="currency_id",
        compute="_compute_amount_total",
        store=True,
        compute_sudo=True,
        help="Sum of the amount moved by every line of this document.",
    )

    @api.depends("enrollment_id")
    def _compute_allowed_term_ids(self):
        """Compute the payment terms selectable as source/destination.

        Nothing is proposed until ``enrollment_id`` is set; otherwise
        the ``school_enrollment_payment_term`` records matching
        ``_get_allowed_term_criteria`` are collected. The view uses
        this field to restrict ``source_term_id`` and
        ``destination_term_id``.

        :return: None
        """
        for record in self:
            result = False
            if record.enrollment_id:
                criteria = record._get_allowed_term_criteria()
                result = self.env["school_enrollment_payment_term"].search(criteria).ids
            record.allowed_term_ids = result

    def _get_allowed_term_criteria(self):
        """Return the domain of payment terms eligible for transfer.

        Extension point of ``_compute_allowed_term_ids``: override it
        to widen or narrow the selection. Matches the payment terms of
        ``enrollment_id`` that have no customer invoice yet -- domain
        enforcement only; the Python-side guard against writing on an
        already-invoiced term is added by a later item in this
        repository.

        :return: search domain for ``school_enrollment_payment_term``.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return [
            ("enrollment_id", "=", self.enrollment_id.id),
            ("customer_invoice_id", "=", False),
        ]

    @api.depends("line_ids.amount")
    def _compute_amount_total(self):
        """Sum the lines into the document total.

        ``amount_total`` is the sum of ``amount`` over ``line_ids``.

        :return: None
        """
        for record in self:
            result = 0.0
            for line in record.line_ids:
                result += line.amount
            record.amount_total = result

    def _get_source_term(self):
        """Return the payment term this document moves the amount out of.

        Extension point: a module giving this document its own extra
        source field overrides this to return that field instead. All
        other code reads the source term through this method rather
        than ``source_term_id`` directly, so the admission side can
        reuse the same logic without duplicating it.

        :return: ``school_enrollment_payment_term`` record, or an
            empty recordset when unset.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return self.source_term_id

    def _get_destination_term(self):
        """Return the payment term this document moves the amount into.

        Extension point: a module giving this document its own extra
        destination field overrides this to return that field
        instead. All other code reads the destination term through
        this method rather than ``destination_term_id`` directly.

        :return: ``school_enrollment_payment_term`` record, or an
            empty recordset when unset.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        return self.destination_term_id

    @api.constrains("source_term_id", "destination_term_id")
    def _check_term_distinct(self):
        """Enforce that the transfer really moves the amount somewhere.

        Runs on every create or write touching ``source_term_id`` or
        ``destination_term_id``: the two must differ, otherwise this
        document would move an amount to the term it already sits on.

        :raises ValidationError: source and destination are the same
            payment term.
        """
        for record in self.sudo():
            if (
                record.source_term_id
                and record.source_term_id == record.destination_term_id
            ):
                error_message = (
                    _(
                        """
Context: Set payment term transfer source/destination
Database ID: %s
Problem: Destination Term '%s' is the same as the Source Term
Solution: Select a different payment term as the transfer destination
"""
                    )
                    % (
                        record.id,
                        record.destination_term_id.name,
                    )
                )
                raise ValidationError(error_message)

    @api.model
    def _get_policy_field(self):
        """Extend the list of policy-controlled boolean fields.

        Adds every ``*_ok`` field contributed by the confirm/done/
        cancel workflow mixins, so ``mixin.policy._compute_policy``
        can assign them from the matching ``policy.template``
        (``policy_template/school_payment_term_transfer.xml``) --
        without this override the fields would never be assigned by
        their own compute method and Odoo would raise a cache error
        the first time a view reads them.

        :return: list of policy field names.
        """
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "done_ok",
            "cancel_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _check_transfer_prerequisites(self):
        """Enforce every prerequisite a transfer must meet to proceed.

        Shared by the ``pre_confirm_check`` and ``pre_done_check``
        hooks below -- the exact same checks run again right before
        ``done`` because a customer invoice may have been created on
        either term (e.g. via Create Due Invoice) in the window
        between Confirm and Approve, after Confirm already passed.

        :raises UserError: ``line_ids`` is empty; the source and
            destination terms are not both set and different; either
            term does not belong to ``enrollment_id``; either term
            already has a customer invoice; a line's source detail
            does not belong to the source term, already has a
            customer invoice line, or is already voided; or a line's
            source detail has a UoM Quantity other than 1.
        :return: None
        """
        self.ensure_one()
        if not self.line_ids:
            error_message = (
                _(
                    """
Context: Confirm/Done payment term transfer
Database ID: %s
Problem: Document has no line
Solution: Add at least one line before continuing
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)

        source_term = self._get_source_term()
        destination_term = self._get_destination_term()
        if not source_term or not destination_term or source_term == destination_term:
            error_message = (
                _(
                    """
Context: Confirm/Done payment term transfer
Database ID: %s
Problem: Source Term and Destination Term must both be set and different
Solution: Select a Source Term and a Destination Term that differ
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)

        for term in (source_term, destination_term):
            if term.enrollment_id != self.enrollment_id:
                error_message = (
                    _(
                        """
Context: Confirm/Done payment term transfer
Database ID: %s
Problem: Payment Term '%s' does not belong to Enrollment '%s'
Solution: Select a Source/Destination Term that belongs to the same Enrollment
"""
                    )
                    % (self.id, term.display_name, self.enrollment_id.display_name)
                )
                raise UserError(error_message)
            if term.customer_invoice_id:
                error_message = (
                    _(
                        """
Context: Confirm/Done payment term transfer
Database ID: %s
Problem: Payment Term '%s' already has a Customer Invoice
Solution: Cancel this document; a term already invoiced can no longer be transferred
"""
                    )
                    % (self.id, term.display_name)
                )
                raise UserError(error_message)

        for line in self.line_ids:
            detail = line.source_detail_id
            if detail.term_id != source_term:
                error_message = (
                    _(
                        """
Context: Confirm/Done payment term transfer
Database ID: %s
Problem: Source Detail '%s' does not belong to the Source Term
Solution: Select a Source Detail that belongs to the Source Term
"""
                    )
                    % (self.id, detail.display_name)
                )
                raise UserError(error_message)
            if detail.customer_invoice_line_id:
                error_message = (
                    _(
                        """
Context: Confirm/Done payment term transfer
Database ID: %s
Problem: Source Detail '%s' already has a Customer Invoice Line
Solution: Cancel this document; an already-invoiced line can no longer be transferred
"""
                    )
                    % (self.id, detail.display_name)
                )
                raise UserError(error_message)
            if detail.voided:
                error_message = (
                    _(
                        """
Context: Confirm/Done payment term transfer
Database ID: %s
Problem: Source Detail '%s' is already voided
Solution: Select a Source Detail that is not already voided
"""
                    )
                    % (self.id, detail.display_name)
                )
                raise UserError(error_message)
            if not float_is_zero(detail.uom_quantity - 1.0, precision_digits=2):
                error_message = (
                    _(
                        """
Context: Confirm/Done payment term transfer
Database ID: %s
Problem: Source Detail '%s' has UoM Quantity %s, which is not 1
Solution: Only source details with a UoM Quantity of exactly 1 can be transferred
"""
                    )
                    % (self.id, detail.display_name, detail.uom_quantity)
                )
                raise UserError(error_message)

    @ssi_decorator.pre_confirm_check()
    def _10_check_transfer_prerequisites_on_confirm(self):
        """Run the transfer prerequisites before Confirm.

        :return: None
        """
        self._check_transfer_prerequisites()

    @ssi_decorator.pre_done_check()
    def _10_check_transfer_prerequisites_on_done(self):
        """Re-run the transfer prerequisites before Done.

        Between Confirm and Approve someone else may run Create Due
        Invoice on either term, so the same checks run again here --
        see ``_check_transfer_prerequisites``.

        :return: None
        """
        self._check_transfer_prerequisites()

    @ssi_decorator.post_done_action()
    def _10_apply_transfer(self):
        """Apply the transfer once Done is reached.

        Runs in ``sudo()`` with ``bypass_addendum_lock`` in context --
        the only sanctioned way through the payment term detail's
        addendum lock, and it only opens after approval. For every
        line, in order: (1) create the destination detail via
        ``_prepare_destination_detail_vals``; (2) adjust the source
        detail (``voided = True`` when ``full_transfer``, otherwise
        ``price_unit = amount_after``); (3) record
        ``destination_detail_id`` on the line. Afterwards
        ``enrollment_id._recompute_product_summaries()`` is called and
        a chatter message summarising the move is posted on the
        enrollment.

        :return: None
        """
        self.ensure_one()
        context_self = self.sudo().with_context(bypass_addendum_lock=True)
        for line in context_self.line_ids:
            detail = line.source_detail_id
            destination_detail = context_self.env[
                "school_enrollment_payment_term_detail"
            ].create(context_self._prepare_destination_detail_vals(line))
            if line.full_transfer:
                detail.write({"voided": True})
            else:
                detail.write({"price_unit": line.amount_after})
            line.write({"destination_detail_id": destination_detail.id})
        # pylint: disable=protected-access
        context_self.enrollment_id._recompute_product_summaries()
        context_self.enrollment_id.message_post(
            body=context_self._prepare_transfer_notification(),
            message_type="notification",
            subtype_xmlid="mail.mt_note",
        )

    def _prepare_destination_detail_vals(self, line):
        """Build the destination detail's create values for one line.

        Extension point of ``_apply_transfer``: override to add extra
        values (e.g. an Operating Unit) on the detail created at the
        destination term. ``uom_quantity`` is always 1 and
        ``price_unit`` is the moved ``amount`` -- ``tax_ids`` is
        copied from the source detail so the enrollment's total stays
        unchanged, and the new detail is locked immediately since it
        is born on an already-locked term.

        :param line: ``school_payment_term_transfer_line`` record
            being applied.
        :return: dict of ``school_enrollment_payment_term_detail``
            create values.
        """
        self.ensure_one()
        detail = line.source_detail_id
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

    def _prepare_transfer_notification(self):
        """Build the chatter message posted on the enrollment on Done.

        Summarises, per line, the product and amount moved from the
        source term to the destination term, and links back to this
        transfer document. The link is a plain ``/web#model=...``
        backend URL rather than a mixin helper -- Odoo 14's
        ``mail.thread`` has no ``_get_html_link``, that method only
        exists from later series onward.

        :return: HTML-safe message body.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        document_url = "/web#model=%s&id=%d&view_type=form" % (
            self._name,
            self.id,
        )
        document_link = '<a href="%s">%s</a>' % (document_url, self.display_name)
        lines_html = "".join(
            _("<li>%s: %s %s</li>")
            % (
                line.product_id.display_name,
                line.amount,
                self.currency_id.symbol,
            )
            for line in self.line_ids
        )
        return _(
            "Payment term transfer %s moved the following from %s to %s:" "<ul>%s</ul>"
        ) % (
            document_link,
            self._get_source_term().display_name,
            self._get_destination_term().display_name,
            lines_html,
        )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        """Reconfigure the statusbar's visible states on the form view.

        ``insert_on_form_view`` hook fired while the form view is
        being assembled. Delegates to
        ``_reconfigure_statusbar_visible`` (from ``mixin.transaction``)
        so only the states listed in ``_statusbar_visible_label``
        ("draft,confirm,done") show on the status bar, hiding
        ``reject``/``cancel`` there -- the same boilerplate every
        model built on these mixins carries.

        :param view_arch: the form view architecture being assembled.
        :return: the (possibly modified) view architecture.
        """
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
