// db.js
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Create database file in the backend directory
const dbPath = path.join(__dirname, 'events.db');

// Create/connect to SQLite database
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
  } else {
    console.log('✅ Connected to SQLite database');
    createTables();
  }
});

// Create tables if they don't exist
function createTables() {
  const createEventsTable = `
    CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      description TEXT,
      start_date TEXT NOT NULL,
      end_date TEXT NOT NULL,
      location_name TEXT,
      latitude REAL DEFAULT 0,
      longitude REAL DEFAULT 0,
      organization_id INTEGER DEFAULT 1,
      event_type TEXT DEFAULT 'other',
      source_url TEXT,
      tags TEXT DEFAULT '',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `;

  const createOrganizationsTable = `
    CREATE TABLE IF NOT EXISTS organizations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE,
      type TEXT,
      website TEXT,
      contact_info TEXT,
      timezone TEXT
    )
  `;

  const createEventTypesTable = `
    CREATE TABLE IF NOT EXISTS event_types (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE,
      category TEXT,
      color_code TEXT
    )
  `;

  db.serialize(() => {
    db.run(createEventsTable, (err) => {
      if (err) {
        console.error('Error creating events table:', err.message);
      } else {
        console.log('✅ Events table ready');
      }
    });

    db.run(createOrganizationsTable, (err) => {
      if (err) {
        console.error('Error creating organizations table:', err.message);
      } else {
        console.log('✅ Organizations table ready');
      }
    });

    db.run(createEventTypesTable, (err) => {
      if (err) {
        console.error('Error creating event_types table:', err.message);
      } else {
        console.log('✅ Event types table ready');
      }
    });

    // Attempt to add missing column 'tags' if upgrading existing DB
    db.run("ALTER TABLE events ADD COLUMN tags TEXT DEFAULT ''", (err) => {
      if (err && !String(err.message).includes('duplicate column')) {
        // Ignore if column exists; log other errors
        console.warn('Note (ALTER TABLE events add tags):', err.message);
      }
    });

    // Seed event types if empty
    db.get('SELECT COUNT(*) as cnt FROM event_types', (err, row) => {
      if (err) return;
      if ((row?.cnt || 0) === 0) {
        const defaults = [
          ['academic', 'Education', '#2563eb'],
          ['government', 'Government', '#16a34a'],
          ['holiday', 'Holiday', '#f59e0b'],
          ['state', 'State', '#7c3aed'],
          ['university', 'Education', '#0ea5e9'],
          ['conference', 'Conference', '#ef4444'],
          ['workshop', 'Workshop', '#10b981'],
          ['other', 'Other', '#6b7280']
        ];
        const stmt = db.prepare('INSERT OR IGNORE INTO event_types (name, category, color_code) VALUES (?, ?, ?)');
        defaults.forEach((d) => stmt.run(d[0], d[1], d[2]));
        stmt.finalize();
        console.log('🌱 Seeded default event_types');
      }
    });

    // Seed minimal organizations if empty
    db.get('SELECT COUNT(*) as cnt FROM organizations', (err, row) => {
      if (err) return;
      if ((row?.cnt || 0) === 0) {
        const orgs = [
          ['UNC Chapel Hill', 'university', 'https://www.unc.edu', '', 'America/New_York'],
          ['Duke University', 'university', 'https://www.duke.edu', '', 'America/New_York'],
          ['NC State University', 'university', 'https://www.ncsu.edu', '', 'America/New_York'],
          ['City of Raleigh', 'government', 'https://raleighnc.gov', '', 'America/New_York'],
          ['City of Durham', 'government', 'https://durhamnc.gov', '', 'America/New_York'],
          ['Wake County', 'government', 'https://www.wake.gov', '', 'America/New_York']
        ];
        const stmt = db.prepare('INSERT OR IGNORE INTO organizations (name, type, website, contact_info, timezone) VALUES (?, ?, ?, ?, ?)');
        orgs.forEach((o) => stmt.run(o[0], o[1], o[2], o[3], o[4]));
        stmt.finalize();
        console.log('🌱 Seeded default organizations');
      }
    });
  });
}

module.exports = db;
