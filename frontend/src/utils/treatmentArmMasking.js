/**
 * Build a stable treatment-name → masked label map for blinded statistician exports.
 * Configured study arms define ordering; any extra names in records follow alphabetically.
 */
export function buildMaskedArmMap(treatmentNames, orderedArmNames = []) {
  const uniqueFromRecords = [...new Set(treatmentNames.filter(Boolean))]
  const ordered = []
  const seen = new Set()

  for (const name of orderedArmNames) {
    if (uniqueFromRecords.includes(name) && !seen.has(name)) {
      ordered.push(name)
      seen.add(name)
    }
  }

  for (const name of uniqueFromRecords.sort((a, b) => a.localeCompare(b))) {
    if (!seen.has(name)) {
      ordered.push(name)
      seen.add(name)
    }
  }

  const map = new Map()
  ordered.forEach((name, index) => {
    map.set(name, `Arm ${index + 1}`)
  })
  return map
}

export function maskTreatmentArm(treatmentName, armMaskMap) {
  if (!treatmentName) return ''
  return armMaskMap.get(treatmentName) || ''
}
