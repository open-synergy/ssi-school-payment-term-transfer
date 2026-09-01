# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Shared helper deriving ``operating_unit_id`` from ``enrollment_id``.

Plain functions (not an Odoo model), mirroring
``school_enrollment_operating_unit_mixin`` in ``ssi_school_operating_unit``,
so the ``school_payment_term_transfer`` ``create``/``write`` overrides do
not duplicate the derivation logic.
"""


def get_operating_unit_id_from_enrollment(env, enrollment_id):
    """Return the id of an enrollment's own Operating Unit, if any.

    Unlike deriving from a School (which may carry zero or several
    Operating Units), an enrollment already carries at most one --
    ``mixin.single_operating_unit`` on ``school_enrollment`` -- so no
    ambiguity check is needed here.

    :param env: the current Odoo environment
    :param enrollment_id: id of the ``school_enrollment`` record, or a
        falsy value
    :return: id of the ``operating.unit`` record set on the
        enrollment, or ``None`` when the enrollment has none
    """
    if not enrollment_id:
        return None
    enrollment = env["school_enrollment"].browse(enrollment_id)
    return enrollment.operating_unit_id.id or None


def derive_operating_unit_from_enrollment_vals(env, vals):
    """Mutate ``vals`` in place, deriving ``operating_unit_id``.

    Applies only when ``enrollment_id`` is present in ``vals`` and the
    caller has not already supplied ``operating_unit_id`` explicitly in
    the same ``vals`` dict -- an explicit value always wins. Used from
    both ``create`` (where it overrides the
    ``mixin.single_operating_unit`` user-default by populating the key
    before the ORM applies it) and ``write`` (where it only triggers
    when ``enrollment_id`` itself changes).

    :param env: the current Odoo environment
    :param vals: the ``create``/``write`` values dict, mutated in place
    :return: None
    """
    if "enrollment_id" not in vals or "operating_unit_id" in vals:
        return
    operating_unit_id = get_operating_unit_id_from_enrollment(
        env, vals.get("enrollment_id")
    )
    if operating_unit_id:
        vals["operating_unit_id"] = operating_unit_id
