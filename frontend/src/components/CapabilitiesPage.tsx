import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  Button, 
  Typography, 
  Box, 
  Stack, 
  Accordion, 
  AccordionSummary, 
  AccordionDetails, 
  Chip, 
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Card,
  CardContent,
  Alert
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Map as MapIcon,
  Analytics as AnalyticsIcon,
  Business as BusinessIcon,
  Search as SearchIcon,
  LocationOn as LocationIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Public as PublicIcon,
  Directions as DirectionsIcon,
  FilterList as FilterIcon,
  Speed as SpeedIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
  Star as StarIcon
} from '@mui/icons-material';

interface CapabilitiesPageProps {
  open: boolean;
  onClose: () => void;
}

export default function CapabilitiesPage({ open, onClose }: CapabilitiesPageProps) {
  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="lg" 
      fullWidth
      PaperProps={{
        sx: {
          backgroundColor: 'rgba(0, 0, 0, 0.95)',
          color: 'white',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)'
        }
      }}
    >
      <DialogTitle sx={{ 
        backgroundColor: 'rgba(59, 130, 246, 0.1)', 
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        display: 'flex',
        alignItems: 'center',
        gap: 2
      }}>
        <StarIcon sx={{ color: '#3B82F6' }} />
        <Typography variant="h4" sx={{ fontWeight: 600 }}>
          D.E.L.T.A 2 - Complete Capabilities Guide
        </Typography>
      </DialogTitle>

      <DialogContent sx={{ p: 3 }}>
        <Stack spacing={3}>
          {/* Introduction */}
          <Alert severity="info" sx={{ backgroundColor: 'rgba(59, 130, 246, 0.1)' }}>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
              Welcome to D.E.L.T.A 2 - Your Complete Location Intelligence Platform
            </Typography>
            <Typography>
              D.E.L.T.A 2 provides comprehensive market analysis using 100% real-time data from multiple authoritative sources. 
              Every piece of information comes directly from live APIs - no mock data, no placeholders, no fallbacks.
            </Typography>
          </Alert>

          {/* Core Features Overview */}
          <Card sx={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}>
            <CardContent>
              <Typography variant="h5" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <CheckCircleIcon sx={{ color: '#10B981' }} />
                Core Features Overview
              </Typography>
              <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
                <Stack sx={{ flex: 1 }}>
                  <List>
                    <ListItem>
                      <ListItemIcon><MapIcon sx={{ color: '#00D9FF' }} /></ListItemIcon>
                      <ListItemText primary="Interactive Map Analysis" secondary="Click anywhere for instant data" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><BusinessIcon sx={{ color: '#00D9FF' }} /></ListItemIcon>
                      <ListItemText primary="Real Competitor Data" secondary="Live Google Places API integration" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><AnalyticsIcon sx={{ color: '#00D9FF' }} /></ListItemIcon>
                      <ListItemText primary="Demographic Intelligence" secondary="US Census Bureau data" />
                    </ListItem>
                  </List>
                </Stack>
                <Stack sx={{ flex: 1 }}>
                  <List>
                    <ListItem>
                      <ListItemIcon><TrendingUpIcon sx={{ color: '#00D9FF' }} /></ListItemIcon>
                      <ListItemText primary="Search Trend Analysis" secondary="SerpAPI integration" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><DirectionsIcon sx={{ color: '#00D9FF' }} /></ListItemIcon>
                      <ListItemText primary="Distance & Travel Analysis" secondary="Mapbox isochrone data" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><LocationIcon sx={{ color: '#00D9FF' }} /></ListItemIcon>
                      <ListItemText primary="ZIP Code Intelligence" secondary="Granular location analysis" />
                    </ListItem>
                  </List>
                </Stack>
              </Stack>
            </CardContent>
          </Card>

          {/* Detailed Capabilities */}
          <Typography variant="h5" sx={{ fontWeight: 600, mb: 2 }}>
            Detailed Capabilities & How to Use Them
          </Typography>

          {/* Map Interaction */}
          <Accordion sx={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: 'white' }} />}>
              <Stack direction="row" spacing={2} alignItems="center">
                <MapIcon sx={{ color: '#3B82F6' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Interactive Map Analysis
                </Typography>
              </Stack>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                <Typography variant="body1">
                  The map is your primary tool for location intelligence. Every click provides real-time data.
                </Typography>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    🖱️ How to Use:
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><LocationIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Click anywhere on the map" 
                        secondary="Get instant demographic, business, and search trend data for that location"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><BusinessIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Click on blue business markers" 
                        secondary="View detailed competitor information including ratings, reviews, and distance"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><SearchIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Use the search bar" 
                        secondary="Search for specific locations, addresses, or ZIP codes"
                      />
                    </ListItem>
                  </List>
                </Box>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    📊 What You Get:
                  </Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    <Chip label="Population Demographics" color="primary" size="small" />
                    <Chip label="Business Count & Types" color="primary" size="small" />
                    <Chip label="Search Volume Trends" color="primary" size="small" />
                    <Chip label="Competitor Analysis" color="primary" size="small" />
                    <Chip label="Distance Calculations" color="primary" size="small" />
                  </Stack>
                </Box>
              </Stack>
            </AccordionDetails>
          </Accordion>

          {/* Distance & Travel Analysis */}
          <Accordion sx={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: 'white' }} />}>
              <Stack direction="row" spacing={2} alignItems="center">
                <DirectionsIcon sx={{ color: '#3B82F6' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Distance & Travel Analysis
                </Typography>
              </Stack>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                <Typography variant="body1">
                  Analyze travel times and distances using real Mapbox isochrone data.
                </Typography>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    🚗 Travel Modes:
                  </Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    <Chip label="🚗 Driving" color="secondary" size="small" />
                    <Chip label="🚶 Walking" color="secondary" size="small" />
                    <Chip label="🚴 Cycling" color="secondary" size="small" />
                    <Chip label="⭕ Radius Circle" color="secondary" size="small" />
                  </Stack>
                </Box>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    📏 How to Use:
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><SpeedIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Select travel mode" 
                        secondary="Choose how people will travel to your business"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><FilterIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Adjust distance/time" 
                        secondary="Set the radius or travel time for analysis"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><MapIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Click on map" 
                        secondary="See the reachable area from that point"
                      />
                    </ListItem>
                  </List>
                </Box>
              </Stack>
            </AccordionDetails>
          </Accordion>

          {/* ZIP Code Intelligence */}
          <Accordion sx={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: 'white' }} />}>
              <Stack direction="row" spacing={2} alignItems="center">
                <LocationIcon sx={{ color: '#3B82F6' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  ZIP Code Intelligence
                </Typography>
              </Stack>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                <Typography variant="body1">
                  Get granular demographic and business data for specific ZIP codes.
                </Typography>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    🎯 How to Use:
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><SearchIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Type a 5-digit ZIP code" 
                        secondary="Enter any US ZIP code in the search bar"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><AnalyticsIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="View detailed demographics" 
                        secondary="Age distribution, income, housing data from Census API"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><BusinessIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Analyze local businesses" 
                        secondary="See all motor boat businesses in that ZIP code"
                      />
                    </ListItem>
                  </List>
                </Box>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    📊 ZIP Code Data Includes:
                  </Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    <Chip label="Population Demographics" color="info" size="small" />
                    <Chip label="Age Distribution" color="info" size="small" />
                    <Chip label="Housing Data" color="info" size="small" />
                    <Chip label="Economic Indicators" color="info" size="small" />
                    <Chip label="Transportation Data" color="info" size="small" />
                    <Chip label="Business Locations" color="info" size="small" />
                  </Stack>
                </Box>
              </Stack>
            </AccordionDetails>
          </Accordion>

          {/* Heat Maps */}
          <Accordion sx={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: 'white' }} />}>
              <Stack direction="row" spacing={2} alignItems="center">
                <AssessmentIcon sx={{ color: '#3B82F6' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Heat Map Visualization
                </Typography>
              </Stack>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                <Typography variant="body1">
                  Visualize data density and patterns across the map using real demographic and business data.
                </Typography>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    🔥 Available Heat Map Types:
                  </Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    <Chip label="Population Density" color="warning" size="small" />
                    <Chip label="Business Density" color="warning" size="small" />
                    <Chip label="Competition Level" color="warning" size="small" />
                    <Chip label="Opportunity Index" color="warning" size="small" />
                  </Stack>
                </Box>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    📈 How to Use:
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><FilterIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Select data type" 
                        secondary="Choose what type of data to visualize"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><PublicIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Adjust density metric" 
                        secondary="View data per square kilometer or mile"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><MapIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Explore patterns" 
                        secondary="Identify high-opportunity areas and gaps"
                      />
                    </ListItem>
                  </List>
                </Box>
              </Stack>
            </AccordionDetails>
          </Accordion>

          {/* Data Sources */}
          <Accordion sx={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: 'white' }} />}>
              <Stack direction="row" spacing={2} alignItems="center">
                <PublicIcon sx={{ color: '#3B82F6' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Real-Time Data Sources
                </Typography>
              </Stack>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                <Typography variant="body1">
                  All data comes from authoritative, real-time APIs. No mock data, no placeholders, no fallbacks.
                </Typography>
                <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
                  <Stack sx={{ flex: 1 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                      📊 Demographic Data:
                    </Typography>
                    <List dense>
                      <ListItem>
                        <ListItemIcon><CheckCircleIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                        <ListItemText primary="US Census Bureau API" secondary="Population, income, age, housing" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon><CheckCircleIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                        <ListItemText primary="Real-time updates" secondary="2021 ACS 5-year estimates" />
                      </ListItem>
                    </List>
                  </Stack>
                  <Stack sx={{ flex: 1 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                      🏢 Business Data:
                    </Typography>
                    <List dense>
                      <ListItem>
                        <ListItemIcon><CheckCircleIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                        <ListItemText primary="Google Places API" secondary="Real business listings, ratings, reviews" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon><CheckCircleIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                        <ListItemText primary="Live competitor data" secondary="Up-to-date business information" />
                      </ListItem>
                    </List>
                  </Stack>
                  <Stack sx={{ flex: 1 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                      🔍 Search Trends:
                    </Typography>
                    <List dense>
                      <ListItem>
                        <ListItemIcon><CheckCircleIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                        <ListItemText primary="SerpAPI Integration" secondary="Real search volume and trends" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon><CheckCircleIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                        <ListItemText primary="Keyword analysis" secondary="Related searches and competition" />
                      </ListItem>
                    </List>
                  </Stack>
                  <Stack sx={{ flex: 1 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                      🗺️ Geographic Data:
                    </Typography>
                    <List dense>
                      <ListItem>
                        <ListItemIcon><CheckCircleIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                        <ListItemText primary="Mapbox API" secondary="Maps, geocoding, isochrones" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon><CheckCircleIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                        <ListItemText primary="Travel time analysis" secondary="Real routing and distance data" />
                      </ListItem>
                    </List>
                  </Stack>
                </Stack>
              </Stack>
            </AccordionDetails>
          </Accordion>

          {/* Best Practices */}
          <Accordion sx={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: 'white' }} />}>
              <Stack direction="row" spacing={2} alignItems="center">
                <StarIcon sx={{ color: '#3B82F6' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Best Practices & Tips
                </Typography>
              </Stack>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    💡 Pro Tips:
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><InfoIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Start with ZIP code analysis" 
                        secondary="Get detailed demographic data for your target area"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><InfoIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Use distance tools strategically" 
                        secondary="Analyze travel times from key population centers"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><InfoIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Compare multiple locations" 
                        secondary="Click different areas to compare demographics and competition"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><InfoIcon sx={{ color: '#10B981', fontSize: '1rem' }} /></ListItemIcon>
                      <ListItemText 
                        primary="Use heat maps to identify patterns" 
                        secondary="Look for gaps in competition or high-opportunity areas"
                      />
                    </ListItem>
                  </List>
                </Box>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                    ⚡ Quick Actions:
                  </Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    <Chip label="Click map for instant analysis" color="success" size="small" />
                    <Chip label="Search ZIP codes for details" color="success" size="small" />
                    <Chip label="Use distance tools for reach analysis" color="success" size="small" />
                    <Chip label="Toggle heat maps for patterns" color="success" size="small" />
                    <Chip label="Click competitors for details" color="success" size="small" />
                  </Stack>
                </Box>
              </Stack>
            </AccordionDetails>
          </Accordion>

          {/* Support */}
          <Card sx={{ backgroundColor: 'rgba(59, 130, 246, 0.1)' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                🆘 Need Help?
              </Typography>
              <Typography variant="body2">
                This system provides 100% real-time data from authoritative sources. If you see any issues or need assistance, 
                all data is sourced directly from live APIs including US Census Bureau, Google Places, SerpAPI, and Mapbox.
              </Typography>
            </CardContent>
          </Card>
        </Stack>
      </DialogContent>

      <DialogActions sx={{ 
        backgroundColor: 'rgba(0, 0, 0, 0.5)', 
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        p: 2
      }}>
        <Button 
          onClick={onClose} 
          variant="contained" 
          sx={{ 
            backgroundColor: '#3B82F6',
            '&:hover': { backgroundColor: '#2563EB' }
          }}
        >
          Got It - Let's Explore!
        </Button>
      </DialogActions>
    </Dialog>
  );
}
