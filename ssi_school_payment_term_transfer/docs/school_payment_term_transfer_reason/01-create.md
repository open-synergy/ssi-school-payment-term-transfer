# Create School Payment Term Transfer Reason

> **Module:** ssi_school_payment_term_transfer
>
> **Model:** `school_payment_term_transfer_reason`
>
> **Menu:** School ‣ Configuration ‣ Enrollment ‣ Payment Term Transfer Reasons
>
> **Actor:** user in group `Payment Term Transfer Reason`
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group `Payment Term Transfer Reason`.

## Flow

1. Open the **School ‣ Configuration ‣ Enrollment ‣ Payment Term Transfer Reasons**
   menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the reason (e.g. "Renegotiation with
     Parent", "Scheduling Mistake").
   - **Code** _(required)_: Enter a unique code identifying this reason, or enter **/**
     to assign it later using **Generate Code**.
4. Click **Generate Code** in the header to automatically assign a code from the
   `sequence.template` configured for `school_payment_term_transfer_reason`. This
   requires an active `sequence.template` for this model — without one, the action fails
   with an error. You may also leave the Code field as **/** or type a code manually
   instead.
5. Click **Save**.

## Post-Condition

- A new Payment Term Transfer Reason record is created and active.
- The new reason becomes selectable from the reason field of a payment term transfer
  document (added by a later module).
