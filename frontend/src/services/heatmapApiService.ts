// Heatmap API service for fetching different heatmap data types
const API_BASE_URL = 'http://localhost:8001/api/v1';

export interface HeatmapFeature {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: [number, number];
  };
  properties: {
    weight: number;
    [key: string]: any;
  };
}

export interface HeatmapResponse {
  type: 'FeatureCollection';
  features: HeatmapFeature[];
  layer_id: string;
  total_points: number;
  scoring_method: string;
}

export type HeatmapDataType = 
  | 'population'
  | 'business_competition'
  | 'demographic_density'
  | 'foot_traffic'
  | 'market_opportunity'
  | 'income_wealth'
  | 'review_power';

// Fetch heatmap data based on type
export async function fetchHeatmapData(
  dataType: HeatmapDataType,
  lat: number,
  lng: number,
  radiusKm: number = 5,
  businessType: string = 'coffee shop'
): Promise<HeatmapResponse | null> {
  try {
    let endpoint = '';
    const params = new URLSearchParams({
      lat: lat.toString(),
      lng: lng.toString(),
      radius_km: radiusKm.toString(),
    });

    // Map data types to API endpoints
    switch (dataType) {
      case 'business_competition':
        endpoint = '/heatmap/business_competition';
        params.append('business_type', businessType);
        break;
      case 'review_power':
        endpoint = '/heatmap/review_power';
        params.append('business_type', businessType);
        break;
      case 'demographic_density':
      case 'population':
        endpoint = '/heatmap/demographics_density';
        break;
      case 'income_wealth':
        endpoint = '/heatmap/income_wealth';
        break;
      case 'market_opportunity':
        endpoint = '/heatmap/opportunity';
        params.append('business_type', businessType);
        break;
      case 'foot_traffic':
        endpoint = '/heatmap/foot_traffic';
        break;
      default:
        console.warn(`Unknown heatmap type: ${dataType}, using business_competition`);
        endpoint = '/heatmap/business_competition';
        params.append('business_type', businessType);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}?${params.toString()}`);
    
    if (!response.ok) {
      throw new Error(`Heatmap API failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Error fetching ${dataType} heatmap:`, error);
    return null;
  }
}

// Fetch multiple heatmap layers at once
export async function fetchMultipleHeatmaps(
  dataTypes: HeatmapDataType[],
  lat: number,
  lng: number,
  radiusKm: number = 5,
  businessType: string = 'coffee shop'
): Promise<Record<HeatmapDataType, HeatmapResponse | null>> {
  const results: Record<string, HeatmapResponse | null> = {};
  
  await Promise.all(
    dataTypes.map(async (dataType) => {
      results[dataType] = await fetchHeatmapData(dataType, lat, lng, radiusKm, businessType);
    })
  );
  
  return results as Record<HeatmapDataType, HeatmapResponse | null>;
}

// Convert heatmap response to Mapbox-compatible GeoJSON
export function convertToMapboxHeatmap(heatmapResponse: HeatmapResponse): any {
  return {
    type: 'FeatureCollection',
    features: heatmapResponse.features.map((feature) => ({
      type: 'Feature',
      geometry: feature.geometry,
      properties: {
        ...feature.properties,
        intensity: feature.properties.weight,
      },
    })),
  };
}