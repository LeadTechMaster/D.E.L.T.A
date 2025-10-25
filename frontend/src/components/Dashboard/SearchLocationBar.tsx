import { useState, useRef, useEffect } from 'react';
import { Box, InputBase, IconButton, Paper, List, ListItem, ListItemText, CircularProgress, styled } from '@mui/material';
import LocationOnOutlinedIcon from '@mui/icons-material/LocationOnOutlined';
import CloseOutlinedIcon from '@mui/icons-material/CloseOutlined';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';

const SearchContainer = styled(Paper)(() => ({
  backgroundColor: 'rgba(0, 0, 0, 0.8)',
  backdropFilter: 'blur(10px)',
  borderRadius: '8px',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  display: 'flex',
  alignItems: 'center',
  padding: '4px 12px',
  minWidth: '400px',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    border: '1px solid rgba(0, 217, 255, 0.3)',
  },
  '&:focus-within': {
    backgroundColor: 'rgba(0, 0, 0, 0.95)',
    border: '1px solid rgba(0, 217, 255, 0.5)',
    boxShadow: '0 0 0 2px rgba(0, 217, 255, 0.1)',
  },
}));

const StyledInputBase = styled(InputBase)(() => ({
  flex: 1,
  color: 'rgba(255, 255, 255, 0.9)',
  fontSize: '0.875rem',
  '& input': {
    padding: '8px 8px',
    '&::placeholder': {
      color: 'rgba(255, 255, 255, 0.5)',
      opacity: 1,
    },
  },
}));

const SuggestionsContainer = styled(Paper)(() => ({
  position: 'absolute',
  top: '100%',
  left: 0,
  right: 0,
  marginTop: '8px',
  backgroundColor: 'rgba(0, 0, 0, 0.95)',
  backdropFilter: 'blur(10px)',
  borderRadius: '8px',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  maxHeight: '300px',
  overflow: 'auto',
  zIndex: 1001,
}));

const SuggestionItem = styled(ListItem)(() => ({
  cursor: 'pointer',
  color: 'rgba(255, 255, 255, 0.9)',
  transition: 'all 0.2s ease',
  '&:hover': {
    backgroundColor: 'rgba(0, 217, 255, 0.1)',
  },
}));

interface SearchLocationBarProps {
  onLocationSelect: (location: { lat: number; lng: number; name: string }) => void;
  onZipcodeSelect?: (zipcode: string) => void;
}

interface Suggestion {
  id: string;
  place_name: string;
  center: [number, number];
}

export default function SearchLocationBar({ onLocationSelect, onZipcodeSelect }: SearchLocationBarProps) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const timeoutRef = useRef<number | undefined>(undefined);

  const searchLocation = async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setSuggestions([]);
      return;
    }

    setLoading(true);
    try {
      const accessToken = import.meta.env.VITE_MAPBOX_TOKEN || 'YOUR_MAPBOX_TOKEN_HERE';
      const response = await fetch(
        `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(searchQuery)}.json?access_token=${accessToken}&types=place,locality,neighborhood,address&limit=5`
      );
      const data = await response.json();
      setSuggestions(data.features || []);
      setShowSuggestions(true);
    } catch (error) {
      console.error('Error searching location:', error);
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setQuery(value);

    // Check if user typed a 5-digit ZIP code directly
    const zipcodeMatch = value.match(/^\d{5}$/);
    if (zipcodeMatch && onZipcodeSelect) {
      onZipcodeSelect(zipcodeMatch[1]);
      setShowSuggestions(false);
      setSuggestions([]);
      return;
    }

    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = window.setTimeout(() => {
      searchLocation(value);
    }, 300);
  };

  const handleSuggestionClick = (suggestion: Suggestion) => {
    setQuery(suggestion.place_name);
    setShowSuggestions(false);
    
    // Check if this is a ZIP code (5-digit number)
    const zipcodeMatch = suggestion.place_name.match(/\b(\d{5})\b/);
    if (zipcodeMatch && onZipcodeSelect) {
      onZipcodeSelect(zipcodeMatch[1]);
    }
    
    onLocationSelect({
      lat: suggestion.center[1],
      lng: suggestion.center[0],
      name: suggestion.place_name,
    });
  };

  const handleClear = () => {
    setQuery('');
    setSuggestions([]);
    setShowSuggestions(false);
  };

  useEffect(() => {
    const currentTimeout = timeoutRef.current;
    return () => {
      if (currentTimeout !== undefined) {
        window.clearTimeout(currentTimeout);
      }
    };
  }, []);

  return (
    <Box
      sx={{
        position: 'absolute',
        top: 80,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 1000,
        width: '100%',
        maxWidth: '500px',
        px: 2,
      }}
    >
      <Box sx={{ position: 'relative' }}>
        <SearchContainer elevation={0}>
          <LocationOnOutlinedIcon sx={{ color: '#00D9FF', mr: 1, fontSize: '1.5rem' }} />
          <StyledInputBase
            placeholder="Search Location"
            value={query}
            onChange={handleInputChange}
            onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
          />
          {loading && <CircularProgress size={20} sx={{ color: '#00D9FF', mr: 1 }} />}
          {query && !loading && (
            <IconButton size="small" onClick={handleClear} sx={{ color: 'rgba(255, 255, 255, 0.5)' }}>
              <CloseOutlinedIcon fontSize="small" />
            </IconButton>
          )}
          {!query && !loading && (
            <SearchOutlinedIcon sx={{ color: 'rgba(255, 255, 255, 0.3)', fontSize: '1.2rem' }} />
          )}
        </SearchContainer>

        {showSuggestions && suggestions.length > 0 && (
          <SuggestionsContainer elevation={0}>
            <List sx={{ py: 0 }}>
              {suggestions.map((suggestion) => (
                <SuggestionItem
                  key={suggestion.id}
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  <LocationOnOutlinedIcon sx={{ color: '#00D9FF', mr: 2, fontSize: '1.2rem' }} />
                  <ListItemText
                    primary={suggestion.place_name}
                    primaryTypographyProps={{
                      fontSize: '0.875rem',
                      fontWeight: 500,
                    }}
                  />
                </SuggestionItem>
              ))}
            </List>
          </SuggestionsContainer>
        )}
      </Box>
    </Box>
  );
}