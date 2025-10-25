import { Card, CardHeader, CardContent, Typography, Stack, Divider, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { LineChart } from '@mui/x-charts/LineChart';
import type { KeywordDemandData } from '../../types/schema';
import { formatNumber, formatCurrency } from '../../utils/formatters';

interface DemandPanelProps {
  data: KeywordDemandData;
}

export default function DemandPanel({ data }: DemandPanelProps) {
  return (
    <Card elevation={3}>
      <CardHeader 
        title="Keyword Demand Analysis" 
        subheader="Search trends and volume"
        titleTypographyProps={{ variant: 'h6', fontWeight: 600 }}
      />
      <Divider />
      <CardContent>
        <Stack spacing={3}>
          {/* Top Keywords Table */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Top Keywords
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Keyword</TableCell>
                    <TableCell align="right">Monthly Searches</TableCell>
                    <TableCell align="right">CPC</TableCell>
                    <TableCell align="right">Competition</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.top_keywords.map((keyword, index) => (
                    <TableRow key={index} hover>
                      <TableCell sx={{ fontWeight: 500 }}>{keyword.keyword}</TableCell>
                      <TableCell align="right">{formatNumber(keyword.monthly_searches)}</TableCell>
                      <TableCell align="right">{formatCurrency(keyword.cpc)}</TableCell>
                      <TableCell align="right">
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            color: keyword.competition > 0.8 ? 'error.main' : keyword.competition > 0.5 ? 'warning.main' : 'success.main',
                            fontWeight: 600
                          }}
                        >
                          {(keyword.competition * 100).toFixed(0)}%
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Stack>

          <Divider />

          {/* Trend Chart */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Search Volume Trend
            </Typography>
            <LineChart
              dataset={data.trend_data as any}
              xAxis={[{ 
                scaleType: 'band', 
                dataKey: 'month',
                tickLabelStyle: { fontSize: 12 }
              }]}
              series={[
                { 
                  dataKey: 'volume', 
                  label: 'Monthly Searches',
                  color: '#10B981',
                  curve: 'natural',
                  showMark: true
                }
              ]}
              height={250}
              margin={{ top: 10, bottom: 30, left: 60, right: 10 }}
            />
          </Stack>

          {/* Summary Stats */}
          <Stack direction="row" spacing={3} sx={{ flexWrap: 'wrap' }}>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Total Monthly Searches
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600, color: 'primary.main' }}>
                {formatNumber(data.top_keywords.reduce((sum, k) => sum + k.monthly_searches, 0))}
              </Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Average CPC
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                {formatCurrency(data.top_keywords.reduce((sum, k) => sum + k.cpc, 0) / data.top_keywords.length)}
              </Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Avg Competition
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                {((data.top_keywords.reduce((sum, k) => sum + k.competition, 0) / data.top_keywords.length) * 100).toFixed(0)}%
              </Typography>
            </Stack>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}