# EventPulse NC 🎯

**Your comprehensive guide to events across North Carolina**

EventPulse NC aggregates real events from universities, government meetings, holidays, and more across the state. Built with React, Node.js, and Python scrapers.

## 🚀 **What's Working Now**

### ✅ **Real Data Sources**
- **NC State University Events** - Career fairs, basketball games, research symposiums
- **Raleigh Government Meetings** - City council, public hearings, budget workshops  
- **NC Holidays & School Breaks** - Federal holidays, UNC/Duke spring breaks
- **Interactive Heat Map** - Visual calendar showing event density
- **Category Filtering** - Filter by university, government, holidays, etc.

### 🎯 **Core Features Implemented**
- **Category Bubbles** - Click to filter events by type
- **Interactive Heat Map** - Click dates to see events
- **Real Event Data** - 20+ actual events from NC sources
- **Responsive Design** - Works on desktop and mobile
- **Event Details** - Times, locations, descriptions, source links

## 🛠 **Tech Stack**

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Leaflet** for interactive maps
- **Date-fns** for date handling

### Backend  
- **Node.js** with Express
- **SQLite** database
- **Python scrapers** for data collection

### Data Sources
- NC State University calendar
- Raleigh government websites
- NC state holiday calendar
- UNC/Duke academic calendars

## 🏃‍♂️ **Quick Start**

### 1. Start the Backend
```bash
cd backend
npm install
npm start
```

### 2. Start the Frontend  
```bash
cd frontend
npm install
npm start
```

### 3. Populate with Real Data
```bash
cd scraper
python run_all_scrapers.py
```

### 4. Visit the App
Open http://localhost:3000 to see EventPulse NC in action!

## 📊 **Current Event Categories**

### 🎓 **University Events**
- NC State Engineering Career Fair
- Wolfpack Basketball vs Duke
- NC State Research Symposium
- Commencement ceremonies

### 🏛️ **Government Meetings**  
- Raleigh City Council meetings
- Public hearings on development
- Parks & Recreation board meetings
- Transportation forums

### 🎉 **Holidays & Breaks**
- Federal holidays (MLK Day, Memorial Day, etc.)
- UNC Chapel Hill Spring Break
- Duke University Spring Break
- Thanksgiving and Christmas

## 🎨 **Key Features**

### **Interactive Category Selection**
Click any category bubble to instantly filter events:
- University Events (blue)
- Government Meetings (green) 
- School Holidays (purple)
- Official Holidays (red)
- Workshops (indigo)
- Tech Events (orange)
- Community (pink)

### **Heat Map Calendar**
- Visual representation of event density
- Click any date to see events
- Color-coded by activity level
- Shows next 30 days

### **Real Event Data**
- Actual event titles and descriptions
- Real locations with coordinates
- Accurate dates and times
- Source links to original websites

## 🔧 **Development**

### Project Structure
```
eventpulse-nc/
├── frontend/          # React app
├── backend/           # Node.js API
├── scraper/           # Python scrapers
└── docs/             # Documentation
```

### Adding New Events
1. Create a new scraper in `scraper/`
2. Add real event data
3. Run `python run_all_scrapers.py`
4. Events appear instantly in the UI

### Customizing Categories
Edit `frontend/src/components/CategoryBubbles.tsx` to:
- Add new categories
- Change colors and icons
- Update event type mappings

## 🎯 **Next Steps**

### High Priority
- [ ] Add more NC universities (UNC, Duke, etc.)
- [ ] Expand government sources (Durham, Chapel Hill)
- [ ] Implement search functionality
- [ ] Add event detail pages

### Medium Priority  
- [ ] User accounts and saved events
- [ ] Email notifications
- [ ] Mobile app optimization
- [ ] API documentation

### Future Ideas
- [ ] Event registration integration
- [ ] Social sharing features
- [ ] Event recommendations
- [ ] Analytics dashboard

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Add real event data or features
4. Submit a pull request

## 📄 **License**

MIT License - see LICENSE file for details

---

**Built with ❤️ for North Carolina**

*Connecting communities through events*
