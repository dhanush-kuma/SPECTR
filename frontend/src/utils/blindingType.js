export const BLINDING_TYPE = {
  OPEN_LABEL: 0,
  PB: 1,
  PIB: 2,
  PISB: 3,
}

export const DEFAULT_BLINDING_TYPE = BLINDING_TYPE.PIB

// PISB is equivalent to PIB from the investigator's perspective.
export const INVESTIGATOR_BLINDED_BLINDING_TYPES = [
  BLINDING_TYPE.PIB,
  BLINDING_TYPE.PISB,
]

export const BLINDING_TYPE_OPTIONS = [
  { value: BLINDING_TYPE.OPEN_LABEL, label: 'Open Label' },
  { value: BLINDING_TYPE.PB, label: 'Participant blinding (PB)' },
  { value: BLINDING_TYPE.PIB, label: 'Participant and Investigator blinding (PIB)' },
  {
    value: BLINDING_TYPE.PISB,
    label: 'Participant, Investigator and Statistician blinding (PISB)',
  },
]

const BLINDING_TYPE_SHORT_LABELS = {
  [BLINDING_TYPE.OPEN_LABEL]: 'Open Label',
  [BLINDING_TYPE.PB]: 'PB',
  [BLINDING_TYPE.PIB]: 'PIB',
  [BLINDING_TYPE.PISB]: 'PISB',
}

export function blindingTypeLabel(value) {
  const option = BLINDING_TYPE_OPTIONS.find((item) => item.value === value)
  return option?.label ?? `Unknown (${value})`
}

export function blindingTypeShortLabel(value) {
  return BLINDING_TYPE_SHORT_LABELS[value] ?? `Unknown (${value})`
}

export function investigatorIsBlinded(blindingType) {
  return INVESTIGATOR_BLINDED_BLINDING_TYPES.includes(blindingType)
}
