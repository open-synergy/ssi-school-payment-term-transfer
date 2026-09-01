# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolPaymentTermTransfer(HttpSavepointCase):
    """Tour tests for ``school_payment_term_transfer`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the enrollment, terms, and fixture documents for the tours.

        The academic term's enrollment window is opened first through
        its public ``action_open_enrollment()`` (see
        ``ssi_school/tests/test_ui_school_academic_term.py``) --
        ``school_enrollment._check_enrollment_window`` rejects an
        enrollment reaching ``open`` while
        ``academic_term_id.enrollment_state`` is still the model's
        default ``close``.

        The enrollment itself is then given a literal ``name`` *before*
        being opened, and is opened through its own
        ``action_open()`` (``mixin.transaction_open``,
        ``_after_approved_method = "action_open"`` on
        ``school_enrollment``) with ``bypass_policy_check`` in the
        context -- exercising its own approval workflow is out of
        scope for this module's tours. ``write({"state": "open"})``
        is deliberately NOT used: it skips ``sudo()``, the
        ``_run_pre_open_check``/``_run_post_open_action`` decorator
        hooks, and -- the part that matters for the create tour's
        many2one dropdown below -- ``_prepare_open_data()``'s call to
        ``_create_sequence()`` (see ``odoo-development-ui-test`` skill,
        ``structure-and-runner.md`` §"Prasyarat state fixture", which
        documents this exact PR). Skipping ``_create_sequence()``
        leaves ``name`` at its default ``"/"``, and ``name_get()``
        (``ssi_transaction_mixin/models/mixin_transaction.py:194-202``)
        then reports every such record as ``"*" + id`` -- indistinguishable
        from the m2o widget's own "Create '...'" entry. Pre-setting
        ``name`` to a literal string (checked by
        ``_create_sequence()`` against the sentinel ``"/"``) also
        skips consuming an ``ir.sequence`` number, avoiding a
        year-dependent ``display_name`` that a tour could not match
        with a literal selector. The edit/delete fixture documents get
        ``user_id`` set explicitly to ``base.user_admin``: ``cls.env``
        runs as superuser, and
        ``school_payment_term_transfer_internal_user_rule`` would
        otherwise hide them from the ``admin`` session the tours log
        in as.
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR PTT Grade Type", "code": "TPTTGT"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR PTT School",
                "code": "TPTTSC",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR PTT Academic Year",
                "code": "TPTTAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR PTT Term",
                "code": "TPTTTM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR PTT Grade",
                "code": "TPTTGR",
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR PTT Class",
                "code": "TPTTCL",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR PTT Contact"})
        student = cls.env["school_student"].create(
            {
                "name": "TOUR PTT Student",
                "code": "TPTTST",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        cls.tour_enrollment = cls.env["school_enrollment"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        academic_term.action_open_enrollment()
        cls.tour_enrollment.write({"name": "TOUR PTT Enrollment"})
        cls.tour_enrollment.with_context(bypass_policy_check=True).action_open()
        account_type_income = cls.env.ref("account.data_account_type_revenue")
        income_account = cls.env["account.account"].create(
            {
                "name": "TOUR PTT Income Account",
                "code": "TPTTIA",
                "user_type_id": account_type_income.id,
                "reconcile": False,
            }
        )
        product = cls.env["product.product"].create(
            {"name": "TOUR PTT Product", "type": "service"}
        )
        cls.tour_source_term = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.tour_enrollment.id,
                "name": "TOUR PTT Source Term",
            }
        )
        cls.tour_destination_term = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.tour_enrollment.id,
                "name": "TOUR PTT Destination Term",
            }
        )
        uom_unit = cls.env.ref("uom.product_uom_unit")
        detail_vals = {
            "term_id": cls.tour_source_term.id,
            "product_id": product.id,
            "account_id": income_account.id,
            "uom_id": uom_unit.id,
            "uom_quantity": 1.0,
            "price_unit": 100000.0,
        }
        cls.tour_detail_create = cls.env[
            "school_enrollment_payment_term_detail"
        ].create(dict(detail_vals, name="TOUR PTT Detail Create"))
        detail_edit = cls.env["school_enrollment_payment_term_detail"].create(
            dict(detail_vals, name="TOUR PTT Detail Edit")
        )
        detail_delete = cls.env["school_enrollment_payment_term_detail"].create(
            dict(detail_vals, name="TOUR PTT Detail Delete")
        )
        cls.tour_reason_create = cls.env["school_payment_term_transfer_reason"].create(
            {"name": "TOUR PTT Reason Create", "code": "/"}
        )
        reason_edit = cls.env["school_payment_term_transfer_reason"].create(
            {"name": "TOUR PTT Reason Edit", "code": "/"}
        )
        reason_delete = cls.env["school_payment_term_transfer_reason"].create(
            {"name": "TOUR PTT Reason Delete", "code": "/"}
        )
        cls.tour_edit_doc = cls.env["school_payment_term_transfer"].create(
            {
                "user_id": admin.id,
                "enrollment_id": cls.tour_enrollment.id,
                "reason_id": reason_edit.id,
                "source_term_id": cls.tour_source_term.id,
                "destination_term_id": cls.tour_destination_term.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "source_detail_id": detail_edit.id,
                            "amount_before": 100000.0,
                            "amount": 25000.0,
                        },
                    )
                ],
            }
        )
        cls.tour_delete_doc = cls.env["school_payment_term_transfer"].create(
            {
                "user_id": admin.id,
                "enrollment_id": cls.tour_enrollment.id,
                "reason_id": reason_delete.id,
                "source_term_id": cls.tour_source_term.id,
                "destination_term_id": cls.tour_destination_term.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "source_detail_id": detail_delete.id,
                            "amount_before": 100000.0,
                            "amount": 10000.0,
                        },
                    )
                ],
            }
        )

        # Fixtures for the confirm/approve/reject/cancel/restart/restart
        # approval tours below. Each uses its own Source Detail (never
        # shared) so ``_check_source_detail_not_targeted_elsewhere``
        # never fires between these fixtures. ``base.user_admin`` is
        # listed in ``school_payment_term_transfer_validator_group``'s
        # ``users`` (see security/res_groups), which implies the user
        # group -- so ``admin`` can Confirm, Approve, Reject, Cancel,
        # and Restart every fixture below, and is the approval
        # template's approver.
        cls.tour_cancel_reason = cls.env["base.cancel_reason"].create(
            {"name": "TOUR PTT Cancel Reason", "code": "/"}
        )

        def _create_transfer_doc(reason_name, detail_name, amount=25000.0):
            """Create one draft transfer document for a workflow tour.

            :param reason_name: value of the fixture Reason's ``name``.
            :param detail_name: value of the fixture Source Detail's
                ``name``.
            :param amount: value written to the line's ``amount``.
            :return: the created ``school_payment_term_transfer``
                record.
            """
            reason = cls.env["school_payment_term_transfer_reason"].create(
                {"name": reason_name, "code": "/"}
            )
            detail = cls.env["school_enrollment_payment_term_detail"].create(
                dict(detail_vals, name=detail_name)
            )
            return cls.env["school_payment_term_transfer"].create(
                {
                    "user_id": admin.id,
                    "enrollment_id": cls.tour_enrollment.id,
                    "reason_id": reason.id,
                    "source_term_id": cls.tour_source_term.id,
                    "destination_term_id": cls.tour_destination_term.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "source_detail_id": detail.id,
                                "amount_before": 100000.0,
                                "amount": amount,
                            },
                        )
                    ],
                }
            )

        cls.tour_confirm_doc = _create_transfer_doc(
            "TOUR PTT Reason Confirm", "TOUR PTT Detail Confirm"
        )

        cls.tour_approve_doc = _create_transfer_doc(
            "TOUR PTT Reason Approve", "TOUR PTT Detail Approve"
        )
        cls.tour_approve_doc.with_context(bypass_policy_check=True).action_confirm()

        cls.tour_reject_doc = _create_transfer_doc(
            "TOUR PTT Reason Reject", "TOUR PTT Detail Reject"
        )
        cls.tour_reject_doc.with_context(bypass_policy_check=True).action_confirm()

        cls.tour_cancel_doc = _create_transfer_doc(
            "TOUR PTT Reason Cancel", "TOUR PTT Detail Cancel"
        )

        cls.tour_restart_doc = _create_transfer_doc(
            "TOUR PTT Reason Restart", "TOUR PTT Detail Restart"
        )
        cls.tour_restart_doc.with_context(bypass_policy_check=True).action_cancel(
            cancel_reason=cls.tour_cancel_reason
        )

        cls.tour_restart_approval_doc = _create_transfer_doc(
            "TOUR PTT Reason Restart Approval", "TOUR PTT Detail Restart Approval"
        )
        cls.tour_restart_approval_doc.with_context(
            bypass_policy_check=True
        ).action_confirm()
        # Simulate a stalled approval process: no approval template
        # assigned. This is not a state transition (``state`` stays
        # ``confirm``), it is exactly the precondition documented in
        # ``14-restart-approval.md`` -- so a plain ``write()`` here
        # matches what it is meant to set up, rather than working
        # around a hook.
        cls.tour_restart_approval_doc.write({"approval_template_id": False})

        cls.tour_reload_template_doc = _create_transfer_doc(
            "TOUR PTT Reason Reload Template", "TOUR PTT Detail Reload Template"
        )

    def test_create(self):
        """Run the create tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``school_payment_term_transfer``.

        IK: docs/school_payment_term_transfer/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_restart_approval",
            login="admin",
        )

    def test_reload_template_policy(self):
        """Run the reload template policy tour.

        IK: docs/school_payment_term_transfer/15-reload-template-policy.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_transfer_reload_template_policy",
            login="admin",
        )
