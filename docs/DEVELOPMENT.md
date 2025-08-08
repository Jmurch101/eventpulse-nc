# EventPulse NC Development Guide

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- npm or yarn
- Git

### Initial Setup

1. **Clone and setup the project**
   ```bash
   git clone <repository-url>
   cd eventpulse-nc
   ```

2. **Install all dependencies**
   ```bash
   # Backend dependencies
   cd backend && npm install
   
   # Frontend dependencies  
   cd ../frontend && npm install
   
   # Python dependencies
   cd ../scraper && pip install -r requirements.txt
   ```

3. **Start the development environment**
   ```bash
   # Terminal 1: Start backend
   cd backend && npm run dev
   
   # Terminal 2: Start frontend
   cd frontend && npm start
   
   # Terminal 3: Run scrapers (when needed)
   cd scraper && python main.py
   ```

## 🏗️ Architecture Overview

### Backend (Node.js/Express)
- **Port**: 5050
- **Database**: SQLite (events.db)
- **Key Files**:
  - `index.js` - Main server file
  - `db.js` - Database configuration
  - `package.json` - Dependencies and scripts

### Frontend (React/TypeScript)
- **Port**: 3000
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Key Files**:
  - `src/App.tsx` - Main application
  - `src/components/` - React components
  - `src/services/api.ts` - API communication
  - `src/types/Event.ts` - TypeScript types

### Scrapers (Python)
- **Framework**: Custom scraper classes
- **Key Files**:
  - `main.py` - Scraper orchestration
  - `base_scraper.py` - Base scraper class
  - `*_scraper.py` - Individual scrapers

## 📁 Project Structure

```
eventpulse-nc/
├── backend/                 # Node.js API server
│   ├── index.js            # Express server
│   ├── db.js               # Database setup
│   ├── events.db           # SQLite database
│   └── package.json        # Backend dependencies
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── EventList.tsx
│   │   │   ├── EventDetail.tsx
│   │   │   ├── EventMap.tsx
│   │   │   ├── Navbar.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── services/       # API services
│   │   │   └── api.ts
│   │   ├── types/          # TypeScript types
│   │   │   └── Event.ts
│   │   └── App.tsx         # Main application
│   └── package.json        # Frontend dependencies
├── scraper/                # Python scraping engine
│   ├── main.py             # Main scraper orchestration
│   ├── base_scraper.py     # Base scraper class
│   ├── requirements.txt    # Python dependencies
│   └── *_scraper.py        # Individual scrapers
└── docs/                   # Documentation
    └── DEVELOPMENT.md      # This file
```

## 🔧 Development Workflow

### Adding New Features

1. **Create a feature branch**
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation

3. **Test your changes**
   ```bash
   # Test backend
   cd backend && npm test
   
   # Test frontend
   cd frontend && npm test
   
   # Test scrapers
   cd scraper && python -m pytest
   ```

4. **Submit a pull request**
   - Include a clear description
   - Reference any related issues
   - Request code review

### Adding New Scrapers

1. **Create a new scraper file**
   ```python
   # scraper/new_source_scraper.py
   from base_scraper import BaseScraper
   from post_event import post_event
   
   class NewSourceScraper(BaseScraper):
       def __init__(self):
           super().__init__("New Source", "https://example.com")
       
       def parse_events(self, html):
           # Implement parsing logic
           pass
   ```

2. **Add to main.py**
   ```python
   from new_source_scraper import NewSourceScraper
   
   # In main section
   print("🔎 New Source Events")
   NewSourceScraper().run_and_post()
   ```

3. **Test the scraper**
   ```bash
   cd scraper && python -c "from new_source_scraper import NewSourceScraper; NewSourceScraper().run_and_post()"
   ```

## 🎨 Coding Standards

### JavaScript/TypeScript
- Use ES6+ features
- Prefer const/let over var
- Use meaningful variable names
- Add JSDoc comments for functions
- Follow Airbnb style guide

### Python
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to classes and functions
- Use type hints where possible

### React Components
- Use functional components with hooks
- Keep components small and focused
- Use TypeScript interfaces for props
- Follow the component naming convention

## 🧪 Testing

### Backend Testing
```bash
cd backend
npm test
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Scraper Testing
```bash
cd scraper
python -m pytest tests/
```

## 🚀 Deployment

### Production Build
```bash
# Frontend
cd frontend && npm run build

# Backend
cd backend && npm start
```

### Environment Variables
Create `.env` files for each environment:

```bash
# Backend .env
PORT=5050
NODE_ENV=production
FRONTEND_URL=https://yourdomain.com

# Frontend .env
REACT_APP_API_URL=https://api.yourdomain.com
```

## 🔍 Debugging

### Backend Debugging
```bash
# Enable debug logging
DEBUG=* npm run dev

# Check database
sqlite3 backend/events.db "SELECT * FROM events LIMIT 5;"
```

### Frontend Debugging
- Use React Developer Tools
- Check browser console
- Use Redux DevTools (if using Redux)

### Scraper Debugging
```bash
# Run individual scraper with verbose output
cd scraper && python -c "from ncsu_scraper import NCSUScraper; scraper = NCSUScraper(); print(scraper.fetch_html(scraper.base_url)[:500])"
```

## 📊 Performance Optimization

### Backend
- Implement caching (Redis)
- Add database indexes
- Use connection pooling
- Implement rate limiting

### Frontend
- Code splitting with React.lazy()
- Optimize bundle size
- Use React.memo() for expensive components
- Implement virtual scrolling for large lists

### Scrapers
- Add retry logic
- Implement concurrent scraping
- Cache scraped data
- Add rate limiting

## 🔒 Security

### Backend Security
- Input validation
- SQL injection prevention
- CORS configuration
- Rate limiting
- Helmet.js for headers

### Frontend Security
- XSS prevention
- Content Security Policy
- HTTPS enforcement
- Secure cookie handling

## 📈 Monitoring

### Logging
- Use structured logging
- Log levels (error, warn, info, debug)
- Centralized log management

### Metrics
- API response times
- Error rates
- Database performance
- Scraper success rates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 🆘 Troubleshooting

### Common Issues

**Backend won't start**
- Check if port 5050 is available
- Verify database permissions
- Check Node.js version

**Frontend won't start**
- Check if port 3000 is available
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall

**Scrapers failing**
- Check internet connection
- Verify target websites are accessible
- Check for rate limiting
- Update user agents if needed

**Database issues**
- Check SQLite file permissions
- Verify database schema
- Backup and recreate if corrupted

## 📚 Additional Resources

- [React Documentation](https://reactjs.org/docs/)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs) 