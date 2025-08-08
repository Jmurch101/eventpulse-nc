# EventPulse NC Deployment Guide

## 🚀 Deployment Options

### 1. Local Development
- **Best for**: Development and testing
- **Setup**: Follow the development guide
- **Access**: http://localhost:3000 (frontend), http://localhost:5050 (backend)

### 2. Cloud Deployment (Recommended)
- **Platforms**: Heroku, Vercel, Netlify, AWS, Google Cloud
- **Best for**: Production applications
- **Features**: Auto-scaling, SSL, CDN

### 3. Self-Hosted
- **Platforms**: VPS, Docker, Kubernetes
- **Best for**: Full control, custom infrastructure
- **Features**: Complete customization

## ☁️ Cloud Deployment

### Heroku Deployment

#### Backend Deployment
1. **Create Heroku app**
   ```bash
   heroku create eventpulse-nc-backend
   ```

2. **Set environment variables**
   ```bash
   heroku config:set NODE_ENV=production
   heroku config:set FRONTEND_URL=https://your-frontend-domain.com
   ```

3. **Deploy backend**
   ```bash
   cd backend
   git add .
   git commit -m "Deploy backend"
   git push heroku main
   ```

#### Frontend Deployment
1. **Create Heroku app**
   ```bash
   heroku create eventpulse-nc-frontend
   ```

2. **Set buildpack**
   ```bash
   heroku buildpacks:set mars/create-react-app
   ```

3. **Set environment variables**
   ```bash
   heroku config:set REACT_APP_API_URL=https://your-backend-domain.com
   ```

4. **Deploy frontend**
   ```bash
   cd frontend
   git add .
   git commit -m "Deploy frontend"
   git push heroku main
   ```

### Vercel Deployment

#### Frontend Deployment
1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy frontend**
   ```bash
   cd frontend
   vercel
   ```

3. **Set environment variables**
   ```bash
   vercel env add REACT_APP_API_URL
   ```

### Netlify Deployment

#### Frontend Deployment
1. **Build the project**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Netlify**
   - Drag and drop the `build` folder to Netlify
   - Or use Netlify CLI

3. **Set environment variables**
   - Go to Site settings > Environment variables
   - Add `REACT_APP_API_URL`

## 🐳 Docker Deployment

### Create Dockerfile for Backend
```dockerfile
# backend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 5050

CMD ["npm", "start"]
```

### Create Dockerfile for Frontend
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Create docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5050:5050"
    environment:
      - NODE_ENV=production
      - FRONTEND_URL=http://localhost:3000
    volumes:
      - ./backend/events.db:/app/events.db

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:5050

  scraper:
    build: ./scraper
    volumes:
      - ./backend/events.db:/app/events.db
    depends_on:
      - backend
```

### Deploy with Docker
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Environment Configuration

### Production Environment Variables

#### Backend (.env)
```bash
NODE_ENV=production
PORT=5050
FRONTEND_URL=https://your-frontend-domain.com
DATABASE_URL=sqlite:///events.db
LOG_LEVEL=info
CORS_ORIGIN=https://your-frontend-domain.com
```

#### Frontend (.env.production)
```bash
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_ENVIRONMENT=production
REACT_APP_VERSION=$npm_package_version
```

### Development Environment Variables

#### Backend (.env.development)
```bash
NODE_ENV=development
PORT=5050
FRONTEND_URL=http://localhost:3000
DATABASE_URL=sqlite:///events.db
LOG_LEVEL=debug
CORS_ORIGIN=http://localhost:3000
```

#### Frontend (.env.development)
```bash
REACT_APP_API_URL=http://localhost:5050
REACT_APP_ENVIRONMENT=development
```

## 🔒 Security Configuration

### SSL/HTTPS Setup
1. **Obtain SSL certificate**
   - Let's Encrypt (free)
   - Cloudflare SSL
   - Paid certificates

2. **Configure SSL in production**
   ```javascript
   // backend/index.js
   const https = require('https');
   const fs = require('fs');
   
   const options = {
     key: fs.readFileSync('path/to/key.pem'),
     cert: fs.readFileSync('path/to/cert.pem')
   };
   
   https.createServer(options, app).listen(443);
   ```

### Security Headers
```javascript
// backend/index.js
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}));
```

## 📊 Monitoring and Logging

### Application Monitoring
1. **Set up logging**
   ```javascript
   // backend/index.js
   const winston = require('winston');
   
   const logger = winston.createLogger({
     level: 'info',
     format: winston.format.json(),
     transports: [
       new winston.transports.File({ filename: 'error.log', level: 'error' }),
       new winston.transports.File({ filename: 'combined.log' })
     ]
   });
   ```

2. **Health checks**
   ```javascript
   app.get('/health', (req, res) => {
     res.json({
       status: 'OK',
       timestamp: new Date().toISOString(),
       uptime: process.uptime(),
       memory: process.memoryUsage()
     });
   });
   ```

### Database Monitoring
```sql
-- Check database size
SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();

-- Check table sizes
SELECT name, sql FROM sqlite_master WHERE type='table';
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Use Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
    - run: npm ci
    - run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: "eventpulse-nc-backend"
        heroku_email: "your-email@example.com"
```

## 📈 Performance Optimization

### Backend Optimization
1. **Database indexing**
   ```sql
   CREATE INDEX idx_events_start_date ON events(start_date);
   CREATE INDEX idx_events_event_type ON events(event_type);
   CREATE INDEX idx_events_location ON events(location_name);
   ```

2. **Caching**
   ```javascript
   const redis = require('redis');
   const client = redis.createClient();
   
   app.get('/api/events', async (req, res) => {
     const cacheKey = `events:${JSON.stringify(req.query)}`;
     const cached = await client.get(cacheKey);
     
     if (cached) {
       return res.json(JSON.parse(cached));
     }
     
     // Fetch from database and cache
   });
   ```

### Frontend Optimization
1. **Code splitting**
   ```javascript
   const EventList = React.lazy(() => import('./components/EventList'));
   const EventDetail = React.lazy(() => import('./components/EventDetail'));
   ```

2. **Service worker for caching**
   ```javascript
   // public/sw.js
   const CACHE_NAME = 'eventpulse-v1';
   const urlsToCache = [
     '/',
     '/static/js/bundle.js',
     '/static/css/main.css'
   ];
   ```

## 🚨 Backup and Recovery

### Database Backup
```bash
# Create backup
sqlite3 backend/events.db ".backup backup/events_$(date +%Y%m%d_%H%M%S).db"

# Restore backup
sqlite3 backend/events.db ".restore backup/events_20231201_120000.db"
```

### Automated Backup Script
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_FILE="backend/events.db"

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/events_$DATE.db

# Keep only last 7 days of backups
find $BACKUP_DIR -name "events_*.db" -mtime +7 -delete
```

## 🔍 Troubleshooting

### Common Deployment Issues

**Backend won't start**
- Check environment variables
- Verify database permissions
- Check port availability

**Frontend build fails**
- Clear npm cache
- Check for missing dependencies
- Verify environment variables

**Database connection issues**
- Check database file permissions
- Verify database path
- Check SQLite version compatibility

**CORS errors**
- Verify CORS configuration
- Check frontend URL in backend config
- Ensure HTTPS/HTTP consistency

### Performance Issues

**Slow API responses**
- Add database indexes
- Implement caching
- Optimize queries
- Add pagination

**Large bundle size**
- Enable code splitting
- Remove unused dependencies
- Optimize images
- Use tree shaking

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Verify environment configuration
4. Contact the development team

## 🔗 Useful Resources

- [Heroku Documentation](https://devcenter.heroku.com/)
- [Vercel Documentation](https://vercel.com/docs)
- [Netlify Documentation](https://docs.netlify.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Node.js Production Best Practices](https://expressjs.com/en/advanced/best-practices-production.html) 