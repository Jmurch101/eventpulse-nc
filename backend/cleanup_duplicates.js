// cleanup_duplicates.js
const db = require('./db');

console.log('🧹 Cleaning up duplicate events...');

// First, let's see what duplicates exist
const checkDuplicatesQuery = `
  SELECT title, start_date, source_url, COUNT(*) as count
  FROM events 
  GROUP BY title, start_date, source_url 
  HAVING COUNT(*) > 1
  ORDER BY count DESC
`;

db.all(checkDuplicatesQuery, (err, duplicates) => {
  if (err) {
    console.error('Error checking duplicates:', err);
    return;
  }
  
  console.log(`Found ${duplicates.length} groups of duplicate events:`);
  duplicates.forEach(dup => {
    console.log(`- "${dup.title}" (${dup.count} copies)`);
  });
  
  if (duplicates.length === 0) {
    console.log('✅ No duplicates found!');
    return;
  }
  
  // Remove duplicates, keeping the first occurrence
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
    
    // Verify cleanup
    db.all(checkDuplicatesQuery, (err, remainingDuplicates) => {
      if (err) {
        console.error('Error verifying cleanup:', err);
        return;
      }
      
      if (remainingDuplicates.length === 0) {
        console.log('✅ All duplicates have been removed!');
      } else {
        console.log(`⚠️  ${remainingDuplicates.length} duplicate groups still remain`);
      }
      
      process.exit(0);
    });
  });
}); 