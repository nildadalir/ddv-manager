import { useEffect, useState } from "react";
import {
  Home,
  Users,
  BriefcaseBusiness,
  Rabbit,
  LibraryBig,
  Settings,
} from "lucide-react";
import "./App.css";

type Insight = {
  type: string;
  priority: string;
  title: string;
  message: string;
};

type Recommendation = {
  type: string;
  priority: string;
  character: string;
  reason: string;
};

type HomeData = {
  next_best_action: {
    type: string;
    character?: string;
    title?: string;
    reason: string;
  } | null;
  recommendations: Recommendation[];
  insights: Insight[];
};

const navigation = [
  { label: "Home", icon: Home },
  { label: "Characters", icon: Users },
  { label: "Activities & Roles", icon: BriefcaseBusiness },
  { label: "Critters", icon: Rabbit },
  { label: "Collection & Progress", icon: LibraryBig },
  { label: "Settings", icon: Settings },
];

function App() {
  const [homeData, setHomeData] = useState<HomeData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/home")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load Home data.");
        }

        return response.json();
      })
      .then((data) => {
        setHomeData(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  if (error) {
    return (
      <div className="app">
        <main className="main">
          <h1>DDV Manager</h1>
          <p>Unable to load Home data.</p>
          <p>{error}</p>
        </main>
      </div>
    );
  }

  if (!homeData) {
    return (
      <div className="app">
        <main className="main">
          <h1>DDV Manager</h1>
          <p>Loading your valley...</p>
        </main>
      </div>
    );
  }

  const nextAction = homeData.next_best_action;

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">✦</div>

          <div>
            <div className="brand-name">DDV Manager</div>
            <div className="brand-subtitle">Decision Companion</div>
          </div>
        </div>

        <nav className="navigation">
          {navigation.map(({ label, icon: Icon }, index) => (
            <button
              key={label}
              className={`nav-item ${index === 0 ? "active" : ""}`}
            >
              <Icon size={19} strokeWidth={1.8} />
              <span>{label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="version">DDV Manager · V1</div>

          <div className="local-status">
            <span className="status-dot" />
            Local data
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <div className="eyebrow">YOUR VALLEY</div>
            <h1>Good afternoon, Niloofar</h1>
          </div>

          <div className="topbar-status">
            <span className="status-dot" />
            Data stored locally
          </div>
        </header>

        <section className="hero">
          <div>
            <p className="section-label">NEXT BEST ACTION</p>

            {nextAction ? (
              <>
                <h2>
                  {nextAction.type === "friendship"
                    ? `Build your friendship with ${nextAction.character}`
                    : nextAction.title}
                </h2>

                <p className="hero-description">{nextAction.reason}</p>

                {nextAction.character && (
                  <button className="primary-button">
                    View {nextAction.character}
                  </button>
                )}
              </>
            ) : (
              <>
                <h2>No action right now</h2>

                <p className="hero-description">
                  Your valley does not currently have a recommended next action.
                </p>
              </>
            )}
          </div>

          <div className="hero-icon">✦</div>
        </section>

        <section className="dashboard-grid">
          <div className="card">
            <div className="card-label">RECOMMENDATIONS</div>

            <div className="metric">{homeData.recommendations.length}</div>

            <div className="card-description">
              current actions for your valley
            </div>
          </div>

          <div className="card">
            <div className="card-label">INSIGHTS</div>

            <div className="metric">{homeData.insights.length}</div>

            <div className="card-description">
              things worth knowing right now
            </div>
          </div>

          <div className="card">
            <div className="card-label">DATA STATUS</div>

            <div className="metric">Local</div>

            <div className="card-description">
              your player data stays on this device
            </div>
          </div>
        </section>

        <section className="insights-section">
          <div className="section-heading">
            <div>
              <p className="section-label">INSIGHTS</p>
              <h2>What matters right now</h2>
            </div>
          </div>

          <div className="insight-list">
            {homeData.insights.map((insight) => (
              <article
                className="insight-card"
                key={`${insight.type}-${insight.title}`}
              >
                <div className="insight-indicator" />

                <div>
                  <h3>{insight.title}</h3>

                  <p>{insight.message}</p>
                </div>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
