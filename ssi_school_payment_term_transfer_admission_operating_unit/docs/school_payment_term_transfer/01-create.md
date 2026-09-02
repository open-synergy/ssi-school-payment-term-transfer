# Create School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer_admission_operating_unit
>
> **Extends:** ssi_school_payment_term_transfer -- model `school_payment_term_transfer`,
> action `01-create`

## Additional Post-Condition

- **Operating Unit** (added by `ssi_school_payment_term_transfer_operating_unit`, hidden
  unless the _Multiple Operating Unit_ group applies) is automatically set to the
  selected **Admission**'s own Operating Unit as soon as Admission is selected, after
  Source Type is set to Admission (see
  `ssi_school_payment_term_transfer_admission/docs/school_payment_term_transfer/ 01-create.md`).
  The field is read-only -- it cannot be changed manually on this form. If the selected
  Admission has no Operating Unit, the field is left unchanged (initially the current
  user's default Operating Unit). On the Enrollment path, the field keeps deriving from
  Enrollment exactly as `ssi_school_payment_term_transfer_operating_unit`'s own
  `01-create.md` describes.
