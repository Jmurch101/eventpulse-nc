// check_status.js
const db = require('./db');

console.log('📊 EventPulse NC Database Status');
console.log('========================================');

// Get total events count
db.get('SELECT COUNT(*) as total FROM events', (err, totalRow) => {
  if (err) {
    console.error('Error getting total count:', err);
    return;
  }
  
  console.log(`📈 Total Events: ${totalRow.total}`);
  
  // Get events by type
  db.all('SELECT event_type, COUNT(*) as count FROM events GROUP BY event_type ORDER BY count DESC', (err, typeRows) => {
    if (err) {
      console.error('Error getting events by type:', err);
      return;
    }
    
    console.log('\n📋 Events by Type:');
    typeRows.forEach(row => {
      console.log(`   ${row.event_type}: ${row.count}`);
    });
    
    // Check for duplicates
    const duplicateQuery = `
      SELECT title, start_date, COUNT(*) as count
      FROM events 
      GROUP BY title, start_date 
      HAVING COUNT(*) > 1
      ORDER BY count DESC
    `;
    
    db.all(duplicateQuery, (err, duplicates) => {
      if (err) {
        console.error('Error checking duplicates:', err);
        return;
      }
      
      console.log(`\n🔍 Duplicate Groups: ${duplicates.length}`);
      
      if (duplicates.length > 0) {
        console.log('   Duplicate events found:');
        duplicates.forEach(dup => {
          console.log(`   - "${dup.title}" (${dup.count} copies)`);
        });
      } else {
        console.log('   ✅ No duplicates found!');
      }
      
      // Get recent events
      db.all('SELECT title, start_date, event_type FROM events ORDER BY created_at DESC LIMIT 5', (err, recentRows) => {
        if (err) {
          console.error('Error getting recent events:', err);
          return;
        }
        
        console.log('\n🕒 Recent Events:');
        recentRows.forEach(row => {
          console.log(`   ${row.title} (${row.event_type}) - ${row.start_date}`);
        });
        
        console.log('\n========================================');
        process.exit(0);
      });
    });
  });
}); 