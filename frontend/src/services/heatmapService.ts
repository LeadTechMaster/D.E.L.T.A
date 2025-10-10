// Heatmap service for motor boat business data
export interface HeatmapPoint {
  lat: number;
  lng: number;
  intensity: number;
  value: number;
  name: string;
  rating: number;
  reviews: number;
}

export interface BusinessLocation {
  name: string;
  rating: number;
  user_ratings_total: number;
  coordinates: {
    latitude: number;
    longitude: number;
  };
}

// Generate heatmap data from business locations
export function generateBusinessHeatmap(businesses: BusinessLocation[]): HeatmapPoint[] {
  return businesses.map((business) => {
    // Calculate intensity based on rating and review count
    const ratingWeight = business.rating / 5.0; // Normalize rating to 0-1
    const reviewWeight = Math.min(business.user_ratings_total / 1000, 1); // Cap at 1000 reviews
    const intensity = (ratingWeight * 0.7) + (reviewWeight * 0.3); // Weighted combination
    
    return {
      lat: business.coordinates.latitude,
      lng: business.coordinates.longitude,
      intensity: intensity,
      value: business.rating,
      name: business.name,
      rating: business.rating,
      reviews: business.user_ratings_total,
    };
  });
}

// Generate competition heatmap data
export function generateCompetitionHeatmap(businesses: BusinessLocation[]): HeatmapPoint[] {
  // Group businesses by proximity and calculate competition density
  const competitionPoints: HeatmapPoint[] = [];
  
  businesses.forEach((business) => {
    // Count nearby competitors (within 5km radius)
    const nearbyCount = businesses.filter(other => {
      if (other.name === business.name) return false;
      
      const distance = calculateDistance(
        business.coordinates.latitude,
        business.coordinates.longitude,
        other.coordinates.latitude,
        other.coordinates.longitude
      );
      
      return distance <= 5; // 5km radius
    }).length;
    
    // Competition intensity based on nearby competitors
    const competitionIntensity = Math.min(nearbyCount / 5, 1); // Cap at 5 competitors
    
    competitionPoints.push({
      lat: business.coordinates.latitude,
      lng: business.coordinates.longitude,
      intensity: competitionIntensity,
      value: nearbyCount,
      name: business.name,
      rating: business.rating,
      reviews: business.user_ratings_total,
    });
  });
  
  return competitionPoints;
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
  return R * c; // Distance in km
}

// Generate opportunity heatmap (combines rating, reviews, and competition)
export function generateOpportunityHeatmap(businesses: BusinessLocation[]): HeatmapPoint[] {
  return businesses.map((business) => {
    // Calculate opportunity score
    const ratingScore = business.rating / 5.0;
    const reviewScore = Math.min(business.user_ratings_total / 500, 1);
    
    // Lower competition = higher opportunity
    const nearbyCount = businesses.filter(other => {
      if (other.name === business.name) return false;
      
      const distance = calculateDistance(
        business.coordinates.latitude,
        business.coordinates.longitude,
        other.coordinates.latitude,
        other.coordinates.longitude
      );
      
      return distance <= 10; // 10km radius for opportunity
    }).length;
    
    const competitionScore = Math.max(0, 1 - (nearbyCount / 3)); // Lower competition = higher score
    
    const opportunityIntensity = (ratingScore * 0.4) + (reviewScore * 0.3) + (competitionScore * 0.3);
    
    return {
      lat: business.coordinates.latitude,
      lng: business.coordinates.longitude,
      intensity: opportunityIntensity,
      value: Math.round(opportunityIntensity * 100), // Convert to percentage
      name: business.name,
      rating: business.rating,
      reviews: business.user_ratings_total,
    };
  });
}

// Generate Mapbox-compatible GeoJSON for heatmaps
export function generateMapboxHeatmapGeoJSON(heatmapPoints: HeatmapPoint[]): any {
  return {
    type: 'FeatureCollection',
    features: heatmapPoints.map((point, index) => ({
      type: 'Feature',
      properties: {
        intensity: point.intensity,
        value: point.value,
        name: point.name,
        rating: point.rating,
        reviews: point.reviews,
        id: index,
      },
      geometry: {
        type: 'Point',
        coordinates: [point.lng, point.lat],
      },
    })),
  };
}
