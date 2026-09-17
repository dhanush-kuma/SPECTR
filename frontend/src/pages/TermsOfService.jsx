import Header from '../components/Header'
import TermsOfServiceContent from '../components/TermsOfServiceContent'

function TermsOfService() {
  return (
    <>
      <Header />

      <main className="app app--legal">
        <div className="legal-page">
          <TermsOfServiceContent />
        </div>
      </main>
    </>
  )
}

export default TermsOfService
