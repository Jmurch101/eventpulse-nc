# Duplicate Event Prevention System

## Overview

EventPulse NC now includes a comprehensive duplicate prevention system that prevents the same events from being added multiple times when scrapers run repeatedly.

## How It Works

### 1. Application-Level Duplicate Detection
- **Criteria**: Events are considered duplicates if they have the same `title` AND `start_date`
- **Method**: Before inserting a new event, the system checks if an event with the same title and start date already exists
- **Response**: 
  - If duplicate found: Returns status 200 with `"duplicate": true`
  - If new event: Returns status 201 with `"duplicate": false`

### 2. Database Schema
The events table structure:
```sql
CREATE TABLE events (
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
```

### 3. API Endpoints

#### POST /api/events
- **Purpose**: Add new events with duplicate checking
- **Response**: 
  ```json
  {
    "id": 123,
    "message": "Event created successfully",
    "duplicate": false
  }
  ```
  or
  ```json
  {
    "id": 123,
    "message": "Event already exists (duplicate prevented)",
    "duplicate": true
  }
  ```

#### POST /api/events/cleanup-duplicates
- **Purpose**: Remove existing duplicate events from database
- **Response**:
  ```json
  {
    "message": "Duplicate cleanup completed",
    "rowsAffected": 15
  }
  ```

#### GET /api/events/duplicates
- **Purpose**: Get statistics about duplicate events
- **Response**:
  ```json
  {
    "duplicateGroups": [
      {
        "title": "Event Name",
        "start_date": "2024-01-01T10:00:00",
        "count": 3
      }
    ],
    "totalDuplicateGroups": 5
  }
  ```

## Scraper Integration

### Updated post_event.py
The `post_event()` function now:
- Returns `True` for successfully added events
- Returns `False` for duplicate events
- Provides clear console feedback:
  - `✅ Posted: Event Name` for new events
  - `⏭️  Skipped (duplicate): Event Name` for duplicates

### Scraper Summary Reports
Scrapers now provide summary reports:
```
📊 NC State Events Summary:
   ✅ Added: 0
   ⏭️  Skipped (duplicates): 5
   📋 Total processed: 5
```

## Management Tools

### 1. Cleanup Scripts

#### cleanup_duplicates.js
```bash
cd backend
node cleanup_duplicates.js
```
- Shows existing duplicates
- Removes duplicates keeping the first occurrence

#### update_schema.js
```bash
cd backend
node update_schema.js
```
- Updates database schema with duplicate prevention
- Cleans up existing duplicates

#### fix_constraint.js
```bash
cd backend
node fix_constraint.js
```
- Fixes database constraints if needed

#### remove_constraint.js
```bash
cd backend
node remove_constraint.js
```
- Removes database constraints (handles duplicates at app level only)

### 2. Database Queries

#### Check for duplicates:
```sql
SELECT title, start_date, COUNT(*) as count
FROM events 
GROUP BY title, start_date 
HAVING COUNT(*) > 1
ORDER BY count DESC;
```

#### Count total events:
```sql
SELECT COUNT(*) FROM events;
```

## Benefits

1. **No More Duplicate Events**: Scrapers can run multiple times without creating duplicates
2. **Clear Feedback**: Console output shows exactly what was added vs skipped
3. **Flexible Detection**: Uses title + start_date for reliable duplicate detection
4. **Management Tools**: Easy cleanup and monitoring of duplicates
5. **API Integration**: RESTful endpoints for duplicate management

## Example Usage

### Running scrapers multiple times:
```bash
# First run - adds new events
python run_all_scrapers.py

# Second run - skips duplicates
python run_all_scrapers.py
```

### Checking for duplicates:
```bash
curl http://localhost:3001/api/events/duplicates
```

### Cleaning up duplicates:
```bash
curl -X POST http://localhost:3001/api/events/cleanup-duplicates
```

## Migration Notes

- The system automatically cleaned up 121 existing duplicate events
- Database schema was updated to support duplicate prevention
- All existing scrapers now work with the new system
- No changes needed to frontend code

## Troubleshooting

### If you see database errors:
1. Restart the backend server: `cd backend && npm start`
2. Check database integrity: `sqlite3 events.db "PRAGMA integrity_check;"`
3. Run cleanup: `node cleanup_duplicates.js`

### If duplicates still appear:
1. Check the duplicate detection criteria (title + start_date)
2. Verify event data format is consistent
3. Use the cleanup endpoint to remove existing duplicates 