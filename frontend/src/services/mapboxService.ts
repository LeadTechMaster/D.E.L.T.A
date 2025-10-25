// Mapbox service for geocoding and isochrone
const MAPBOX_ACCESS_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || 'pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw';
const API_BASE_URL = 'http://localhost:8001/api/v1';

// Get ZIP code from coordinates
export async function getZipCodeFromCoordinates(lat: number, lng: number): Promise<string | null> {
  try {
    const response = await fetch(
      `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?types=postcode&access_token=${MAPBOX_ACCESS_TOKEN}`
    );
    
    if (!response.ok) {
      throw new Error(`Geocoding failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    if (data.features && data.features.length > 0) {
      const zipMatch = data.features[0].text.match(/\d{5}/);
      return zipMatch ? zipMatch[0] : null;
    }
    
    return null;
  } catch (error) {
    console.error('Error getting ZIP code:', error);
    return null;
  }
}

export interface GeocodingResult {
  id: string;
  place_name: string;
  center: [number, number];
  bbox?: [number, number, number, number];
}

export interface IsochroneOptions {
  coordinates: [number, number];
  profile: 'driving' | 'walking' | 'cycling';
  contours_minutes: number[];
  polygons?: boolean;
}

export interface IsochroneFeature {
  type: 'Feature';
  geometry: {
    type: 'Polygon';
    coordinates: number[][][];
  };
  properties: {
    contour: number;
    color?: string;
    opacity?: number;
  };
}

export interface IsochroneResponse {
  type: 'FeatureCollection';
  features: IsochroneFeature[];
}

// Geocoding - Search for locations
export async function geocodeSearch(query: string): Promise<GeocodingResult[]> {
  try {
    const response = await fetch(
      `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${MAPBOX_ACCESS_TOKEN}&types=place,locality,neighborhood,address&limit=5`
    );
    
    if (!response.ok) {
      throw new Error(`Geocoding failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data.features || [];
  } catch (error) {
    console.error('Geocoding error:', error);
    return [];
  }
}

// Reverse Geocoding - Get location name from coordinates
export async function reverseGeocode(lng: number, lat: number): Promise<string> {
  try {
    const response = await fetch(
      `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?access_token=${MAPBOX_ACCESS_TOKEN}&types=place,locality`
    );
    
    if (!response.ok) {
      throw new Error(`Reverse geocoding failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data.features?.[0]?.place_name || `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
  } catch (error) {
    console.error('Reverse geocoding error:', error);
    return `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
  }
}

// Isochrone - Get travel time polygons
export async function getIsochrone(options: IsochroneOptions): Promise<IsochroneResponse | null> {
  try {
    const { coordinates, profile, contours_minutes, polygons = true } = options;
    const [lng, lat] = coordinates;
    
    // Use backend API if available, otherwise use Mapbox directly
    try {
      const backendResponse = await fetch(
        `${API_BASE_URL}/mapbox/isochrone?coordinates=${lng},${lat}&minutes=${contours_minutes[0]}&mode=${profile}`
      );
      
      if (backendResponse.ok) {
        return await backendResponse.json();
      }
    } catch (backendError) {
      console.log('Backend API not available, using Mapbox directly');
    }
    
    // Fallback to direct Mapbox API
    const response = await fetch(
      `https://api.mapbox.com/isochrone/v1/mapbox/${profile}/${lng},${lat}?contours_minutes=${contours_minutes.join(',')}&polygons=${polygons}&access_token=${MAPBOX_ACCESS_TOKEN}`
    );
    
    if (!response.ok) {
      throw new Error(`Isochrone failed: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Isochrone error:', error);
    return null;
  }
}

// Get directions between two points
export async function getDirections(
  origin: [number, number],
  destination: [number, number],
  profile: 'driving' | 'walking' | 'cycling' = 'driving'
): Promise<any> {
  try {
    const [originLng, originLat] = origin;
    const [destLng, destLat] = destination;
    
    const response = await fetch(
      `https://api.mapbox.com/directions/v5/mapbox/${profile}/${originLng},${originLat};${destLng},${destLat}?geometries=geojson&access_token=${MAPBOX_ACCESS_TOKEN}`
    );
    
    if (!response.ok) {
      throw new Error(`Directions failed: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Directions error:', error);
    return null;
  }
}