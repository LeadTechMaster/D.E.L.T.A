import { Card, CardHeader, CardContent, Typography, Stack, Divider, IconButton, CircularProgress, Alert, Chip, Box } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import BusinessIcon from '@mui/icons-material/Business';
import PeopleIcon from '@mui/icons-material/People';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

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

interface AreaDataPanelProps {
  data: AreaData | null;
  loading: boolean;
  error: string | null;
  onClose: () => void;
}

export default function AreaDataPanel({ data, loading, error, onClose }: AreaDataPanelProps) {
  if (!data) return null;

  return (
    <Card
      elevation={3}
      sx={{
        position: 'absolute',
        top: 10,
        right: 10,
        zIndex: 1000,
        width: 380,
        maxHeight: '90vh',
        overflowY: 'auto',
        backgroundColor: 'rgba(0, 0, 0, 0.9)',
        backdropFilter: 'blur(10px)',
        color: 'white',
        border: '1px solid rgba(255, 255, 255, 0.1)',
      }}
    >
      <CardHeader
        title={
          <Stack direction="row" spacing={1} alignItems="center">
            <LocationOnIcon sx={{ color: '#00D9FF' }} />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              {data.zipcode ? `ZIP: ${data.zipcode}` : 'Area Analysis'}
            </Typography>
          </Stack>
        }
        subheader={`${data.coordinates.lat.toFixed(4)}, ${data.coordinates.lng.toFixed(4)}`}
        titleTypographyProps={{ variant: 'h6', fontWeight: 600 }}
        subheaderTypographyProps={{ color: 'text.secondary', fontSize: '0.8rem' }}
        action={
          <IconButton onClick={onClose} sx={{ color: 'white' }}>
            <CloseIcon />
          </IconButton>
        }
      />
      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.1)' }} />
      <CardContent>
        {loading && (
          <Box display="flex" justifyContent="center" mb={2}>
            <CircularProgress size={20} sx={{ color: '#00D9FF' }} />
          </Box>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mb: 2, backgroundColor: 'rgba(244, 67, 54, 0.1)' }}>
            {error}
          </Alert>
        )}

        <Stack spacing={2}>
          {/* Demographics Section */}
          {data.demographics && (
            <>
              <Stack direction="row" spacing={1} alignItems="center">
                <PeopleIcon sx={{ color: '#00D9FF' }} />
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  Demographics
                </Typography>
              </Stack>
              <Stack spacing={1} sx={{ ml: 3 }}>
                <Typography variant="body2">
                  <strong>Population:</strong> {data.demographics.total_population.toLocaleString()}
                </Typography>
                <Typography variant="body2">
                  <strong>Median Income:</strong> ${data.demographics.median_household_income.toLocaleString()}
                </Typography>
                <Typography variant="body2">
                  <strong>Median Age:</strong> {data.demographics.median_age} years
                </Typography>
                <Typography variant="body2">
                  <strong>Employment Rate:</strong> {data.demographics.employment_rate.toFixed(1)}%
                </Typography>
              </Stack>
              <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.1)' }} />
            </>
          )}

          {/* Business Section */}
          {data.businesses && (
            <>
              <Stack direction="row" spacing={1} alignItems="center">
                <BusinessIcon sx={{ color: '#00D9FF' }} />
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  Business Landscape
                </Typography>
              </Stack>
              <Stack spacing={1} sx={{ ml: 3 }}>
                <Typography variant="body2">
                  <strong>Total Businesses:</strong> {data.businesses.count}
                </Typography>
                <Typography variant="body2">
                  <strong>Average Rating:</strong> {data.businesses.average_rating.toFixed(1)}/5
                </Typography>
                <Typography variant="body2">
                  <strong>Total Reviews:</strong> {data.businesses.total_reviews.toLocaleString()}
                </Typography>
                
                {data.businesses.top_competitors.length > 0 && (
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                      Top Competitors:
                    </Typography>
                    <Stack spacing={0.5}>
                      {data.businesses.top_competitors.slice(0, 3).map((competitor, index) => (
                        <Box key={index} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="caption" sx={{ flex: 1 }}>
                            {competitor.name}
                          </Typography>
                          <Stack direction="row" spacing={0.5}>
                            <Chip 
                              label={`${competitor.rating}/5`} 
                              size="small" 
                              sx={{ height: 20, fontSize: '0.7rem' }}
                            />
                            <Chip 
                              label={`${competitor.distance.toFixed(1)}km`} 
                              size="small" 
                              sx={{ height: 20, fontSize: '0.7rem' }}
                            />
                          </Stack>
                        </Box>
                      ))}
                    </Stack>
                  </Box>
                )}
              </Stack>
              <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.1)' }} />
            </>
          )}

          {/* Search Volume Section */}
          {data.searchVolume && (
            <>
              <Stack direction="row" spacing={1} alignItems="center">
                <TrendingUpIcon sx={{ color: '#00D9FF' }} />
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  Search Trends
                </Typography>
              </Stack>
              <Stack spacing={1} sx={{ ml: 3 }}>
                <Typography variant="body2">
                  <strong>Monthly Searches:</strong> {data.searchVolume.monthly_searches.toLocaleString()}
                </Typography>
                <Typography variant="body2">
                  <strong>Avg CPC:</strong> ${data.searchVolume.avg_cpc}
                </Typography>
                <Typography variant="body2">
                  <strong>Competition:</strong> {data.searchVolume.competition_level}%
                </Typography>
                
                {data.searchVolume.top_keywords.length > 0 && (
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>
                      Top Keywords:
                    </Typography>
                    <Stack spacing={0.5}>
                      {data.searchVolume.top_keywords.slice(0, 3).map((keyword, index) => (
                        <Box key={index} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="caption" sx={{ flex: 1 }}>
                            {keyword.keyword}
                          </Typography>
                          <Stack direction="row" spacing={0.5}>
                            <Chip 
                              label={`${keyword.searches}`} 
                              size="small" 
                              sx={{ height: 20, fontSize: '0.7rem' }}
                            />
                            <Chip 
                              label={`$${keyword.cpc}`} 
                              size="small" 
                              sx={{ height: 20, fontSize: '0.7rem' }}
                            />
                          </Stack>
                        </Box>
                      ))}
                    </Stack>
                  </Box>
                )}
              </Stack>
            </>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
}
