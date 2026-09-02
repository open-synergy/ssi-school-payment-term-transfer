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

                // Flow 3 — Source Type is left at its default (Enrollment,
                // the only value this module offers)
                {
                    content: "Source Type shows Enrollment",
                    trigger:
                        "select.o_field_widget[name='source_type']:contains(Enrollment)",
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
                    // The row is still `.o_selected_row` at this point, and
                    // `source_detail_id` (editable m2o) renders as an input
                    // widget rather than plain text while selected, so
                    // `:contains(TOUR PTT Detail Create)` cannot match yet.
                    // Anchor on the currently selected row instead. The
                    // `name` attribute lives on the inner field widget
                    // (`.o_field_widget`), not on the `<td>` itself -- 14.0
                    // `<td>` carries no `name` attribute at all.
                    trigger: ".o_selected_row .o_field_widget[name='amount_before']",
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
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Confirm button is visible in the header",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
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
                {
                    content: "Status is Draft with Confirm available",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Confirm button is visible in the header",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
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

        // IK: docs/school_payment_term_transfer/04-confirm.md
        tour.register(
            "ssi_school_payment_term_transfer_confirm",
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

                // Flow 2 — Open the record to confirm
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Confirm) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Confirm button
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — status changes to Waiting for Approval
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer/05-approve.md
        tour.register(
            "ssi_school_payment_term_transfer_approve",
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

                // Flow 2 — Open the record to approve
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Approve) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Approve button
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — all approval levels fulfilled, status
                // changes automatically to Done
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

        // IK: docs/school_payment_term_transfer/06-reject.md
        tour.register(
            "ssi_school_payment_term_transfer_reject",
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

                // Flow 2 — Open the record to reject
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Reject) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Reject button
                {
                    content: "Click the Reject button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reject_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — status changes to Rejected
                {
                    content: "Status is Rejected",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer/10-cancel.md
        tour.register(
            "ssi_school_payment_term_transfer_cancel",
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

                // Flow 2 — Open the record to cancel
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Cancel) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Cancel button. The header button is
                // `type="action"` naming a numeric action id, never
                // `[name='action_cancel']` -- `:contains(Cancel)` is the
                // only stable selector (odoo-development-ui-test skill,
                // patterns-dialogs-and-wizards.md §H).
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — In the wizard, select the Cancellation Reason.
                // 14.0: no `.modal` prefix -- the trigger is searched
                // INSIDE the already-open modal (§H).
                {
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(TOUR PTT Cancel Reason) input",
                },

                // Flow 5 — Click Confirm
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                },

                // Post-Condition — status changes to Cancelled
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer/12-restart.md
        tour.register(
            "ssi_school_payment_term_transfer_restart",
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

                // Flow 2 — Open the record to restart
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Restart) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Restart button
                {
                    content: "Click the Restart button",
                    trigger: ".o_statusbar_buttons button[name='action_restart']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — status returns to Draft
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer/14-restart-approval.md
        tour.register(
            "ssi_school_payment_term_transfer_restart_approval",
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

                // Flow 2 — Open the record whose approval process is
                // stalled
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Restart Approval) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Restart Approval Process button
                {
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reload_approval_template']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — status remains Waiting for Approval,
                // and a new approval process is rebuilt from the
                // approval template that now matches (visible on the
                // Approvals tab as `approval_template_id` = "Standard",
                // populated again where it was cleared to False by the
                // fixture)
                {
                    content: "Status is still Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Open the Approvals tab",
                    trigger: ".o_notebook .nav-link:contains(Approvals)",
                },
                {
                    content: "Approval Template is re-assigned",
                    trigger:
                        ".o_field_widget[name='approval_template_id']:contains(Standard)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_transfer/15-reload-template-policy.md
        tour.register(
            "ssi_school_payment_term_transfer_reload_template_policy",
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

                // Flow 2 — Open the record whose assigned policy
                // template should be re-evaluated
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTT Reason Reload Template) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — On the Policies tab, click Reload Template
                // Policy
                {
                    content: "Open the Policies tab",
                    trigger: ".o_notebook .nav-link:contains(Policies)",
                },
                {
                    content: "Click Reload Template Policy",
                    trigger: "button[name='action_reload_policy_template']",
                },

                // Post-Condition — Policy Template is recomputed and
                // re-assigned (still "Standard", the only template
                // this module ships, so the visible field keeps
                // showing the same value across the reload)
                {
                    content: "Policy Template is assigned",
                    trigger:
                        ".o_field_widget[name='policy_template_id']:contains(Standard)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
