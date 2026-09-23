import { TOS_URL } from '../content/termsOfService'

function TermsOfServiceContent() {
  return (
    <article className="tos-document">
      <header className="tos-document__header">
        <h1 id="tos-modal-title" className="tos-document__title">
          Terms of Service and Platform Use Agreement
        </h1>
        <p className="tos-document__subtitle">
          For the SPECTR&trade; Clinical Trial Allocation Platform
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
          PLEASE READ THIS ENTIRE AGREEMENT CAREFULLY. BY CREATING AN ACCOUNT, LOGGING INTO,
          ACCESSING, OR USING THE SPECTR PLATFORM, YOU ACKNOWLEDGE THAT YOU HAVE READ,
          UNDERSTOOD, AND UNEQUIVOCALLY AGREE TO BE LEGALLY BOUND BY ALL TERMS AND CONDITIONS
          STATED HEREIN. IF YOU DO NOT AGREE, DO NOT ACCESS OR USE THIS PLATFORM.
        </p>
      </aside>

      <section className="tos-document__section">
        <h2>1. Parties, Corporate Identity, and Electronic Consent</h2>
        <h3>1.1 Service Provider</h3>
        <p>
          This system is owned, developed, and operated by Manakkodam Manu Medical Research
          (OPC) Pvt. Ltd., having its registered office in Cherthala, Kerala, India (hereinafter
          referred to as the &ldquo;Service Provider&rdquo; or &ldquo;Company&rdquo;).
        </p>
        <h3>1.2 User</h3>
        <p>
          Any individual logging into or utilizing this platform—including Principal Investigators
          (PIs), Co-Investigators, Clinical Trial Coordinators (CTCs), Study Biostatisticians,
          Bedside Research Nurses, Data Managers, and Institutional Site Personnel (hereinafter
          referred to as the &ldquo;User&rdquo;)—accesses this service subject to these Terms of
          Service.
        </p>
        <h3>1.3 Electronic Consent &amp; Audit Trail</h3>
        <p>
          By clicking &ldquo;I Have Read and Agree to the Terms of Service&rdquo; or logging into
          an active account, you execute a legally valid, binding electronic agreement under the
          Information Technology Act, 2000 (India) and applicable electronic signature
          regulations. In compliance with ICH-GCP E6 Section 5.5.3, your unique user
          identification, IP address, and acceptance timestamp (in UTC) are automatically and
          immutably logged in the database audit repository.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>2. Service Scope &amp; Operational Delivery Tracks</h2>
        <p>
          The Service Provider operates SPECTR as an allocation concealment and centralized
          sequence management engine for prospective randomized controlled clinical trials under
          two operational tracks:
        </p>
        <h3>2.1 Self-Service Academic Track (Free of Charge)</h3>
        <p>
          The core SPECTR platform is made available free of software licensing fees for
          investigator-initiated, academic, non-profit, and postgraduate/doctoral thesis clinical
          trials. Under this track, the User self-onboards their trial, creates strata, uploads or
          generates their sequence lists, and administers site accounts independently. The Service
          Provider does not charge licensing fees, nor does it act as a commercial Contract Research
          Organization (CRO) or trial sponsor.
        </p>
        <h3>2.2 Managed Biostatistical Onboarding Services (Optional Professional Service)</h3>
        <p>
          Where an investigator, university, hospital, or commercial/non-profit sponsor explicitly
          contracts the Service Provider for professional onboarding assistance (such as bespoke
          offline sequence generation in R/Stata, multi-center site profile configuration, and Trial
          Master File validation documentation packages), such activities constitute a separate
          professional service engagement. The delivery of managed services does not alter the
          underlying non-delegable clinical responsibilities of the Principal Investigator as
          outlined in Section 4.
        </p>
        <h3>2.3 Functional Boundaries (What SPECTR Does Not Do)</h3>
        <p>
          The User expressly acknowledges that SPECTR is strictly a centralized randomization and
          allocation concealment tool. SPECTR does not function as an Electronic Data Capture (EDC)
          system, does not process electronic Case Report Forms (eCRFs), does not execute dynamic
          adaptive minimization algorithms, does not support cluster-randomized or stepped-wedge
          designs, does not track cross-over visit washouts, and does not provide drug supply
          packaging, batch dispensing, or depot logistics management.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>3. &ldquo;AS IS&rdquo; Provision and Warranty Disclaimers</h2>
        <h3>3.1 Express Warranty Disclaimer</h3>
        <p>
          THE SPECTR PLATFORM AND ALL HOSTED SERVICES ARE PROVIDED ON AN &ldquo;AS IS&rdquo; AND
          &ldquo;AS AVAILABLE&rdquo; BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
          IMPLIED. TO THE MAXIMUM EXTENT PERMISSIBLE UNDER APPLICABLE LAW, THE SERVICE PROVIDER
          DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF
          MERCHANTABILITY, FITNESS FOR A PARTICULAR CLINICAL OR SCIENTIFIC PURPOSE, ACCURACY OF
          USER-INGESTED SEQUENCE FILES, CONTINUOUS PLATFORM AVAILABILITY, OR NON-INFRINGEMENT.
        </p>
        <h3>3.2 Absence of Service Level Agreement (SLA)</h3>
        <p>
          While the Service Provider implements automated backups, PostgreSQL row-level concurrency
          locking, and security controls, the Service Provider does not warrant uninterrupted,
          error-free, or zero-latency operation. Scheduled system maintenance, emergency
          infrastructure upgrades, cloud hosting interruptions, third-party internet gateway failures,
          or regional telecommunications outages may occur without prior warning.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>4. Regulatory Governance &amp; Clinical Investigator Responsibilities</h2>
        <h3>4.1 Non-Delegable Regulatory Ownership (ICH-GCP E6 &amp; New Drugs and Clinical Trials Rules)</h3>
        <p>
          Under ICH-GCP E6(R2/R3) guidelines, CDSCO regulations, and international ethics standards,
          the Trial Sponsor and Principal Investigator retain absolute, non-delegable responsibility
          for the trial&apos;s design, ethical conduct, clinical safety, protocol compliance, data
          integrity, and institutional oversight. SPECTR acts solely as an automated technical
          instrument at the direction of the study team.
        </p>
        <h3>4.2 Independent Sequence Verification Sign-off</h3>
        <p>
          Whether an allocation sequence is uploaded by the User via CSV or generated through
          SPECTR&apos;s integrated sequence utility, the Principal Investigator and Study
          Biostatistician bear sole responsibility for verifying the final sequence—including block
          sizes, stratification factors, allocation ratios, and sample size caps—against the
          approved institutional protocol before randomizing the first human participant.
        </p>
        <h3>4.3 Institutional Ethics Committee (IEC/IRB) Validation</h3>
        <p>
          The User warrants that the use of SPECTR, including its centralized allocation
          methodology, has been disclosed to and approved by their respective Institutional Ethics
          Committee (IEC) or Institutional Review Board (IRB) where required by applicable local
          regulations.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>5. Data Collection, Telemetry, and Strict Zero-PHI Policy</h2>
        <h3>5.1 Operational Data Collected (Limited Platform Telemetry)</h3>
        <p>
          To maintain system integrity, manage authentication, and fulfill computerized system audit
          requirements under ICH-GCP, the SPECTR administration collects and stores only the
          following administrative and operational metadata:
        </p>
        <ul>
          <li>
            <strong>Clinical Trialist &amp; Coordinator Profiles:</strong> User names, institutional
            email addresses, designations, affiliated trial sites/institutions, and phone numbers (if
            submitted during onboarding).
          </li>
          <li>
            <strong>Trial Administrative Metrics:</strong> Study codes/names, total count of approved
            trial centers, stratum definitions, total allocation sequence size, active sequence
            counter pointers (total rows allocated vs. unconsumed), and configuration flags.
          </li>
          <li>
            <strong>System Audit Trail Logs:</strong> Operator user ID, client IP address, actions
            executed (e.g., login, allocation, unblinding request), and authoritative server-side UTC
            timestamps.
          </li>
        </ul>
        <h3>5.2 Strict Zero-PHI / Zero-PII Policy (Prohibition of Patient Identifiers)</h3>
        <p>
          SPECTR operates under a strict data minimization policy. USERS ARE STRICTLY PROHIBITED
          FROM ENTERING DIRECT PERSONALLY IDENTIFIABLE INFORMATION (PII) OR PROTECTED HEALTH
          INFORMATION (PHI) INTO THE PLATFORM.
        </p>
        <ul>
          <li>
            The platform shall never receive patient full names, national identity numbers (e.g.,
            Aadhaar, SSN, PAN), phone numbers, physical residential addresses, dates of birth, or
            biometric identifiers.
          </li>
          <li>
            Only pseudonymized, non-identifying participant screening codes (e.g., AMP-001) assigned
            locally by the trial site may be inputted.
          </li>
          <li>
            SPECTR does not collect clinical baseline covariates, laboratory results, or adverse event
            records.
          </li>
        </ul>
        <h3>5.3 Independent Secondary Record Keeping</h3>
        <p>
          SPECTR does not serve as a permanent Trial Master File (TMF) repository. Participating
          trial sites must maintain their own secondary, offline, physical or institutional records
          of all allocations (e.g., signed enrollment logs, printed or archived automated
          confirmation email receipts).
        </p>
      </section>

      <section className="tos-document__section">
        <h2>6. Intellectual Property &amp; Open Source Governance</h2>
        <h3>6.1 Open Source Codebase</h3>
        <p>
          The core underlying source code of SPECTR is released under the GNU Affero General Public
          License version 3 (AGPLv3). Nothing in this agreement restricts rights granted to users
          under the open-source AGPLv3 license regarding the independent modification or
          self-hosting of that underlying code.
        </p>
        <h3>6.2 Proprietary Trademarks &amp; Corporate Assets</h3>
        <p>
          The brand name SPECTR&trade;, the SPECTR logo, platform user interface design assets,
          documentation, and the corporate marks of MM Medical Research (OPC) Pvt. Ltd. remain the
          exclusive intellectual property of Manakkodam Manu Medical Research (OPC) Pvt. Ltd. The
          AGPLv3 license does not grant any license or right to use the Company&apos;s trademarks,
          trade names, or commercial branding without prior written authorization.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>7. Limitation of Liability &amp; Indemnification</h2>
        <h3>7.1 Comprehensive Liability Disclaimer</h3>
        <p>
          TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL THE SERVICE PROVIDER,
          ITS DIRECTORS, SHAREHOLDERS, EMPLOYEES, AGENTS, OR DEVELOPERS BE LIABLE FOR ANY DIRECT,
          INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES ARISING OUT
          OF OR IN CONNECTION WITH THE USE OR INABILITY TO USE THE PLATFORM. THIS EXCLUSION APPLIES
          TO, WITHOUT LIMITATION:
        </p>
        <ul>
          <li>
            Interrupted clinical recruitment, bedside allocation delays, or server connection
            timeouts.
          </li>
          <li>
            Protocol deviations, sequence skips, allocation errors arising from corrupted
            user-uploaded files, or unblinding disputes.
          </li>
          <li>
            Institutional Ethics Committee sanctions, clinical trial suspensions, CDSCO/regulatory
            penalties, or clinical research funding withdrawals.
          </li>
          <li>
            Infrastructure interruptions, data losses, or cybersecurity incidents outside the
            Service Provider&apos;s reasonable control.
          </li>
        </ul>
        <h3>7.2 Liability Cap</h3>
        <p>
          For all users accessing the platform via the free, self-service academic tier, the Service
          Provider&apos;s cumulative aggregate financial liability shall be strictly ₹0 (Zero Indian
          Rupees).
        </p>
        <p>
          For users or institutions with an active, paid contract for managed biostatistical
          onboarding services, the Service Provider&apos;s total aggregate financial liability
          arising under or relating to that trial shall be strictly limited to the actual fee amount
          paid by the client to the Service Provider for that specific onboarding contract.
        </p>
        <h3>7.3 Indemnification</h3>
        <p>
          The User and their Sponsoring Institution agree to indemnify, hold harmless, and defend the
          Service Provider, its directors, and technical developers against any third-party claims,
          liabilities, damages, regulatory penalties, legal fees, and expenses resulting from:
        </p>
        <ul>
          <li>
            The medical conduct, intervention, or clinical outcomes of the underlying clinical study.
          </li>
          <li>
            The User&apos;s breach of protocol, violation of ethics approvals, or input of
            unauthorized protected personal data (PII/PHI).
          </li>
          <li>Unauthorized disclosure or mishandling of trial credentials by site research personnel.</li>
        </ul>
      </section>

      <section className="tos-document__section">
        <h2>8. Account Security, Suspension, and Data Lifecycle</h2>
        <h3>8.1 Credential Integrity</h3>
        <p>
          Users are solely responsible for maintaining the confidentiality of their authentication
          credentials. Shared login profiles among multiple bedside coordinators or investigators are
          strictly prohibited. The platform logs client IP addresses and user accounts during every
          allocation transaction.
        </p>
        <h3>8.2 Account Suspension &amp; Termination</h3>
        <p>
          The Service Provider reserves the right to immediately suspend, restrict, or permanently
          revoke platform access for any user account or trial profile in cases of suspected security
          violations, database tampering, ethical violations, or non-compliance with these terms.
        </p>
        <h3>8.3 Trial Closure and Data Retention</h3>
        <p>
          Following formal notification of study completion, recruitment termination, or prolonged
          platform inactivity exceeding twelve (12) consecutive months, the Service Provider
          reserves the right to archive or decommission study allocation tables from the production
          database. The Study Coordinator will be granted a reasonable window (not less than 30 days
          following formal notification) to export their final allocation and audit logs.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>9. Modifications to Terms</h2>
        <p>
          The Service Provider reserves the right to update or modify this Agreement to reflect
          platform feature updates, regulatory revisions, or legal requirements. Continued use of the
          platform following the posting of updated terms constitutes binding electronic acceptance
          of the amended Agreement.
        </p>
      </section>

      <section className="tos-document__section">
        <h2>10. Governing Law and Exclusive Dispute Jurisdiction</h2>
        <p>
          This Agreement, its interpretation, and any non-contractual obligations or disputes arising
          out of or in connection with the SPECTR platform shall be governed by, construed, and
          enforced in accordance with the substantive laws of India.
        </p>
        <p>
          The parties unequivocally agree that any legal suit, action, arbitration, or proceeding
          arising under or relating to this Agreement shall be subject to the exclusive jurisdiction
          of the competent courts situated in Alappuzha, Kerala, India.
        </p>
      </section>
    </article>
  )
}

export default TermsOfServiceContent
