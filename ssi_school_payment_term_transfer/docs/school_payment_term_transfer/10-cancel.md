# Cancel School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer
>
> **Model:** `school_payment_term_transfer`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Transfers
>
> **Actor:** user in group _School Payment Term Transfer — Validator_
>
> **State:** `draft` | `confirm` | `reject` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Rejected**. Once the
  transfer reaches **Done**, it is terminal and can no longer be cancelled.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group _School Payment Term Transfer — Validator_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Transfers** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- No line, Source Term, or Destination Term has been changed -- a cancelled transfer
  never applies.
