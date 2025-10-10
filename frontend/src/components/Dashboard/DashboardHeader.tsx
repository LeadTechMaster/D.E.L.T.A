import { AppBar, Toolbar, Typography, Button, IconButton, Stack, Chip } from '@mui/material';
import MapOutlinedIcon from '@mui/icons-material/MapOutlined';
import BentoOutlinedIcon from '@mui/icons-material/BentoOutlined';
import SplitscreenOutlinedIcon from '@mui/icons-material/SplitscreenOutlined';
import SaveOutlinedIcon from '@mui/icons-material/SaveOutlined';
import ShareOutlinedIcon from '@mui/icons-material/ShareOutlined';
import MoreVertOutlinedIcon from '@mui/icons-material/MoreVertOutlined';
import { ViewMode } from '../../types/enums';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { setViewMode } from '../../store/mapSlice';
import { formatTimeAgo } from '../../utils/formatters';

interface DashboardHeaderProps {
  projectName: string;
  lastSaved: Date;
  userName: string;
  onSave: () => void;
  onShare: () => void;
}

export default function DashboardHeader({ projectName, lastSaved, userName, onSave, onShare }: DashboardHeaderProps) {
  const dispatch = useAppDispatch();
  const activeViewMode = useAppSelector((state) => state.map.activeViewMode);

  const handleViewModeChange = (mode: ViewMode) => {
    dispatch(setViewMode(mode));
  };

  return (
    <AppBar position="static" elevation={2} sx={{ bgcolor: 'background.paper' }}>
      <Toolbar sx={{ gap: 2 }}>
        <Typography variant="h5" sx={{ fontWeight: 700, color: 'primary.main' }}>
          D.E.L.T.A
        </Typography>
        
        <Stack direction="row" spacing={1} sx={{ ml: 4 }}>
          <Button
            variant={activeViewMode === ViewMode.MAP ? 'contained' : 'outlined'}
            startIcon={<MapOutlinedIcon />}
            onClick={() => handleViewModeChange(ViewMode.MAP)}
            size="small"
          >
            Map
          </Button>
          <Button
            variant={activeViewMode === ViewMode.DASHBOARD ? 'contained' : 'outlined'}
            startIcon={<BentoOutlinedIcon />}
            onClick={() => handleViewModeChange(ViewMode.DASHBOARD)}
            size="small"
          >
            Dashboard
          </Button>
          <Button
            variant={activeViewMode === ViewMode.SPLIT ? 'contained' : 'outlined'}
            startIcon={<SplitscreenOutlinedIcon />}
            onClick={() => handleViewModeChange(ViewMode.SPLIT)}
            size="small"
          >
            Split
          </Button>
        </Stack>

        <Stack direction="row" spacing={1} alignItems="center" sx={{ ml: 'auto' }}>
          <Stack direction="column" alignItems="flex-end" spacing={0.5}>
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              {projectName}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Saved {formatTimeAgo(lastSaved)}
            </Typography>
          </Stack>
          
          <Button
            variant="contained"
            startIcon={<SaveOutlinedIcon />}
            onClick={onSave}
            size="small"
          >
            Save
          </Button>
          
          <Button
            variant="outlined"
            startIcon={<ShareOutlinedIcon />}
            onClick={onShare}
            size="small"
          >
            Share
          </Button>

          <Chip 
            label={userName} 
            size="small" 
            sx={{ ml: 2 }}
          />
          
          <IconButton size="small">
            <MoreVertOutlinedIcon />
          </IconButton>
        </Stack>
      </Toolbar>
    </AppBar>
  );
}