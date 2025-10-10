// Type definitions for D.E.L.T.A Dashboard

import type { ViewMode, MapLayer, DrawingTool, SaturationLevel, RiskLevel, RecommendedAction, PriceLevel } from './enums';

// Props types
export interface RootProps {
  initialViewMode: ViewMode;
  initialCenter: Coordinates;
  initialZoom: number;
  projectName: string;
  lastSaved: Date;
  userName: string;
}

export interface Coordinates {
  lat: number;
  lng: number;
}

// Store types
export interface StoreState {
  activeViewMode: ViewMode;
  activeLayers: MapLayer[];
  selectedDrawingTool: DrawingTool | null;
  drawnShapes: DrawnShape[];
  selectedShapeId: string | null;
  comparisonTerritories: string[];
  filters: FilterState;
  mapCenter: Coordinates;
  mapZoom: number;
}

export interface DrawnShape {
  id: string;
  type: 'circle' | 'polygon';
  name: string;
  center?: Coordinates;
  radius?: number;
  coordinates?: Coordinates[];
  color: string;
}

export interface FilterState {
  incomeRange: [number, number];
  minSearchVolume: number;
  radius: number;
  businessType: string;
}

// Query types (API responses)
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
  age_distribution: Record<string, number>;
  gender_breakdown: {
    male: number;
    female: number;
  };
  education_levels: Record<string, number>;
}

export interface KeywordDemandData {
  top_keywords: KeywordMetric[];
  trend_data: TrendDataPoint[];
}

export interface KeywordMetric {
  keyword: string;
  monthly_searches: number;
  cpc: number;
  competition: number;
}

export interface TrendDataPoint {
  month: string;
  volume: number;
}

export interface CompetitorData {
  name: string;
  rating: number;
  review_count: number;
  price_level: PriceLevel;
  lat: number;
  lng: number;
  types: string[];
}

export interface TerritoryAnalysisData {
  total_businesses: number;
  area_square_miles: number;
  density_per_square_mile: number;
  saturation_level: SaturationLevel;
  average_rating: number;
  total_reviews: number;
  opportunity_score: number;
  risk_level: RiskLevel;
  recommended_action: RecommendedAction;
  top_competitors: TopCompetitor[];
}

export interface TopCompetitor {
  name: string;
  rating: number;
  reviews: number;
}

export interface OpportunityIndexData {
  overall_score: number;
  demand_score: number;
  competition_score: number;
  spending_power_score: number;
  risk_assessment: RiskLevel;
  recommended_action: RecommendedAction;
  insights: string[];
}

export interface ComparisonDataItem {
  territory: string;
  population: number;
  median_income: number;
  competitors: number;
  search_volume: number;
  opportunity_score: number;
}

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection';
  features: GeoJSONFeature[];
}

export interface GeoJSONFeature {
  type: 'Feature';
  geometry: GeoJSONGeometry;
  properties: Record<string, any>;
}

export interface GeoJSONGeometry {
  type: 'Point' | 'Polygon' | 'LineString';
  coordinates: number[] | number[][] | number[][][];
}