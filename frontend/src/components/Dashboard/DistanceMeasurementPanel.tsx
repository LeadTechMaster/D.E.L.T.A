import { useState, useRef, useEffect } from 'react';
import { Box, Paper, Typography, IconButton, Slider, ToggleButton, ToggleButtonGroup, styled } from '@mui/material';
import CloseOutlinedIcon from '@mui/icons-material/CloseOutlined';
import MinimizeOutlinedIcon from '@mui/icons-material/MinimizeOutlined';
import DragIndicatorIcon from '@mui/icons-material/DragIndicator';
import DirectionsCarOutlinedIcon from '@mui/icons-material/DirectionsCarOutlined';
import DirectionsWalkOutlinedIcon from '@mui/icons-material/DirectionsWalkOutlined';
import DirectionsBikeOutlinedIcon from '@mui/icons-material/DirectionsBikeOutlined';
import RadioButtonUncheckedOutlinedIcon from '@mui/icons-material/RadioButtonUncheckedOutlined';

const PanelContainer = styled(Paper)(() => ({
  backgroundColor: 'rgba(0, 0, 0, 0.85)',
  backdropFilter: 'blur(10px)',
  borderRadius: '12px',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  padding: '16px',
  minWidth: '280px',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
  cursor: 'move',
  userSelect: 'none',
}));

const DragHandle = styled(Box)(() => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  cursor: 'grab',
  color: 'rgba(255, 255, 255, 0.3)',
  marginBottom: '8px',
  '&:active': {
    cursor: 'grabbing',
  },
}));

const ModeButton = styled(ToggleButton)(() => ({
  width: '48px',
  height: '48px',
  borderRadius: '50%',
  border: '2px solid rgba(255, 255, 255, 0.2)',
  color: 'rgba(255, 255, 255, 0.6)',
  backgroundColor: 'transparent',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  '&.Mui-selected': {
    backgroundColor: 'rgba(0, 217, 255, 0.15)',
    borderColor: '#00D9FF',
    color: '#00D9FF',
    '&:hover': {
      backgroundColor: 'rgba(0, 217, 255, 0.25)',
    },
  },
}));

const UnitButton = styled(ToggleButton)(() => ({
  padding: '4px 12px',
  fontSize: '0.75rem',
  fontWeight: 600,
  border: '1px solid rgba(255, 255, 255, 0.2)',
  color: 'rgba(255, 255, 255, 0.6)',
  backgroundColor: 'transparent',
  textTransform: 'none',
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
  },
  '&.Mui-selected': {
    backgroundColor: 'rgba(0, 217, 255, 0.2)',
    borderColor: '#00D9FF',
    color: '#00D9FF',
    '&:hover': {
      backgroundColor: 'rgba(0, 217, 255, 0.3)',
    },
  },
}));

export type TravelMode = 'driving' | 'walking' | 'cycling' | 'circle';
export type DistanceUnit = 'km' | 'mi';

interface DistanceMeasurementPanelProps {
  onClose: () => void;
  onModeChange?: (mode: TravelMode) => void;
  onDistanceChange?: (distance: number, unit: DistanceUnit) => void;
  initialPosition?: { x: number; y: number };
}

export default function DistanceMeasurementPanel({
  onClose,
  onModeChange,
  onDistanceChange,
  initialPosition = { x: 16, y: 16 },
}: DistanceMeasurementPanelProps) {
  const [mode, setMode] = useState<TravelMode>('cycling');
  const [distance, setDistance] = useState(1);
  const [unit, setUnit] = useState<DistanceUnit>('km');
  const [isMinimized, setIsMinimized] = useState(false);
  const [position, setPosition] = useState(initialPosition);
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const panelRef = useRef<HTMLDivElement>(null);

  const handleModeChange = (_event: React.MouseEvent<HTMLElement>, newMode: TravelMode | null) => {
    if (newMode !== null) {
      setMode(newMode);
      onModeChange?.(newMode);
    }
  };

  const handleUnitChange = (_event: React.MouseEvent<HTMLElement>, newUnit: DistanceUnit | null) => {
    if (newUnit !== null) {
      // Convert distance when changing units
      const convertedDistance = newUnit === 'mi' ? distance * 0.621371 : distance / 0.621371;
      setUnit(newUnit);
      setDistance(Math.round(convertedDistance * 10) / 10);
      onDistanceChange?.(convertedDistance, newUnit);
    }
  };

  const handleDistanceChange = (_event: Event, newValue: number | number[]) => {
    const value = Array.isArray(newValue) ? newValue[0] : newValue;
    // Round to nearest 100 meters (0.1 km)
    const roundedValue = Math.round(value * 10) / 10;
    setDistance(roundedValue);
    onDistanceChange?.(roundedValue, unit);
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('.no-drag')) return;
    
    setIsDragging(true);
    setDragOffset({
      x: e.clientX - position.x,
      y: e.clientY - position.y,
    });
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDragging) {
        setPosition({
          x: e.clientX - dragOffset.x,
          y: e.clientY - dragOffset.y,
        });
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  return (
    <Box
      ref={panelRef}
      sx={{
        position: 'absolute',
        top: position.y,
        left: position.x,
        zIndex: 1000,
      }}
      onMouseDown={handleMouseDown}
    >
      <PanelContainer elevation={0}>
        <DragHandle>
          <DragIndicatorIcon fontSize="small" />
        </DragHandle>
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600, flex: 1 }}>
            Distance
          </Typography>
          <Box className="no-drag" sx={{ display: 'flex', gap: 0.5 }}>
            <IconButton
              size="small"
              onClick={() => setIsMinimized(!isMinimized)}
              sx={{ color: 'rgba(255, 255, 255, 0.5)', '&:hover': { color: 'rgba(255, 255, 255, 0.8)' } }}
            >
              <MinimizeOutlinedIcon fontSize="small" />
            </IconButton>
            <IconButton
              size="small"
              onClick={onClose}
              sx={{ color: 'rgba(255, 255, 255, 0.5)', '&:hover': { color: 'rgba(255, 255, 255, 0.8)' } }}
            >
              <CloseOutlinedIcon fontSize="small" />
            </IconButton>
          </Box>
        </Box>

        {!isMinimized && (
          <>
            <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)', display: 'block', mb: 2 }}>
              Mode
            </Typography>

        <ToggleButtonGroup
          value={mode}
          exclusive
          onChange={handleModeChange}
          sx={{ display: 'flex', gap: 1.5, mb: 3 }}
        >
          <ModeButton value="driving" aria-label="driving">
            <DirectionsCarOutlinedIcon />
          </ModeButton>
          <ModeButton value="walking" aria-label="walking">
            <DirectionsWalkOutlinedIcon />
          </ModeButton>
          <ModeButton value="cycling" aria-label="cycling">
            <DirectionsBikeOutlinedIcon />
          </ModeButton>
          <ModeButton value="circle" aria-label="circle">
            <RadioButtonUncheckedOutlinedIcon />
          </ModeButton>
        </ToggleButtonGroup>

        <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)', display: 'block', mb: 1 }}>
          Distance
        </Typography>

        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <ToggleButtonGroup value={unit} exclusive onChange={handleUnitChange} size="small">
            <UnitButton value="mi">mi</UnitButton>
            <UnitButton value="km">km</UnitButton>
          </ToggleButtonGroup>
        </Box>

        <Box sx={{ px: 1 }}>
          <Slider
            value={distance}
            onChange={handleDistanceChange}
            min={0.1}
            max={unit === 'km' ? 10 : 6.2}
            step={0.1}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${value.toFixed(1)} ${unit}`}
            sx={{
              color: '#00D9FF',
              '& .MuiSlider-thumb': {
                width: 16,
                height: 16,
                backgroundColor: '#00D9FF',
                border: '2px solid #fff',
                '&:hover, &.Mui-focusVisible': {
                  boxShadow: '0 0 0 8px rgba(0, 217, 255, 0.16)',
                },
              },
              '& .MuiSlider-track': {
                height: 4,
                backgroundColor: '#00D9FF',
              },
              '& .MuiSlider-rail': {
                height: 4,
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
              },
            }}
          />
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 1 }}>
            <Typography
              variant="body2"
              sx={{
                color: '#00D9FF',
                fontWeight: 600,
                fontSize: '1rem',
              }}
            >
              {distance.toFixed(1)} {unit}
            </Typography>
          </Box>
        </Box>
          </>
        )}
      </PanelContainer>
    </Box>
  );
}