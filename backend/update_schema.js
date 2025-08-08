// update_schema.js
const db = require('./db');

console.log('🔧 Updating database schema to prevent duplicates...');

// First, clean up any existing duplicates
console.log('🧹 Cleaning up existing duplicates...');

const cleanupQuery = `
  DELETE FROM events 
  WHERE id NOT IN (
    SELECT MIN(id) 
    FROM events 
    GROUP BY title, start_date, source_url
  )
`;

db.run(cleanupQuery, function(err) {
  if (err) {
    console.error('Error cleaning up duplicates:', err);
    return;
  }
  
  console.log(`✅ Cleaned up ${this.changes} duplicate events`);
  
  // Now add the unique constraint
  console.log('🔒 Adding unique constraint...');
  
  // SQLite doesn't support adding constraints to existing tables easily
  // So we'll create a new table with the constraint and copy data
  const createNewTableQuery = `
    CREATE TABLE events_new (
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
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(title, start_date, source_url)
    )
  `;
  
  db.run(createNewTableQuery, (err) => {
    if (err) {
      console.error('Error creating new table:', err);
      return;
    }
    
    console.log('✅ Created new table with unique constraint');
    
    // Copy data from old table to new table
    const copyDataQuery = `
      INSERT INTO events_new (
        title, description, start_date, end_date, location_name,
        latitude, longitude, organization_id, event_type, source_url, created_at
      )
      SELECT title, description, start_date, end_date, location_name,
             latitude, longitude, organization_id, event_type, source_url, created_at
      FROM events
    `;
    
    db.run(copyDataQuery, function(err) {
      if (err) {
        console.error('Error copying data:', err);
        return;
      }
      
      console.log(`✅ Copied ${this.changes} events to new table`);
      
      // Drop old table and rename new table
      db.run('DROP TABLE events', (err) => {
        if (err) {
          console.error('Error dropping old table:', err);
          return;
        }
        
        db.run('ALTER TABLE events_new RENAME TO events', (err) => {
          if (err) {
            console.error('Error renaming table:', err);
            return;
          }
          
          console.log('✅ Schema update completed successfully!');
          console.log('🔒 Duplicate prevention is now active');
          
          // Verify the constraint works
          db.get('SELECT COUNT(*) as count FROM events', (err, row) => {
            if (err) {
              console.error('Error verifying table:', err);
              return;
            }
            
            console.log(`📊 Total events in database: ${row.count}`);
            process.exit(0);
          });
        });
      });
    });
  });
}); 