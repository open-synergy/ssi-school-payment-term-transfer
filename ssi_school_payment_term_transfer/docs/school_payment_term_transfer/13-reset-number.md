# Reset Document Number — School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer
>
> **Model:** `school_payment_term_transfer`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Transfers
>
> **Actor:** user in group _School Payment Term Transfer — Validator_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `sequence.template` exists for this model.
- **Config:** An active `policy.template` grants `manual_number_ok` for state `draft` to
  the actor's group.
- **Access:** User is in group _School Payment Term Transfer — Validator_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Transfers** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the **# Document** field directly
   and change it to **/**).
4. Click **OK** on the confirmation dialog (only when the button was used).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Done**, according
  to the configured sequence.
