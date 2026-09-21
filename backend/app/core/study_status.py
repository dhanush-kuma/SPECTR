"""Study lifecycle status values."""

DRAFT = "Draft"
GENERATED = "Generated"
ACTIVE = "Active"
COMPLETE = "Complete"

# Studies with randomization that must not be edited via arms/settings UI.
LOCKED_STATUSES = frozenset({GENERATED, ACTIVE, COMPLETE})

# Live or finished trials cannot replace CSV data.
CSV_REUPLOAD_BLOCKED_STATUSES = frozenset({ACTIVE, COMPLETE})

# Only pre-live studies may be permanently removed.
DELETABLE_STATUSES = frozenset({DRAFT, GENERATED})
