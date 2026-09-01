odoo.define(
    "ssi_school_payment_term_transfer.school_payment_term_transfer_reason_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_payment_term_transfer_reason/01-create.md
        tour.register(
            "ssi_school_payment_term_transfer_reason_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Configuration > Enrollment >
                // Payment Term Transfer Reasons menu. "Enrollment" is a
                // level-3 grouping header (has children, no data-menu-xmlid)
                // so it is not a clickable step — go straight to the leaf.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
                },
                {
                    content: "Open the Payment Term Transfer Reasons menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_transfer.school_payment_term_transfer_reason_menu"]',
                },
                {
                    content: "Payment Term Transfer Reasons list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Transfer Reasons)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Click the New button
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

                // Flow 3 — Fill in the required fields
                {
                    content: "Fill in Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR Payment Term Transfer Reason Create",
                },
                {
                    content: "Fill in Code",
                    trigger: ".o_field_widget[name='code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text /",
                },

                // Flow 5 — Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition — record is created and active
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer_reason/02-edit.md
        tour.register(
            "ssi_school_payment_term_transfer_reason_edit",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Configuration > Enrollment >
                // Payment Term Transfer Reasons menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
                },
                {
                    content: "Open the Payment Term Transfer Reasons menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_transfer.school_payment_term_transfer_reason_menu"]',
                },
                {
                    content: "Payment Term Transfer Reasons list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Transfer Reasons)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Find and open the record to edit
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR Payment Term Transfer Reason Edit) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Change the required fields
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR Payment Term Transfer Reason Edited",
                },

                // Flow 5 — Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition — the record is updated with the new values
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer_reason/03-delete.md
        tour.register(
            "ssi_school_payment_term_transfer_reason_delete",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Configuration > Enrollment >
                // Payment Term Transfer Reasons menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
                },
                {
                    content: "Open the Payment Term Transfer Reasons menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_transfer.school_payment_term_transfer_reason_menu"]',
                },
                {
                    content: "Payment Term Transfer Reasons list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Transfer Reasons)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Select the record to delete
                {
                    content: "Select the record",
                    trigger:
                        ".o_data_row:contains(TOUR Payment Term Transfer Reason Delete) .o_list_record_selector input",
                    extra_trigger: ".o_list_view",
                },

                // Flow 3 — Click Action > Delete
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Delete";
                            }
                        );
                        $delete[0].click();
                    },
                },

                // Flow 4 — Click OK to confirm
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — the record no longer appears in the list
                {
                    content: "Record is removed from the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR Payment Term Transfer Reason Delete)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
