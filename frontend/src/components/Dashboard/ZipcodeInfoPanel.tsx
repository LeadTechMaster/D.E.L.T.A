import { Card, CardHeader, CardContent, Typography, Stack, Divider, Box, Chip, IconButton } from '@mui/material';
import { CloseOutlined, LocationOnOutlined } from '@mui/icons-material';
import { formatNumber, formatCurrency } from '../../utils/formatters';
import { useZipcodeData } from '../../hooks/useZipcodeData';

interface ZipcodeInfoPanelProps {
  onClose: () => void;
}

export default function ZipcodeInfoPanel({ onClose }: ZipcodeInfoPanelProps) {
  const { currentZipcode, zipcodeData, clearZipcodeData } = useZipcodeData();

  if (!currentZipcode || !zipcodeData.demographics) {
    return null;
  }

  const handleClose = () => {
    clearZipcodeData();
    onClose();
  };

  return (
    <Card 
      elevation={8}
      sx={{
        position: 'absolute',
        top: 16,
        right: 16,
        width: 320,
        backgroundColor: 'rgba(0, 0, 0, 0.9)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(0, 217, 255, 0.3)',
        borderRadius: 2,
        zIndex: 1000,
      }}
    >
      <CardHeader
        title={
          <Stack direction="row" spacing={1} alignItems="center">
            <LocationOnOutlined sx={{ color: '#00D9FF', fontSize: '1.2rem' }} />
            <Typography variant="h6" sx={{ color: '#00D9FF', fontWeight: 600 }}>
              ZIP {currentZipcode}
            </Typography>
          </Stack>
        }
        action={
          <IconButton 
            size="small" 
            onClick={handleClose}
            sx={{ color: 'rgba(255, 255, 255, 0.6)' }}
          >
            <CloseOutlined fontSize="small" />
          </IconButton>
        }
        sx={{ pb: 1 }}
      />
      
      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.1)' }} />
      
      <CardContent sx={{ pt: 2 }}>
        <Stack spacing={2}>
          {/* Demographics */}
          {zipcodeData.demographics && (
            <Box>
              <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.8)', mb: 1 }}>
                Demographics
              </Typography>
              <Stack spacing={1}>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Population:
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#00D9FF' }}>
                    {formatNumber(zipcodeData.demographics.total_population)}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Median Income:
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#00D9FF' }}>
                    {formatCurrency(zipcodeData.demographics.median_household_income)}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Median Home Value:
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#00D9FF' }}>
                    {formatCurrency(zipcodeData.demographics.median_home_value)}
                  </Typography>
                </Stack>
              </Stack>
            </Box>
          )}

          {/* Age Distribution */}
          {zipcodeData.ageDistribution && (
            <Box>
              <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.8)', mb: 1 }}>
                Age Distribution
              </Typography>
              <Stack spacing={0.5}>
                {Object.entries(zipcodeData.ageDistribution.age_groups).map(([age, percentage]) => (
                  <Stack key={age} direction="row" justifyContent="space-between">
                    <Typography variant="caption" color="text.secondary">
                      {age.replace('_', '-')}:
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#00D9FF' }}>
                      {String(percentage)}%
                    </Typography>
                  </Stack>
                ))}
              </Stack>
            </Box>
          )}

          {/* Businesses */}
          {zipcodeData.businesses && (
            <Box>
              <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.8)', mb: 1 }}>
                Motor Boat Businesses
              </Typography>
              <Stack direction="row" spacing={1} alignItems="center">
                <Chip 
                  label={`${(zipcodeData.businesses as any)?.total_results || 0} found`}
                  size="small"
                  sx={{ 
                    backgroundColor: 'rgba(0, 217, 255, 0.2)',
                    color: '#00D9FF',
                    border: '1px solid rgba(0, 217, 255, 0.3)'
                  }}
                />
              </Stack>
            </Box>
          )}

          {/* Data Source */}
          <Box>
            <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic' }}>
              Real data from US Census Bureau & Google Places API
            </Typography>
          </Box>

          {/* Loading State */}
          {zipcodeData.loading && (
            <Box sx={{ textAlign: 'center', py: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Loading ZIP code data...
              </Typography>
            </Box>
          )}

          {/* Error State */}
          {zipcodeData.error && (
            <Box sx={{ textAlign: 'center', py: 2 }}>
              <Typography variant="body2" color="error">
                {zipcodeData.error}
              </Typography>
            </Box>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
}
