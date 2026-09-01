# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Payment Term Transfer",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_company_currency_mixin",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category/school_payment_term_transfer.xml",
        "security/res_groups/school_payment_term_transfer_reason.xml",
        "security/res_groups/school_payment_term_transfer.xml",
        "security/ir_model_access/school_payment_term_transfer_reason.xml",
        "security/ir_model_access/school_payment_term_transfer.xml",
        "security/ir_rule/school_payment_term_transfer.xml",
        "ir_sequence/school_payment_term_transfer.xml",
        "sequence_template/school_payment_term_transfer.xml",
        "views/school_payment_term_transfer_reason.xml",
        "views/school_payment_term_transfer.xml",
        "views/assets.xml",
    ],
}
