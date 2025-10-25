import { useState, useCallback } from 'react';
import { api } from '../services/api';

interface AreaData {
  coordinates: { lat: number; lng: number };
  zipcode?: string;
  demographics?: {
    total_population: number;
    median_household_income: number;
    median_age: number;
    employment_rate: number;
  };
  businesses?: {
    count: number;
    average_rating: number;
    total_reviews: number;
    top_competitors: Array<{
      name: string;
      rating: number;
      review_count: number;
      distance: number;
    }>;
  };
  searchVolume?: {
    monthly_searches: number;
    avg_cpc: number;
    competition_level: number;
    top_keywords: Array<{
      keyword: string;
      searches: number;
      cpc: number;
    }>;
  };
}

export const useAreaData = () => {
  const [areaData, setAreaData] = useState<AreaData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAreaData = useCallback(async (coordinates: { lat: number; lng: number }) => {
    setLoading(true);
    setError(null);
    
    try {
      // Get ZIP code from coordinates
      const zipcodeResponse = await api.getZipcodeCoordinates(coordinates.lat.toString());
      const zipcode = zipcodeResponse.data?.zipcode || null;
      
      // Fetch all data in parallel
      const promises = [];
      
      // Demographics data
      if (zipcode) {
        promises.push(
          api.getZipcodeDemographics(zipcode).catch(() => null)
        );
      } else {
        // Fallback to state data if no ZIP code
        promises.push(
          api.getDemographics('53').catch(() => null) // Washington state
        );
      }
      
      // Business data
      promises.push(
        api.getBusinesses(`${coordinates.lat},${coordinates.lng}`, 'motor boat', 5000).catch(() => null)
      );
      
      // Search volume data
      promises.push(
        api.getSearchTrends('motor boat', `${coordinates.lat},${coordinates.lng}`).catch(() => null)
      );
      
      const [demographicsRes, businessRes, searchRes] = await Promise.all(promises);
      
      // Process demographics
      let demographics = null;
      if (demographicsRes?.data && 'total_population' in demographicsRes.data) {
        const demoData = demographicsRes.data as any; // Type assertion for now
        demographics = {
          total_population: demoData.total_population || 0,
          median_household_income: demoData.median_household_income || 0,
          median_age: demoData.median_age || 0,
          employment_rate: demoData.employment_rate || 0,
        };
      }
      
      // Process business data
      let businesses = null;
      if (businessRes?.data && 'results' in businessRes.data) {
        const businessResults = (businessRes.data as any).results;
        const totalReviews = businessResults.reduce((sum: number, business: any) => sum + (business.user_ratings_total || 0), 0);
        const avgRating = businessResults.reduce((sum: number, business: any) => sum + (business.rating || 0), 0) / businessResults.length;
        
        // Calculate distances and sort by proximity
        const competitorsWithDistance = businessResults.map((business: any) => {
          const distance = calculateDistance(
            coordinates.lat, coordinates.lng,
            business.geometry.location.lat, business.geometry.location.lng
          );
          return {
            name: business.name,
            rating: business.rating || 0,
            review_count: business.user_ratings_total || 0,
            distance: distance
          };
        }).sort((a: any, b: any) => a.distance - b.distance);
        
        businesses = {
          count: businessResults.length,
          average_rating: avgRating,
          total_reviews: totalReviews,
          top_competitors: competitorsWithDistance.slice(0, 5)
        };
      }
      
      // Process search volume data
      let searchVolume = null;
      if (searchRes?.data && 'search_volume' in searchRes.data) {
        const searchData = searchRes.data as any;
        searchVolume = {
          monthly_searches: searchData.search_volume || 0,
          avg_cpc: searchData.average_cpc || 0,
          competition_level: searchData.competition_level || 0,
          top_keywords: (searchData.related_searches || []).slice(0, 5).map((keyword: any) => ({
            keyword: keyword.keyword || '',
            searches: keyword.monthly_searches || 0,
            cpc: keyword.cpc || 0
          }))
        };
      }
      
      const newAreaData: AreaData = {
        coordinates,
        zipcode: zipcode || undefined,
        demographics: demographics || undefined,
        businesses: businesses || undefined,
        searchVolume: searchVolume || undefined
      };
      
      setAreaData(newAreaData);
    } catch (err: any) {
      setError(`Failed to fetch area data: ${err.message}`);
      console.error('Error fetching area data:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearAreaData = useCallback(() => {
    setAreaData(null);
    setError(null);
  }, []);

  return {
    areaData,
    loading,
    error,
    fetchAreaData,
    clearAreaData
  };
};

// Helper function to calculate distance between two coordinates
function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371; // Radius of the Earth in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c; // Distance in kilometers
}
