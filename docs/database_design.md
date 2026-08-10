# DDV Manager Database Design

## Purpose

The database stores all Disney Dreamlight Valley game information and separates it from personal player progress.

## Main Schemas

### Game Schema

Contains all permanent game information:

- Characters
- Items
- Recipes
- Locations
- Quests
- Critters

### Player Schema

Contains user-specific information:

- Character friendship levels
- Storage
- Collection progress
- Valley design

### Analytics Schema

Contains calculated information:

- Completion percentages
- Recommendations
- Progress statistics

### System Schema

Contains technical information:

- Data sources
- Game versions
- Update history

## Design Principles

1. Avoid duplicated information.
2. Separate game data from player data.
3. Support future DLC updates.
4. Allow local-only usage without servers.
5. Keep the database expandable.
