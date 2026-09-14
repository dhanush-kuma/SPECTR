"""Study lifecycle status values."""

DRAFT = "Draft"
GENERATED = "Generated"
ACTIVE = "Active"

# Studies with randomization that must not be edited via arms/settings UI.
LOCKED_STATUSES = frozenset({GENERATED, ACTIVE})

# Only Active studies cannot replace CSV data (live trial).
CSV_REUPLOAD_BLOCKED_STATUSES = frozenset({ACTIVE})
