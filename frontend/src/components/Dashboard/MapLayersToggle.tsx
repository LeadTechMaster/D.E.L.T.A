import { Box, IconButton, Tooltip, styled } from '@mui/material';
import LayersOutlinedIcon from '@mui/icons-material/LayersOutlined';

const ToggleButton = styled(IconButton)(() => ({
  width: '40px',
  height: '40px',
  backgroundColor: 'rgba(0, 0, 0, 0.85)',
  backdropFilter: 'blur(10px)',
  borderRadius: '8px',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  color: 'rgba(255, 255, 255, 0.6)',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: 'rgba(0, 0, 0, 0.95)',
    color: 'rgba(255, 255, 255, 0.9)',
    borderColor: 'rgba(0, 217, 255, 0.3)',
  },
}));

interface MapLayersToggleProps {
  onClick: () => void;
}

export default function MapLayersToggle({ onClick }: MapLayersToggleProps) {
  return (
    <Box
      sx={{
        position: 'absolute',
        top: 16,
        left: 16,
        zIndex: 999,
      }}
    >
      <Tooltip title="Map Layers" placement="right" arrow>
        <ToggleButton onClick={onClick} size="small">
          <LayersOutlinedIcon />
        </ToggleButton>
      </Tooltip>
    </Box>
  );
}