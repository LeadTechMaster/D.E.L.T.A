import { useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import type { DemographicsData, AgeDistributionData, BusinessData } from '../services/api';

interface ZipcodeData {
  demographics: DemographicsData | null;
  ageDistribution: AgeDistributionData | null;
  businesses: BusinessData | null;
  coordinates: { lat: number; lng: number } | null;
  isochrone: any | null;
  loading: boolean;
  error: string | null;
}

interface ZipcodeState {
  currentZipcode: string | null;
  zipcodeData: ZipcodeData;
}

export function useZipcodeData() {
  const [state, setState] = useState<ZipcodeState>({
    currentZipcode: null,
    zipcodeData: {
      demographics: null,
      ageDistribution: null,
      businesses: null,
      coordinates: null,
      isochrone: null,
      loading: false,
      error: null
    }
  });

  const setCurrentZipcode = useCallback((zipcode: string | null) => {
    setState(prev => ({
      ...prev,
      currentZipcode: zipcode,
      zipcodeData: {
        ...prev.zipcodeData,
        loading: zipcode !== null,
        error: null
      }
    }));
  }, []);

  const loadZipcodeData = useCallback(async (zipcode: string) => {
    if (!zipcode) return;

    setState(prev => ({
      ...prev,
      zipcodeData: {
        ...prev.zipcodeData,
        loading: true,
        error: null
      }
    }));

    try {
      // Load all ZIP code data in parallel
      const [
        demographicsResponse,
        ageResponse,
        businessesResponse,
        coordinatesResponse
      ] = await Promise.allSettled([
        api.getZipcodeDemographics(zipcode),
        api.getZipcodeAgeDistribution(zipcode),
        api.getZipcodeBusinesses(zipcode, 'motor boat', 50000),
        api.getZipcodeCoordinates(zipcode)
      ]);

      const demographics = demographicsResponse.status === 'fulfilled' 
        ? demographicsResponse.value.data 
        : null;
      
      const ageDistribution = ageResponse.status === 'fulfilled' 
        ? ageResponse.value.data 
        : null;
      
      const businesses = businessesResponse.status === 'fulfilled' 
        ? businessesResponse.value.data 
        : null;
      
      const coordinates = coordinatesResponse.status === 'fulfilled' 
        ? coordinatesResponse.value.data?.center 
        : null;

      setState(prev => ({
        ...prev,
        zipcodeData: {
          demographics: demographics || null,
          ageDistribution: ageDistribution || null,
          businesses: businesses || null,
          coordinates: coordinates || null,
          isochrone: prev.zipcodeData.isochrone, // Keep existing isochrone
          loading: false,
          error: null
        }
      }));

    } catch (error) {
      setState(prev => ({
        ...prev,
        zipcodeData: {
          ...prev.zipcodeData,
          loading: false,
          error: error instanceof Error ? error.message : 'Failed to load ZIP code data'
        }
      }));
    }
  }, []);

  const generateIsochrone = useCallback(async (
    zipcode: string, 
    minutes: number, 
    mode: 'driving' | 'walking' | 'cycling'
  ) => {
    try {
      const response = await api.getZipcodeIsochrone(zipcode, minutes, mode);
      setState(prev => ({
        ...prev,
        zipcodeData: {
          ...prev.zipcodeData,
          isochrone: response.data
        }
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        zipcodeData: {
          ...prev.zipcodeData,
          error: error instanceof Error ? error.message : 'Failed to generate isochrone'
        }
      }));
    }
  }, []);

  const clearZipcodeData = useCallback(() => {
    setState(prev => ({
      ...prev,
      currentZipcode: null,
      zipcodeData: {
        demographics: null,
        ageDistribution: null,
        businesses: null,
        coordinates: null,
        isochrone: null,
        loading: false,
        error: null
      }
    }));
  }, []);

  // Auto-load data when ZIP code changes
  useEffect(() => {
    if (state.currentZipcode) {
      loadZipcodeData(state.currentZipcode);
    }
  }, [state.currentZipcode, loadZipcodeData]);

  return {
    currentZipcode: state.currentZipcode,
    zipcodeData: state.zipcodeData,
    setCurrentZipcode,
    generateIsochrone,
    clearZipcodeData,
    loadZipcodeData
  };
}
