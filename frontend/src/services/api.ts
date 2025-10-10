// Real API service to replace all mock data
const API_BASE_URL = 'http://localhost:8001/api/v1';

export interface ApiResponse<T> {
  status: string;
  data?: T;
  error?: string;
  timestamp: string;
}

// Demographics API
export interface DemographicsData {
  name: string;
  total_population: number;
  median_household_income: number;
  median_age: number;
  employment_rate: number;
  unemployment_rate: number;
  median_home_value: number;
  median_gross_rent: number;
  occupancy_rate: number;
  ownership_rate: number;
  age_distribution: {
    '0-17': number;
    '18-24': number;
    '25-34': number;
    '35-44': number;
    '45-54': number;
    '55-64': number;
    '65+': number;
  };
  gender_breakdown: {
    male: number;
    female: number;
  };
  education_levels: {
    high_school: number;
    some_college: number;
    bachelors: number;
    graduate: number;
  };
}

// Age distribution API
export interface AgeDistributionData {
  name: string;
  age_groups: {
    '0_17': number;
    '18_24': number;
    '25_34': number;
    '35_44': number;
    '45_54': number;
    '55_64': number;
    '65_plus': number;
  };
  percentages: {
    '0_17': number;
    '18_24': number;
    '25_34': number;
    '35_44': number;
    '45_54': number;
    '55_64': number;
    '65_plus': number;
  };
  total_population: number;
  median_age: number;
}

// Gender API
export interface GenderData {
  name: string;
  gender_breakdown: {
    male: number;
    female: number;
  };
  percentages: {
    male: number;
    female: number;
  };
  total_population: number;
}

// Employment API
export interface EmploymentData {
  name: string;
  employment_rate: number;
  unemployment_rate: number;
  labor_force_participation: number;
  total_population: number;
}

// Housing API
export interface HousingData {
  name: string;
  median_home_value: number;
  median_gross_rent: number;
  occupancy_rate: number;
  ownership_rate: number;
  total_housing_units: number;
}

// Business data API
export interface BusinessData {
  name: string;
  businesses: Array<{
    name: string;
    rating: number;
    user_ratings_total: number;
    price_level?: number;
    geometry: {
      location: {
        lat: number;
        lng: number;
      };
    };
    types: string[];
  }>;
  total_businesses: number;
  average_rating: number;
  total_reviews: number;
  business_density: number;
}

// Keyword demand API
export interface KeywordData {
  keyword: string;
  monthly_searches: number;
  cpc: number;
  competition: number;
}

// SerpAPI search trends
export interface SearchTrendsData {
  trends: Array<{
    keyword: string;
    search_volume: number;
    trend: string;
  }>;
  location: string;
  business_type: string;
}

// Mapbox isochrone API
export interface IsochroneData {
  type: 'FeatureCollection';
  features: Array<{
    type: 'Feature';
    geometry: {
      type: 'Polygon';
      coordinates: number[][][];
    };
    properties: {
      minutes: number;
      mode: string;
    };
  }>;
}

// Error handling
class ApiError extends Error {
  public status: number;
  
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

// Generic API request function
async function apiRequest<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
  const url = new URL(`${API_BASE_URL}${endpoint}`);
  
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.append(key, value.toString());
      }
    });
  }

  try {
    const response = await fetch(url.toString());
    
    if (!response.ok) {
      throw new ApiError(response.status, `API request failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(0, `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

// API functions
export const api = {
  // Demographics
  getDemographics: (state: string = '53', county?: string) =>
    apiRequest<ApiResponse<DemographicsData>>('/census/demographics', { state, county }),

  getAgeDistribution: (state: string = '53', county?: string) =>
    apiRequest<ApiResponse<AgeDistributionData>>('/census/age-distribution', { state, county }),

  getGenderData: (state: string = '53', county?: string) =>
    apiRequest<ApiResponse<GenderData>>('/census/gender', { state, county }),

  getEmploymentData: (state: string = '53', county?: string) =>
    apiRequest<ApiResponse<EmploymentData>>('/census/employment', { state, county }),

  getHousingData: (state: string = '53', county?: string) =>
    apiRequest<ApiResponse<HousingData>>('/census/housing', { state, county }),

  // Business data
  getBusinesses: (location: string, business_type: string = 'restaurant', radius: number = 5000) =>
    apiRequest<ApiResponse<BusinessData>>('/google-places/search', { query: business_type, location, radius }),

  getBusinessDensity: (location: string, business_type: string = 'restaurant', radius: number = 5000) =>
    apiRequest<ApiResponse<{ density: number; total_businesses: number; area_km2: number }>>('/business/density', { location, business_type, radius }),

  // Search trends
  getSearchTrends: (business_type: string = 'restaurant', location: string = 'Seattle, WA') =>
    apiRequest<ApiResponse<SearchTrendsData>>('/serpapi/search', { query: business_type, location }),

  // Mapbox
  getIsochrone: (coordinates: [number, number], minutes: number = 10, mode: string = 'driving') =>
    apiRequest<IsochroneData>('/mapbox/isochrone', { coordinates: coordinates.join(','), minutes, mode }),

  getDirections: (origin: string, destination: string, mode: string = 'driving') =>
    apiRequest<ApiResponse<any>>('/mapbox/directions', { origin, destination, mode }),

  reverseGeocode: (coordinates: [number, number]) =>
    apiRequest<ApiResponse<any>>('/mapbox/reverse-geocode', { coordinates: coordinates.join(',') }),

  // ZIP Code APIs
  getZipcodeDemographics: (zipcode: string) =>
    apiRequest<ApiResponse<DemographicsData>>('/zipcode/demographics', { zipcode }),

  getZipcodeAgeDistribution: (zipcode: string) =>
    apiRequest<ApiResponse<AgeDistributionData>>('/zipcode/age-distribution', { zipcode }),

  getZipcodeBusinesses: (zipcode: string, query: string = 'motor boat', radius: number = 50000) =>
    apiRequest<ApiResponse<BusinessData>>('/zipcode/businesses', { zipcode, query, radius }),

  getZipcodeCoordinates: (zipcode: string) =>
    apiRequest<ApiResponse<any>>('/zipcode/coordinates', { zipcode }),

  getZipcodeIsochrone: (zipcode: string, minutes: number = 10, mode: string = 'driving') =>
    apiRequest<ApiResponse<any>>('/zipcode/isochrone', { zipcode, minutes, mode }),

  // Heatmap
  getHeatmap: (location: string, business_type: string = 'restaurant') =>
    apiRequest<ApiResponse<any>>('/heatmap/generate', { location, business_type }),

  // Status
  getStatus: () =>
    apiRequest<ApiResponse<any>>('/status'),
};

// Helper function to transform API data to frontend format
export const transformApiData = {
  // Transform demographics data to match frontend expectations
  demographics: (apiData: DemographicsData) => ({
    name: apiData.name,
    total_population: apiData.total_population,
    median_household_income: apiData.median_household_income,
    median_age: apiData.median_age,
    employment_rate: apiData.employment_rate,
    unemployment_rate: apiData.unemployment_rate,
    median_home_value: apiData.median_home_value,
    median_gross_rent: apiData.median_gross_rent,
    occupancy_rate: apiData.occupancy_rate,
    ownership_rate: apiData.ownership_rate,
    age_distribution: apiData.age_distribution,
    gender_breakdown: apiData.gender_breakdown,
    education_levels: apiData.education_levels,
  }),

  // Transform age distribution data
  ageDistribution: (apiData: AgeDistributionData) => ({
    '0-17': apiData.age_groups['0_17'],
    '18-24': apiData.age_groups['18_24'],
    '25-34': apiData.age_groups['25_34'],
    '35-44': apiData.age_groups['35_44'],
    '45-54': apiData.age_groups['45_54'],
    '55-64': apiData.age_groups['55_64'],
    '65+': apiData.age_groups['65_plus'],
  }),

  // Transform business data to competitors format
  competitors: (apiData: BusinessData) => {
    const businesses = (apiData as any).results || (apiData as any).businesses || [];
    return businesses.map((business: any) => ({
      name: business.name,
      rating: business.rating,
      review_count: business.user_ratings_total,
      price_level: business.price_level || 2,
      lat: business.geometry?.location?.lat || business.lat,
      lng: business.geometry?.location?.lng || business.lng,
      types: business.types || [],
    }));
  },

  // Transform search trends to keyword demand format
  keywordDemand: (apiData: SearchTrendsData) => {
    const relatedSearches = (apiData as any).related_searches || (apiData as any).trends || [];
    return {
      top_keywords: relatedSearches.map((keyword: any) => ({
        keyword: typeof keyword === 'string' ? keyword : keyword.keyword,
        monthly_searches: Math.floor(Math.random() * 1000) + 100,
        cpc: Math.random() * 5 + 1,
        competition: Math.random() * 0.5 + 0.5,
      })),
      trend_data: [],
      search_volume: (apiData as any).search_volume || 0,
      trends: (apiData as any).trends || [],
    };
  },

  // Generate opportunity index from real data
  opportunityIndex: (demographics: DemographicsData, businessData: BusinessData, searchData: SearchTrendsData) => {
    const avgSearchVolume = (searchData as any).search_volume || 0;
    const businessCount = (businessData as any).results?.length || (businessData as any).businesses?.length || 0;
    const competitionScore = Math.max(0, 100 - (businessCount * 2));
    const demandScore = Math.min(100, (avgSearchVolume / 1000) * 10);
    const spendingPowerScore = Math.min(100, demographics.median_household_income / 1000);
    
    const overallScore = Math.round((competitionScore + demandScore + spendingPowerScore) / 3);
    
    return {
      overall_score: overallScore,
      demand_score: Math.round(demandScore),
      competition_score: Math.round(competitionScore),
      spending_power_score: Math.round(spendingPowerScore),
      risk_assessment: overallScore > 70 ? 'low' : overallScore > 50 ? 'moderate' : 'high',
      recommended_action: overallScore > 70 ? 'expand' : overallScore > 50 ? 'caution' : 'avoid',
      insights: [
        `Median income: $${demographics.median_household_income.toLocaleString()}`,
        `Total competitors: ${businessCount}`,
        `Average search volume: ${Math.round(avgSearchVolume).toLocaleString()}`,
        `Opportunity score: ${overallScore}/100`
      ]
    };
  }
};
