# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

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

    This item only installs the document's framework: header, lines
    (``line_ids``), fields, compute/onchange/constraint, and CRUD
    while still ``draft``. No ``policy.template``/``approval.template``
    data is shipped here, so the Confirm/Approve/Done buttons stay
    hidden for every user and the document cannot actually reach
    ``done`` yet -- workflow policy and the code that applies the
    transfer onto ``school_enrollment_payment_term``/
    ``school_enrollment_payment_term_detail`` are added by a later
    item in this repository.
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
        can assign them from a matching ``policy.template`` -- without
        this override the fields would never be assigned by their own
        compute method and Odoo would raise a cache error the first
        time a view reads them. No ``policy.template`` data is shipped
        by this item, so every field simply evaluates to ``False``
        until a later item adds the matching template records.

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
