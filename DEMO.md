# 🎯 EventPulse NC - Demo Guide

## 🚀 **Quick Start**

### Option 1: Use the Startup Script
```bash
./start.sh
```

### Option 2: Manual Start
```bash
# Terminal 1 - Backend
cd backend && npm start

# Terminal 2 - Frontend  
cd frontend && npm start

# Terminal 3 - Populate Data
cd scraper && python run_all_scrapers.py
```

## 🎨 **Demo Walkthrough**

### 1. **Homepage Features**
- **Hero Section**: "EventPulse NC" with tagline
- **Category Bubbles**: 8 interactive category buttons
- **Heat Map Calendar**: 30-day visual calendar
- **Quick Stats**: Event counts and sources

### 2. **Category Exploration**
Click any category bubble to see filtered events:

#### 🎓 **University Events** (Blue)
- NC State Engineering Career Fair
- Wolfpack Basketball vs Duke
- NC State Research Symposium
- Commencement ceremonies

#### 🏛️ **Government Meetings** (Green)
- Raleigh City Council meetings
- Public hearings on development
- Parks & Recreation board meetings
- Transportation forums

#### 🎉 **School Holidays** (Purple)
- UNC Chapel Hill Spring Break
- Duke University Spring Break
- Academic calendar events

#### 📅 **Official Holidays** (Red)
- Martin Luther King Jr. Day
- Presidents' Day
- Memorial Day
- Independence Day
- Labor Day
- Thanksgiving
- Christmas

### 3. **Interactive Heat Map**
- **Visual Calendar**: Shows event density
- **Color Coding**: 
  - Gray = No events
  - Green = 1-3 events
  - Yellow = 4-7 events
  - Orange = 8-12 events
  - Red = 13+ events
- **Click Dates**: See events for specific days
- **Today/Tomorrow**: Special highlighting

### 4. **Event Details**
Each event shows:
- **Event Type Badge**: University/Government/Holiday
- **Date Badge**: Today/Tomorrow/This Week/Date
- **Title & Description**: Real event information
- **Time & Location**: Actual details
- **Source Link**: "View Original" button
- **Action Button**: "View Details"

## 📊 **Real Data Showcase**

### **20+ Real Events** from:
- **NC State University** calendar
- **Raleigh Government** meetings
- **NC State Holidays** and school breaks
- **UNC/Duke** academic calendars

### **Geographic Coverage**:
- **Raleigh**: City Hall, PNC Arena, Convention Center
- **NC State**: Talley Student Union, Hunt Library, Carter-Finley Stadium
- **UNC Chapel Hill**: Campus locations
- **Duke University**: Campus locations
- **Statewide**: Federal holidays

## 🎯 **Key Features to Highlight**

### **1. Real Data Integration**
- Actual event titles and descriptions
- Real locations with coordinates
- Accurate dates and times
- Source links to original websites

### **2. Smart Filtering**
- Category-based filtering
- Date-based filtering
- Combined filters work together
- Quick stats show filtered results

### **3. User Experience**
- Responsive design (mobile-friendly)
- Smooth transitions and animations
- Intuitive navigation
- Clear visual hierarchy

### **4. Technical Implementation**
- React 18 with TypeScript
- Node.js backend with SQLite
- Python scrapers for data collection
- Tailwind CSS for styling

## 🔧 **Customization Options**

### **Add More Events**
```bash
cd scraper
# Edit any scraper file to add more events
python run_all_scrapers.py
```

### **Modify Categories**
Edit `frontend/src/components/CategoryBubbles.tsx`:
- Add new categories
- Change colors and icons
- Update event type mappings

### **Update Styling**
Edit `frontend/src/index.css`:
- Modify Tailwind classes
- Add custom CSS
- Update color scheme

## 🎉 **Demo Tips**

### **Best Demo Flow**:
1. **Start with Homepage**: Show the beautiful landing page
2. **Click Category Bubbles**: Demonstrate filtering
3. **Use Heat Map**: Click dates to show events
4. **Show Event Details**: Highlight real data
5. **Mobile View**: Demonstrate responsiveness

### **Key Talking Points**:
- "Real events from actual NC sources"
- "Comprehensive coverage of universities, government, and holidays"
- "Interactive filtering and search capabilities"
- "Built for North Carolina communities"
- "Scalable platform for adding more sources"

### **Technical Highlights**:
- "Modern React with TypeScript"
- "Node.js backend with SQLite database"
- "Python scrapers for data collection"
- "Responsive design with Tailwind CSS"
- "Real-time data updates"

---

**🎯 Ready to showcase EventPulse NC!** 