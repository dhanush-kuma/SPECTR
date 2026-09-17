import { useEffect } from 'react'
import { renderTextWithLinks } from '../utils/renderTextWithLinks'

function InclusionExclusionModal({ criteria, onAttest, onDecline }) {
  const inclusions = criteria?.inclusions ?? []
  const exclusions = criteria?.exclusions ?? []

  useEffect(() => {
    const { overflow, paddingRight } = document.body.style
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth
    document.body.style.overflow = 'hidden'
    if (scrollbarWidth > 0) {
      document.body.style.paddingRight = `${scrollbarWidth}px`
    }
    return () => {
      document.body.style.overflow = overflow
      document.body.style.paddingRight = paddingRight
    }
  }, [])

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="ie-modal-title">
      <div className="modal-box modal-box--scrollable" style={{ maxWidth: '640px' }}>
        <div className="modal-box__scroll">
          <h3
            id="ie-modal-title"
            style={{ margin: '0 0 6px', fontSize: '17px', fontWeight: 700, color: '#1a1a2e' }}
          >
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
        </div>

        <div className="modal-box__footer">
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
