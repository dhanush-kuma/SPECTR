import { TOS_URL } from '../content/termsOfService'

function TermsOfServiceContent() {
  return (
    <article className="tos-document">
      <header className="tos-document__header">
        <h1 id="tos-modal-title" className="tos-document__title">
          Terms of Service and Platform Use Agreement
        </h1>
        <p className="tos-document__subtitle">
          For the SPECTR Clinical Trial Allocation Platform
        </p>
        <p className="tos-document__meta">
          Available via{' '}
          <a href={TOS_URL} target="_blank" rel="noopener noreferrer">
            {TOS_URL}
          </a>
        </p>
      </header>

      <aside className="tos-document__notice" role="note">
        <h2 className="tos-document__notice-title">Important Notice to All Users</h2>
        <p>
          Please read this entire agreement carefully. By logging into, accessing, or using the
          SPECTR platform, you acknowledge that you have read, understood, and unequivocally agree
          to be legally bound by all terms and conditions stated herein. If you do not agree, do not
          access or use this platform.
        </p>
      </aside>

      <section className="tos-document__section">
        <h2>1. Parties and Acceptance</h2>
        <h3>1.1 Service Provider</h3>
        <p>
          This system is operated by Manakkodam Manu Medical Research (OPC) Pvt. Ltd., Cherthala,
          Kerala, India (hereinafter referred to as the &ldquo;Service Provider&rdquo;).
        </p>
        <h3>1.2 User</h3>
        <p>
          Any individual logging into this platform—including Trial Coordinators, Principal
          Investigators, Co-Investigators, Biostatisticians, and Site Research Staff (hereinafter
          referred to as the &ldquo;User&rdquo;)—accesses this service subject to these Terms of
          Service.
        </p>
        <h3>1.3 Electronic Consent</h3>
        <p>
          By clicking &ldquo;I Have Read and Agree to the Terms of Service&rdquo; below, you
          execute a legally binding electronic agreement under the Information Technology Act, 2000
          (India) and applicable electronic signature laws. Your user ID, IP address, and
          acceptance timestamp will be permanently logged in the system&apos;s immutable audit
          trail.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>2. Scope of Service</h2>
        <h3>2.1</h3>
        <p>
          The Service Provider grants authorized users access to the SPECTR platform solely for the
          purpose of executing centralized, stratified, point-of-care randomization and allocation
          concealment for designated clinical protocols.
        </p>
        <h3>2.2</h3>
        <p>
          The service is provided as a free academic and community tool. The Service Provider does
          not charge licensing or operational fees, nor does it act as a commercial Contract
          Research Organization (CRO) or trial sponsor.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>3. &ldquo;AS IS&rdquo; Provision and Warranty Disclaimer</h2>
        <h3>3.1 No Warranties</h3>
        <p>
          The SPECTR platform is provided on an &ldquo;AS IS&rdquo; and &ldquo;AS AVAILABLE&rdquo;
          basis, without warranties of any kind, express or implied, including but not limited to
          warranties of merchantability, fitness for a particular purpose, continuous availability,
          accuracy of user-uploaded data, or non-infringement.
        </p>
        <h3>3.2 No Service Level Agreement (SLA)</h3>
        <p>
          The Service Provider makes reasonable efforts to maintain platform uptime, but does not
          guarantee uninterrupted, secure, or error-free operation. Scheduled maintenance, emergency
          downtime, server interruptions, or network failures may occur without prior notice.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>4. Regulatory and ICH-GCP Compliance</h2>
        <h3>4.1 Regulatory Responsibility</h3>
        <p>
          Under ICH-GCP E6 (Section 5.5.3) and relevant national regulations, the Study Sponsor
          and Principal Investigator retain ultimate and non-delegable legal responsibility for the
          trial&apos;s conduct, protocol compliance, data integrity, and compliance with
          computerized system validation requirements.
        </p>
        <h3>4.2 System Validation</h3>
        <p>
          The User and their Sponsoring Institution acknowledge that they have independently
          evaluated the SPECTR platform and determined that its functionality satisfies their
          institutional ethics committee (IEC/IRB) and protocol requirements.
        </p>
        <h3>4.3 Independent Sequence Verification</h3>
        <p>
          The Trial Coordinator and Study Biostatistician are strictly responsible for the
          statistical design, accuracy, block structure, and integrity of any randomization lists
          generated and uploaded to the platform.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>5. Data Protection, Backup, and Participant Anonymity</h2>
        <h3>5.1 No Protected Health Information (PHI)</h3>
        <p>
          Users warrant that they shall only enter de-identified, pseudonymized screening/participant
          identifiers into the platform. No direct patient identifiers (e.g., patient names,
          government identity numbers, phone numbers, addresses) shall ever be inputted.
        </p>
        <h3>5.2 Independent Record Retention</h3>
        <p>
          The platform is not a permanent data repository or Trial Master File (TMF). Users must
          maintain independent, secondary offline documentation of all allocations (e.g., preserving
          timestamped email confirmations, site enrollment logs, and audit records).
        </p>
      </section>

      <section className="tos-document__section">
        <h2>6. Limitation of Liability and Indemnification</h2>
        <h3>6.1 Exclusion of Damages</h3>
        <p>
          To the maximum extent permitted by law, in no event shall the Service Provider, its
          directors, employees, or developers be liable for any direct, indirect, incidental,
          special, consequential, or punitive damages, including but not limited to:
        </p>
        <ul>
          <li>Loss of trial data, sequence corruptions, or allocation errors.</li>
          <li>Service disruptions, server downtime, or inability to randomize participants.</li>
          <li>Security breaches, unauthorized access, server compromises, or hacking events.</li>
          <li>
            Trial suspensions, protocol deviations, ethics committee actions, or regulatory
            sanctions.
          </li>
        </ul>
        <h3>6.2 Indemnification</h3>
        <p>
          The User and their Sponsoring Institution agree to indemnify, defend, and hold harmless
          the Service Provider from any third-party claims, liabilities, or regulatory actions
          arising from the conduct of the trial, site investigator actions, or misuse of the
          platform.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>7. Account Security and Termination</h2>
        <h3>7.1</h3>
        <p>
          Users are strictly responsible for maintaining the confidentiality of their login
          credentials. Sharing accounts between multiple investigators is prohibited.
        </p>
        <h3>7.2</h3>
        <p>
          The Service Provider reserves the right to suspend or revoke access to any user or trial
          profile in the event of suspected misuse, security threats, or regulatory concerns.
        </p>
        <h3>7.3</h3>
        <p>
          Following completion of trial recruitment or upon written request, the Service Provider
          reserves the right to archive or purge study records and allocation tables from the live
          server after allowing the Trial Coordinator a reasonable window to export their final
          allocation and audit logs.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>8. Governing Law</h2>
        <p>
          This Agreement shall be governed by and construed in accordance with the laws of India.
          Any disputes arising under this agreement shall fall within the exclusive jurisdiction of
          the courts located in Kochi, Kerala, India.
        </p>
      </section>
    </article>
  )
}

export default TermsOfServiceContent
