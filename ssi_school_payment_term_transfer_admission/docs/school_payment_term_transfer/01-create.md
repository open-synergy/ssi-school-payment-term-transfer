# Create School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer_admission
>
> **Extends:** ssi_school_payment_term_transfer -- model `school_payment_term_transfer`,
> action `01-create`

## Additional Fields

When this module is installed, **Source Type** (Flow step 3 of the base module's
`01-create`) gains a second value, **Admission**, alongside Enrollment. Selecting it
shows a different set of fields, and hides the Enrollment ones:

- **Source Type = Admission** _(Flow step 3)_: Selecting **Admission** hides
  **Enrollment** and shows the fields below instead.
- **Admission** _(required)_: Select the open admission whose billed amount is being
  moved between payment terms.
- **Admission Source Term** / **Admission Destination Term** _(required)_: shown on the
  **Transfer Detail** tab, replacing Source Term/Destination Term. Select the Admission
  payment terms the amount is moved out of and into. Only payment terms of the selected
  Admission that have no customer invoice yet are selectable.
- **Admission Source Detail** _(required on each line)_: shown on each **Line** row,
  replacing Source Detail. Select the original Admission fee line the amount is being
  moved from. Only detail lines of the selected Admission Source Term that have no
  customer invoice line yet and are not already voided are selectable. Selecting it
  fills **Amount Before** and **Product** automatically, the same as Source Detail does
  for the Enrollment path.

## Additional Post-Condition

- A **Transfers** smart button is added to the Admission form, mirroring the one the
  base module adds to the Enrollment form, and opens a list of this Admission's own
  documents with Source Type pre-selected to Admission.
