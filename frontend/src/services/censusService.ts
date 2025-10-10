// Census API service for fetching demographic data by ZIP code
const API_BASE_URL = 'http://localhost:8001/api/v1';
const CENSUS_API_KEY = 'ab4c49e507688c08e5346543c6d355a2e6b37c8c';

export interface ZipCodeDemographics {
  zip_code: string;
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

export interface ZipCodeInfo {
  zip_code: string;
  city: string;
  state: string;
  latitude: number;
  longitude: number;
  distance_km?: number;
}

// Get ZIP code from coordinates using reverse geocoding
export async function getZipCodeFromCoordinates(
  lat: number,
  lng: number
): Promise<string | null> {
  try {
    const MAPBOX_TOKEN = 'pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw';
    const response = await fetch(
      `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?types=postcode&access_token=${MAPBOX_TOKEN}`
    );
    
    if (!response.ok) {
      throw new Error(`Geocoding failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    if (data.features && data.features.length > 0) {
      // Extract ZIP code from the place name
      const zipMatch = data.features[0].text.match(/\d{5}/);
      return zipMatch ? zipMatch[0] : null;
    }
    
    return null;
  } catch (error) {
    console.error('Error getting ZIP code:', error);
    return null;
  }
}

// Get nearby ZIP codes within a radius
export async function getNearbyZipCodes(
  lat: number,
  lng: number,
  radiusKm: number = 10
): Promise<ZipCodeInfo[]> {
  try {
    // Use a simple grid search approach
    const zipCodes: Set<string> = new Set();
    const zipCodeInfos: ZipCodeInfo[] = [];
    
    // Search in a grid pattern
    const steps = 8;
    const latStep = (radiusKm / 111) / steps; // ~111 km per degree latitude
    const lngStep = (radiusKm / (111 * Math.cos(lat * Math.PI / 180))) / steps;
    
    for (let i = -steps; i <= steps; i++) {
      for (let j = -steps; j <= steps; j++) {
        const searchLat = lat + (i * latStep);
        const searchLng = lng + (j * lngStep);
        
        const zipCode = await getZipCodeFromCoordinates(searchLat, searchLng);
        if (zipCode && !zipCodes.has(zipCode)) {
          zipCodes.add(zipCode);
          
          // Calculate distance
          const distance = calculateDistance(lat, lng, searchLat, searchLng);
          
          zipCodeInfos.push({
            zip_code: zipCode,
            city: '',
            state: '',
            latitude: searchLat,
            longitude: searchLng,
            distance_km: distance,
          });
        }
      }
    }
    
    return zipCodeInfos.sort((a, b) => (a.distance_km || 0) - (b.distance_km || 0));
  } catch (error) {
    console.error('Error getting nearby ZIP codes:', error);
    return [];
  }
}

// Calculate distance between two points using Haversine formula
function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371; // Radius of the Earth in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

// Fetch demographics data for a ZIP code
export async function getZipCodeDemographics(
  zipCode: string
): Promise<ZipCodeDemographics | null> {
  try {
    // Try backend API first
    try {
      const response = await fetch(
        `${API_BASE_URL}/census/demographics?zip_code=${zipCode}`
      );
      
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'success' && data.data) {
          return data.data;
        }
      }
    } catch (backendError) {
      console.log('Backend API not available, using Census API directly');
    }
    
    // Fallback to direct Census API call
    const url = 'https://api.census.gov/data/2021/acs/acs5';
    const params = new URLSearchParams({
      get: 'NAME,B01001_001E,B01001_002E,B01001_026E,B19013_001E,B08301_001E,B08301_002E,B08301_010E,B15003_001E,B15003_022E,B15003_023E,B15003_024E,B15003_025E,B25077_001E,B25064_001E',
      for: `zip code tabulation area:${zipCode}`,
      key: CENSUS_API_KEY,
    });
    
    const response = await fetch(`${url}?${params.toString()}`);
    
    if (!response.ok) {
      throw new Error(`Census API failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (data.length > 1) {
      const row = data[1];
      const totalPop = parseInt(row[1]) || 0;
      const males = parseInt(row[2]) || 0;
      const females = parseInt(row[3]) || 0;
      const medianIncome = parseInt(row[4]) || 0;
      const educationTotal = parseInt(row[8]) || 0;
      const bachelors = parseInt(row[9]) || 0;
      const masters = parseInt(row[10]) || 0;
      const professional = parseInt(row[11]) || 0;
      const doctorate = parseInt(row[12]) || 0;
      const medianHomeValue = parseInt(row[13]) || 0;
      const medianRent = parseInt(row[14]) || 0;
      
      return {
        zip_code: zipCode,
        name: row[0] || `ZIP ${zipCode}`,
        total_population: totalPop,
        median_household_income: medianIncome,
        median_age: 35, // Default value
        employment_rate: 0.95,
        unemployment_rate: 0.05,
        median_home_value: medianHomeValue,
        median_gross_rent: medianRent,
        occupancy_rate: 0.92,
        ownership_rate: 0.65,
        age_distribution: {
          '0-17': 0.22,
          '18-24': 0.10,
          '25-34': 0.14,
          '35-44': 0.13,
          '45-54': 0.13,
          '55-64': 0.13,
          '65+': 0.15,
        },
        gender_breakdown: {
          male: males / totalPop,
          female: females / totalPop,
        },
        education_levels: {
          high_school: 0.25,
          some_college: 0.30,
          bachelors: bachelors / educationTotal,
          graduate: (masters + professional + doctorate) / educationTotal,
        },
      };
    }
    
    return null;
  } catch (error) {
    console.error(`Error fetching demographics for ZIP ${zipCode}:`, error);
    return null;
  }
}

// Fetch demographics for multiple ZIP codes
export async function getMultipleZipCodeDemographics(
  zipCodes: string[]
): Promise<Record<string, ZipCodeDemographics | null>> {
  const results: Record<string, ZipCodeDemographics | null> = {};
  
  // Fetch in batches to avoid rate limiting
  const batchSize = 5;
  for (let i = 0; i < zipCodes.length; i += batchSize) {
    const batch = zipCodes.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map(async (zipCode) => ({
        zipCode,
        data: await getZipCodeDemographics(zipCode),
      }))
    );
    
    batchResults.forEach(({ zipCode, data }) => {
      results[zipCode] = data;
    });
    
    // Small delay between batches
    if (i + batchSize < zipCodes.length) {
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  }
  
  return results;
}