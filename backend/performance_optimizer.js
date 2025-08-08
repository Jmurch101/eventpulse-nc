// performance_optimizer.js
const db = require('./db');

console.log('🚀 EventPulse NC - Performance Optimization');
console.log('=' * 50);

// Add database indexes for better query performance
const indexes = [
  {
    name: 'idx_events_start_date',
    query: 'CREATE INDEX IF NOT EXISTS idx_events_start_date ON events(start_date)'
  },
  {
    name: 'idx_events_event_type',
    query: 'CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type)'
  },
  {
    name: 'idx_events_location',
    query: 'CREATE INDEX IF NOT EXISTS idx_events_location ON events(latitude, longitude)'
  },
  {
    name: 'idx_events_title_search',
    query: 'CREATE INDEX IF NOT EXISTS idx_events_title_search ON events(title)'
  },
  {
    name: 'idx_events_created_at',
    query: 'CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at)'
  },
  {
    name: 'idx_events_composite',
    query: 'CREATE INDEX IF NOT EXISTS idx_events_composite ON events(event_type, start_date, created_at)'
  }
];

let createdIndexes = 0;

function createIndexes() {
  return new Promise((resolve, reject) => {
    console.log('📊 Creating database indexes...');
    
    indexes.forEach((index, i) => {
      db.run(index.query, (err) => {
        if (err) {
          console.error(`❌ Error creating index ${index.name}:`, err);
        } else {
          createdIndexes++;
          console.log(`   ✅ Created index: ${index.name}`);
        }
        
        if (i === indexes.length - 1) {
          resolve();
        }
      });
    });
  });
}

// Analyze table for query optimization
function analyzeTable() {
  return new Promise((resolve, reject) => {
    console.log('\n📈 Analyzing table for optimization...');
    
    db.run('ANALYZE events', (err) => {
      if (err) {
        console.error('❌ Error analyzing table:', err);
        reject(err);
      } else {
        console.log('   ✅ Table analysis complete');
        resolve();
      }
    });
  });
}

// Get performance statistics
function getPerformanceStats() {
  return new Promise((resolve, reject) => {
    console.log('\n📊 Performance Statistics:');
    
    // Get table size
    db.get("SELECT COUNT(*) as total_events FROM events", (err, totalRow) => {
      if (err) {
        console.error('❌ Error getting total events:', err);
        reject(err);
        return;
      }
      
      console.log(`   📈 Total Events: ${totalRow.total_events}`);
      
      // Get events by type
      db.all("SELECT event_type, COUNT(*) as count FROM events GROUP BY event_type ORDER BY count DESC", (err, typeRows) => {
        if (err) {
          console.error('❌ Error getting events by type:', err);
          reject(err);
          return;
        }
        
        console.log('   📋 Events by Type:');
        typeRows.forEach(row => {
          console.log(`      ${row.event_type}: ${row.count}`);
        });
        
        // Get upcoming events
        db.get("SELECT COUNT(*) as upcoming FROM events WHERE start_date > datetime('now')", (err, upcomingRow) => {
          if (err) {
            console.error('❌ Error getting upcoming events:', err);
            reject(err);
            return;
          }
          
          console.log(`   🔮 Upcoming Events: ${upcomingRow.upcoming}`);
          
          // Get recent events
          db.get("SELECT COUNT(*) as recent FROM events WHERE created_at > datetime('now', '-7 days')", (err, recentRow) => {
            if (err) {
              console.error('❌ Error getting recent events:', err);
              reject(err);
              return;
            }
            
            console.log(`   🆕 Recent Events (7 days): ${recentRow.recent}`);
            resolve();
          });
        });
      });
    });
  });
}

// Test query performance
function testQueryPerformance() {
  return new Promise((resolve, reject) => {
    console.log('\n⚡ Testing Query Performance:');
    
    const queries = [
      {
        name: 'All Events',
        query: 'SELECT * FROM events LIMIT 100'
      },
      {
        name: 'Events by Type',
        query: "SELECT * FROM events WHERE event_type = 'academic' LIMIT 100"
      },
      {
        name: 'Upcoming Events',
        query: "SELECT * FROM events WHERE start_date > datetime('now') LIMIT 100"
      },
      {
        name: 'Search Events',
        query: "SELECT * FROM events WHERE title LIKE '%conference%' LIMIT 100"
      }
    ];
    
    let completedQueries = 0;
    
    queries.forEach((queryInfo, i) => {
      const startTime = Date.now();
      
      db.all(queryInfo.query, (err, rows) => {
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        if (err) {
          console.error(`   ❌ ${queryInfo.name}: Error - ${err.message}`);
        } else {
          console.log(`   ✅ ${queryInfo.name}: ${duration}ms (${rows.length} results)`);
        }
        
        completedQueries++;
        if (completedQueries === queries.length) {
          resolve();
        }
      });
    });
  });
}

// Main optimization function
async function optimizePerformance() {
  try {
    await createIndexes();
    await analyzeTable();
    await getPerformanceStats();
    await testQueryPerformance();
    
    console.log('\n🎉 Performance Optimization Complete!');
    console.log(`📊 Created ${createdIndexes} database indexes`);
    console.log('⚡ Query performance should be significantly improved');
    console.log('📈 Database is now optimized for high-volume operations');
    
  } catch (error) {
    console.error('❌ Performance optimization failed:', error);
  } finally {
    process.exit(0);
  }
}

// Run optimization
optimizePerformance(); 