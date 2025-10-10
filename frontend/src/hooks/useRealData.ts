import { useState, useEffect } from 'react';
import { api, transformApiData } from '../services/api';
import type { DemographicsData, BusinessData, SearchTrendsData } from '../services/api';

export interface RealDataState {
  demographics: DemographicsData | null;
  ageDistribution: any | null;
  genderData: any | null;
  employmentData: any | null;
  housingData: any | null;
  businessData: BusinessData | null;
  searchTrends: SearchTrendsData | null;
  competitors: any[] | null;
  keywordDemand: any | null;
  opportunityIndex: any | null;
  loading: boolean;
  error: string | null;
}

export function useRealData(location: string = 'Seattle, WA', businessType: string = 'motor boat') {
  const [data, setData] = useState<RealDataState>({
    demographics: null,
    ageDistribution: null,
    genderData: null,
    employmentData: null,
    housingData: null,
    businessData: null,
    searchTrends: null,
    competitors: null,
    keywordDemand: null,
    opportunityIndex: null,
    loading: true,
    error: null,
  });

  const fetchAllData = async () => {
    setData(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      // Seattle coordinates
      const coordinates = '47.6062,-122.3321';
      
      // Fetch all data in parallel for better performance
      const [
        demographicsResponse,
        ageResponse,
        genderResponse,
        employmentResponse,
        housingResponse,
        businessResponse,
        searchTrendsResponse,
      ] = await Promise.allSettled([
        api.getDemographics('53'), // Washington state
        api.getAgeDistribution('53'),
        api.getGenderData('53'),
        api.getEmploymentData('53'),
        api.getHousingData('53'),
        api.getBusinesses(coordinates, businessType, 50000),
        api.getSearchTrends(businessType, location),
      ]);

      // Process demographics data
      let demographics: DemographicsData | null = null;
      let ageDistribution: any = null;
      let genderData: any = null;
      let employmentData: any = null;
      let housingData: any = null;

      if (demographicsResponse.status === 'fulfilled' && demographicsResponse.value.status === 'success') {
        demographics = demographicsResponse.value.data || null;
      }

      if (ageResponse.status === 'fulfilled' && ageResponse.value.status === 'success') {
        ageDistribution = ageResponse.value.data || null;
        if (ageDistribution && demographics) {
          demographics.age_distribution = transformApiData.ageDistribution(ageDistribution);
        }
      }

      if (genderResponse.status === 'fulfilled' && genderResponse.value.status === 'success') {
        genderData = genderResponse.value.data || null;
        if (genderData && demographics) {
          demographics.gender_breakdown = {
            male: genderData.gender_breakdown.male,
            female: genderData.gender_breakdown.female,
          };
        }
      }

      if (employmentResponse.status === 'fulfilled' && employmentResponse.value.status === 'success') {
        employmentData = employmentResponse.value.data || null;
        if (employmentData && demographics) {
          demographics.employment_rate = employmentData.employment_rate;
          demographics.unemployment_rate = employmentData.unemployment_rate;
        }
      }

      if (housingResponse.status === 'fulfilled' && housingResponse.value.status === 'success') {
        housingData = housingResponse.value.data || null;
        if (housingData && demographics) {
          demographics.median_home_value = housingData.median_home_value;
          demographics.median_gross_rent = housingData.median_gross_rent;
          demographics.occupancy_rate = housingData.occupancy_rate;
          demographics.ownership_rate = housingData.ownership_rate;
        }
      }

      // Process business data
      let businessData: BusinessData | null = null;
      let competitors: any[] = [];

      if (businessResponse.status === 'fulfilled' && businessResponse.value.status === 'success') {
        businessData = businessResponse.value.data || null;
        if (businessData) {
          competitors = transformApiData.competitors(businessData);
        }
      }

      // Process search trends
      let searchTrends: SearchTrendsData | null = null;
      let keywordDemand: any = null;

      if (searchTrendsResponse.status === 'fulfilled' && searchTrendsResponse.value.status === 'success') {
        searchTrends = searchTrendsResponse.value.data || null;
        if (searchTrends) {
          keywordDemand = transformApiData.keywordDemand(searchTrends);
        }
      }

      // Generate opportunity index
      let opportunityIndex: any = null;
      if (demographics && businessData && searchTrends) {
        opportunityIndex = transformApiData.opportunityIndex(demographics, businessData, searchTrends);
      }

      setData({
        demographics,
        ageDistribution,
        genderData,
        employmentData,
        housingData,
        businessData,
        searchTrends,
        competitors,
        keywordDemand,
        opportunityIndex,
        loading: false,
        error: null,
      });

    } catch (error) {
      console.error('Error fetching real data:', error);
      setData(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch data',
      }));
    }
  };

  useEffect(() => {
    fetchAllData();
  }, [location, businessType]);

  return {
    ...data,
    refetch: fetchAllData,
  };
}

// Hook that provides only real data - no fallbacks
export function useDataWithFallback(location: string = 'Seattle, WA', businessType: string = 'motor boat') {
  const realData = useRealData(location, businessType);
  
  return {
    demographics: realData.demographics,
    competitors: realData.competitors || [],
    keywordDemand: realData.keywordDemand,
    opportunityIndex: realData.opportunityIndex,
    loading: realData.loading,
    error: realData.error,
    isRealData: !realData.loading && !realData.error,
    refetch: realData.refetch,
  };
}
