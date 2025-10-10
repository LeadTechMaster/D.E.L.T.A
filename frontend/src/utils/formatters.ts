import { format } from 'date-fns';
import type { SaturationLevel, RiskLevel, RecommendedAction, PriceLevel } from '../types/enums';

// Number formatting
export const formatNumber = (num: number | null | undefined): string => {
  if (num === null || num === undefined || isNaN(num)) {
    return '0';
  }
  return new Intl.NumberFormat('en-US').format(num);
};

export const formatCurrency = (amount: number | null | undefined): string => {
  if (amount === null || amount === undefined || isNaN(amount)) {
    return '$0';
  }
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

export const formatPercentage = (value: number | null | undefined): string => {
  if (value === null || value === undefined || isNaN(value)) {
    return '0.0%';
  }
  return `${value.toFixed(1)}%`;
};

export const formatDecimal = (value: number | null | undefined, decimals: number = 2): string => {
  if (value === null || value === undefined || isNaN(value)) {
    return '0.00';
  }
  return value.toFixed(decimals);
};

export const formatCompactNumber = (num: number | null | undefined): string => {
  if (num === null || num === undefined || isNaN(num)) {
    return '0';
  }
  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    compactDisplay: 'short'
  }).format(num);
};

// Date formatting
export const formatDate = (date: Date): string => {
  return format(date, 'MMM dd, yyyy');
};

export const formatDateTime = (date: Date): string => {
  return format(date, 'MMM dd, yyyy HH:mm');
};

export const formatTimeAgo = (date: Date): string => {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
  
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
  return formatDate(date);
};

// Enum value formatting
export const formatSaturationLevel = (level: SaturationLevel): string => {
  const labels: Record<SaturationLevel, string> = {
    low: 'Low Competition',
    moderate: 'Moderate Competition',
    high: 'High Competition',
    very_high: 'Very High Competition'
  };
  return labels[level];
};

export const formatRiskLevel = (level: RiskLevel): string => {
  const labels: Record<RiskLevel, string> = {
    low: 'Low Risk',
    moderate: 'Moderate Risk',
    high: 'High Risk'
  };
  return labels[level];
};

export const formatRecommendedAction = (action: RecommendedAction): string => {
  const labels: Record<RecommendedAction, string> = {
    expand: 'Expand Here ✅',
    caution: 'Proceed with Caution ⚠️',
    avoid: 'Avoid ❌'
  };
  return labels[action];
};

export const formatPriceLevel = (level: PriceLevel): string => {
  return '$'.repeat(level);
};

// Distance and area formatting
export const formatDistance = (meters: number): string => {
  const miles = meters * 0.000621371;
  return miles < 1 
    ? `${Math.round(meters)} m` 
    : `${miles.toFixed(1)} mi`;
};

export const formatArea = (squareMeters: number): string => {
  const squareMiles = squareMeters * 0.000000386102;
  return `${squareMiles.toFixed(2)} sq mi`;
};

export const formatDuration = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return `${hours}h ${remainingMinutes}m`;
};

// Score formatting
export const formatScore = (score: number): string => {
  return `${Math.round(score)}/100`;
};

export const formatRating = (rating: number): string => {
  return `${rating.toFixed(1)} ★`;
};