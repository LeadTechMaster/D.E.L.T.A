import { Box, Stack, Alert, Button, CircularProgress } from '@mui/material';
import { useState } from 'react';
import { useAppSelector } from '../../store/hooks';
import { ViewMode } from '../../types/enums';
import DashboardHeader from './DashboardHeader';
import MapView from './MapView';
import DemographicsPanel from './DemographicsPanel';
import DemandPanel from './DemandPanel';
import CompetitorPanel from './CompetitorPanel';
import OpportunityPanel from './OpportunityPanel';
import CapabilitiesPage from '../CapabilitiesPage';
import { useDataWithFallback } from '../../hooks/useRealData';

interface DashboardProps {
  projectName: string;
  lastSaved: Date;
  userName: string;
}

export default function Dashboard({ projectName, lastSaved, userName }: DashboardProps) {
  const [showCapabilities, setShowCapabilities] = useState(false);
  const activeViewMode = useAppSelector((state) => state.map.activeViewMode);
  const mapCenter = useAppSelector((state) => state.map.mapCenter);
  const mapZoom = useAppSelector((state) => state.map.mapZoom);
  
  // Use real data with fallback to mock data
  const { 
    demographics, 
    competitors, 
    keywordDemand, 
    opportunityIndex, 
    loading, 
    error, 
    isRealData, 
    refetch 
  } = useDataWithFallback('Seattle, WA', 'motor boat');

  const handleSave = () => {
    console.log('Saving project...');
    // TODO: Implement save functionality
  };

  const handleShare = () => {
    console.log('Sharing project...');
    // TODO: Implement share functionality
  };

  const handleShowCapabilities = () => {
    setShowCapabilities(true);
  };

  const handleCloseCapabilities = () => {
    setShowCapabilities(false);
  };

  const renderMapView = () => (
    <Box sx={{ flex: 1, position: 'relative', height: '100%' }}>
      <MapView 
        center={mapCenter} 
        zoom={mapZoom} 
        businesses={competitors?.map(comp => ({
          name: comp.name,
          rating: comp.rating,
          user_ratings_total: comp.review_count,
          coordinates: {
            latitude: comp.lat,
            longitude: comp.lng
          }
        }))}
      />
    </Box>
  );

  const renderDashboardView = () => {
    if (loading) {
      return (
        <Box 
          sx={{ 
            flex: 1, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            flexDirection: 'column',
            gap: 2
          }}
        >
          <CircularProgress size={60} />
          <Box sx={{ color: 'text.secondary' }}>
            Loading real market data...
          </Box>
        </Box>
      );
    }

    return (
      <Box 
        sx={{ 
          flex: 1, 
          overflow: 'auto', 
          p: 3,
          bgcolor: 'background.default'
        }}
      >
        <Stack spacing={3}>
          {/* Data source indicator */}
          {error && (
            <Alert 
              severity="error" 
              action={
                <Button color="inherit" size="small" onClick={refetch}>
                  Retry
                </Button>
              }
            >
              Failed to load real data: {error}
            </Alert>
          )}
          
          {isRealData && (
            <Alert severity="success">
              ✅ Real data loaded from backend APIs - {competitors?.length || 0} motor boat businesses found in Seattle area
            </Alert>
          )}

          <Stack direction="row" spacing={3} sx={{ flexWrap: 'wrap' }}>
            <Box sx={{ flex: '1 1 600px', minWidth: 0 }}>
              {demographics && <DemographicsPanel data={demographics} />}
            </Box>
            <Box sx={{ flex: '1 1 600px', minWidth: 0 }}>
              {keywordDemand && <DemandPanel data={keywordDemand} />}
            </Box>
          </Stack>
          <Stack direction="row" spacing={3} sx={{ flexWrap: 'wrap' }}>
            <Box sx={{ flex: '1 1 600px', minWidth: 0 }}>
              {competitors && <CompetitorPanel competitors={competitors} />}
            </Box>
            <Box sx={{ flex: '1 1 600px', minWidth: 0 }}>
              {opportunityIndex && <OpportunityPanel data={opportunityIndex} />}
            </Box>
          </Stack>
          <Stack direction="row" spacing={3} sx={{ flexWrap: 'wrap' }}>
            {/* ZIP Code analysis is now integrated into MapView */}
          </Stack>
        </Stack>
      </Box>
    );
  };

  const renderContent = () => {
    switch (activeViewMode) {
      case ViewMode.MAP:
        return renderMapView();
      case ViewMode.DASHBOARD:
        return renderDashboardView();
      case ViewMode.SPLIT:
        return (
          <Stack direction="row" sx={{ flex: 1, height: '100%' }}>
            <Box sx={{ flex: 1, height: '100%' }}>
              {renderMapView()}
            </Box>
            <Box sx={{ flex: 1, height: '100%', overflow: 'auto' }}>
              {renderDashboardView()}
            </Box>
          </Stack>
        );
      default:
        return renderMapView();
    }
  };

  return (
    <Stack sx={{ height: '100vh', width: '100%' }}>
      <DashboardHeader
        projectName={projectName}
        lastSaved={lastSaved}
        userName={userName}
        onSave={handleSave}
        onShare={handleShare}
        onShowCapabilities={handleShowCapabilities}
      />
      <Box sx={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {renderContent()}
      </Box>
      
      {/* Capabilities Modal */}
      <CapabilitiesPage 
        open={showCapabilities} 
        onClose={handleCloseCapabilities} 
      />
    </Stack>
  );
}