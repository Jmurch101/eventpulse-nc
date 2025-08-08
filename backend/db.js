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
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `;

  db.run(createEventsTable, (err) => {
    if (err) {
      console.error('Error creating events table:', err.message);
    } else {
      console.log('✅ Events table ready');
    }
  });
}

module.exports = db;
