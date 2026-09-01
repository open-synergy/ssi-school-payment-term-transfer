# Approve School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer
>
> **Model:** `school_payment_term_transfer`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Transfers
>
> **Actor:** approver on the pending approval level, in group _School Payment Term
> Transfer — Validator_
>
> **State:** `confirm` → `done`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** Neither Source Term nor Destination Term has received a Customer Invoice
  since Confirm -- if either has, Approve fails and the term that is already invoiced is
  named in the error.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Transfers** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If all approval levels are fulfilled, status changes automatically to **Done** and the
  transfer is applied: for every line, a new detail line is created on the Destination
  Term carrying the moved product, amount, and tax(es), and the Source Term's own detail
  line is adjusted (see `01-create` and `02-edit` for what the document looked like
  before this point). The enrollment's total billed amount stays unchanged, and its
  chatter receives a message summarising the move with a link back to this document.
  Once Done, the transfer is terminal and can no longer be cancelled or reverted -- to
  undo it, create a new transfer in the opposite direction.

> **Note:** `school_payment_term_transfer` has no manual Done button
> (`_automatically_insert_done_button` is disabled). The transition to **Done** always
> happens automatically as soon as the last approval level is fulfilled -- there is no
> `07-start.md`, `08-open.md`, or `09-finish.md` for this model.
