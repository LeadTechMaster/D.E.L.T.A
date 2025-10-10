import { Box, ToggleButton, ToggleButtonGroup, styled } from '@mui/material';
import MapOutlinedIcon from '@mui/icons-material/MapOutlined';
import TerrainOutlinedIcon from '@mui/icons-material/TerrainOutlined';
import WbSunnyOutlinedIcon from '@mui/icons-material/WbSunnyOutlined';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import SatelliteAltOutlinedIcon from '@mui/icons-material/SatelliteAltOutlined';
import LayersOutlinedIcon from '@mui/icons-material/LayersOutlined';

const StyledToggleButtonGroup = styled(ToggleButtonGroup)(() => ({
  backgroundColor: 'rgba(0, 0, 0, 0.8)',
  backdropFilter: 'blur(10px)',
  borderRadius: '8px',
  padding: '4px',
  gap: '4px',
  border: '1px solid rgba(255, 255, 255, 0.1)',
}));

const StyledToggleButton = styled(ToggleButton)(() => ({
  color: 'rgba(255, 255, 255, 0.7)',
  border: 'none',
  borderRadius: '6px',
  padding: '8px 16px',
  fontSize: '0.875rem',
  textTransform: 'none',
  fontWeight: 500,
  gap: '6px',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    color: 'rgba(255, 255, 255, 0.9)',
  },
  '&.Mui-selected': {
    backgroundColor: 'rgba(0, 217, 255, 0.2)',
    color: '#00D9FF',
    '&:hover': {
      backgroundColor: 'rgba(0, 217, 255, 0.3)',
    },
  },
  '& .MuiSvgIcon-root': {
    fontSize: '1.2rem',
  },
}));

export type MapStyle = 'street' | 'outdoor' | 'light' | 'dark' | 'satellite' | 'hybrid';

interface MapStyleSwitcherProps {
  value: MapStyle;
  onChange: (style: MapStyle) => void;
}

const mapStyles = [
  { value: 'street' as MapStyle, label: 'Street', icon: <MapOutlinedIcon /> },
  { value: 'outdoor' as MapStyle, label: 'Outdoor', icon: <TerrainOutlinedIcon /> },
  { value: 'light' as MapStyle, label: 'Light', icon: <WbSunnyOutlinedIcon /> },
  { value: 'dark' as MapStyle, label: 'Dark', icon: <DarkModeOutlinedIcon /> },
  { value: 'satellite' as MapStyle, label: 'Satellite', icon: <SatelliteAltOutlinedIcon /> },
  { value: 'hybrid' as MapStyle, label: 'Hybrid', icon: <LayersOutlinedIcon /> },
];

export default function MapStyleSwitcher({ value, onChange }: MapStyleSwitcherProps) {
  const handleChange = (_event: React.MouseEvent<HTMLElement>, newStyle: MapStyle | null) => {
    if (newStyle !== null) {
      onChange(newStyle);
    }
  };

  return (
    <Box
      sx={{
        position: 'absolute',
        top: 16,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 1000,
      }}
    >
      <StyledToggleButtonGroup
        value={value}
        exclusive
        onChange={handleChange}
        aria-label="map style"
      >
        {mapStyles.map((style) => (
          <StyledToggleButton key={style.value} value={style.value} aria-label={style.label}>
            {style.icon}
            {style.label}
          </StyledToggleButton>
        ))}
      </StyledToggleButtonGroup>
    </Box>
  );
}