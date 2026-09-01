# Delete School Payment Term Transfer

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
2. Select the record to delete (or open it).
3. Click the **Action** menu, then **Delete**. When deleting from the list, select the
   record's checkbox first.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- The Payment Term Transfer document, along with all of its lines, no longer exists.
- The Source Term, Destination Term, and their detail lines are unaffected.
