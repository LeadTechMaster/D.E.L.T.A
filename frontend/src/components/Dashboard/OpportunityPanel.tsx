import { Card, CardHeader, CardContent, Typography, Stack, Divider, LinearProgress, Chip, Box } from '@mui/material';
import { RadarChart } from '@mui/x-charts/RadarChart';
import type { OpportunityIndexData } from '../../types/schema';
import { formatScore, formatRiskLevel, formatRecommendedAction } from '../../utils/formatters';

interface OpportunityPanelProps {
  data: OpportunityIndexData;
}

export default function OpportunityPanel({ data }: OpportunityPanelProps) {
  const radarData = [
    { metric: 'Demand', value: data.demand_score },
    { metric: 'Competition', value: 100 - data.competition_score },
    { metric: 'Spending Power', value: data.spending_power_score }
  ];

  const getScoreColor = (score: number) => {
    if (score >= 75) return 'success.main';
    if (score >= 50) return 'warning.main';
    return 'error.main';
  };

  const getRiskColor = (risk: string) => {
    if (risk === 'low') return 'success';
    if (risk === 'moderate') return 'warning';
    return 'error';
  };

  return (
    <Card elevation={3}>
      <CardHeader 
        title="Opportunity Index" 
        subheader="Market opportunity analysis"
        titleTypographyProps={{ variant: 'h6', fontWeight: 600 }}
      />
      <Divider />
      <CardContent>
        <Stack spacing={3}>
          {/* Overall Score */}
          <Stack spacing={2} alignItems="center">
            <Typography variant="h2" sx={{ fontWeight: 700, color: getScoreColor(data.overall_score) }}>
              {formatScore(data.overall_score)}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Overall Opportunity Score
            </Typography>
            <Chip 
              label={formatRecommendedAction(data.recommended_action)}
              color={getRiskColor(data.risk_assessment) as any}
              sx={{ fontWeight: 600 }}
            />
          </Stack>

          <Divider />

          {/* Score Breakdown */}
          <Stack spacing={2}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Score Breakdown
            </Typography>
            
            <Stack spacing={1}>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="body2">Demand Score</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600, color: getScoreColor(data.demand_score) }}>
                  {data.demand_score}/100
                </Typography>
              </Stack>
              <LinearProgress 
                variant="determinate" 
                value={data.demand_score} 
                sx={{ height: 8, borderRadius: 1 }}
              />
            </Stack>

            <Stack spacing={1}>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="body2">Competition Score</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600, color: getScoreColor(100 - data.competition_score) }}>
                  {100 - data.competition_score}/100
                </Typography>
              </Stack>
              <LinearProgress 
                variant="determinate" 
                value={100 - data.competition_score} 
                sx={{ height: 8, borderRadius: 1 }}
                color="warning"
              />
            </Stack>

            <Stack spacing={1}>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="body2">Spending Power Score</Typography>
                <Typography variant="body2" sx={{ fontWeight: 600, color: getScoreColor(data.spending_power_score) }}>
                  {data.spending_power_score}/100
                </Typography>
              </Stack>
              <LinearProgress 
                variant="determinate" 
                value={data.spending_power_score} 
                sx={{ height: 8, borderRadius: 1 }}
                color="success"
              />
            </Stack>
          </Stack>

          <Divider />

          {/* Radar Chart */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Opportunity Radar
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
              <RadarChart
                series={[
                  {
                    data: radarData.map(d => d.value),
                    label: 'Score',
                    valueFormatter: (v: number) => `${v}/100`
                  }
                ]}
                radar={{
                  metrics: radarData.map(d => d.metric)
                }}
                height={250}
                margin={{ top: 20, bottom: 20, left: 20, right: 20 }}
              />
            </Box>
          </Stack>

          <Divider />

          {/* Insights */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Key Insights
            </Typography>
            <Stack spacing={1}>
              {data.insights.map((insight, index) => (
                <Typography 
                  key={index} 
                  variant="body2" 
                  sx={{ 
                    pl: 2, 
                    position: 'relative',
                    '&::before': {
                      content: '"•"',
                      position: 'absolute',
                      left: 0,
                      color: 'primary.main'
                    }
                  }}
                >
                  {insight}
                </Typography>
              ))}
            </Stack>
          </Stack>

          {/* Risk Assessment */}
          <Stack direction="row" spacing={2} alignItems="center" sx={{ pt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Risk Level:
            </Typography>
            <Chip 
              label={formatRiskLevel(data.risk_assessment)}
              color={getRiskColor(data.risk_assessment) as any}
              size="small"
            />
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}