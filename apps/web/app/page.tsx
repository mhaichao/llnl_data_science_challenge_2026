const foundations = [
  { label: "Frontend", value: "Next.js · React · TypeScript", state: "Ready" },
  { label: "Analysis API", value: "FastAPI · Python", state: "Ready" },
  { label: "Scientific layer", value: "Service boundary reserved", state: "Preserved" },
  { label: "Cloud deployment", value: "Cloud Run · Storage", state: "Planned" },
];

export default function HomePage() {
  return (
    <main className="workspace">
      <aside className="rail" aria-label="Project context">
        <div className="mark" aria-hidden="true">
          ◈
        </div>
        <div>
          <p className="rail-kicker">LLNL DSSI 2026</p>
          <p className="rail-title">Lattice Inspect</p>
        </div>
        <div className="rail-rule" />
        <span className="status-pill">
          <span aria-hidden="true">●</span> Demo foundation
        </span>
        <p className="rail-copy">
          Phase 1 establishes independent web and API services. Scientific results remain
          intentionally mocked and out of scope.
        </p>
      </aside>

      <section className="content">
        <div className="eyebrow">Application foundation</div>
        <h1>Multi-Agent Lattice CT Inspection</h1>
        <p className="lede">
          A modular research workspace for future CT inspection, defect analysis,
          measurement, grounded assistance, and NDE reporting.
        </p>

        <div className="notice" role="status">
          <strong>Phase 1 scaffold</strong>
          <span>No real CT analysis is running, and no cloud credentials are required.</span>
        </div>

        <div className="foundation-grid">
          {foundations.map((item) => (
            <article className="foundation-card" key={item.label}>
              <div className="card-heading">
                <span>{item.label}</span>
                <span className={`state state-${item.state.toLowerCase()}`}>{item.state}</span>
              </div>
              <p>{item.value}</p>
            </article>
          ))}
        </div>

        <section className="boundary-panel">
          <div>
            <p className="panel-kicker">Architecture boundary</p>
            <h2>Presentation, orchestration, and science stay independent.</h2>
          </div>
          <div className="flow" aria-label="Application data flow">
            <span>Browser</span>
            <span aria-hidden="true">→</span>
            <span>FastAPI</span>
            <span aria-hidden="true">→</span>
            <span>Typed services</span>
            <span aria-hidden="true">→</span>
            <span>Scientific Python</span>
          </div>
        </section>
      </section>
    </main>
  );
}
