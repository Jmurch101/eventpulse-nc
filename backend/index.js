const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet());

// CORS configuration - allow any origin for frontend access
app.use(cors());

// Logging middleware
app.use(morgan('combined'));

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// API Routes
app.get('/api/events', async (req, res) => {
  try {
    const { event_type, search, year, limit = 100, offset = 0 } = req.query;
    
    let query = 'SELECT * FROM events WHERE 1=1';
    const params = [];
    
    if (event_type) {
      query += ' AND event_type = ?';
      params.push(event_type);
    }
    
    if (search) {
      query += ' AND (title LIKE ? OR description LIKE ? OR location_name LIKE ?)';
      const searchTerm = `%${search}%`;
      params.push(searchTerm, searchTerm, searchTerm);
    }
    
    if (year) {
      query += ' AND start_date LIKE ?';
      params.push(`${year}-%`);
    }
    
    query += ' ORDER BY start_date DESC LIMIT ? OFFSET ?';
    params.push(parseInt(limit), parseInt(offset));
    
    db.all(query, params, (err, rows) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      res.json(rows);
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Event Statistics Endpoint (MUST come before /api/events/:id)
app.get('/api/events/stats', async (req, res) => {
  try {
    const statsQueries = [
      {
        name: 'totalEvents',
        query: 'SELECT COUNT(*) as count FROM events'
      },
      {
        name: 'eventsByType',
        query: 'SELECT event_type, COUNT(*) as count FROM events GROUP BY event_type ORDER BY count DESC'
      },
      {
        name: 'upcomingEvents',
        query: "SELECT COUNT(*) as count FROM events WHERE start_date > datetime('now')"
      },
      {
        name: 'eventsThisWeek',
        query: "SELECT COUNT(*) as count FROM events WHERE start_date BETWEEN datetime('now') AND datetime('now', '+7 days')"
      },
      {
        name: 'eventsThisMonth',
        query: "SELECT COUNT(*) as count FROM events WHERE start_date BETWEEN datetime('now') AND datetime('now', '+30 days')"
      }
    ];
    
    const results = {};
    let completedQueries = 0;
    
    statsQueries.forEach((queryInfo) => {
      db.all(queryInfo.query, (err, rows) => {
        if (err) {
          console.error(`Stats query error (${queryInfo.name}):`, err);
        } else {
          if (queryInfo.name === 'totalEvents' || queryInfo.name === 'upcomingEvents' || 
              queryInfo.name === 'eventsThisWeek' || queryInfo.name === 'eventsThisMonth') {
            results[queryInfo.name] = rows[0].count;
          } else {
            results[queryInfo.name] = rows;
          }
        }
        
        completedQueries++;
        if (completedQueries === statsQueries.length) {
          res.json(results);
        }
      });
    });
  } catch (error) {
    console.error('Stats API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/api/events/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    db.get('SELECT * FROM events WHERE id = ?', [id], (err, row) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      
      if (!row) {
        return res.status(404).json({ error: 'Event not found' });
      }
      
      res.json(row);
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/events', async (req, res) => {
  try {
    const {
      title,
      description,
      start_date,
      end_date,
      location_name,
      latitude,
      longitude,
      organization_id,
      event_type,
      source_url
    } = req.body;
    
    // Validation
    if (!title || !start_date || !end_date) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    // Check for existing event with same title and exact same start_date (includes time)
    const checkQuery = `
      SELECT id FROM events 
      WHERE title = ? AND start_date = ?
    `;
    
    db.get(checkQuery, [title, start_date], (err, existingEvent) => {
      if (err) {
        console.error('Database error checking for duplicates:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      
      if (existingEvent) {
        // Event already exists, return success but indicate it's a duplicate
        return res.status(200).json({
          id: existingEvent.id,
          message: 'Event already exists (duplicate prevented)',
          duplicate: true
        });
      }
      
      // Insert new event
      const insertQuery = `
        INSERT INTO events (
          title, description, start_date, end_date, location_name,
          latitude, longitude, organization_id, event_type, source_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `;
      
      const params = [
        title, description, start_date, end_date, location_name,
        latitude || 0, longitude || 0, organization_id || 1, event_type || 'other', source_url || ''
      ];
      
      db.run(insertQuery, params, function(err) {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Database error' });
        }
        
        res.status(201).json({
          id: this.lastID,
          message: 'Event created successfully',
          duplicate: false
        });
      });
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Cleanup old events endpoint (older than 3 months)
app.post('/api/events/cleanup-old', async (req, res) => {
  try {
    // Remove events older than 3 months from today
    const cleanupQuery = `
      DELETE FROM events 
      WHERE start_date < datetime('now', '-90 days')
    `;
    
    db.run(cleanupQuery, function(err) {
      if (err) {
        console.error('Database error during old events cleanup:', err);
        return res.status(500).json({ error: 'Database error during cleanup' });
      }
      
      res.json({
        message: 'Old events cleanup completed',
        rowsAffected: this.changes
      });
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Cleanup duplicates endpoint
app.post('/api/events/cleanup-duplicates', async (req, res) => {
  try {
    // Find and remove duplicates, keeping the first occurrence
    const cleanupQuery = `
      DELETE FROM events 
      WHERE id NOT IN (
        SELECT MIN(id) 
        FROM events 
        GROUP BY title, start_date
      )
    `;
    
    db.run(cleanupQuery, function(err) {
      if (err) {
        console.error('Database error during cleanup:', err);
        return res.status(500).json({ error: 'Database error during cleanup' });
      }
      
      res.json({
        message: 'Duplicate cleanup completed',
        rowsAffected: this.changes
      });
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get duplicate statistics
app.get('/api/events/duplicates', async (req, res) => {
  try {
    const duplicateQuery = `
      SELECT title, start_date, COUNT(*) as count
      FROM events 
      GROUP BY title, start_date 
      HAVING COUNT(*) > 1
      ORDER BY count DESC
    `;
    
    db.all(duplicateQuery, (err, duplicates) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      
      res.json({
        duplicateGroups: duplicates,
        totalDuplicateGroups: duplicates.length
      });
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Statistics endpoint
app.get('/api/stats', async (req, res) => {
  try {
    db.get('SELECT COUNT(*) as total FROM events', (err, totalRow) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      
      db.get('SELECT COUNT(*) as upcoming FROM events WHERE start_date > datetime("now")', (err, upcomingRow) => {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Database error' });
        }
        
        db.all('SELECT event_type, COUNT(*) as count FROM events GROUP BY event_type', (err, typeRows) => {
          if (err) {
            console.error('Database error:', err);
            return res.status(500).json({ error: 'Database error' });
          }
          
          const stats = {
            total: totalRow.total,
            upcoming: upcomingRow.upcoming,
            byType: typeRows.reduce((acc, row) => {
              acc[row.event_type] = row.count;
              return acc;
            }, {})
          };
          
          res.json(stats);
        });
      });
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Advanced Search Endpoint
app.post('/api/events/search', async (req, res) => {
  try {
    const { query, eventTypes, dateRange, location, tags } = req.body;
    
    let sql = 'SELECT * FROM events WHERE 1=1';
    const params = [];
    
    // Text search
    if (query) {
      sql += ' AND (title LIKE ? OR description LIKE ? OR location_name LIKE ?)';
      const searchTerm = `%${query}%`;
      params.push(searchTerm, searchTerm, searchTerm);
    }
    
    // Event type filter
    if (eventTypes && eventTypes.length > 0) {
      const placeholders = eventTypes.map(() => '?').join(',');
      sql += ` AND event_type IN (${placeholders})`;
      params.push(...eventTypes);
    }
    
    // Date range filter
    if (dateRange && dateRange.start) {
      sql += ' AND start_date >= ?';
      params.push(dateRange.start);
    }
    if (dateRange && dateRange.end) {
      sql += ' AND start_date <= ?';
      params.push(dateRange.end);
    }
    
    // Location filter (simplified - could be enhanced with geospatial queries)
    if (location && location.city) {
      sql += ' AND location_name LIKE ?';
      params.push(`%${location.city}%`);
    }
    
    sql += ' ORDER BY start_date ASC LIMIT 100';
    
    db.all(sql, params, (err, events) => {
      if (err) {
        console.error('Search error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      res.json({ events, count: events.length });
    });
  } catch (error) {
    console.error('Search API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Analytics Endpoint
app.get('/api/analytics', async (req, res) => {
  try {
    const { timeRange = '7d' } = req.query;
    
    // Calculate date range
    const now = new Date();
    let startDate;
    switch (timeRange) {
      case '7d':
        startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case '30d':
        startDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      case '90d':
        startDate = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000);
        break;
      default:
        startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    }
    
    const analyticsQueries = [
      {
        name: 'totalEvents',
        query: 'SELECT COUNT(*) as count FROM events'
      },
      {
        name: 'eventsByType',
        query: 'SELECT event_type, COUNT(*) as count FROM events GROUP BY event_type ORDER BY count DESC'
      },
      {
        name: 'eventsByLocation',
        query: `SELECT 
                  CASE 
                    WHEN location_name LIKE '%Raleigh%' THEN 'Raleigh'
                    WHEN location_name LIKE '%Durham%' THEN 'Durham'
                    WHEN location_name LIKE '%Chapel Hill%' THEN 'Chapel Hill'
                    WHEN location_name LIKE '%Cary%' THEN 'Cary'
                    ELSE 'Other'
                  END as location,
                  COUNT(*) as count 
                FROM events 
                GROUP BY location 
                ORDER BY count DESC`
      },
      {
        name: 'upcomingEvents',
        query: "SELECT COUNT(*) as count FROM events WHERE start_date > datetime('now')"
      },
      {
        name: 'recentEvents',
        query: `SELECT COUNT(*) as count FROM events WHERE created_at > datetime('now', '-7 days')`
      }
    ];
    
    const results = {};
    let completedQueries = 0;
    
    analyticsQueries.forEach((queryInfo) => {
      db.all(queryInfo.query, (err, rows) => {
        if (err) {
          console.error(`Analytics query error (${queryInfo.name}):`, err);
        } else {
          if (queryInfo.name === 'totalEvents' || queryInfo.name === 'upcomingEvents' || queryInfo.name === 'recentEvents') {
            results[queryInfo.name] = rows[0].count;
          } else {
            results[queryInfo.name] = rows;
          }
        }
        
        completedQueries++;
        if (completedQueries === analyticsQueries.length) {
          // Add mock data for features not yet implemented
          results.popularEvents = [
            { id: 1, title: 'NC State Engineering Career Fair', views: 1245, event_type: 'academic' },
            { id: 2, title: 'Raleigh City Council Meeting', views: 892, event_type: 'government' },
            { id: 3, title: 'Triangle Tech Meetup', views: 756, event_type: 'tech' },
            { id: 4, title: 'Durham Farmers Market', views: 634, event_type: 'community' },
            { id: 5, title: 'UNC Research Symposium', views: 523, event_type: 'academic' }
          ];
          
          results.performanceMetrics = {
            avgLoadTime: 1.2,
            apiResponseTime: 0.8,
            cacheHitRate: 85.5,
            errorRate: 0.3
          };
          
          res.json(results);
        }
      });
    });
  } catch (error) {
    console.error('Analytics API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Performance Monitoring Endpoint
app.get('/api/performance', async (req, res) => {
  try {
    const startTime = Date.now();
    
    // Test various queries
    const performanceTests = [
      {
        name: 'totalEvents',
        query: 'SELECT COUNT(*) as count FROM events'
      },
      {
        name: 'eventsByType',
        query: 'SELECT event_type, COUNT(*) as count FROM events GROUP BY event_type'
      },
      {
        name: 'upcomingEvents',
        query: "SELECT COUNT(*) as count FROM events WHERE start_date > datetime('now')"
      },
      {
        name: 'searchEvents',
        query: "SELECT * FROM events WHERE title LIKE '%conference%' LIMIT 10"
      }
    ];
    
    const results = {};
    let completedTests = 0;
    
    performanceTests.forEach((test) => {
      const testStartTime = Date.now();
      
      db.all(test.query, (err, rows) => {
        const testEndTime = Date.now();
        const duration = testEndTime - testStartTime;
        
        if (err) {
          results[test.name] = { error: err.message, duration };
        } else {
          results[test.name] = { 
            success: true, 
            duration, 
            resultCount: rows.length 
          };
        }
        
        completedTests++;
        if (completedTests === performanceTests.length) {
          const totalTime = Date.now() - startTime;
          
          res.json({
            timestamp: new Date().toISOString(),
            totalResponseTime: totalTime,
            tests: results,
            database: {
              totalEvents: results.totalEvents?.resultCount || 0,
              avgQueryTime: Object.values(results)
                .filter(r => r.success)
                .reduce((sum, r) => sum + r.duration, 0) / 
                Object.values(results).filter(r => r.success).length
            }
          });
        }
      });
    });
  } catch (error) {
    console.error('Performance API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 EventPulse NC Backend running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`📚 API docs: http://localhost:${PORT}/api/events`);
});
