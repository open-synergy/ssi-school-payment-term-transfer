# Approve School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer_admission
>
> **Extends:** ssi_school_payment_term_transfer -- model `school_payment_term_transfer`,
> action `05-approve`

## Additional Post-Condition

The Approve button, its confirmation dialog, and the automatic transition to **Done**
are unchanged -- there is no new step to click. When the document's billing source is
Admission instead of Enrollment, reaching Done applies the transfer against the
Admission side instead:

- A new detail line is created on the **Admission Destination Term** (not the Enrollment
  Destination Term), carrying the moved product, amount, and tax(es).
- The **Admission Source Term**'s own detail line is adjusted the same way the
  Enrollment side is (see `01-create` for what the document looked like before this
  point): fully voided when the whole line was moved, or reduced by the moved amount
  otherwise.
- The Admission's own aggregated product summary is refreshed, and its chatter receives
  the same move-summary message the base module posts on the Enrollment, linking back to
  this document.
- The pre-Done gate rejects Done the same way if either Admission term has received a
  customer invoice since Confirm -- exactly like the Enrollment side.

As with the base module, this document has no manual Done button -- the transition
happens automatically as soon as the last approval level is fulfilled.
