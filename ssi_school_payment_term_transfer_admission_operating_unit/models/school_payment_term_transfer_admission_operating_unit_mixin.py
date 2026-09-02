# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Shared helper deriving ``operating_unit_id`` from ``admission_id``.

Plain functions (not an Odoo model), mirroring
``school_payment_term_transfer_operating_unit_mixin`` in
``ssi_school_payment_term_transfer_operating_unit`` -- which derives
``operating_unit_id`` from ``enrollment_id`` -- so the
``school_payment_term_transfer`` ``create``/``write`` overrides added
here do not duplicate that module's derivation logic.
"""


def get_operating_unit_id_from_admission(env, admission_id):
    """Return the id of an admission's own Operating Unit, if any.

    Unlike deriving from a School (which may carry zero or several
    Operating Units), an admission already carries at most one --
    ``mixin.single_operating_unit`` on ``school_admission`` -- so no
    ambiguity check is needed here.

    :param env: the current Odoo environment
    :param admission_id: id of the ``school_admission`` record, or a
        falsy value
    :return: id of the ``operating.unit`` record set on the
        admission, or ``None`` when the admission has none
    """
    if not admission_id:
        return None
    admission = env["school_admission"].browse(admission_id)
    return admission.operating_unit_id.id or None


def derive_operating_unit_from_admission_vals(env, vals):
    """Mutate ``vals`` in place, deriving ``operating_unit_id``.

    Applies only when ``admission_id`` is present in ``vals`` and the
    caller has not already supplied ``operating_unit_id`` explicitly
    in the same ``vals`` dict -- an explicit value always wins. Used
    from both ``create`` (where it overrides the
    ``mixin.single_operating_unit`` user-default, and the Enrollment-
    based derivation from ``ssi_school_payment_term_transfer_
    operating_unit``, by populating the key before either applies)
    and ``write`` (where it only triggers when ``admission_id``
    itself changes).

    :param env: the current Odoo environment
    :param vals: the ``create``/``write`` values dict, mutated in
        place
    :return: None
    """
    if "admission_id" not in vals or "operating_unit_id" in vals:
        return
    operating_unit_id = get_operating_unit_id_from_admission(
        env, vals.get("admission_id")
    )
    if operating_unit_id:
        vals["operating_unit_id"] = operating_unit_id
