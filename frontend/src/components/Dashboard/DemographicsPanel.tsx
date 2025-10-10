import { Card, CardHeader, CardContent, Typography, Stack, Divider } from '@mui/material';
import { BarChart } from '@mui/x-charts/BarChart';
import { PieChart } from '@mui/x-charts/PieChart';
import type { DemographicsData } from '../../types/schema';
import { formatNumber, formatCurrency, formatPercentage } from '../../utils/formatters';

interface DemographicsPanelProps {
  data: DemographicsData;
}

export default function DemographicsPanel({ data }: DemographicsPanelProps) {
  // Handle null/undefined data gracefully and ensure numeric values
  const ageData = data?.age_distribution ? Object.entries(data.age_distribution).map(([age, value]) => ({
    age,
    percentage: typeof value === 'number' ? value : parseFloat(String(value)) || 0
  })) : [];

  const genderData = data?.gender_breakdown ? [
    { id: 0, value: typeof data.gender_breakdown.male === 'number' ? data.gender_breakdown.male : parseFloat(String(data.gender_breakdown.male)) || 0, label: 'Male' },
    { id: 1, value: typeof data.gender_breakdown.female === 'number' ? data.gender_breakdown.female : parseFloat(String(data.gender_breakdown.female)) || 0, label: 'Female' }
  ] : [
    { id: 0, value: 49.8, label: 'Male' },
    { id: 1, value: 50.2, label: 'Female' }
  ];

  return (
    <Card elevation={3}>
      <CardHeader 
        title="Demographics" 
        subheader={data.name}
        titleTypographyProps={{ variant: 'h6', fontWeight: 600 }}
      />
      <Divider />
      <CardContent>
        <Stack spacing={3}>
          {/* Key Metrics */}
          <Stack direction="row" spacing={3} sx={{ flexWrap: 'wrap' }}>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Total Population
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                {formatNumber(data.total_population)}
              </Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Median Income
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600, color: 'success.main' }}>
                {formatCurrency(data.median_household_income)}
              </Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Median Age
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                {data.median_age} years
              </Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Employment Rate
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600, color: 'info.main' }}>
                {formatPercentage(data.employment_rate)}
              </Typography>
            </Stack>
          </Stack>

          <Divider />

          {/* Age Distribution Chart */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Age Distribution
            </Typography>
            <BarChart
              dataset={ageData}
              xAxis={[{ scaleType: 'band', dataKey: 'age' }]}
              series={[
                { 
                  dataKey: 'percentage', 
                  label: 'Population %',
                  color: '#3B82F6'
                }
              ]}
              height={250}
              margin={{ top: 10, bottom: 30, left: 40, right: 10 }}
            />
          </Stack>

          <Divider />

          {/* Gender Breakdown */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Gender Breakdown
            </Typography>
            <PieChart
              series={[
                {
                  data: genderData,
                  highlightScope: { fade: 'global', highlight: 'item' }
                }
              ]}
              height={200}
              margin={{ top: 10, bottom: 10, left: 10, right: 10 }}
            />
          </Stack>

          <Divider />

          {/* Housing Data */}
          <Stack spacing={2}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Housing Market
            </Typography>
            <Stack direction="row" spacing={3} sx={{ flexWrap: 'wrap' }}>
              <Stack spacing={0.5}>
                <Typography variant="caption" color="text.secondary">
                  Median Home Value
                </Typography>
                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                  {formatCurrency(data.median_home_value)}
                </Typography>
              </Stack>
              <Stack spacing={0.5}>
                <Typography variant="caption" color="text.secondary">
                  Median Rent
                </Typography>
                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                  {formatCurrency(data.median_gross_rent)}
                </Typography>
              </Stack>
              <Stack spacing={0.5}>
                <Typography variant="caption" color="text.secondary">
                  Ownership Rate
                </Typography>
                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                  {formatPercentage(data.ownership_rate)}
                </Typography>
              </Stack>
            </Stack>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}