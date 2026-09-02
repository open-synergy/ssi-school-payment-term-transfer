# Create School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer_admission
>
> **Extends:** ssi_school_payment_term_transfer -- model `school_payment_term_transfer`,
> action `01-create`

## Additional Fields

When this module is installed, the document gains a second, mutually-exclusive billing
source alongside Enrollment:

- **Admission** _(required when Enrollment is not set)_: Select the open admission whose
  billed amount is being moved between payment terms. Exactly one of Enrollment or
  Admission must be set -- setting both, or neither, is rejected on Save.
- **Admission Source Term** / **Admission Destination Term** _(required together with
  Admission)_: shown on the **Transfer Detail** tab, alongside Source Term/Destination
  Term. Select the Admission payment terms the amount is moved out of and into. Only
  payment terms of the selected Admission that have no customer invoice yet are
  selectable.
- **Admission Source Detail** _(required on each line, together with Admission)_: shown
  on each **Line** row, alongside Source Detail. Select the original Admission fee line
  the amount is being moved from. Only detail lines of the selected Admission Source
  Term that have no customer invoice line yet and are not already voided are selectable.
  Selecting it fills **Amount Before** and **Product** automatically, the same as Source
  Detail does for the Enrollment path.

## Removed / Relaxed

- **Enrollment**, **Source Term**, **Destination Term**, and each line's **Source
  Detail** are no longer individually required -- the exactly-one-of-two-paths rule
  above replaces their previous per-field requirement.

## Additional Post-Condition

- A new menu entry, **School ‣ Admission ‣ Payment Term Transfers**, opens the same list
  filtered to documents whose Admission is set. A **Transfers** smart button is also
  added to the Admission form, mirroring the one the base module adds to the Enrollment
  form.
