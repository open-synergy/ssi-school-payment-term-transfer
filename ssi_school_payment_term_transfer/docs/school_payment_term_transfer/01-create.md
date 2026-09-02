# Create School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer
>
> **Model:** `school_payment_term_transfer`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Transfers
>
> **Actor:** user in group _School Payment Term Transfer — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** An open Enrollment exists for the student, with at least two Payment Terms
  that have no customer invoice yet -- one to use as Source Term, one as Destination
  Term.
- **Data:** At least one detail line on the intended Source Term has no customer invoice
  line yet and is not already voided, so it can be picked as a Source Detail.
- **Data:** A Payment Term Transfer Reason exists (see
  `school_payment_term_transfer_reason/01-create`).
- **Access:** User is in group _School Payment Term Transfer — User_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Transfers** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Source Type** _(required)_: Leave it as **Enrollment** -- this module only offers
     that value. It controls which fields below are shown and required.
   - **Enrollment** _(required)_: Select the open enrollment whose billed amount is
     being moved. Selecting it fills Student, Academic Year, and Academic Term
     automatically.
   - **Reason** _(required)_: Select why this amount is being moved.
4. **Date** is filled with today's date automatically; change it if needed.
5. Open the **Transfer Detail** tab.
6. Fill in the required fields:
   - **Source Term** _(required)_: Select the payment term the amount is being moved out
     of. Only payment terms of the selected Enrollment that have no customer invoice yet
     are selectable.
   - **Destination Term** _(required)_: Select the payment term the amount is being
     moved into. Must be different from Source Term.
7. In the **Line** table, click **Add a line** and fill in:
   - **Source Detail** _(required)_: Select the original fee line the amount is being
     moved from. Only detail lines of the selected Source Term that have no customer
     invoice line yet and are not already voided are selectable. Selecting it fills
     **Amount Before** and **Product** automatically.
   - **Amount** _(required)_: Enter the portion of Amount Before being moved to the
     Destination Term. Must be greater than zero and no greater than Amount Before.
     **Amount After** and **Full Transfer** are computed automatically as you type.
8. Repeat step 7 for additional lines if more than one fee line is being moved. Each
   line must use a different Source Detail.
9. Optionally fill in **Note** with a free-form explanation.
10. Click **Save**.

## Post-Condition

- A new Payment Term Transfer document is created in **Draft** status. It has no
  document number yet.
- **Total** on the header equals the sum of **Amount** across all lines.
- The document does not write anything to the Source Term, Destination Term, or their
  detail lines yet -- moving the amount is not part of this action.
- The **Confirm** button is visible in the header (usable once the prerequisites in
  `04-confirm` are met), and the statusbar shows **Draft ‣ Waiting for Approval ‣
  Done**.
- The list view shows this document's **Source Document**, **Source Term**, and
  **Destination Term** columns filled with the Enrollment, Source Term, and Destination
  Term's names, instead of separate Enrollment/Source Term/Destination Term columns.
