# 🚀 D.E.L.T.A Business Intelligence Dashboard

A beautiful, modern React TypeScript dashboard for comprehensive business analysis and franchise opportunities. This dashboard connects to your real D.E.L.T.A APIs to provide live market intelligence, heatmap visualizations, and investment analysis.

## ✨ Features

### 🔍 **Smart Business Analysis**
- **Natural Language Queries**: Ask questions like "Should I open a coffee shop in Miami?"
- **Real-time Data**: Connects to live APIs (Google Places, US Census, Mapbox, SerpAPI)
- **Comprehensive Analysis**: Competition, demographics, market opportunity, investment analysis

### 🗺️ **Interactive Heatmap Visualizations**
- **6 Heatmap Layers**: Competition, Demographics, Foot Traffic, Market Opportunity, Income/Wealth, Review Power
- **Real-time Map**: Interactive Mapbox integration with competitor markers
- **Layer Controls**: Toggle different data layers for comprehensive analysis

### 📊 **Business Intelligence**
- **Competitor Analysis**: Real competitor data with ratings, reviews, and locations
- **Demographics**: Population density, income levels, education, employment rates
- **Market Opportunity**: Opportunity scoring, market saturation, growth potential
- **Investment Analysis**: Startup costs, revenue projections, ROI calculations, risk assessment

### 🏆 **Franchise Opportunities**
- **Real Franchise Data**: Available franchise opportunities with investment requirements
- **Investment Breakdown**: Initial investment, royalty fees, marketing costs
- **Risk Assessment**: Investment recommendations based on market analysis

### 📈 **Search Trends & Marketing**
- **Search Volume Data**: Monthly search trends and keyword analysis
- **Social Media Insights**: Instagram hashtags and social media mentions
- **Marketing Intelligence**: Trending keywords and market positioning

## 🛠️ Technology Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS with custom glass morphism effects
- **Maps**: Mapbox GL JS with React Map GL
- **APIs**: Real-time integration with D.E.L.T.A backend services
- **Data Visualization**: Custom heatmap layers and interactive charts

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Your D.E.L.T.A backend services running (ports 8001, 8002)

### Installation

1. **Install Dependencies**
```bash
cd /Users/udishkolnik/3/D.E.L.T.A
npm install
```

2. **Start Backend Services**
```bash
# Terminal 1: Start API server
cd backend
python real_api_server.py

# Terminal 2: Start Bot server  
cd BOT
python bot_server.py
```

3. **Start Frontend Dashboard**
```bash
# Terminal 3: Start React dashboard
npm run dev
```

4. **Open Dashboard**
- Navigate to `http://localhost:3000`
- The dashboard will automatically connect to your backend APIs

## 🎯 Usage Examples

### Natural Language Queries
```
"I want to open a pizza restaurant in Manhattan"
"Should I start a coffee shop in Miami Beach?"
"Analyze the gym market in Los Angeles"
"Franchise opportunities for restaurants in Chicago"
```

### Manual Analysis
1. Select business type from dropdown (Coffee Shop, Restaurant, Pizza, etc.)
2. Choose location (Miami, New York, Los Angeles, etc.)
3. Click "Get Analysis" for comprehensive market intelligence

### Heatmap Analysis
1. Use the heatmap layer controls on the right
2. Toggle between different data layers:
   - 🏢 **Competition**: Business competition intensity
   - 👥 **Demographics**: Population and demographic density  
   - 🚶 **Foot Traffic**: Foot traffic and movement patterns
   - 🎯 **Opportunity**: Market opportunity zones
   - 💰 **Income**: Income and wealth distribution
   - ⭐ **Reviews**: Review power and marketing influence

## 📊 Data Sources

The dashboard integrates with these real APIs:

- **🗺️ Mapbox API**: Geocoding, maps, and geographic data
- **🏢 Google Places API**: Business listings, reviews, ratings, photos
- **👥 US Census API**: Demographics, income, education, population data
- **🔍 SerpAPI**: Search trends, market data, franchise information
- **🤖 D.E.L.T.A Bot API**: Natural language processing and business intelligence
- **🔥 Heatmap Engine**: Multi-layer spatial analysis and opportunity scoring

## 🎨 UI Features

### Modern Design
- **Glass Morphism**: Beautiful frosted glass effects with backdrop blur
- **Gradient Backgrounds**: Stunning purple-to-slate gradient backgrounds
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark Theme**: Professional dark theme optimized for data visualization

### Interactive Elements
- **Real-time Loading States**: Smooth loading animations and progress indicators
- **Error Handling**: Graceful error handling with user-friendly messages
- **Responsive Charts**: Interactive data visualizations that adapt to screen size
- **Smooth Animations**: Framer Motion animations for enhanced user experience

## 🔧 Configuration

### API Endpoints
The dashboard connects to these backend services:
- **API Server**: `http://localhost:8001/api/v1`
- **Bot Server**: `http://localhost:8002`

### Mapbox Configuration
- **Access Token**: Configured in the component (replace with your token)
- **Map Style**: Dark theme optimized for business data
- **Default View**: Times Square, NYC (updates based on search location)

### Business Types Supported
- Coffee Shop, Restaurant, Fast Food, Pizza
- Gym, Salon, Retail Store, Pharmacy
- Bank, Auto Repair, Dentist, Lawyer

## 📱 Responsive Design

The dashboard is fully responsive and optimized for:
- **Desktop**: Full feature set with side-by-side layouts
- **Tablet**: Adapted layouts with collapsible sections
- **Mobile**: Stacked layouts with touch-optimized controls

## 🚀 Production Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Vercel/Netlify
```bash
# Build the project
npm run build

# Deploy the dist/ folder to your hosting platform
```

### Environment Variables
Create a `.env` file for production:
```env
VITE_API_BASE_URL=https://your-api-domain.com/api/v1
VITE_BOT_API_URL=https://your-bot-domain.com
VITE_MAPBOX_ACCESS_TOKEN=your_mapbox_token
```

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure backend services are running on ports 8001 and 8002
   - Check CORS settings in backend configuration
   - Verify API endpoints are accessible

2. **Map Not Loading**
   - Verify Mapbox access token is valid
   - Check network connectivity
   - Ensure Mapbox GL JS is properly loaded

3. **Heatmap Layers Not Showing**
   - Check if heatmap data is being returned from API
   - Verify GeoJSON format is correct
   - Check browser console for errors

### Debug Mode
Enable debug logging by opening browser console and looking for:
- 🚀 Analysis start messages
- ✅ Successful API responses  
- ❌ Error messages with details

## 📈 Performance Optimization

- **Lazy Loading**: Components load on demand
- **API Caching**: Intelligent caching of API responses
- **Image Optimization**: Optimized map tiles and assets
- **Bundle Splitting**: Code splitting for faster initial load

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For support and questions:
- Check the troubleshooting section above
- Review the browser console for error messages
- Ensure all backend services are running properly
- Verify API keys and endpoints are configured correctly

---

**Built with ❤️ by the D.E.L.T.A Team**

*Real data. Real insights. Real business intelligence.*
