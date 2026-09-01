# Restart School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer
>
> **Model:** `school_payment_term_transfer`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Transfers
>
> **Actor:** user in group _School Payment Term Transfer — Validator_
>
> **State:** `cancel` | `reject` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` grants `restart_ok` for that state to the
  actor's group.
- **Access:** User is in group _School Payment Term Transfer — Validator_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Transfers** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  starts the approval process from the beginning.
