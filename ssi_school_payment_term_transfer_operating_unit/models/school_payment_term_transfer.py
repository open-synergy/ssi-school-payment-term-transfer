# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

from .school_payment_term_transfer_operating_unit_mixin import (
    derive_operating_unit_from_enrollment_vals,
)


class SchoolPaymentTermTransfer(models.Model):
    """Extends School Payment Term Transfer with single Operating Unit.

    Restricts each transfer document to one Operating Unit, and
    derives ``operating_unit_id`` from ``enrollment_id`` -- the
    enrollment being targeted -- instead of relying solely on the
    creating user's default Operating Unit. The enrollment already
    carries its own Operating Unit via ``ssi_school_operating_unit``,
    so reading it here guarantees this document never lands on a
    different Operating Unit than the enrollment it moves an amount
    on. Source Term and Destination Term always belong to the same
    enrollment (enforced by ``_check_transfer_prerequisites`` on the
    base model), so this document never needs to reconcile two
    different Operating Units on its own.
    """

    _name = "school_payment_term_transfer"
    _inherit = [
        "school_payment_term_transfer",
        "mixin.single_operating_unit",
    ]

    @api.model
    def create(self, vals):
        """Derive ``operating_unit_id`` from ``enrollment_id`` on create.

        Overridden so ``operating_unit_id`` always reflects the
        targeted enrollment's own Operating Unit rather than the
        creating user's default Operating Unit from
        ``mixin.single_operating_unit``, unless the caller explicitly
        passes ``operating_unit_id`` in the same ``vals``.

        :param vals: values for the new record
        :return: the created ``school_payment_term_transfer`` record
        """
        derive_operating_unit_from_enrollment_vals(self.env, vals)
        return super().create(vals)

    def write(self, vals):
        """Re-derive ``operating_unit_id`` when ``enrollment_id`` changes.

        Only triggers when ``enrollment_id`` is part of ``vals``, so a
        write that only sets ``operating_unit_id`` passes through
        unchanged.

        :param vals: values to write
        :return: True
        """
        derive_operating_unit_from_enrollment_vals(self.env, vals)
        return super().write(vals)

    @api.onchange("enrollment_id")
    def onchange_operating_unit_id(self):
        """Set ``operating_unit_id`` from the selected Enrollment.

        Mirrors the ``create``/``write`` derivation so the form shows
        the correct Operating Unit before the record is saved. Only
        sets a value when the enrollment has an Operating Unit;
        otherwise the current value is left untouched.
        """
        if self.enrollment_id and self.enrollment_id.operating_unit_id:
            self.operating_unit_id = self.enrollment_id.operating_unit_id
