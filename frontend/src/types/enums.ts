// Enums for D.E.L.T.A Dashboard

export const ViewMode = {
  MAP: 'map',
  DASHBOARD: 'dashboard',
  SPLIT: 'split'
} as const;

export type ViewMode = typeof ViewMode[keyof typeof ViewMode];

export const DrawingTool = {
  CIRCLE: 'circle',
  POLYGON: 'polygon',
  DRIVE_TIME: 'drive_time',
  ZIP_SELECT: 'zip_select',
  MEASURE_DISTANCE: 'measure_distance',
  TRAVEL_TIME: 'travel_time'
} as const;

export type DrawingTool = typeof DrawingTool[keyof typeof DrawingTool];

export const MapLayer = {
  DEMOGRAPHICS: 'demographics',
  POPULATION_DENSITY: 'population_density',
  INCOME_WEALTH: 'income_wealth',
  HOME_OWNERSHIP: 'home_ownership',
  KEYWORD_DEMAND: 'keyword_demand',
  COMPETITORS: 'competitors',
  BOUNDARIES: 'boundaries',
  ZIP_CODES: 'zip_codes',
  CITIES: 'cities',
  COUNTIES: 'counties'
} as const;

export type MapLayer = typeof MapLayer[keyof typeof MapLayer];

export const HeatmapType = {
  BUSINESS_COMPETITION: 'business_competition',
  DEMOGRAPHIC_DENSITY: 'demographic_density',
  FOOT_TRAFFIC: 'foot_traffic',
  MARKET_OPPORTUNITY: 'market_opportunity',
  INCOME_WEALTH: 'income_wealth',
  REVIEW_POWER: 'review_power'
} as const;

export type HeatmapType = typeof HeatmapType[keyof typeof HeatmapType];

export const TravelMode = {
  DRIVING: 'driving',
  WALKING: 'walking',
  CYCLING: 'cycling'
} as const;

export type TravelMode = typeof TravelMode[keyof typeof TravelMode];

export const SaturationLevel = {
  LOW: 'low',
  MODERATE: 'moderate',
  HIGH: 'high',
  VERY_HIGH: 'very_high'
} as const;

export type SaturationLevel = typeof SaturationLevel[keyof typeof SaturationLevel];

export const RiskLevel = {
  LOW: 'low',
  MODERATE: 'moderate',
  HIGH: 'high'
} as const;

export type RiskLevel = typeof RiskLevel[keyof typeof RiskLevel];

export const RecommendedAction = {
  EXPAND: 'expand',
  CAUTION: 'caution',
  AVOID: 'avoid'
} as const;

export type RecommendedAction = typeof RecommendedAction[keyof typeof RecommendedAction];

export const ReportType = {
  ONE_PAGE_SUMMARY: 'one_page_summary',
  FULL_REPORT: 'full_report'
} as const;

export type ReportType = typeof ReportType[keyof typeof ReportType];

export const ExportFormat = {
  CSV: 'csv',
  PDF: 'pdf',
  PNG: 'png',
  JSON: 'json'
} as const;

export type ExportFormat = typeof ExportFormat[keyof typeof ExportFormat];

export const ChartType = {
  BAR: 'bar',
  LINE: 'line',
  PIE: 'pie',
  RADAR: 'radar',
  HISTOGRAM: 'histogram',
  HEATMAP: 'heatmap'
} as const;

export type ChartType = typeof ChartType[keyof typeof ChartType];

export const PriceLevel = {
  BUDGET: 1,
  MODERATE: 2,
  EXPENSIVE: 3,
  VERY_EXPENSIVE: 4
} as const;

export type PriceLevel = typeof PriceLevel[keyof typeof PriceLevel];