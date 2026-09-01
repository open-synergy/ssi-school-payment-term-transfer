# Confirm School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer
>
> **Model:** `school_payment_term_transfer`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Transfers
>
> **Actor:** user in group _School Payment Term Transfer — User_
>
> **State:** `draft` → `confirm`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** The document has at least one line.
- **Record:** Source Term and Destination Term are both set and different, and both
  belong to the selected Enrollment.
- **Record:** Neither Source Term nor Destination Term has a Customer Invoice yet.
- **Record:** Every line's Source Detail belongs to the Source Term, has no Customer
  Invoice Line yet, is not already voided, and has a UoM Quantity of exactly 1.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _School Payment Term Transfer — User_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Transfers** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
- No line, Source Term, or Destination Term has been changed yet -- the transfer is only
  applied once the document reaches **Done**.
