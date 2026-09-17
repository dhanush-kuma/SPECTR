import { useEffect } from 'react'
import TermsOfServiceContent from './TermsOfServiceContent'

function TermsOfServiceModal({
  onAccept,
  onDecline,
  accepting = false,
  error = null,
  termsAccepted,
  onTermsAcceptedChange,
}) {
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
    <div
      className="modal-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="tos-modal-title"
    >
      <div className="modal-box modal-box--scrollable tos-modal" style={{ maxWidth: '760px' }}>
        <div className="modal-box__scroll">
          <TermsOfServiceContent />
        </div>

        <div className="modal-box__footer tos-modal__footer">
          <div className="tos-modal__acceptance">
            <label htmlFor="org-accept-terms" className="checkbox-label tos-modal__checkbox">
              <input
                id="org-accept-terms"
                type="checkbox"
                checked={termsAccepted}
                onChange={(e) => onTermsAcceptedChange(e.target.checked)}
              />
              I Have Read and Agree to the Terms of Service
            </label>
            {error && <p className="error tos-modal__error">{error}</p>}
          </div>

          <div className="tos-modal__actions">
            <button type="button" className="btn-secondary" onClick={onDecline} disabled={accepting}>
              Cancel
            </button>
            <button
              id="btn-org-accept-terms"
              type="button"
              className="btn-primary"
              onClick={onAccept}
              disabled={accepting || !termsAccepted}
            >
              {accepting ? 'Accepting…' : 'Accept and Continue'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TermsOfServiceModal
