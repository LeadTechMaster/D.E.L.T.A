import { useState, useEffect } from "react";
import { X, Users, Home, DollarSign, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

interface DemographicsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  zipcode?: string;
}

interface DemographicsData {
  zipcode: string;
  name: string;
  total_population: number;
  median_household_income: number;
  median_home_value: number;
  data_source: string;
}

interface AgeDistributionData {
  zipcode: string;
  name: string;
  age_groups: {
    "0_17": string;
    "18_24": string;
    "25_34": string;
    "35_44": string;
    "45_54": string;
    "55_64": string;
    "65_plus": string;
  };
  total_population: number;
  data_source: string;
}

interface HousingData {
  zipcode: string;
  name: string;
  housing_intelligence: {
    total_housing_units: number;
    occupied_units: number;
    vacant_units: number;
    owner_occupied: number;
    renter_occupied: number;
    vacancy_rate: string;
    ownership_rate: string;
    rental_rate: string;
  };
  data_source: string;
}

export function DemographicsPanel({ isOpen, onClose, zipcode = "94103" }: DemographicsPanelProps) {
  const [demographics, setDemographics] = useState<DemographicsData | null>(null);
  const [ageData, setAgeData] = useState<AgeDistributionData | null>(null);
  const [housingData, setHousingData] = useState<HousingData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && zipcode) {
      fetchDemographicsData();
    }
  }, [isOpen, zipcode]);

  const fetchDemographicsData = async () => {
    setLoading(true);
    setError(null);

    try {
      // Fetch demographics data
      const demoResponse = await fetch(`http://localhost:8001/api/v1/zipcode/demographics?zipcode=${zipcode}`);
      if (!demoResponse.ok) throw new Error("Failed to fetch demographics");
      const demoData = await demoResponse.json();
      if (demoData.status === "success") {
        setDemographics(demoData.data);
      }

      // Fetch age distribution
      const ageResponse = await fetch(`http://localhost:8001/api/v1/zipcode/age-distribution?zipcode=${zipcode}`);
      if (!ageResponse.ok) throw new Error("Failed to fetch age data");
      const ageResponseData = await ageResponse.json();
      if (ageResponseData.status === "success") {
        setAgeData(ageResponseData.data);
      }

      // Fetch housing data
      const housingResponse = await fetch(`http://localhost:8001/api/v1/zipcode/housing?zipcode=${zipcode}`);
      if (!housingResponse.ok) throw new Error("Failed to fetch housing data");
      const housingResponseData = await housingResponse.json();
      if (housingResponseData.status === "success") {
        setHousingData(housingResponseData.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load data");
      console.error("Error fetching demographics:", err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed right-0 top-0 h-screen w-[480px] z-40 bg-[#1a1f2e]/95 backdrop-blur-md border-l border-[#2d3548] shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-[#2d3548]">
        <h2 className="text-xl font-semibold text-white flex items-center gap-2">
          <Users className="h-5 w-5 text-[#00bcd4]" />
          Demographics
        </h2>
        <Button
          variant="ghost"
          size="icon"
          onClick={onClose}
          className="text-[#8b92a7] hover:text-white hover:bg-[#2d3548]"
        >
          <X className="h-5 w-5" />
        </Button>
      </div>

      <ScrollArea className="h-[calc(100vh-73px)]">
        <div className="p-4 space-y-4">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#00bcd4]"></div>
            </div>
          )}

          {error && (
            <Card className="bg-red-500/10 border-red-500/30">
              <CardContent className="p-4">
                <p className="text-red-400">{error}</p>
              </CardContent>
            </Card>
          )}

          {!loading && !error && demographics && (
            <>
              {/* Location Info */}
              <Card className="bg-[#0f1219] border-[#2d3548]">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Location</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-[#00bcd4] font-semibold">{demographics.name}</p>
                  <p className="text-[#8b92a7] text-sm mt-1">ZIP Code: {demographics.zipcode}</p>
                </CardContent>
              </Card>

              {/* Key Metrics */}
              <div className="grid grid-cols-2 gap-3">
                <Card className="bg-[#0f1219] border-[#2d3548] hover:border-[#00bcd4]/30 transition-colors">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Users className="h-4 w-4 text-[#00bcd4]" />
                      <p className="text-[#8b92a7] text-xs">Population</p>
                    </div>
                    <p className="text-white text-2xl font-bold">{demographics.total_population.toLocaleString()}</p>
                  </CardContent>
                </Card>

                <Card className="bg-[#0f1219] border-[#2d3548] hover:border-[#00bcd4]/30 transition-colors">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <DollarSign className="h-4 w-4 text-[#26c6da]" />
                      <p className="text-[#8b92a7] text-xs">Med. Income</p>
                    </div>
                    <p className="text-white text-2xl font-bold">${demographics.median_household_income.toLocaleString()}</p>
                  </CardContent>
                </Card>

                <Card className="bg-[#0f1219] border-[#2d3548] hover:border-[#00bcd4]/30 transition-colors">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Home className="h-4 w-4 text-[#4dd0e1]" />
                      <p className="text-[#8b92a7] text-xs">Med. Home Value</p>
                    </div>
                    <p className="text-white text-2xl font-bold">${demographics.median_home_value.toLocaleString()}</p>
                  </CardContent>
                </Card>

                {housingData && (
                  <Card className="bg-[#0f1219] border-[#2d3548] hover:border-[#00bcd4]/30 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Home className="h-4 w-4 text-[#80deea]" />
                        <p className="text-[#8b92a7] text-xs">Housing Units</p>
                      </div>
                      <p className="text-white text-2xl font-bold">
                        {housingData.housing_intelligence.total_housing_units.toLocaleString()}
                      </p>
                    </CardContent>
                  </Card>
                )}
              </div>

              {/* Age Distribution */}
              {ageData && (
                <Card className="bg-[#0f1219] border-[#2d3548]">
                  <CardHeader>
                    <CardTitle className="text-white text-sm">Age Distribution</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {Object.entries(ageData.age_groups).map(([ageGroup, percentage]) => {
                      const label = ageGroup.replace("_", "-").replace("plus", "+");
                      return (
                        <div key={ageGroup}>
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-[#8b92a7]">{label}</span>
                            <span className="text-white font-medium">{percentage}%</span>
                          </div>
                          <div className="w-full bg-[#2d3548] rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-[#00bcd4] to-[#26c6da] h-2 rounded-full transition-all"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </CardContent>
                </Card>
              )}

              {/* Housing Details */}
              {housingData && (
                <Card className="bg-[#0f1219] border-[#2d3548]">
                  <CardHeader>
                    <CardTitle className="text-white text-sm">Housing</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-[#8b92a7] text-xs mb-1">Occupied</p>
                        <p className="text-white font-semibold">
                          {housingData.housing_intelligence.occupied_units.toLocaleString()}
                        </p>
                      </div>
                      <div>
                        <p className="text-[#8b92a7] text-xs mb-1">Vacant</p>
                        <p className="text-white font-semibold">
                          {housingData.housing_intelligence.vacant_units.toLocaleString()}
                        </p>
                      </div>
                      <div>
                        <p className="text-[#8b92a7] text-xs mb-1">Owner Occupied</p>
                        <p className="text-white font-semibold">
                          {housingData.housing_intelligence.ownership_rate}%
                        </p>
                      </div>
                      <div>
                        <p className="text-[#8b92a7] text-xs mb-1">Renter Occupied</p>
                        <p className="text-white font-semibold">
                          {housingData.housing_intelligence.rental_rate}%
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Data Source */}
              <p className="text-[#6b7280] text-xs text-center">
                Data from {demographics.data_source}
              </p>
            </>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

