import { useEffect, useState } from "react";
import {
  Home,
  Users,
  BriefcaseBusiness,
  Rabbit,
  LibraryBig,
  Settings,
  Search,
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

type Character = {
  name: string;
  species: string | null;
  franchise: string | null;
  unlocked: boolean | null;
  friendship_level: number | null;
  role: string | null;
  role_status: "assigned" | "no_role" | "unknown";
};

type RoleCharacter = {
  name: string;
  friendship_level: number | null;
  unlocked: boolean | null;
};

type ActivityRole = {
  role_id: number;
  role: string;
  assigned_count: number;
  assigned_characters: RoleCharacter[];
  no_role_count: number;
  unknown_count: number;
};

type Page = "Home" | "Characters" | "Activities & Roles";

const navigation = [
  { label: "Home" as Page, icon: Home },
  { label: "Characters" as Page, icon: Users },
  { label: "Activities & Roles", icon: BriefcaseBusiness },
  { label: "Critters", icon: Rabbit },
  { label: "Collection & Progress", icon: LibraryBig },
  { label: "Settings", icon: Settings },
];

function App() {
  const [page, setPage] = useState<Page>("Home");

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
          {navigation.map(({ label, icon: Icon }) => (
            <button
              key={label}
              className={`nav-item ${page === label ? "active" : ""}`}
              onClick={() => {
                if (
                  label === "Home" ||
                  label === "Characters" ||
                  label === "Activities & Roles"
                ) {
                  setPage(label);
                }
              }}
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

      {page === "Home" && <HomePage />}
      {page === "Characters" && <CharactersPage />}
      {page === "Activities & Roles" && <ActivitiesRolesPage />}
    </div>
  );
}

/* =========================================================
   HOME
   ========================================================= */

function HomePage() {
  const [homeData, setHomeData] = useState<HomeData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/home/")
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
      <main className="main">
        <h1>DDV Manager</h1>
        <p>Unable to load Home data.</p>
        <p>{error}</p>
      </main>
    );
  }

  if (!homeData) {
    return (
      <main className="main">
        <h1>DDV Manager</h1>
        <p>Loading your valley...</p>
      </main>
    );
  }

  const nextAction = homeData.next_best_action;

  return (
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

          <div className="card-description">things worth knowing right now</div>
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
  );
}

/* =========================================================
   CHARACTERS
   ========================================================= */

function CharactersPage() {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/characters/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load characters.");
        }

        return response.json();
      })
      .then((data) => {
        setCharacters(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const filteredCharacters = characters.filter((character) =>
    character.name.toLowerCase().includes(search.toLowerCase()),
  );

  function getRoleDisplay(character: Character) {
    if (character.role_status === "assigned") {
      return character.role ?? "Unknown";
    }

    if (character.role_status === "no_role") {
      return "No Role";
    }

    return "Unknown";
  }

  return (
    <main className="main">
      <header className="topbar">
        <div>
          <div className="eyebrow">YOUR VALLEY</div>
          <h1>Characters</h1>
        </div>

        <div className="topbar-status">{characters.length} characters</div>
      </header>

      <section className="page-intro">
        <div>
          <p className="section-label">CHARACTER DIRECTORY</p>

          <h2>Meet the characters in your valley</h2>

          <p>Browse the game knowledge available to DDV Manager.</p>
        </div>

        <div className="search-box">
          <Search size={17} strokeWidth={1.8} />

          <input
            type="text"
            placeholder="Search characters..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>
      </section>

      {loading && <div className="empty-state">Loading characters...</div>}

      {error && (
        <div className="empty-state">
          Unable to load characters.
          <br />
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          <div className="character-count">
            {filteredCharacters.length} characters
          </div>

          <section className="character-grid">
            {filteredCharacters.map((character) => (
              <article className="character-card" key={character.name}>
                <div className="character-avatar">
                  {character.name.charAt(0)}
                </div>

                <div className="character-info">
                  <h3>{character.name}</h3>

                  {character.species && <p>{character.species}</p>}

                  {character.franchise && <span>{character.franchise}</span>}

                  <div className="character-state">
                    <div>
                      <strong>Unlock:</strong>{" "}
                      {character.unlocked === true
                        ? "Unlocked"
                        : character.unlocked === false
                          ? "Locked"
                          : "Unknown"}
                    </div>

                    <div>
                      <strong>Friendship:</strong>{" "}
                      {character.friendship_level !== null
                        ? `${character.friendship_level}/10`
                        : "Unknown"}
                    </div>

                    <div>
                      <strong>Role:</strong> {getRoleDisplay(character)}
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </section>

          {filteredCharacters.length === 0 && (
            <div className="empty-state">No characters found.</div>
          )}
        </>
      )}
    </main>
  );
}

function ActivitiesRolesPage() {
  const [roles, setRoles] = useState<ActivityRole[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/players/1/activities-roles")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load Activities & Roles.");
        }

        return response.json();
      })
      .then((data) => {
        setRoles(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <main className="main">
        <h1>Activities & Roles</h1>
        <div className="empty-state">Loading your activity assignments...</div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="main">
        <h1>Activities & Roles</h1>
        <div className="empty-state">
          Unable to load Activities & Roles.
          <br />
          {error}
        </div>
      </main>
    );
  }

  return (
    <main className="main">
      <header className="topbar">
        <div>
          <div className="eyebrow">YOUR VALLEY</div>
          <h1>Activities & Roles</h1>
        </div>

        <div className="topbar-status">{roles.length} activities</div>
      </header>

      <section className="page-intro">
        <div>
          <p className="section-label">ACTIVITY COVERAGE</p>

          <h2>How your companions are assigned</h2>

          <p>
            See which companions are supporting each activity in your valley.
          </p>
        </div>
      </section>

      <section className="role-grid">
        {roles.map((role) => (
          <article className="role-card" key={role.role_id}>
            <div className="role-card-header">
              <div>
                <p className="section-label">ACTIVITY</p>
                <h2>{role.role}</h2>
              </div>

              <div className="role-count">{role.assigned_count}</div>
            </div>

            {role.assigned_characters.length > 0 ? (
              <div className="role-characters">
                {role.assigned_characters.map((character) => (
                  <div className="role-character" key={character.name}>
                    <div className="character-avatar">
                      {character.name.charAt(0)}
                    </div>

                    <div>
                      <h3>{character.name}</h3>

                      <p>
                        Friendship{" "}
                        {character.friendship_level !== null
                          ? `${character.friendship_level}/10`
                          : "Unknown"}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="role-empty">No companions assigned</div>
            )}
          </article>
        ))}
      </section>
    </main>
  );
}
export default App;
