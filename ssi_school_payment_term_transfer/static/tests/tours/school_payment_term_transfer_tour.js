odoo.define(
    "ssi_school_payment_term_transfer.school_payment_term_transfer_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_payment_term_transfer/01-create.md
        tour.register(
            "ssi_school_payment_term_transfer_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Transfers menu. "Student Activities" is a
                // level-2 menu (direct child of the app root), so unlike
                // a level-3 grouping header it IS clickable.
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

                // Flow 3 — Fill in the required header fields
                {
                    content: "Select the Enrollment",
                    trigger: ".o_field_many2one[name='enrollment_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR PTT Enrollment",
                },
                {
                    content: "Pick the Enrollment from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTT Enrollment)",
                    in_modal: false,
                },
                {
                    content: "Select the Reason",
                    trigger: ".o_field_many2one[name='reason_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR PTT Reason Create",
                },
                {
                    content: "Pick the Reason from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTT Reason Create)",
                    in_modal: false,
                },

                // Flow 5 — Open the Transfer Detail tab
                {
                    content: "Open the Transfer Detail tab",
                    trigger: ".o_notebook .nav-link:contains(Transfer Detail)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },

                // Flow 6 — Fill in Source Term and Destination Term
                {
                    content: "Select the Source Term",
                    trigger: ".o_field_many2one[name='source_term_id'] input",
                    run: "text TOUR PTT Source Term",
                },
                {
                    content: "Pick the Source Term from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTT Source Term)",
                    in_modal: false,
                },
                {
                    content: "Select the Destination Term",
                    trigger: ".o_field_many2one[name='destination_term_id'] input",
                    run: "text TOUR PTT Destination Term",
                },
                {
                    content: "Pick the Destination Term from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTT Destination Term)",
                    in_modal: false,
                },

                // Flow 7 — Add a line and fill Source Detail and Amount
                {
                    content: "Click Add a line",
                    trigger: ".o_field_x2many .o_field_x2many_list_row_add a",
                },
                {
                    content: "Select the Source Detail",
                    trigger:
                        ".o_selected_row .o_field_widget[name='source_detail_id'] input",
                    run: "text TOUR PTT Detail Create",
                },
                {
                    content: "Pick the Source Detail from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTT Detail Create)",
                    in_modal: false,
                },
                {
                    content: "Fill in Amount",
                    trigger: ".o_selected_row .o_field_widget[name='amount'] input",
                    run: "text 25000",
                },
                {
                    content: "Commit the line by clicking another cell",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Detail Create) .o_field_cell[name='amount_before']",
                },

                // Flow 10 — Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition — document created in Draft
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status button.o_arrow_button_current:contains(Draft)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer/02-edit.md
        tour.register(
            "ssi_school_payment_term_transfer_edit",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Transfers menu
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

                // Flow 2 — Open the record to edit (found by its Reason,
                // since the document number stays "/" while still Draft)
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Edit) .o_data_cell:first",
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

                // Flow 3 — Change the Note field
                {
                    content: "Fill in Note",
                    trigger:
                        ".o_notebook .tab-pane.active textarea.o_field_widget[name='note']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Edited via tour",
                },

                // Flow 4 — Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition — the change is saved
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer/03-delete.md
        tour.register(
            "ssi_school_payment_term_transfer_delete",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Transfers menu
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

                // Flow 2 — Select the record to delete (found by its
                // Reason, since the document number stays "/" while
                // still Draft)
                {
                    content: "Select the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Delete) .o_list_record_selector input",
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
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR PTT Reason Delete)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
