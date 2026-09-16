import { renderTextWithLinks } from '../utils/renderTextWithLinks'

function InclusionExclusionModal({ criteria, onAttest, onDecline }) {
  const inclusions = criteria?.inclusions ?? []
  const exclusions = criteria?.exclusions ?? []

  return (
    <div className="modal-overlay">
      <div className="modal-box" style={{ maxWidth: '640px' }}>
        <h3 style={{ margin: '0 0 6px', fontSize: '17px', fontWeight: 700, color: '#1a1a2e' }}>
          Inclusion / Exclusion Criteria
        </h3>
        <p style={{ fontSize: '13px', color: '#555', margin: '0 0 20px', lineHeight: '1.5' }}>
          Review the study eligibility criteria below before attesting that this patient meets
          inclusion/exclusion requirements.
        </p>

        <div className="ie-modal-grid">
          <div className="ie-modal-column ie-modal-column--inclusions">
            <h4>Inclusions</h4>
            {inclusions.length > 0 ? (
              <ol className="ie-modal-list">
                {inclusions.map((item, index) => (
                  <li key={`inclusion-${index}`}>{renderTextWithLinks(item)}</li>
                ))}
              </ol>
            ) : (
              <p className="ie-modal-empty">No inclusion criteria defined.</p>
            )}
          </div>

          <div className="ie-modal-column ie-modal-column--exclusions">
            <h4>Exclusions</h4>
            {exclusions.length > 0 ? (
              <ol className="ie-modal-list">
                {exclusions.map((item, index) => (
                  <li key={`exclusion-${index}`}>{renderTextWithLinks(item)}</li>
                ))}
              </ol>
            ) : (
              <p className="ie-modal-empty">No exclusion criteria defined.</p>
            )}
          </div>
        </div>

        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', marginTop: '20px' }}>
          <button type="button" className="btn-secondary" onClick={onDecline}>
            I Do Not Attest
          </button>
          <button type="button" className="btn-primary" onClick={onAttest}>
            I Attest — Patient Meets I/E Criteria
          </button>
        </div>
      </div>
    </div>
  )
}

export default InclusionExclusionModal
