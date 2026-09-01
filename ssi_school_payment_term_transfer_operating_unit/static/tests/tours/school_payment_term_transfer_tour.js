odoo.define(
    "ssi_school_payment_term_transfer_operating_unit.school_payment_term_transfer_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_payment_term_transfer/01-create.md
        // Delta tour: navigation steps 1-3 are the base module's Flow
        // (docs/school_payment_term_transfer/01-create.md in
        // ssi_school_payment_term_transfer), the assertion after is
        // this module's Additional Post-Condition. Deliberately stops
        // right after that assertion -- confirm/approve are out of
        // scope for this delta.
        tour.register(
            "ssi_school_payment_term_transfer_operating_unit_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 (base) — Open the School > Student Activities >
                // Payment Term Transfers menu.
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

                // Flow 2 (base) — Click the New button
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

                // Flow 3 (base) — Select the Enrollment
                {
                    content: "Select the Enrollment",
                    trigger: ".o_field_many2one[name='enrollment_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR PTTOU Enrollment",
                },
                {
                    content: "Pick the Enrollment from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTTOU Enrollment)",
                    in_modal: false,
                },

                // Additional Post-Condition (this module) — Operating
                // Unit is filled from the Enrollment's own Operating
                // Unit. This would NOT match if the field had kept the
                // logged-in user's default Operating Unit instead.
                {
                    content: "Operating Unit is filled from the Enrollment",
                    trigger:
                        ".o_field_widget[name='operating_unit_id']:contains(TOUR PTTOU Operating Unit)",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
