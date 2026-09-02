# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

from .school_payment_term_transfer_admission_operating_unit_mixin import (
    derive_operating_unit_from_admission_vals,
)


class SchoolPaymentTermTransfer(models.Model):
    """Derive ``operating_unit_id`` from ``admission_id`` as well.

    ``ssi_school_payment_term_transfer_operating_unit`` already gives
    ``school_payment_term_transfer`` its ``operating_unit_id`` field
    (via ``mixin.single_operating_unit``) and derives it from
    ``enrollment_id``. That derivation leaves the Admission path
    (``admission_id``, added by
    ``ssi_school_payment_term_transfer_admission``) unserved -- an
    Admission-path document has no enrollment to derive from, so its
    Operating Unit would stay empty. This module adds a second
    derivation source, layered in front of the Enrollment one via
    ``super()``: when ``admission_id`` is set, the Operating Unit is
    taken from the admission itself (which already carries its own,
    via ``ssi_school_admission_operating_unit``); otherwise the call
    falls through unchanged to the Enrollment-based derivation. No
    second ``mixin.single_operating_unit`` is installed here -- the
    one from ``ssi_school_payment_term_transfer_operating_unit``
    already applies to every document, whichever path it takes.
    """

    _name = "school_payment_term_transfer"
    _inherit = [
        "school_payment_term_transfer",
    ]

    @api.model
    def create(self, vals):
        """Derive ``operating_unit_id`` from ``admission_id`` on create.

        Runs before ``super()``'s Enrollment-based derivation, so an
        ``admission_id`` on the same ``vals`` wins by populating
        ``operating_unit_id`` first -- ``super()`` then leaves it
        alone, exactly as it already does for any other explicit
        value. When ``admission_id`` is not part of ``vals``, this is
        a no-op and ``super()`` proceeds unchanged.

        :param vals: values for the new record
        :return: the created ``school_payment_term_transfer`` record
        """
        derive_operating_unit_from_admission_vals(self.env, vals)
        return super().create(vals)

    def write(self, vals):
        """Re-derive ``operating_unit_id`` when ``admission_id`` changes.

        Only triggers when ``admission_id`` is part of ``vals``, so a
        write that only sets ``operating_unit_id`` passes through
        unchanged, and a write that only touches ``enrollment_id``
        is left entirely to ``super()``.

        :param vals: values to write
        :return: True
        """
        derive_operating_unit_from_admission_vals(self.env, vals)
        return super().write(vals)

    @api.onchange("admission_id")
    def onchange_operating_unit_id_from_admission(self):
        """Set ``operating_unit_id`` from the selected Admission.

        Mirrors the ``create``/``write`` derivation so the form shows
        the correct Operating Unit before the record is saved. Only
        sets a value when the admission has an Operating Unit;
        otherwise the current value is left untouched.
        """
        if self.admission_id and self.admission_id.operating_unit_id:
            self.operating_unit_id = self.admission_id.operating_unit_id
