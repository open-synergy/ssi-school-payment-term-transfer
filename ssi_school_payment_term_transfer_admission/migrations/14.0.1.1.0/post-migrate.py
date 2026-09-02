# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.0.0 -> 14.0.1.1.0
#
# Changes: the second menu ("School > Admission > Payment Term
#          Transfers") and its action are removed from the code --
#          routing to the Admission billing source now goes through
#          the single base menu's "Source Type" selector instead.
#          Rows already carrying an Admission (``admission_id`` set)
#          still have ``source_type`` at its "enrollment" default,
#          since that field's value was only ever set by this
#          module's now-removed action context -- stamp it to
#          "admission" so the routing added in this release resolves
#          them correctly.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Drop the removed menu/action and stamp ``source_type``.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; deletes two XML-ID-identified records and
        updates ``school_payment_term_transfer`` rows
    """
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "ssi_school_payment_term_transfer_admission."
            "school_payment_term_transfer_menu_admission",
            "ssi_school_payment_term_transfer_admission."
            "school_payment_term_transfer_action_admission",
        ],
    )
    rows = openupgrade.logged_query(
        env.cr,
        """
        UPDATE school_payment_term_transfer
        SET source_type = 'admission'
        WHERE admission_id IS NOT NULL
        """,
    )
    _logger.info("Stamped source_type='admission' on %s row(s).", rows)
