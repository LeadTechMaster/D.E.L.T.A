import { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { MAPBOX_ACCESS_TOKEN } from "@/config/mapbox";

interface SearchBarProps {
  onLocationSelect: (location: { lat: number; lng: number; name: string }) => void;
  onZipcodeSelect?: (zipcode: string) => void;
}

interface Suggestion {
  place_name: string;
  center: [number, number];
}

export function SearchBar({ onLocationSelect, onZipcodeSelect }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const debounceTimeout = useRef<NodeJS.Timeout>();
  const searchContainerRef = useRef<HTMLDivElement>(null);

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        searchContainerRef.current &&
        !searchContainerRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const searchLocation = async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setSuggestions([]);
      return;
    }

    setLoading(true);
    try {
      const accessToken = MAPBOX_ACCESS_TOKEN;
      console.log("Searching for:", searchQuery, "with token:", accessToken.substring(0, 20) + "...");

      // Check if it's a ZIP code (5 digits)
      const isZipCode = /^\d{5}$/.test(searchQuery.trim());
      const types = isZipCode ? "postcode" : "place,locality,neighborhood,address,postcode";

      const response = await fetch(
        `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(
          searchQuery
        )}.json?access_token=${accessToken}&types=${types}&limit=5`
      );

      if (!response.ok) {
        throw new Error(`Mapbox API error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Mapbox response:", data);
      setSuggestions(data.features || []);
      setShowSuggestions(true);
    } catch (error) {
      console.error("Error searching location:", error);
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);

    // Debounce the search
    if (debounceTimeout.current) {
      clearTimeout(debounceTimeout.current);
    }

    debounceTimeout.current = setTimeout(() => {
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

  return (
    <div className="fixed left-1/2 -translate-x-1/2 top-20 z-30" ref={searchContainerRef}>
      {/* Search Bar */}
      <div className="bg-[#1a1f2e]/40 backdrop-blur-md border border-[#2d3548]/50 shadow-xl p-2 transition-all hover:bg-[#1a1f2e] hover:border-[#2d3548] group rounded-none">
        {/* Search Input Container */}
        <div className="relative w-[400px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#8b92a7] transition-colors group-hover:text-[#00bcd4] z-10 pointer-events-none" />
          <Input
            type="text"
            placeholder="Search locations..."
            value={query}
            onChange={handleInputChange}
            onFocus={() => {
              if (suggestions.length > 0) {
                setShowSuggestions(true);
              }
            }}
            className="pl-10 h-9 bg-[#0a0a0a]/60 border-0 text-white placeholder:text-[#6b7280] cursor-text transition-all focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:outline-none focus:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)] rounded-none"
          />
          {loading && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-[#00bcd4]"></div>
            </div>
          )}
        </div>

        {/* Suggestions Dropdown */}
        {showSuggestions && suggestions.length > 0 && (
          <div className="absolute top-full left-0 right-0 mt-1 bg-[#1a1f2e] border border-[#2d3548] shadow-xl rounded-none overflow-hidden">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="w-full px-4 py-2 text-left text-sm text-white hover:bg-[#2d3548] transition-colors cursor-pointer border-b border-[#2d3548] last:border-b-0"
              >
                {suggestion.place_name}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

