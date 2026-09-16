from enum import IntEnum


class BlindingType(IntEnum):
    OPEN_LABEL = 0
    PB = 1  # Participant blinding
    PIB = 2  # Participant and Investigator blinding
    PISB = 3  # Participant, Investigator and Statistician blinding


BLINDING_TYPE_LABELS: dict[BlindingType, str] = {
    BlindingType.OPEN_LABEL: "Open Label",
    BlindingType.PB: "Participant blinding (PB)",
    BlindingType.PIB: "Participant and Investigator blinding (PIB)",
    BlindingType.PISB: "Participant, Investigator and Statistician blinding (PISB)",
}

# PISB is equivalent to PIB from the investigator's perspective.
INVESTIGATOR_BLINDED_BLINDING_TYPES = frozenset({BlindingType.PIB, BlindingType.PISB})


def validate_blinding_type(value: int) -> int:
    try:
        BlindingType(value)
    except ValueError:
        raise ValueError("blinding_type must be 0 (Open Label), 1 (PB), 2 (PIB), or 3 (PISB)")
    return value


def investigator_is_blinded(blinding_type: int) -> bool:
    return blinding_type in INVESTIGATOR_BLINDED_BLINDING_TYPES
