import { Card, CardHeader, CardContent, Typography, Stack, Divider, List, ListItem, ListItemText, Rating, Chip } from '@mui/material';
import { BarChart } from '@mui/x-charts/BarChart';
import type { CompetitorData } from '../../types/schema';
import { formatNumber, formatPriceLevel } from '../../utils/formatters';

interface CompetitorPanelProps {
  competitors: CompetitorData[];
}

export default function CompetitorPanel({ competitors }: CompetitorPanelProps) {
  const sortedCompetitors = [...competitors].sort((a, b) => b.review_count - a.review_count).slice(0, 10);
  
  const ratingDistribution = [
    { rating: '5 ★', count: competitors.filter(c => c.rating >= 4.5).length },
    { rating: '4 ★', count: competitors.filter(c => c.rating >= 4 && c.rating < 4.5).length },
    { rating: '3 ★', count: competitors.filter(c => c.rating >= 3 && c.rating < 4).length },
    { rating: '< 3 ★', count: competitors.filter(c => c.rating < 3).length }
  ];

  const avgRating = competitors.reduce((sum, c) => sum + c.rating, 0) / competitors.length;
  const totalReviews = competitors.reduce((sum, c) => sum + c.review_count, 0);

  return (
    <Card elevation={3}>
      <CardHeader 
        title="Competitor Landscape" 
        subheader={`${competitors.length} competitors found`}
        titleTypographyProps={{ variant: 'h6', fontWeight: 600 }}
      />
      <Divider />
      <CardContent>
        <Stack spacing={3}>
          {/* Summary Stats */}
          <Stack direction="row" spacing={3} sx={{ flexWrap: 'wrap' }}>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Average Rating
              </Typography>
              <Stack direction="row" spacing={1} alignItems="center">
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {avgRating.toFixed(1)}
                </Typography>
                <Rating value={avgRating} precision={0.1} size="small" readOnly />
              </Stack>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Total Reviews
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600, color: 'info.main' }}>
                {formatNumber(totalReviews)}
              </Typography>
            </Stack>
            <Stack spacing={0.5}>
              <Typography variant="caption" color="text.secondary">
                Total Competitors
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                {competitors.length}
              </Typography>
            </Stack>
          </Stack>

          <Divider />

          {/* Rating Distribution */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Rating Distribution
            </Typography>
            <BarChart
              dataset={ratingDistribution}
              xAxis={[{ scaleType: 'band', dataKey: 'rating' }]}
              series={[
                { 
                  dataKey: 'count', 
                  label: 'Number of Businesses',
                  color: '#F59E0B'
                }
              ]}
              height={200}
              margin={{ top: 10, bottom: 30, left: 40, right: 10 }}
            />
          </Stack>

          <Divider />

          {/* Top Competitors List */}
          <Stack spacing={1}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Top Competitors by Reviews
            </Typography>
            <List dense>
              {sortedCompetitors.map((competitor, index) => (
                <ListItem 
                  key={index}
                  sx={{ 
                    bgcolor: 'background.default', 
                    mb: 1, 
                    borderRadius: 1,
                    border: '1px solid',
                    borderColor: 'divider'
                  }}
                >
                  <ListItemText
                    primary={competitor.name}
                    primaryTypographyProps={{
                      variant: 'body2',
                      sx: { fontWeight: 600 }
                    }}
                    secondary={
                      <Stack component="span" direction="row" spacing={1} alignItems="center" sx={{ mt: 0.5 }}>
                        <Rating value={competitor.rating} precision={0.1} size="small" readOnly />
                        <Typography component="span" variant="caption" color="text.secondary">
                          {formatNumber(competitor.review_count)} reviews
                        </Typography>
                      </Stack>
                    }
                  />
                  <Chip 
                    label={formatPriceLevel(competitor.price_level)} 
                    size="small" 
                    color="secondary"
                    sx={{ ml: 1 }}
                  />
                </ListItem>
              ))}
            </List>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}