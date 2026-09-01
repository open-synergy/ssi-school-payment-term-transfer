# Create School Payment Term Transfer

> **Module:** ssi_school_payment_term_transfer_operating_unit
>
> **Extends:** ssi_school_payment_term_transfer -- model `school_payment_term_transfer`,
> action `01-create`

## Additional Post-Condition

- **Operating Unit** (added by this module, hidden unless the _Multiple Operating Unit_
  group applies) is automatically set to the selected **Enrollment**'s own Operating
  Unit as soon as Enrollment is selected in Flow step 3. The field is read-only -- it
  cannot be changed manually on this form. If the selected Enrollment has no Operating
  Unit, the field is left unchanged (initially the current user's default Operating
  Unit).

## Modified — Record Visibility

- Users in the _Operating Unit_ group only see, edit, and delete Payment Term Transfer
  records whose Operating Unit matches one of their own Operating Units. Users outside
  this group are not restricted by this rule.
