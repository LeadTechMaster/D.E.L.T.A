import { Box, IconButton, Tooltip, styled, Paper } from '@mui/material';
import CreateOutlinedIcon from '@mui/icons-material/CreateOutlined';
import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined';
import StraightenOutlinedIcon from '@mui/icons-material/StraightenOutlined';
import GridOnOutlinedIcon from '@mui/icons-material/GridOnOutlined';
import FolderOutlinedIcon from '@mui/icons-material/FolderOutlined';
import ContentCopyOutlinedIcon from '@mui/icons-material/ContentCopyOutlined';

const ToolbarContainer = styled(Paper)(() => ({
  backgroundColor: 'rgba(0, 0, 0, 0.85)',
  backdropFilter: 'blur(10px)',
  borderRadius: '12px',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  padding: '8px',
  display: 'flex',
  flexDirection: 'column',
  gap: '4px',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
}));

const ToolButton = styled(IconButton, {
  shouldForwardProp: (prop) => prop !== 'isActive',
})<{ isActive?: boolean }>(({ isActive }) => ({
  width: '40px',
  height: '40px',
  borderRadius: '8px',
  color: isActive ? '#00D9FF' : 'rgba(255, 255, 255, 0.6)',
  backgroundColor: isActive ? 'rgba(0, 217, 255, 0.15)' : 'transparent',
  border: isActive ? '1px solid #00D9FF' : '1px solid transparent',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: isActive ? 'rgba(0, 217, 255, 0.25)' : 'rgba(255, 255, 255, 0.05)',
    color: isActive ? '#00D9FF' : 'rgba(255, 255, 255, 0.9)',
    borderColor: isActive ? '#00D9FF' : 'rgba(255, 255, 255, 0.2)',
  },
}));

export type DrawingTool = 'pen' | 'time' | 'ruler' | 'grid' | 'folder' | 'copy' | null;

interface DrawingToolsToolbarProps {
  activeTool: DrawingTool;
  onToolChange: (tool: DrawingTool) => void;
}

const tools = [
  { id: 'pen' as DrawingTool, icon: <CreateOutlinedIcon />, label: 'Draw Polygon' },
  { id: 'time' as DrawingTool, icon: <AccessTimeOutlinedIcon />, label: 'Travel Time' },
  { id: 'ruler' as DrawingTool, icon: <StraightenOutlinedIcon />, label: 'Measure Distance' },
  { id: 'grid' as DrawingTool, icon: <GridOnOutlinedIcon />, label: 'Area Selection' },
  { id: 'folder' as DrawingTool, icon: <FolderOutlinedIcon />, label: 'Saved Shapes' },
  { id: 'copy' as DrawingTool, icon: <ContentCopyOutlinedIcon />, label: 'Copy Shape' },
];

export default function DrawingToolsToolbar({ activeTool, onToolChange }: DrawingToolsToolbarProps) {
  const handleToolClick = (toolId: DrawingTool) => {
    // Toggle tool - if clicking active tool, deactivate it
    onToolChange(activeTool === toolId ? null : toolId);
  };

  return (
    <Box
      sx={{
        position: 'absolute',
        left: 16,
        top: '50%',
        transform: 'translateY(-50%)',
        zIndex: 1000,
      }}
    >
      <ToolbarContainer elevation={0}>
        {tools.map((tool) => (
          <Tooltip key={tool.id} title={tool.label} placement="right" arrow>
            <ToolButton
              isActive={activeTool === tool.id}
              onClick={() => handleToolClick(tool.id)}
              size="small"
            >
              {tool.icon}
            </ToolButton>
          </Tooltip>
        ))}
      </ToolbarContainer>
    </Box>
  );
}