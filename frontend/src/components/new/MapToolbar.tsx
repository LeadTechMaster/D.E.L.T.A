import { Card } from "@/components/ui/card";
import { useState, useEffect } from "react";
import { Slider } from "@/components/ui/slider";
import { Car, Footprints, Bike, Circle, Building2, Search, MapIcon } from "lucide-react";
import { Input } from "@/components/ui/input";

// REMOVED: tools array (Pencil, Clock, Ruler, Grid) - no longer needed

interface MapToolbarProps {
  onPanelChange?: (isOpen: boolean, panelHeight: number) => void;
  activeTool?: string | null;
  onApplyAreaSelector?: (areaType: string, location: string) => void;
  isOpen?: boolean; // NEW: Control visibility from parent
}

export function MapToolbar({ onPanelChange, activeTool: externalActiveTool, onApplyAreaSelector, isOpen = false }: MapToolbarProps) {
  const [internalActiveTool, setInternalActiveTool] = useState<string | null>(null);
  const activeTool = externalActiveTool !== undefined ? externalActiveTool : internalActiveTool;
  const [travelMode, setTravelMode] = useState("driving");
  const [travelTime, setTravelTime] = useState([20]);
  const [distanceMode, setDistanceMode] = useState("driving");
  const [distance, setDistance] = useState([20]);
  const [distanceUnit, setDistanceUnit] = useState("mi");
  const [areaSelector, setAreaSelector] = useState("zip");
  const [locationInput, setLocationInput] = useState("San Francisco, CA");
  
  const handleApplyAreaSelector = () => {
    console.log("Applying Area Selector:", areaSelector, locationInput);
    if (onApplyAreaSelector) {
      onApplyAreaSelector(areaSelector, locationInput);
    }
    // Keep panel open as requested
  };

  // Panel height tracking
  useEffect(() => {
    if (activeTool) {
      onPanelChange?.(true, 450);
    } else {
      onPanelChange?.(false, 0);
    }
  }, [activeTool, onPanelChange]);

  const handleClosePanel = () => {
    setInternalActiveTool(null);
  };

  // REMOVED: handleToolClick - no longer needed without tool buttons

  const handleTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    if (val === "") {
      setTravelTime([0]);
    } else {
      const num = parseInt(val, 10);
      if (!isNaN(num)) {
        setTravelTime([num]);
      }
    }
  };

  const handleDistanceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    // Allow empty string or parse to number
    if (val === "") {
      setDistance([0]);
    } else {
      const num = parseInt(val, 10);
      if (!isNaN(num)) {
        setDistance([num]);
      }
    }
  };

  return (
    <>
      {/* REMOVED: Old toolbar icons */}

      {/* Area Selector Panel - Shows when Plus button is clicked */}
      {isOpen && (
        <div className="fixed bottom-4 left-4 z-50">
          <Card className="w-[450px] bg-[#0a0a0a] border-[#2d3548] shadow-2xl rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-white font-semibold">Area Selector</h3>
              <button 
                onClick={handleApplyAreaSelector}
                className="px-3 py-1 text-[#00bcd4] border border-[#00bcd4] rounded hover:bg-[#00bcd4] hover:text-black transition-colors cursor-pointer text-sm"
              >
                Apply
              </button>
            </div>

            {/* Starting Location */}
            <div className="mb-4">
              <label className="text-[#8b92a7] text-sm mb-2 block">Starting Location</label>
              <div className="relative bg-[#1a1f2e] border border-[#2d3548] rounded p-2">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6b7280]" />
                <Input
                  type="text"
                  placeholder="Search location..."
                  value={locationInput}
                  onChange={(e) => setLocationInput(e.target.value)}
                  className="pl-10 h-9 bg-transparent border-0 text-white placeholder:text-[#6b7280] cursor-text rounded transition-all focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:outline-none"
                />
              </div>
            </div>

            {/* Select Area Type */}
            <div className="mb-3">
              <label className="text-[#8b92a7] text-sm mb-2 block">Select Area Type</label>
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => setAreaSelector("zip")}
                  className={`flex items-center gap-2 p-3 rounded border transition-all cursor-pointer ${
                    areaSelector === "zip"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "bg-[#1a1f2e] border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50"
                  }`}
                >
                  <MapIcon className="h-4 w-4" />
                  <span className="text-sm">ZIP Codes</span>
                </button>

                <button
                  onClick={() => setAreaSelector("city")}
                  className={`flex items-center gap-2 p-3 rounded border transition-all cursor-pointer ${
                    areaSelector === "city"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "bg-[#1a1f2e] border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50"
                  }`}
                >
                  <Building2 className="h-4 w-4" />
                  <span className="text-sm">Cities</span>
                </button>

                <button
                  onClick={() => setAreaSelector("county")}
                  className={`flex items-center gap-2 p-3 rounded border transition-all cursor-pointer ${
                    areaSelector === "county"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "bg-[#1a1f2e] border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50"
                  }`}
                >
                  <MapIcon className="h-4 w-4" />
                  <span className="text-sm">Counties</span>
                </button>

                <button
                  onClick={() => setAreaSelector("state")}
                  className={`flex items-center gap-2 p-3 rounded border transition-all cursor-pointer ${
                    areaSelector === "state"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "bg-[#1a1f2e] border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50"
                  }`}
                >
                  <MapIcon className="h-4 w-4" />
                  <span className="text-sm">States</span>
                </button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* OLD PANELS BELOW - Keep for other tools if needed */}
      <div className="fixed right-4 bottom-8 z-30">
        {/* Distance by Time Panel - Clock */}
        {activeTool === "history" && (
          <Card className="w-[450px] bg-[#0a0a0a] border-[#2d3548] shadow-2xl rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-white">Distance by Time</h3>
              <div className="flex items-center gap-2">
                <button className="px-3 py-1 text-[#00bcd4] border border-[#00bcd4] rounded hover:bg-[#00bcd4] hover:text-black transition-colors cursor-pointer text-sm">
                  Apply
                </button>
                <button
                  onClick={handleClosePanel}
                  className="text-[#8b92a7] hover:text-white transition-colors cursor-pointer"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* Starting Location Search Bar */}
            <div className="mb-3">
              <label className="text-[#8b92a7] text-sm mb-2 block">Starting Location</label>
              <div className="relative bg-[#1a1f2e] border border-[#2d3548] rounded p-2">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6b7280]" />
                <Input
                  type="text"
                  placeholder="Search location..."
                  defaultValue="San Francisco, CA"
                  className="pl-10 h-9 bg-transparent border-0 text-white placeholder:text-[#6b7280] cursor-text rounded transition-all focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:outline-none"
                />
              </div>
            </div>

            <div className="mb-3">
              <label className="text-[#8b92a7] text-sm mb-2 block">Travel Mode</label>
              <div className="flex gap-2">
                <button
                  onClick={() => setTravelMode("driving")}
                  className={`flex-1 flex items-center justify-center gap-2 p-2 rounded border transition-colors cursor-pointer ${
                    travelMode === "driving"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50 hover:text-[#00bcd4]"
                  }`}
                >
                  <Car className="h-4 w-4" />
                  <span className="text-sm">Driving</span>
                </button>
                <button
                  onClick={() => setTravelMode("walking")}
                  className={`flex-1 flex items-center justify-center gap-2 p-2 rounded border transition-colors cursor-pointer ${
                    travelMode === "walking"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50 hover:text-[#00bcd4]"
                  }`}
                >
                  <Footprints className="h-4 w-4" />
                  <span className="text-sm">Walking</span>
                </button>
                <button
                  onClick={() => setTravelMode("bicycling")}
                  className={`flex-1 flex items-center justify-center gap-2 p-2 rounded border transition-colors cursor-pointer ${
                    travelMode === "bicycling"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50 hover:text-[#00bcd4]"
                  }`}
                >
                  <Bike className="h-4 w-4" />
                  <span className="text-sm">Biking</span>
                </button>
              </div>
            </div>

            <div>
              <label className="text-[#8b92a7] text-sm mb-2 block">Travel Time</label>
              <div className="flex items-center gap-3">
                <Slider
                  value={travelTime}
                  onValueChange={setTravelTime}
                  max={60}
                  step={5}
                  className="flex-1"
                />
                <Input
                  type="number"
                  value={travelTime[0]}
                  onChange={handleTimeChange}
                  className="w-20 bg-[#1a1f2e] border-[#2d3548] text-white"
                />
                <span className="text-[#8b92a7] text-sm">min</span>
              </div>
            </div>
          </Card>
        )}

        {/* Distance by Radius Panel - Measure */}
        {activeTool === "measure" && (
          <Card className="w-[450px] bg-[#0a0a0a] border-[#2d3548] shadow-2xl rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-white">Distance by Radius</h3>
              <div className="flex items-center gap-2">
                <button className="px-3 py-1 text-[#00bcd4] border border-[#00bcd4] rounded hover:bg-[#00bcd4] hover:text-black transition-colors cursor-pointer text-sm">
                  Apply
                </button>
                <button
                  onClick={handleClosePanel}
                  className="text-[#8b92a7] hover:text-white transition-colors cursor-pointer"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* Starting Location Search Bar */}
            <div className="mb-3">
              <label className="text-[#8b92a7] text-sm mb-2 block">Starting Location</label>
              <div className="relative bg-[#1a1f2e] border border-[#2d3548] rounded p-2">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6b7280]" />
                <Input
                  type="text"
                  placeholder="Search location..."
                  defaultValue="San Francisco, CA"
                  className="pl-10 h-9 bg-transparent border-0 text-white placeholder:text-[#6b7280] cursor-text rounded transition-all focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:outline-none"
                />
              </div>
            </div>

            <div className="mb-3">
              <label className="text-[#8b92a7] text-sm mb-2 block">Travel Mode</label>
              <div className="flex gap-2">
                <button
                  onClick={() => setDistanceMode("driving")}
                  className={`flex-1 flex items-center justify-center gap-2 p-2 rounded border transition-colors cursor-pointer ${
                    distanceMode === "driving"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50 hover:text-[#00bcd4]"
                  }`}
                >
                  <Car className="h-4 w-4" />
                  <span className="text-sm">Driving</span>
                </button>
                <button
                  onClick={() => setDistanceMode("straight")}
                  className={`flex-1 flex items-center justify-center gap-2 p-2 rounded border transition-colors cursor-pointer ${
                    distanceMode === "straight"
                      ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                      : "border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50 hover:text-[#00bcd4]"
                  }`}
                >
                  <Circle className="h-4 w-4" />
                  <span className="text-sm">Straight Line</span>
                </button>
              </div>
            </div>

            <div>
              <label className="text-[#8b92a7] text-sm mb-2 block">Distance</label>
              <div className="flex items-center gap-3">
                <Slider
                  value={distance}
                  onValueChange={setDistance}
                  max={100}
                  step={5}
                  className="flex-1"
                />
                <Input
                  type="number"
                  value={distance[0]}
                  onChange={handleDistanceChange}
                  className="w-20 bg-[#1a1f2e] border-[#2d3548] text-white"
                />
                <select
                  value={distanceUnit}
                  onChange={(e) => setDistanceUnit(e.target.value)}
                  className="bg-[#1a1f2e] border border-[#2d3548] text-white rounded px-2 py-1 text-sm cursor-pointer"
                >
                  <option value="mi">mi</option>
                  <option value="km">km</option>
                </select>
              </div>
            </div>
          </Card>
        )}

        {/* Area Selector Panel - Grid */}
        {activeTool === "grid" && (
          <Card className="w-[450px] bg-[#0a0a0a] border-[#2d3548] shadow-2xl rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-white">Area Selector</h3>
              <div className="flex items-center gap-2">
                <button 
                  onClick={handleApplyAreaSelector}
                  className="px-3 py-1 text-[#00bcd4] border border-[#00bcd4] rounded hover:bg-[#00bcd4] hover:text-black transition-colors cursor-pointer text-sm"
                >
                  Apply
                </button>
                <button
                  onClick={handleClosePanel}
                  className="text-[#8b92a7] hover:text-white transition-colors cursor-pointer"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* Starting Location Search Bar */}
            <div className="mb-3">
              <label className="text-[#8b92a7] text-sm mb-2 block">Starting Location</label>
              <div className="relative bg-[#1a1f2e] border border-[#2d3548] rounded p-2">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6b7280]" />
                <Input
                  type="text"
                  placeholder="Search location..."
                  value={locationInput}
                  onChange={(e) => setLocationInput(e.target.value)}
                  className="pl-10 h-9 bg-transparent border-0 text-white placeholder:text-[#6b7280] cursor-text rounded transition-all focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="text-[#8b92a7] text-sm mb-2 block">Select Area Type</label>
              <div className="grid grid-cols-2 gap-2">
                {[
                  { id: "zip", label: "ZIP Codes", icon: MapIcon },
                  { id: "city", label: "Cities", icon: Building2 },
                  { id: "county", label: "Counties", icon: MapIcon },
                  { id: "state", label: "States", icon: MapIcon },
                ].map((area) => {
                  const AreaIcon = area.icon;
                  return (
                    <button
                      key={area.id}
                      onClick={() => setAreaSelector(area.id)}
                      className={`flex items-center gap-2 p-3 rounded border transition-colors cursor-pointer ${
                        areaSelector === area.id
                          ? "bg-[#00bcd4]/10 border-[#00bcd4] text-[#00bcd4]"
                          : "border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/50 hover:text-[#00bcd4]"
                      }`}
                    >
                      <AreaIcon className="h-4 w-4" />
                      <span className="text-sm">{area.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </Card>
        )}
      </div>
    </>
  );
}

