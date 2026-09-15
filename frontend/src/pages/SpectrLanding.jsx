function SpectrLanding() {
  return (
    <article className="landing">
      <header className="landing__hero">
        <h1 className="landing__title">
          SPECTR: Secure Point-of-care Enrollment and Centralized Trial Randomization
        </h1>
        <p className="landing__lead">
          A lightweight, GCP-compliant central allocation engine for multicenter clinical
          trials.
        </p>
      </header>

      <section className="landing__section">
        <h2>Overview</h2>
        <p>
          SPECTR provides central randomization and allocation concealment for
          investigator-initiated and multicentric randomized controlled trials. Designed by
          trial methodologists, it eliminates the need for cumbersome physical envelopes and
          cost-prohibitive enterprise IWRS/RTSM software, delivering instant, tamper-proof
          treatment allocations directly to point-of-care investigators.
        </p>
      </section>

      <section className="landing__section">
        <h2>Key Capabilities</h2>

        <div className="landing__capability">
          <h3>Methodological Flexibility</h3>
          <p>
            Generate complex, customized randomization schedules offline using your preferred
            biostatistical workflows (e.g., R, Stata, SAS) with permuted blocks of varying sizes
            and multi-level stratification (by study center, age, clinical severity). Simply
            import your pre-computed sequences into SPECTR. Or you may use our inhouse random
            sequence generator, designed for multicentric trials, with simple/block
            randomisation with stratification.
          </p>
        </div>

        <div className="landing__capability">
          <h3>Frictionless Point-of-Care Allocation</h3>
          <p>
            Site investigators access a fast, clean interface optimized for clinic and bedside
            use. Automatically generates participant IDs and delivers an immediate, unalterable
            treatment assignment.
          </p>
        </div>

        <div className="landing__capability">
          <h3>Audit Trails &amp; Automated Verification</h3>
          <p>
            Every allocation event triggers an immutable digital receipt with participant IDs,
            stratum tags, and precise UTC timestamps. Both the site investigator and the central
            coordinating team can review and export allocation history in real-time.
          </p>
        </div>
      </section>

      <section className="landing__section">
        <h2>Regulatory &amp; GCP Integrity</h2>
        <p>Built around ICH-GCP E6(R2/R3) and 21 CFR Part 11 principles:</p>
        <ul className="landing__list">
          <li>Strict allocation concealment with zero sequence predictability</li>
          <li>
            Database-level concurrency locks to prevent race conditions during simultaneous
            enrollments
          </li>
          <li>Strict role-based access control (RBAC) across participating centers</li>
        </ul>
      </section>

      <section className="landing__section">
        <h2>How It Works</h2>
        <ol className="landing__steps">
          <li>
            <strong>Setup &amp; Ingestion:</strong> The Trial Biostatistician or Central
            Coordinator uploads the stratified block sequence and sets site permissions.
          </li>
          <li>
            <strong>Screen &amp; Validate:</strong> The site investigator confirms participant
            eligibility and validates before randomisation.
          </li>
          <li>
            <strong>Instant Assignment:</strong> SPECTR locks the next sequential allocation in
            real time and reveals the assigned arm.
          </li>
          <li>
            <strong>Central Confirmation:</strong> Dual verification confirmation immediately
            visible to both the investigator and trial oversight.
          </li>
        </ol>
      </section>

      <section className="landing__section landing__citation">
        <h2>Citation</h2>
        <p>
          When reporting methodology in trial protocols, ethics submissions, or peer-reviewed
          publications, please cite:
        </p>
        <p className="landing__cite-block">
          Pradeep M, Kumar D. SPECTR: Secure Point-of-care Enrollment and Centralized Trial
          Randomization [Computer software]. Available from:{' '}
          <a href="https://mmmr.in/services/spectr" target="_blank" rel="noopener noreferrer">
            https://mmmr.in/services/spectr
          </a>
        </p>
      </section>

      <footer className="landing__footer">
        <p>
          <strong>Developed &amp; Maintained by:</strong> Dr. Manu Pradeep &amp; Dhanush Kumar
        </p>
        <p>
          A free open-source tool by MM Medical Research (OPC) Pvt. Ltd., Cherthala, Kerala,
          India.
        </p>
        <p>
          View Github source code here:{' '}
          <a
            href="https://github.com/dhanush-kuma/SPECTR"
            target="_blank"
            rel="noopener noreferrer"
          >
            https://github.com/dhanush-kuma/SPECTR
          </a>
        </p>
        <p>
          Inquiries &amp; Setup Support:{' '}
          <a href="mailto:mmmedicalresearch@outlook.in">mmmedicalresearch@outlook.in</a>
        </p>
      </footer>
    </article>
  )
}

export default SpectrLanding
