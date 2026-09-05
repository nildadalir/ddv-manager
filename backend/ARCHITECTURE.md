# DDV Manager · Architecture

## Product Architecture

DDV Manager is a local-first decision-support companion for Disney Dreamlight Valley.

Its core data flow is:

```text
RAW GAME DATA
      ↓
GAME KNOWLEDGE
      +
PLAYER STATE
      ↓
DERIVED DATA
      ↓
METRICS
      ↓
INSIGHTS
      ↓
RECOMMENDATIONS
      ↓
USER INTERFACE
```

The application should answer:

> **What does my valley state mean, and what should I consider doing next?**

It should not become a second game, a giant checklist, or a database viewer.

---

## Data Layers

### 1. Game Knowledge

Facts about Disney Dreamlight Valley.

Examples:

- Characters
- Activities
- Roles
- Critters
- Recipes
- Ingredients
- Areas
- Realms
- Content / DLC
- Mechanics
- Rewards
- Requirements
- Schedules
- Sources
- Game version
- Confidence / provenance

Game knowledge is shared application data.

### 2. Player State

Information belonging to a specific player's valley.

Examples:

- Owned content
- Character unlock state
- Character welcome status
- Friendship levels
- Character roles
- Critter collection
- Progress

Player state must remain separate from game knowledge.

### 3. Player Preferences

Settings that affect how DDV Manager behaves for a particular player.

Examples:

- Recommendation strategy
- Display preferences
- Other future user preferences

### 4. Derived Data

Calculated information that should not be treated as primary stored state.

Examples:

- Metrics
- Completion percentages
- Insights
- Recommendations
- Next Best Action

Derived data should be recalculated from the underlying state.

---

## Unknown Is a Real State

Missing information must not automatically become `false`, `0`, or "not collected."

Examples:

```text
Character Welcome:
- Welcomed
- Not Welcomed
- Unknown
- Unavailable

Progress:
- Unlocked
- Locked
- Unknown

Role:
- Assigned
- No Role
- Unknown

Friendship:
- Level 1–10
- Unknown
```

The application must preserve the difference between:

```text
Known false
```

and:

```text
Unknown
```

---

## Core Domain Distinctions

These concepts must remain separate:

```text
Character ≠ Friend ≠ Companion ≠ Critter
```

"Villager" should not be used as the primary product term.

---

## Backend Architecture

```text
backend/
├── api/
│   ├── characters.py
│   ├── home.py
│   ├── items.py
│   ├── players.py
│   ├── recipes.py
│   └── role_preferences.py
│
├── database/
│   ├── models/
│   ├── raw/
│   ├── migrations/
│   └── session.py
│
├── ingestion/
├── schemas/
├── services/
│   ├── home.py
│   ├── insights.py
│   ├── metrics.py
│   ├── recommendation.py
│   └── player_unlock_source_service.py
│
├── transform/
├── validation/
└── main.py
```

### API Layer

Handles HTTP requests and responses.

The API should not contain the main business logic.

### Service Layer

Contains decision-support logic such as:

- Metrics
- Insights
- Recommendations
- Home summaries
- Player-state calculations

### Database Layer

Contains:

- SQLAlchemy models
- SQLite database
- Database sessions
- Migrations
- Raw game data

### Schema Layer

Defines API input and output structures using Pydantic.

---

## Frontend Architecture

```text
frontend/
└── src/
    ├── App.tsx
    ├── App.css
    └── ...
```

The frontend consumes API data rather than directly querying the database.

The UI should present decisions, context, and insights rather than expose database structure.

---

## V1 Navigation

```text
Home
Characters
Activities & Roles
Critters
Collection & Progress
Settings
```

### Home

Decision hub.

Provides:

- Next Best Action
- Recommendations
- Insights
- Relevant valley context

### Characters

Directory and discovery.

Character information includes:

- Artwork
- Name
- Welcome status
- Friendship
- Role
- Content association
- Relevant insights
- Suggested action

### Activities & Roles

Analyzes character role assignments.

The analysis should consider:

- Available characters
- Assigned roles
- Characters without roles
- Unknown role state
- Friendship levels

### Critters

Lightweight critter companion.

Includes:

- Critter information
- Schedule
- Favorite foods
- Collection state
- Estimated feedings

No unnecessary personal feeding history.

### Collection & Progress

Valley-wide progress dashboard.

It must not invent an arbitrary overall completion score.

### Settings

Local data management and application information.

Includes:

- Export player data
- Import player data
- Clear player data
- Game knowledge/version information
- Sources

---

## Local-First Architecture

Player data is designed to remain on the player's device/browser.

The application does not require:

- Accounts
- Login
- Passwords
- Paid backend infrastructure
- Cloud player databases
- Subscriptions

The project should be deployable using free infrastructure.

Player data should eventually use browser-local persistence such as IndexedDB, with local export/import support.

---

## Game Knowledge Provenance

Game knowledge may change as the game changes.

Knowledge should support:

```text
Source
Game Version
Confidence
Provenance
```

Confidence states:

```text
Confirmed
Community-reported
Derived
Unknown
```

---

## Recommendation Architecture

Recommendations are generated from player state and game knowledge.

Example:

```text
PLAYER STATE
     ↓
METRICS
     ↓
INSIGHTS
     ↓
RECOMMENDATIONS
     ↓
NEXT BEST ACTION
```

"Next Best Action" represents one useful recommended action.

It is not presented as mathematically optimal.

Internal scoring may be used to rank recommendations, but arbitrary internal scores should not be exposed to the player.

---

## Current Development Scope

### Active

- Home
- Characters
- Activities & Roles
- Critters
- Collection & Progress
- Settings
- Game knowledge
- Player state
- Metrics
- Insights
- Recommendations
- Local persistence
- Export/import
- Free deployment

### On Hold

**Valley Planner**

Do not design or implement Valley Planner unless the project scope is explicitly changed.
