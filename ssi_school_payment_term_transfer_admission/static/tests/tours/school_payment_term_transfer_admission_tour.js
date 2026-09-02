odoo.define(
    "ssi_school_payment_term_transfer_admission.school_payment_term_transfer_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_payment_term_transfer/01-create.md
        // Additional Fields delta -- select Source Type = Admission, then
        // assert the Admission field appears, then stop. Does not
        // continue to Confirm/Approve (E1 tour rule,
        // odoo-development-ui-test skill, scope-and-boundaries.md §3).
        tour.register(
            "ssi_school_payment_term_transfer_admission_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow — Open the School > Student Activities > Payment
                // Term Transfers menu (base module's Flow -- the second
                // "Admission" menu has been removed, see the migration
                // script in this module).
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Transfers menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_transfer.school_payment_term_transfer_menu"]',
                },
                {
                    content: "Payment Term Transfers list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Transfers)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow — Click the New button
                {
                    content: "Click New",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Additional Fields — Select Source Type = Admission.
                // 14.0's <select> carries the o_field_widget class
                // itself, not a wrapping div (patterns-fields.md
                // "Field selection").
                {
                    content: "Select Source Type Admission",
                    trigger: "select.o_field_widget[name='source_type']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Admission",
                },

                // Additional Fields — the Admission field is visible
                // once Source Type is Admission; Enrollment is hidden.
                {
                    content: "Admission field is visible",
                    trigger: ".o_field_many2one[name='admission_id']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer/05-approve.md
        // Additional Post-Condition delta -- the Approve action itself is
        // unchanged, so this re-traces the base flow on an Admission-path
        // document and asserts it still reaches Done (E2a "aksi tetap
        // selesai" framing, odoo-development-ui-test skill,
        // scope-and-boundaries.md §3).
        tour.register(
            "ssi_school_payment_term_transfer_admission_approve",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow — Open the School > Student Activities > Payment
                // Term Transfers menu (base module's Flow -- the second
                // "Admission" menu has been removed).
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Transfers menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_transfer.school_payment_term_transfer_menu"]',
                },
                {
                    content: "Payment Term Transfers list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Transfers)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow — Open the record to approve
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTTA Reason Approve) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow — Click the Approve button
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Additional Post-Condition — the Admission-path document
                // still reaches Done automatically, exactly like the
                // Enrollment path
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
