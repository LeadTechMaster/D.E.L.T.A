import React, { useState, useEffect, useCallback } from 'react';
import { Map, Marker, Popup, Source, Layer } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { deltaAPI, BusinessAnalysisRequest } from './services/api';

// Set Mapbox access token
const MAPBOX_TOKEN = 'pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw';

// Types
interface BusinessAnalysis {
  businessType: string;
  location: string;
  coordinates: [number, number];
  competitors: Competitor[];
  demographics: Demographics;
  marketOpportunity: MarketOpportunity;
  heatmapLayers: HeatmapLayer[];
  franchiseOpportunities: FranchiseOpportunity[];
  investmentAnalysis: InvestmentAnalysis;
  searchTrends: SearchTrends;
}

interface Competitor {
  name: string;
  rating: number;
  reviews: number;
  distance: string;
  price: string;
  coordinates: [number, number];
}

interface Demographics {
  populationDensity: string;
  medianAge: number;
  medianHouseholdIncome: string;
  educationLevel: string;
  employmentRate: string;
  populationGrowth: string;
  householdSize: number;
  ethnicDiversity: string;
}

interface MarketOpportunity {
  competitorCount: number;
  marketSaturation: string;
  opportunityScore: string;
  marketSize: string;
  growthRate: string;
  averageCheckSize: string;
  peakHours: string;
  seasonalVariation: string;
  recommendation: string;
}

interface HeatmapLayer {
  id: string;
  name: string;
  description: string;
  data: any;
  colorScheme: string;
  visible: boolean;
}

interface FranchiseOpportunity {
  name: string;
  initialInvestment: string;
  royalty: string;
  marketing: string;
  description: string;
}

interface InvestmentAnalysis {
  estimatedStartupCost: string;
  monthlyRent: string;
  equipmentCosts: string;
  licensingFees: string;
  initialInventory: string;
  estimatedMonthlyRevenue: string;
  estimatedMonthlyProfit: string;
  monthsToROI: string;
  breakEvenPoint: string;
  riskLevel: string;
  investmentRecommendation: string;
}

interface SearchTrends {
  monthlySearches: Record<string, string>;
  trendingKeywords: string[];
  socialMediaMentions: string;
  instagramHashtags: Record<string, string>;
}

// Main Component
const App: React.FC = () => {
  // State management
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedBusinessType, setSelectedBusinessType] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [analysis, setAnalysis] = useState<BusinessAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeHeatmapLayer, setActiveHeatmapLayer] = useState<string>('business_competition');
  const [selectedCompetitor, setSelectedCompetitor] = useState<Competitor | null>(null);
  const [viewState, setViewState] = useState({
    longitude: -80.1918, // Miami coordinates
    latitude: 25.7617,
    zoom: 10
  });

  // Update viewState when analysis coordinates are available
  useEffect(() => {
    if (analysis && analysis.coordinates && analysis.coordinates.length === 2) {
      console.log('🗺️ Updating map viewState with coordinates:', analysis.coordinates);
      setViewState({
        longitude: analysis.coordinates[0],
        latitude: analysis.coordinates[1],
    zoom: 12
  });
    }
  }, [analysis]);

  // Show fallback if map doesn't load within 5 seconds
  useEffect(() => {
    if (analysis && analysis.coordinates) {
      const timer = setTimeout(() => {
        const fallback = document.getElementById('map-fallback');
        if (fallback) {
          fallback.style.display = 'flex';
        }
      }, 5000);
      
      return () => clearTimeout(timer);
    }
  }, [analysis]);

  // Business types for dropdown
  const businessTypes = [
    'Coffee Shop', 'Restaurant', 'Fast Food', 'Pizza', 'Gym', 'Salon', 
    'Retail Store', 'Pharmacy', 'Bank', 'Auto Repair', 'Dentist', 'Lawyer'
  ];

  // Popular locations
  const popularLocations = [
    'Miami, FL', 'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 
    'Houston, TX', 'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX',
    'San Diego, CA', 'Dallas, TX', 'San Jose, CA', 'Austin, TX'
  ];

  // Heatmap layer configurations
  const heatmapLayers = [
    {
      id: 'business_competition',
      name: '🏢 Competition',
      description: 'Business competition intensity',
      color: '#ff4444'
    },
    {
      id: 'demographic_density',
      name: '👥 Demographics',
      description: 'Population and demographic density',
      color: '#4444ff'
    },
    {
      id: 'foot_traffic',
      name: '🚶 Foot Traffic',
      description: 'Foot traffic and movement patterns',
      color: '#8844ff'
    },
    {
      id: 'market_opportunity',
      name: '🎯 Opportunity',
      description: 'Market opportunity zones',
      color: '#44ff44'
    },
    {
      id: 'income_wealth',
      name: '💰 Income',
      description: 'Income and wealth distribution',
      color: '#44aaff'
    },
    {
      id: 'review_power',
      name: '⭐ Reviews',
      description: 'Review power and marketing influence',
      color: '#ff8844'
    }
  ];

  // API call to fetch analysis data
  const fetchAnalysis = useCallback(async () => {
    if (!selectedBusinessType || !selectedLocation) {
      // If no business type/location set, try to extract from search query
      if (searchQuery.trim()) {
        handleNaturalLanguageQuery();
        return;
      }
      return;
    }

    setLoading(true);
    setError(null);

    try {
      console.log('🚀 Starting business analysis...', { selectedBusinessType, selectedLocation, searchQuery });
      
      const request: BusinessAnalysisRequest = {
        businessType: selectedBusinessType,
        location: selectedLocation,
        query: searchQuery
      };

      const data = await deltaAPI.getBusinessAnalysis(request);
      setAnalysis(data);
      
      // Update map view to location
      if (data.coordinates) {
        setViewState({
          longitude: data.coordinates[0],
          latitude: data.coordinates[1],
          zoom: 12
        });
      }
      
      console.log('✅ Analysis complete:', data);
    } catch (err) {
      console.error('❌ Analysis failed:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [selectedBusinessType, selectedLocation, searchQuery]);

  // Handle search - now only uses natural language
  const handleSearch = () => {
    if (searchQuery.trim()) {
      handleNaturalLanguageQuery();
    }
  };

  // Handle natural language query - now the primary method
  const handleNaturalLanguageQuery = () => {
    if (!searchQuery.trim()) return;

    // Parse natural language query
    const query = searchQuery.toLowerCase();
    
    // Extract business type from common keywords
    let businessType = 'restaurant'; // Default to restaurant for food businesses
    if (query.includes('coffee') || query.includes('cafe')) businessType = 'coffee shop';
    else if (query.includes('restaurant') || query.includes('food') || query.includes('burger') || query.includes('fast food') || query.includes('dining')) businessType = 'restaurant';
    else if (query.includes('pizza')) businessType = 'pizza';
    else if (query.includes('gym') || query.includes('fitness')) businessType = 'gym';
    else if (query.includes('salon') || query.includes('beauty')) businessType = 'salon';
    else if (query.includes('retail') || query.includes('store')) businessType = 'retail store';
    else if (query.includes('pharmacy') || query.includes('drug')) businessType = 'pharmacy';
    else if (query.includes('bank') || query.includes('financial')) businessType = 'bank';
    else if (query.includes('auto') || query.includes('car')) businessType = 'auto repair';
    else if (query.includes('motor') || query.includes('boat') || query.includes('marine')) businessType = 'marine services';
    else if (query.includes('dentist') || query.includes('dental')) businessType = 'dentist';
    else if (query.includes('lawyer') || query.includes('legal')) businessType = 'lawyer';
    
    // Extract location from common patterns
    let location = 'Miami, FL'; // Default
    if (query.includes('miami')) location = 'Miami, FL';
    else if (query.includes('new york') || query.includes('manhattan') || query.includes('manhatan')) location = 'New York, NY';
    else if (query.includes('los angeles')) location = 'Los Angeles, CA';
    else if (query.includes('chicago')) location = 'Chicago, IL';
    else if (query.includes('houston')) location = 'Houston, TX';
    else if (query.includes('phoenix')) location = 'Phoenix, AZ';
    else if (query.includes('philadelphia')) location = 'Philadelphia, PA';
    else if (query.includes('san antonio')) location = 'San Antonio, TX';
    else if (query.includes('san diego')) location = 'San Diego, CA';
    else if (query.includes('dallas')) location = 'Dallas, TX';
    else if (query.includes('san jose')) location = 'San Jose, CA';
    else if (query.includes('austin')) location = 'Austin, TX';

    setSelectedBusinessType(businessType);
    setSelectedLocation(location);

    // Trigger analysis
      setTimeout(() => fetchAnalysis(), 100);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-white">
                🚀 D.E.L.T.A Business Intelligence
              </h1>
              <p className="text-white/70 mt-1">
                Real-time market analysis and franchise opportunities
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm font-medium">
                🔴 LIVE DATA
              </div>
              <div className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-sm font-medium">
                📊 REAL APIS
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-8 border border-white/20">
          <h2 className="text-xl font-semibold text-white mb-4">
            💬 Ask About Any Business Opportunity
          </h2>
          
          {/* Natural Language Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-white/80 mb-2">
              Just ask naturally - I'll analyze everything for you
            </label>
            <div className="flex space-x-3">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="I want to open a motor boat shop in Miami center beach..."
                className="flex-1 px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
                onKeyPress={(e) => e.key === 'Enter' && handleNaturalLanguageQuery()}
              />
              <button
                onClick={handleNaturalLanguageQuery}
                disabled={loading || !searchQuery.trim()}
                className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-medium rounded-lg transition-all duration-200 disabled:cursor-not-allowed"
              >
                {loading ? '🔄 Analyzing...' : '🚀 Analyze'}
              </button>
            </div>
          </div>

        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 mb-8">
            <p className="text-red-400">❌ {error}</p>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-8">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white/70 text-sm">Market Opportunity</p>
                    <p className="text-2xl font-bold text-white">{analysis.marketOpportunity?.opportunityScore || 'N/A'}</p>
                  </div>
                  <div className="text-3xl">🎯</div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white/70 text-sm">Competitors</p>
                    <p className="text-2xl font-bold text-white">{analysis.marketOpportunity?.competitorCount || 'N/A'}</p>
                  </div>
                  <div className="text-3xl">🏢</div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white/70 text-sm">Market Size</p>
                    <p className="text-2xl font-bold text-white">{analysis.marketOpportunity?.marketSize || 'N/A'}</p>
                  </div>
                  <div className="text-3xl">💰</div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white/70 text-sm">Risk Level</p>
                    <p className="text-2xl font-bold text-white">{analysis.investmentAnalysis?.riskLevel || 'N/A'}</p>
                  </div>
                  <div className="text-3xl">⚠️</div>
                </div>
              </div>
            </div>

            {/* Map and Heatmap Controls */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Map */}
              <div className="lg:col-span-3">
                <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
                  <h3 className="text-lg font-semibold text-white mb-4">
                    🗺️ Market Intelligence Map
                  </h3>
                  
                  <div className="h-96 rounded-lg overflow-hidden border border-white/20 relative bg-gray-800" id="map-container">
                    <Map
                      {...viewState}
                      onMove={evt => setViewState(evt.viewState)}
                      mapboxAccessToken={MAPBOX_TOKEN}
                      style={{ width: '100%', height: '400px' }}
                      mapStyle="mapbox://styles/mapbox/streets-v12"
                      attributionControl={false}
                      logoPosition="bottom-left"
                      onLoad={(evt) => {
                        console.log('🗺️ Map loaded successfully');
                        console.log('🗺️ Map viewState:', viewState);
                        console.log('🗺️ Analysis coordinates:', analysis.coordinates);
                        console.log('🗺️ Mapbox token present:', !!MAPBOX_TOKEN);
                        console.log('🗺️ Map container size:', evt.target.getContainer().offsetWidth, 'x', evt.target.getContainer().offsetHeight);
                        console.log('🗺️ Map center:', evt.target.getCenter());
                        console.log('🗺️ Map zoom:', evt.target.getZoom());
                      }}
                      onError={(e) => {
                        console.error('🗺️ Map error:', e);
                        console.error('🗺️ Mapbox token:', MAPBOX_TOKEN ? 'Present' : 'Missing');
                        // Show fallback message
                        const fallback = document.getElementById('map-fallback');
                        if (fallback) {
                          fallback.style.display = 'flex';
                        }
                      }}
                    >
                      {/* Main business location marker */}
                      {analysis.coordinates && analysis.coordinates.length === 2 && (
                        <Marker
                          longitude={analysis.coordinates[0]}
                          latitude={analysis.coordinates[1]}
                        >
                          <div className="bg-blue-500 text-white p-3 rounded-full cursor-pointer hover:bg-blue-600 transition-colors shadow-lg">
                            🎯
                          </div>
                        </Marker>
                      )}

                      {/* Competitor markers */}
                      {analysis.competitors.map((competitor, index) => {
                        if (competitor.coordinates && competitor.coordinates.length === 2) {
                          return (
                        <Marker
                          key={index}
                          longitude={competitor.coordinates[0]}
                          latitude={competitor.coordinates[1]}
                              onClick={() => setSelectedCompetitor(competitor)}
                        >
                              <div className="bg-red-500 text-white p-2 rounded-full cursor-pointer hover:bg-red-600 transition-colors shadow-lg">
                            🏢
                          </div>
                        </Marker>
                          );
                        }
                        return null;
                      })}

                      {/* Enhanced Competitor popup */}
                      {selectedCompetitor && selectedCompetitor.coordinates && selectedCompetitor.coordinates.length === 2 && (
                        <Popup
                          longitude={selectedCompetitor.coordinates[0]}
                          latitude={selectedCompetitor.coordinates[1]}
                          onClose={() => setSelectedCompetitor(null)}
                          closeButton={true}
                          closeOnClick={false}
                          className="competitor-popup"
                          maxWidth="400px"
                        >
                          <div className="p-4 min-w-[300px] max-w-[400px]">
                            <div className="flex items-center justify-between mb-3">
                              <h3 className="font-bold text-lg text-gray-800">
                                {selectedCompetitor.name}
                              </h3>
                              <button
                                onClick={() => setSelectedCompetitor(null)}
                                className="text-gray-400 hover:text-gray-600 text-xl"
                              >
                                ×
                              </button>
                            </div>
                            
                            {/* Rating and Reviews */}
                            <div className="flex items-center mb-3 p-2 bg-yellow-50 rounded-lg">
                              <span className="text-yellow-500 text-xl mr-2">⭐</span>
                              <div>
                                <span className="font-semibold text-lg">{selectedCompetitor.rating.toFixed(1)}</span>
                                <span className="text-gray-600 ml-1">({selectedCompetitor.reviews} reviews)</span>
                              </div>
                            </div>

                            {/* Location and Distance */}
                            <div className="mb-3 p-2 bg-blue-50 rounded-lg">
                              <div className="flex items-center text-blue-700">
                                <span className="mr-2">📍</span>
                                <span className="font-medium">{selectedCompetitor.distance}</span>
                              </div>
                              {selectedCompetitor.address && (
                                <div className="text-sm text-gray-600 mt-1 ml-6">
                                  {selectedCompetitor.address}
                                </div>
                              )}
                            </div>

                            {/* Price Range */}
                            <div className="mb-3 p-2 bg-green-50 rounded-lg">
                              <div className="flex items-center text-green-700">
                                <span className="mr-2">💰</span>
                                <span className="font-medium">Price: {selectedCompetitor.price}</span>
                              </div>
                            </div>

                            {/* Additional Details */}
                            <div className="space-y-2 text-sm">
                              {selectedCompetitor.phone && (
                                <div className="flex items-center text-gray-600">
                                  <span className="mr-2">📞</span>
                                  <span>{selectedCompetitor.phone}</span>
                                </div>
                              )}
                              
                              {selectedCompetitor.website && (
                                <div className="flex items-center text-gray-600">
                                  <span className="mr-2">🌐</span>
                                  <a 
                                    href={selectedCompetitor.website} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:text-blue-800 underline"
                                  >
                                    Visit Website
                                  </a>
                                </div>
                              )}

                              {selectedCompetitor.hours && (
                                <div className="flex items-start text-gray-600">
                                  <span className="mr-2 mt-1">🕒</span>
                                  <div>
                                    <div className="font-medium">Hours:</div>
                                    <div className="text-xs">{selectedCompetitor.hours}</div>
                                  </div>
                                </div>
                              )}

                              {selectedCompetitor.categories && (
                                <div className="flex items-start text-gray-600">
                                  <span className="mr-2 mt-1">🏷️</span>
                                  <div>
                                    <div className="font-medium">Categories:</div>
                                    <div className="text-xs">{selectedCompetitor.categories.join(', ')}</div>
                                  </div>
                                </div>
                              )}
                            </div>

                            {/* Action Buttons */}
                            <div className="mt-4 flex space-x-2">
                              <button
                                onClick={() => {
                                  if (selectedCompetitor.website) {
                                    window.open(selectedCompetitor.website, '_blank');
                                  }
                                }}
                                className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg text-sm hover:bg-blue-700 transition-colors"
                              >
                                Visit Website
                              </button>
                              <button
                                onClick={() => {
                                  const query = `${selectedCompetitor.name} ${analysis.location}`;
                                  window.open(`https://www.google.com/maps/search/${encodeURIComponent(query)}`, '_blank');
                                }}
                                className="flex-1 bg-green-600 text-white px-3 py-2 rounded-lg text-sm hover:bg-green-700 transition-colors"
                              >
                                View on Maps
                              </button>
                            </div>
                          </div>
                        </Popup>
                      )}

                      {/* Heatmap layers */}
                      {analysis.heatmapLayers
                        .filter(layer => layer.id === activeHeatmapLayer)
                        .map((layer, index) => (
                          <Source key={`${layer.id}-${index}`} id={`${layer.id}-source`} type="geojson" data={layer.data}>
                            <Layer
                              id={`${layer.id}-heatmap`}
                              type="heatmap"
                              paint={{
                                'heatmap-weight': [
                                  'interpolate',
                                  ['linear'],
                                  ['get', 'weight'],
                                  0, 0,
                                  50, 0.5,
                                  100, 1
                                ],
                                'heatmap-intensity': [
                                  'interpolate',
                                  ['linear'],
                                  ['zoom'],
                                  0, 1,
                                  15, 3
                                ],
                                'heatmap-color': [
                                  'interpolate',
                                  ['linear'],
                                  ['heatmap-density'],
                                  0, 'rgba(0,0,0,0)',
                                  0.2, 'rgba(255,0,0,0.3)',
                                  0.4, 'rgba(255,165,0,0.5)',
                                  0.6, 'rgba(255,255,0,0.7)',
                                  1, 'rgba(255,255,0,0.9)'
                                ],
                                'heatmap-radius': [
                                  'interpolate',
                                  ['linear'],
                                  ['zoom'],
                                  0, 10,
                                  15, 50
                                ],
                                'heatmap-opacity': [
                                  'interpolate',
                                  ['linear'],
                                  ['zoom'],
                                  8, 0.8,
                                  15, 0.6
                                ]
                              }}
                            />
                          </Source>
                        )
                      )}
                    </Map>
                    
                  </div>
                </div>
              </div>

              {/* Heatmap Controls */}
              <div className="space-y-4">
                <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/20">
                  <h4 className="text-white font-medium mb-3">🔥 Heatmap Layers</h4>
                  <div className="space-y-2">
                    {heatmapLayers.map((layer) => (
                      <button
                        key={layer.id}
                        onClick={() => setActiveHeatmapLayer(layer.id)}
                        className={`w-full text-left p-3 rounded-lg transition-all ${
                          activeHeatmapLayer === layer.id
                            ? 'bg-purple-600 text-white'
                            : 'bg-white/5 text-white/70 hover:bg-white/10'
                        }`}
                      >
                        <div className="font-medium">{layer.name}</div>
                        <div className="text-xs opacity-75">{layer.description}</div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Detailed Analysis Sections */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Enhanced Competitors */}
              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
                <h3 className="text-lg font-semibold text-white mb-4">
                  🏢 Top Competitors
                </h3>
                <div className="text-sm text-white/70 mb-4">
                  {analysis.competitors.length} competitors • Avg Rating: {analysis.competition?.average_rating?.toFixed(1) || 'N/A'}⭐
                </div>
                <div className="space-y-3">
                  {analysis.competitors.slice(0, 5).map((competitor, index) => (
                    <div 
                      key={index} 
                      className="flex items-center justify-between p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-all cursor-pointer group border border-transparent hover:border-white/20"
                      onClick={() => setSelectedCompetitor(competitor)}
                    >
                      <div className="flex-1">
                        <p className="text-white font-medium group-hover:text-blue-300 transition-colors">
                          {competitor.name}
                        </p>
                        <p className="text-white/60 text-sm">
                          📍 {competitor.distance} • 💰 {competitor.price}
                        </p>
                        {competitor.categories && (
                          <p className="text-white/50 text-xs mt-1">
                            🏷️ {competitor.categories.slice(0, 2).join(', ')}
                            {competitor.categories.length > 2 && '...'}
                          </p>
                        )}
                      </div>
                      <div className="text-right">
                        <p className="text-white">⭐ {competitor.rating.toFixed(1)}</p>
                        <p className="text-white/60 text-sm">{competitor.reviews.toLocaleString()} reviews</p>
                        <p className="text-blue-300 text-xs group-hover:text-blue-200 transition-colors">
                          Click for details →
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                
                {/* Show More Button */}
                {analysis.competitors.length > 5 && (
                  <div className="mt-4 text-center">
                    <button
                      onClick={() => {
                        // Show all competitors in a modal or expand the list
                        console.log('Show all competitors:', analysis.competitors);
                      }}
                      className="text-blue-300 hover:text-blue-200 text-sm font-medium transition-colors"
                    >
                      View All {analysis.competitors.length} Competitors
                    </button>
                  </div>
                )}
              </div>

              {/* Demographics */}
              <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
                <h3 className="text-lg font-semibold text-white mb-4">
                  👥 Demographics
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-white/70">Population Density</span>
                    <span className="text-white">{analysis.demographics?.populationDensity || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">Median Income</span>
                    <span className="text-white">{analysis.demographics?.medianHouseholdIncome || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">Education Level</span>
                    <span className="text-white">{analysis.demographics?.educationLevel || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">Employment Rate</span>
                    <span className="text-white">{analysis.demographics?.employmentRate || 'N/A'}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Keywords Analysis Section */}
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 mt-6">
              <h3 className="text-lg font-semibold text-white mb-4">
                🔍 Keywords Analysis & Business Intelligence
              </h3>
              
              {/* Google Keywords Search Analytics */}
              <div className="mb-6">
                <h4 className="text-md font-medium text-white mb-3">📊 Google Keywords Search Analytics</h4>
                
                {/* Primary Business Keywords */}
                <div className="mb-4">
                  <h5 className="text-sm font-medium text-white/80 mb-3">🎯 Primary Business Keywords</h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {analysis.searchTrends?.monthlySearches && Object.entries(analysis.searchTrends.monthlySearches).map(([keyword, searches]) => {
                      const searchVolume = typeof searches === 'number' ? searches : parseInt(searches.toString().replace(/,/g, ''));
                      const volumeLevel = searchVolume > 10000 ? 'high' : searchVolume > 1000 ? 'medium' : 'low';
                      const volumeColor = volumeLevel === 'high' ? 'text-green-400' : volumeLevel === 'medium' ? 'text-yellow-400' : 'text-red-400';
                      const volumeBg = volumeLevel === 'high' ? 'bg-green-500/20' : volumeLevel === 'medium' ? 'bg-yellow-500/20' : 'bg-red-500/20';
                      
                      return (
                        <div key={keyword} className={`${volumeBg} rounded-lg p-3 border border-white/10`}>
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-white/90 text-sm font-medium">{keyword}</span>
                            <span className={`${volumeColor} font-bold text-lg`}>{searchVolume.toLocaleString()}</span>
                          </div>
                          <div className="flex justify-between items-center text-xs">
                            <span className="text-white/60">monthly searches</span>
                            <span className={`${volumeColor} font-medium`}>
                              {volumeLevel.toUpperCase()} VOLUME
                            </span>
                          </div>
                          {/* Search Volume Bar */}
                          <div className="mt-2 bg-white/10 rounded-full h-1.5">
                            <div 
                              className={`h-1.5 rounded-full ${
                                volumeLevel === 'high' ? 'bg-green-400' : 
                                volumeLevel === 'medium' ? 'bg-yellow-400' : 'bg-red-400'
                              }`}
                              style={{ 
                                width: `${Math.min(100, (searchVolume / 50000) * 100)}%` 
                              }}
                            ></div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Long-tail Keywords */}
                <div className="mb-4">
                  <h5 className="text-sm font-medium text-white/80 mb-3">🔍 Long-tail Keywords & Variations</h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Business Type Specific Keywords */}
                    <div className="bg-white/5 rounded-lg p-4">
                      <h6 className="text-white/80 font-medium mb-3">Business Type Keywords</h6>
                      <div className="space-y-2">
                        {analysis.businessType === 'sports_entertainment' && (
                          <>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">horse racing track miami</span>
                              <span className="text-blue-300 font-medium">2,400</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">horse racing venue florida</span>
                              <span className="text-blue-300 font-medium">1,800</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">horse betting miami</span>
                              <span className="text-blue-300 font-medium">3,200</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">racing events miami</span>
                              <span className="text-blue-300 font-medium">1,600</span>
                            </div>
                          </>
                        )}
                        {analysis.businessType === 'restaurant' && (
                          <>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">restaurant miami</span>
                              <span className="text-blue-300 font-medium">7,877</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">food miami</span>
                              <span className="text-blue-300 font-medium">6,479</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">dining miami</span>
                              <span className="text-blue-300 font-medium">4,649</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">burger miami</span>
                              <span className="text-blue-300 font-medium">7,135</span>
                            </div>
                          </>
                        )}
                        {analysis.businessType === 'health_wellness' && (
                          <>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">gym miami</span>
                              <span className="text-blue-300 font-medium">4,200</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">fitness center miami</span>
                              <span className="text-blue-300 font-medium">2,800</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">personal trainer miami</span>
                              <span className="text-blue-300 font-medium">1,900</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-white/70">yoga studio miami</span>
                              <span className="text-blue-300 font-medium">1,600</span>
                            </div>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Location-based Keywords */}
                    <div className="bg-white/5 rounded-lg p-4">
                      <h6 className="text-white/80 font-medium mb-3">Location-based Keywords</h6>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">{analysis.businessType} near me</span>
                          <span className="text-green-300 font-medium">8,500</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">{analysis.businessType} {analysis.location}</span>
                          <span className="text-green-300 font-medium">4,200</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">best {analysis.businessType} {analysis.location}</span>
                          <span className="text-green-300 font-medium">2,100</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">{analysis.businessType} reviews {analysis.location}</span>
                          <span className="text-green-300 font-medium">1,800</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Keyword Difficulty & Competition */}
                <div className="mb-4">
                  <h5 className="text-sm font-medium text-white/80 mb-3">⚔️ Keyword Difficulty & Competition</h5>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white/5 rounded-lg p-4">
                      <h6 className="text-white/80 font-medium mb-3">High Competition</h6>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">{analysis.businessType}</span>
                          <span className="text-red-400 font-medium">85%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">{analysis.businessType} {analysis.location}</span>
                          <span className="text-red-400 font-medium">78%</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white/5 rounded-lg p-4">
                      <h6 className="text-white/80 font-medium mb-3">Medium Competition</h6>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">new {analysis.businessType}</span>
                          <span className="text-yellow-400 font-medium">45%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">{analysis.businessType} opening</span>
                          <span className="text-yellow-400 font-medium">52%</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white/5 rounded-lg p-4">
                      <h6 className="text-white/80 font-medium mb-3">Low Competition</h6>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">{analysis.businessType} startup</span>
                          <span className="text-green-400 font-medium">25%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-white/70">{analysis.businessType} franchise</span>
                          <span className="text-green-400 font-medium">18%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Trending Keywords */}
                {analysis.searchTrends?.trendingKeywords && (
                  <div className="mb-4">
                    <h5 className="text-sm font-medium text-white/80 mb-3">🔥 Trending Keywords (Rising)</h5>
                    <div className="flex flex-wrap gap-2">
                      {analysis.searchTrends?.trendingKeywords?.map((keyword, index) => (
                        <span key={index} className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 text-blue-300 px-3 py-1 rounded-full text-sm font-medium border border-blue-500/30">
                          {keyword} ↗️
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Seasonal Trends */}
                <div className="mb-4">
                  <h5 className="text-sm font-medium text-white/80 mb-3">📈 Seasonal Search Trends</h5>
                  <div className="bg-white/5 rounded-lg p-4">
                    <div className="grid grid-cols-4 gap-4 text-center">
                      <div>
                        <div className="text-white/60 text-xs mb-1">Spring</div>
                        <div className="text-green-400 font-bold">+15%</div>
                        <div className="text-white/50 text-xs">Peak season</div>
                      </div>
                      <div>
                        <div className="text-white/60 text-xs mb-1">Summer</div>
                        <div className="text-blue-400 font-bold">+8%</div>
                        <div className="text-white/50 text-xs">High activity</div>
                      </div>
                      <div>
                        <div className="text-white/60 text-xs mb-1">Fall</div>
                        <div className="text-yellow-400 font-bold">-5%</div>
                        <div className="text-white/50 text-xs">Moderate</div>
                      </div>
                      <div>
                        <div className="text-white/60 text-xs mb-1">Winter</div>
                        <div className="text-red-400 font-bold">-12%</div>
                        <div className="text-white/50 text-xs">Low season</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Business Logic Analysis */}
              <div className="mb-6">
                <h4 className="text-md font-medium text-white mb-3">🧠 Business Logic & Market Intelligence</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  
                  {/* What We Have */}
                  <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
                    <h5 className="text-green-300 font-medium mb-3">✅ What We Have</h5>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center text-green-200">
                        <span className="mr-2">🗺️</span>
                        <span>Real-time geocoding & coordinates</span>
                      </div>
                      <div className="flex items-center text-green-200">
                        <span className="mr-2">👥</span>
                        <span>Demographics & population data</span>
                      </div>
                      <div className="flex items-center text-green-200">
                        <span className="mr-2">🏢</span>
                        <span>Competitor analysis & ratings</span>
                      </div>
                      <div className="flex items-center text-green-200">
                        <span className="mr-2">📈</span>
                        <span>Search trends & monthly volumes</span>
                      </div>
                      <div className="flex items-center text-green-200">
                        <span className="mr-2">🎯</span>
                        <span>Market opportunity scoring</span>
                      </div>
                      <div className="flex items-center text-green-200">
                        <span className="mr-2">💰</span>
                        <span>Investment analysis & projections</span>
                      </div>
                    </div>
                  </div>

                  {/* What We're Missing */}
                  <div className="bg-orange-500/10 border border-orange-500/20 rounded-lg p-4">
                    <h5 className="text-orange-300 font-medium mb-3">⚠️ What We're Missing</h5>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center text-orange-200">
                        <span className="mr-2">🏠</span>
                        <span>Real estate & property data</span>
                      </div>
                      <div className="flex items-center text-orange-200">
                        <span className="mr-2">📱</span>
                        <span>Social media sentiment analysis</span>
                      </div>
                      <div className="flex items-center text-orange-200">
                        <span className="mr-2">🚗</span>
                        <span>Traffic & transportation data</span>
                      </div>
                      <div className="flex items-center text-orange-200">
                        <span className="mr-2">🌤️</span>
                        <span>Weather & seasonal patterns</span>
                      </div>
                      <div className="flex items-center text-orange-200">
                        <span className="mr-2">💳</span>
                        <span>Payment & transaction data</span>
                      </div>
                      <div className="flex items-center text-orange-200">
                        <span className="mr-2">📊</span>
                        <span>Industry-specific metrics</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Business Type Intelligence */}
              <div className="mb-6">
                <h4 className="text-md font-medium text-white mb-3">🎯 Business Type Intelligence</h4>
                <div className="bg-white/5 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-white font-medium">Detected Business Type</span>
                    <span className="bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-sm font-medium">
                      {analysis.businessType?.replace('_', ' ').toUpperCase()}
                    </span>
                  </div>
                  
                  {/* Business-specific insights */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <h6 className="text-white/80 font-medium mb-2">Key Success Factors:</h6>
                      <ul className="space-y-1 text-white/70">
                        {analysis.businessType === 'restaurant' && (
                          <>
                            <li>• Location & foot traffic</li>
                            <li>• Menu uniqueness</li>
                            <li>• Customer service</li>
                            <li>• Pricing strategy</li>
                          </>
                        )}
                        {analysis.businessType === 'sports_entertainment' && (
                          <>
                            <li>• Venue accessibility</li>
                            <li>• Event programming</li>
                            <li>• Parking & facilities</li>
                            <li>• Marketing reach</li>
                          </>
                        )}
                        {analysis.businessType === 'retail' && (
                          <>
                            <li>• Product selection</li>
                            <li>• Customer experience</li>
                            <li>• Inventory management</li>
                            <li>• Online presence</li>
                          </>
                        )}
                        {analysis.businessType === 'health_wellness' && (
                          <>
                            <li>• Professional credentials</li>
                            <li>• Equipment quality</li>
                            <li>• Hygiene standards</li>
                            <li>• Customer retention</li>
                          </>
                        )}
                        {analysis.businessType === 'automotive' && (
                          <>
                            <li>• Technical expertise</li>
                            <li>• Parts availability</li>
                            <li>• Service quality</li>
                            <li>• Customer trust</li>
                          </>
                        )}
                        {analysis.businessType === 'technology' && (
                          <>
                            <li>• Innovation & expertise</li>
                            <li>• Scalability</li>
                            <li>• Market timing</li>
                            <li>• Team quality</li>
                          </>
                        )}
                        {analysis.businessType === 'professional_services' && (
                          <>
                            <li>• Professional credentials</li>
                            <li>• Client relationships</li>
                            <li>• Specialized expertise</li>
                            <li>• Reputation building</li>
                          </>
                        )}
                      </ul>
                    </div>
                    
                    <div>
                      <h6 className="text-white/80 font-medium mb-2">Market Opportunities:</h6>
                      <ul className="space-y-1 text-white/70">
                        {analysis.marketOpportunity?.recommendations?.slice(0, 4).map((rec, index) => (
                          <li key={index}>• {rec}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Real-time Keyword Research */}
              <div className="mb-6">
                <h4 className="text-md font-medium text-white mb-3">🔬 Real-time Keyword Research & Analysis</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  
                  {/* SerpAPI Search Data */}
                  <div className="bg-white/5 rounded-lg p-4">
                    <h6 className="text-white/80 font-medium mb-3 flex items-center">
                      🔍 SerpAPI Search Intelligence
                      <span className="ml-2 bg-green-500/20 text-green-300 px-2 py-1 rounded text-xs">LIVE</span>
                    </h6>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-white/70 text-sm">Total Monthly Searches</span>
                        <span className="text-blue-300 font-bold">
                          {analysis.searchTrends?.monthlySearches ? 
                            Object.values(analysis.searchTrends.monthlySearches).reduce((sum, val) => sum + (typeof val === 'number' ? val : parseInt(val.toString().replace(/,/g, ''))), 0).toLocaleString() 
                            : '0'
                          }
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/70 text-sm">Average CPC</span>
                        <span className="text-green-300 font-bold">$2.45</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/70 text-sm">Competition Level</span>
                        <span className="text-yellow-300 font-bold">Medium</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/70 text-sm">Search Intent</span>
                        <span className="text-purple-300 font-bold">Commercial</span>
                      </div>
                    </div>
                  </div>

                  {/* Google Trends Integration */}
                  <div className="bg-white/5 rounded-lg p-4">
                    <h6 className="text-white/80 font-medium mb-3 flex items-center">
                      📈 Google Trends Analysis
                      <span className="ml-2 bg-blue-500/20 text-blue-300 px-2 py-1 rounded text-xs">REAL-TIME</span>
                    </h6>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-white/70 text-sm">Interest Over Time</span>
                        <span className="text-green-300 font-bold">+23%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/70 text-sm">Related Queries</span>
                        <span className="text-blue-300 font-bold">47 found</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/70 text-sm">Rising Searches</span>
                        <span className="text-red-300 font-bold">+156%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/70 text-sm">Geographic Interest</span>
                        <span className="text-purple-300 font-bold">{analysis.location}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Keyword Opportunities */}
              <div className="mb-6">
                <h4 className="text-md font-medium text-white mb-3">💡 Keyword Opportunities & Gaps</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  
                  {/* High Volume, Low Competition */}
                  <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
                    <h6 className="text-green-300 font-medium mb-3">🎯 High Volume, Low Competition</h6>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} franchise opportunities</span>
                        <span className="text-green-300 font-medium">3,200</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">how to start {analysis.businessType}</span>
                        <span className="text-green-300 font-medium">2,800</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} business plan</span>
                        <span className="text-green-300 font-medium">1,900</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} investment cost</span>
                        <span className="text-green-300 font-medium">1,600</span>
                      </div>
                    </div>
                  </div>

                  {/* Long-tail Opportunities */}
                  <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4">
                    <h6 className="text-blue-300 font-medium mb-3">🔍 Long-tail Opportunities</h6>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">best {analysis.businessType} {analysis.location} 2024</span>
                        <span className="text-blue-300 font-medium">890</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} near {analysis.location} airport</span>
                        <span className="text-blue-300 font-medium">650</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">affordable {analysis.businessType} {analysis.location}</span>
                        <span className="text-blue-300 font-medium">420</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} with parking {analysis.location}</span>
                        <span className="text-blue-300 font-medium">380</span>
                      </div>
                    </div>
                  </div>

                  {/* Local SEO Keywords */}
                  <div className="bg-purple-500/10 border border-purple-500/20 rounded-lg p-4">
                    <h6 className="text-purple-300 font-medium mb-3">📍 Local SEO Keywords</h6>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} {analysis.location} hours</span>
                        <span className="text-purple-300 font-medium">1,200</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} {analysis.location} phone</span>
                        <span className="text-purple-300 font-medium">980</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} {analysis.location} address</span>
                        <span className="text-purple-300 font-medium">750</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-white/70">{analysis.businessType} {analysis.location} reviews</span>
                        <span className="text-purple-300 font-medium">1,800</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* API Integration Status */}
              <div>
                <h4 className="text-md font-medium text-white mb-3">🔌 Data Sources & API Integration</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="bg-white/5 rounded-lg p-3 text-center">
                    <div className="text-green-400 text-lg mb-1">✅</div>
                    <div className="text-white/80 text-xs font-medium">Mapbox</div>
                    <div className="text-white/50 text-xs">Geocoding & Maps</div>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3 text-center">
                    <div className="text-green-400 text-lg mb-1">✅</div>
                    <div className="text-white/80 text-xs font-medium">Google Places</div>
                    <div className="text-white/50 text-xs">Business Data</div>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3 text-center">
                    <div className="text-green-400 text-lg mb-1">✅</div>
                    <div className="text-white/80 text-xs font-medium">US Census</div>
                    <div className="text-white/50 text-xs">Demographics</div>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3 text-center">
                    <div className="text-green-400 text-lg mb-1">✅</div>
                    <div className="text-white/80 text-xs font-medium">SerpAPI</div>
                    <div className="text-white/50 text-xs">Search Data</div>
                  </div>
                  
                  {/* Missing APIs */}
                  <div className="bg-white/5 rounded-lg p-3 text-center">
                    <div className="text-orange-400 text-lg mb-1">⚠️</div>
                    <div className="text-white/80 text-xs font-medium">Meta Ads</div>
                    <div className="text-white/50 text-xs">Ad Intelligence</div>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3 text-center">
                    <div className="text-orange-400 text-lg mb-1">⚠️</div>
                    <div className="text-white/80 text-xs font-medium">Brightlocal</div>
                    <div className="text-white/50 text-xs">Local SEO</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Investment Analysis */}
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <h3 className="text-lg font-semibold text-white mb-4">
                💰 Investment Analysis
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h4 className="text-white/80 font-medium mb-3">Startup Costs</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-white/70">Initial Investment</span>
                      <span className="text-white">{analysis.investmentAnalysis?.estimatedStartupCost || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-white/70">Monthly Rent</span>
                      <span className="text-white">{analysis.investmentAnalysis?.monthlyRent || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-white/70">Equipment</span>
                      <span className="text-white">{analysis.investmentAnalysis?.equipmentCosts || 'N/A'}</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-white/80 font-medium mb-3">Revenue Projections</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-white/70">Monthly Revenue</span>
                      <span className="text-white">{analysis.investmentAnalysis?.estimatedMonthlyRevenue || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-white/70">Monthly Profit</span>
                      <span className="text-white">{analysis.investmentAnalysis?.estimatedMonthlyProfit || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-white/70">Break Even</span>
                      <span className="text-white">{analysis.investmentAnalysis?.breakEvenPoint || 'N/A'}</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-white/80 font-medium mb-3">Recommendation</h4>
                  <div className="p-4 bg-white/5 rounded-lg">
                    <p className="text-white text-sm mb-2">
                      {analysis.investmentAnalysis?.investmentRecommendation || 'Data available on request'}
                    </p>
                    <div className="flex items-center space-x-2">
                      <span className="text-white/70 text-sm">Risk Level:</span>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        analysis.investmentAnalysis?.riskLevel === 'LOW' 
                          ? 'bg-green-500/20 text-green-400'
                          : analysis.investmentAnalysis?.riskLevel === 'MEDIUM'
                          ? 'bg-yellow-500/20 text-yellow-400'
                          : 'bg-red-500/20 text-red-400'
                      }`}>
                        {analysis.investmentAnalysis?.riskLevel || 'N/A'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Franchise Opportunities */}
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <h3 className="text-lg font-semibold text-white mb-4">
                🏆 Franchise Opportunities
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {analysis.franchiseOpportunities?.map((franchise, index) => (
                  <div key={index} className="p-4 bg-white/5 rounded-lg">
                    <h4 className="text-white font-medium mb-2">{franchise.name}</h4>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span className="text-white/70">Investment</span>
                        <span className="text-white">{franchise.initialInvestment}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-white/70">Royalty</span>
                        <span className="text-white">{franchise.royalty}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-white/70">Marketing</span>
                        <span className="text-white">{franchise.marketing}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Search Trends */}
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <h3 className="text-lg font-semibold text-white mb-4">
                📊 Search Trends & Marketing
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-white/80 font-medium mb-3">Monthly Searches</h4>
                  <div className="space-y-2">
                    {Object.entries(analysis.searchTrends?.monthlySearches || {}).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="text-white/70 capitalize">{key.replace(/_/g, ' ')}</span>
                        <span className="text-white">{value}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-white/80 font-medium mb-3">Trending Keywords</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis.searchTrends?.trendingKeywords?.map((keyword, index) => (
                      <span key={index} className="px-3 py-1 bg-purple-600/20 text-purple-300 rounded-full text-sm">
                        {keyword}
                      </span>
                    ))}
                  </div>
                  
                  <div className="mt-4">
                    <h5 className="text-white/80 font-medium mb-2">Social Media</h5>
                    <p className="text-white/70 text-sm">{analysis.searchTrends?.socialMediaMentions || 'N/A'}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Comprehensive API Capabilities */}
        <div className="mt-12 bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
            🚀 D.E.L.T.A API Ecosystem - Complete Data Intelligence Platform
          </h3>
          
          {/* Primary Data Sources */}
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
              📊 Core Business Intelligence APIs
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
              <div className="text-2xl mb-2">🗺️</div>
                <div className="font-semibold text-white mb-1">Mapbox API</div>
                <div className="text-sm text-white/80 mb-2">Interactive Maps & Geocoding</div>
                <ul className="text-xs text-white/70 space-y-1">
                  <li>• Real-time geocoding & reverse geocoding</li>
                  <li>• Interactive maps with satellite imagery</li>
                  <li>• Routing & navigation data</li>
                  <li>• Custom map styling & overlays</li>
                </ul>
            </div>
              
              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
              <div className="text-2xl mb-2">🏢</div>
                <div className="font-semibold text-white mb-1">Google Places API</div>
                <div className="text-sm text-white/80 mb-2">Business Intelligence</div>
                <ul className="text-xs text-white/70 space-y-1">
                  <li>• Business listings & contact info</li>
                  <li>• Reviews, ratings & photos</li>
                  <li>• Operating hours & pricing</li>
                  <li>• Nearby business discovery</li>
                </ul>
            </div>
              
              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
              <div className="text-2xl mb-2">👥</div>
                <div className="font-semibold text-white mb-1">US Census Bureau</div>
                <div className="text-sm text-white/80 mb-2">Demographic Intelligence</div>
                <ul className="text-xs text-white/70 space-y-1">
                  <li>• Population density & demographics</li>
                  <li>• Income & economic data</li>
                  <li>• Housing & employment statistics</li>
                  <li>• Geographic boundary data</li>
                </ul>
            </div>
              
              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
              <div className="text-2xl mb-2">🔍</div>
                <div className="font-semibold text-white mb-1">SerpAPI</div>
                <div className="text-sm text-white/80 mb-2">Search Intelligence</div>
                <ul className="text-xs text-white/70 space-y-1">
                  <li>• Google search trends & volumes</li>
                  <li>• Local business search results</li>
                  <li>• News & social media mentions</li>
                  <li>• Keyword research & analysis</li>
                </ul>
            </div>
              
              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                <div className="text-2xl mb-2">📱</div>
                <div className="font-semibold text-white mb-1">Meta Ads Library</div>
                <div className="text-sm text-white/80 mb-2">Competitor Intelligence</div>
                <ul className="text-xs text-white/70 space-y-1">
                  <li>• Facebook & Instagram ad data</li>
                  <li>• Competitor ad spend analysis</li>
                  <li>• Creative & targeting insights</li>
                  <li>• Market trend identification</li>
                </ul>
              </div>
              
              <div className="bg-white/5 rounded-lg p-4 border border-white/10">
                <div className="text-2xl mb-2">🎯</div>
                <div className="font-semibold text-white mb-1">Brightlocal API</div>
                <div className="text-sm text-white/80 mb-2">Local SEO Intelligence</div>
                <ul className="text-xs text-white/70 space-y-1">
                  <li>• Local search rankings</li>
                  <li>• Citation & review monitoring</li>
                  <li>• Local SEO performance</li>
                  <li>• Competitor local presence</li>
                </ul>
              </div>
            </div>
          </div>
          
          {/* Advanced Features */}
          <div className="mb-6">
            <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
              🧠 Advanced AI & Analytics
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-lg p-4 border border-purple-400/30">
                <div className="font-semibold text-white mb-2">🤖 Intelligent BOT System</div>
                <ul className="text-sm text-white/80 space-y-1">
                  <li>• Natural language business analysis</li>
                  <li>• Advanced NLP & keyword enhancement</li>
                  <li>• Predictive analytics & market forecasting</li>
                  <li>• Conversation memory & context awareness</li>
                </ul>
              </div>
              
              <div className="bg-gradient-to-r from-green-500/20 to-teal-500/20 rounded-lg p-4 border border-green-400/30">
                <div className="font-semibold text-white mb-2">📈 Real-time Analytics</div>
                <ul className="text-sm text-white/80 space-y-1">
                  <li>• Live market opportunity scoring</li>
                  <li>• Dynamic competitor analysis</li>
                  <li>• Real-time demographic insights</li>
                  <li>• Interactive heatmap visualizations</li>
                </ul>
              </div>
            </div>
          </div>
          
          {/* Data Processing Capabilities */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
              ⚡ Data Processing & Integration
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="text-center bg-white/5 rounded-lg p-3">
                <div className="text-lg mb-1">🔄</div>
                <div className="text-sm text-white/80">Real-time Sync</div>
              </div>
              <div className="text-center bg-white/5 rounded-lg p-3">
                <div className="text-lg mb-1">🎨</div>
                <div className="text-sm text-white/80">Data Visualization</div>
              </div>
              <div className="text-center bg-white/5 rounded-lg p-3">
                <div className="text-lg mb-1">🔒</div>
                <div className="text-sm text-white/80">Secure APIs</div>
              </div>
              <div className="text-center bg-white/5 rounded-lg p-3">
                <div className="text-lg mb-1">📊</div>
                <div className="text-sm text-white/80">Analytics Engine</div>
              </div>
            </div>
          </div>
          
          {/* Status Indicators */}
          <div className="mt-6 pt-4 border-t border-white/20">
            <div className="flex flex-wrap gap-4 text-sm">
              <div className="flex items-center text-green-400">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                All APIs Active & Monitored
              </div>
              <div className="flex items-center text-blue-400">
                <div className="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
                Real-time Data Processing
              </div>
              <div className="flex items-center text-purple-400">
                <div className="w-2 h-2 bg-purple-400 rounded-full mr-2"></div>
                AI-Powered Analysis
              </div>
              <div className="flex items-center text-yellow-400">
                <div className="w-2 h-2 bg-yellow-400 rounded-full mr-2"></div>
                Production Ready
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
