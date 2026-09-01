# Edit School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer
>
> **Model:** `school_payment_term_transfer`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Transfers
>
> **Actor:** user in group _School Payment Term Transfer — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _School Payment Term Transfer — User_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Transfers** menu.
2. Open the record to edit.
3. Change any of the editable fields: **Enrollment**, **Reason**, **Date**, **Source
   Term**, **Destination Term**, the **Line** table (add, edit, or remove lines), or
   **Note**.
4. Click **Save**.

## Post-Condition

- The changes are saved.
- **Total**, **Amount After**, and **Full Transfer** recompute to reflect the change.
