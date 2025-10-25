import { useState, useRef, useEffect } from 'react';
import { Box, Paper, Typography, IconButton, Select, MenuItem, styled } from '@mui/material';
import CloseOutlinedIcon from '@mui/icons-material/CloseOutlined';
import MinimizeOutlinedIcon from '@mui/icons-material/MinimizeOutlined';
import WhatshotOutlinedIcon from '@mui/icons-material/WhatshotOutlined';
import GridOnOutlinedIcon from '@mui/icons-material/GridOnOutlined';
import DragIndicatorIcon from '@mui/icons-material/DragIndicator';

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

const StyledSelect = styled(Select)(() => ({
  backgroundColor: 'rgba(255, 255, 255, 0.05)',
  borderRadius: '6px',
  color: 'rgba(255, 255, 255, 0.9)',
  fontSize: '0.875rem',
  '& .MuiOutlinedInput-notchedOutline': {
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  '&:hover .MuiOutlinedInput-notchedOutline': {
    borderColor: 'rgba(0, 217, 255, 0.3)',
  },
  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
    borderColor: '#00D9FF',
  },
  '& .MuiSvgIcon-root': {
    color: 'rgba(255, 255, 255, 0.5)',
  },
}));

const GradientBar = styled(Box)(() => ({
  height: '24px',
  borderRadius: '4px',
  background: 'linear-gradient(to right, #2166ac, #67a9cf, #d1e5f0, #fddbc7, #ef8a62, #b2182b)',
  position: 'relative',
  marginTop: '8px',
  marginBottom: '8px',
}));

export type HeatmapDataType = 
  | 'population'
  | 'business_competition'
  | 'demographic_density'
  | 'foot_traffic'
  | 'market_opportunity'
  | 'income_wealth'
  | 'review_power';

interface HeatmapPanelProps {
  onClose: () => void;
  onDataTypeChange?: (dataType: HeatmapDataType) => void;
  initialPosition?: { x: number; y: number };
}

const dataTypes = [
  { value: 'population' as HeatmapDataType, label: 'Population' },
  { value: 'business_competition' as HeatmapDataType, label: 'Business Competition' },
  { value: 'demographic_density' as HeatmapDataType, label: 'Demographic Density' },
  { value: 'foot_traffic' as HeatmapDataType, label: 'Foot Traffic' },
  { value: 'market_opportunity' as HeatmapDataType, label: 'Market Opportunity' },
  { value: 'income_wealth' as HeatmapDataType, label: 'Income/Wealth' },
  { value: 'review_power' as HeatmapDataType, label: 'Review Power' },
];

export default function HeatmapPanel({ onClose, onDataTypeChange, initialPosition = { x: 16, y: 140 } }: HeatmapPanelProps) {
  const [dataType, setDataType] = useState<HeatmapDataType>('population');
  const [maxValue] = useState(14998); // This would come from actual data
  const [isMinimized, setIsMinimized] = useState(false);
  const [position, setPosition] = useState(initialPosition);
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const panelRef = useRef<HTMLDivElement>(null);

  const handleDataTypeChange = (event: any) => {
    const newType = event.target.value as HeatmapDataType;
    setDataType(newType);
    onDataTypeChange?.(newType);
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
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flex: 1 }}>
            <WhatshotOutlinedIcon sx={{ color: '#FF6B35', fontSize: '1.2rem' }} />
            <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.9)', fontWeight: 600 }}>
              Heat Maps
            </Typography>
          </Box>
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
            <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)', display: 'block', mb: 1 }}>
              Data Type
            </Typography>

        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <StyledSelect
            value={dataType}
            onChange={handleDataTypeChange}
            size="small"
            fullWidth
            MenuProps={{
              PaperProps: {
                sx: {
                  backgroundColor: 'rgba(0, 0, 0, 0.95)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  '& .MuiMenuItem-root': {
                    color: 'rgba(255, 255, 255, 0.9)',
                    fontSize: '0.875rem',
                    '&:hover': {
                      backgroundColor: 'rgba(0, 217, 255, 0.1)',
                    },
                    '&.Mui-selected': {
                      backgroundColor: 'rgba(0, 217, 255, 0.2)',
                      '&:hover': {
                        backgroundColor: 'rgba(0, 217, 255, 0.3)',
                      },
                    },
                  },
                },
              },
            }}
            className="no-drag"
          >
            {dataTypes.map((type) => (
              <MenuItem key={type.value} value={type.value}>
                {type.label}
              </MenuItem>
            ))}
          </StyledSelect>
          <IconButton
            size="small"
            className="no-drag"
            sx={{
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
              borderRadius: '6px',
              color: 'rgba(255, 255, 255, 0.6)',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                color: 'rgba(255, 255, 255, 0.9)',
              },
            }}
          >
            <GridOnOutlinedIcon fontSize="small" />
          </IconButton>
        </Box>

        <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)', display: 'block', mb: 1 }}>
          Density by km²
        </Typography>

        <GradientBar />

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '0.7rem' }}>
            Extremes
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '0.7rem' }}>
            Extremes
          </Typography>
        </Box>

        <Box sx={{ textAlign: 'center', mt: 2 }}>
          <Typography
            variant="h6"
            sx={{
              color: '#00D9FF',
              fontWeight: 700,
              fontSize: '1.25rem',
            }}
          >
            {maxValue.toLocaleString()}
          </Typography>
        </Box>
          </>
        )}
      </PanelContainer>
    </Box>
  );
}