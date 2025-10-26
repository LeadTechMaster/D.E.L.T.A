import { X, Circle, Square, Pentagon, Hash, Building2, MapIcon, Building } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { useState } from "react";

interface ToolPanelsProps {
  activeTool: string | null;
  onClose: () => void;
  onAreaTypeApply?: (areaType: string) => void;
}

export function ToolPanels({ activeTool, onClose, onAreaTypeApply }: ToolPanelsProps) {
  const [startingLocation, setStartingLocation] = useState("San Francisco, CA");
  const [travelMode, setTravelMode] = useState<"driving" | "walking" | "biking">("driving");
  const [travelTime, setTravelTime] = useState(20);
  const [distanceMode, setDistanceMode] = useState<"driving" | "radius">("driving");
  const [distance, setDistance] = useState(20);
  const [selectedAreaType, setSelectedAreaType] = useState<string | null>(null);
  const [selectedDrawTool, setSelectedDrawTool] = useState<string | null>(null);

  if (!activeTool) return null;

  const renderTimePanel = () => (
    <div className="w-[280px] bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md rounded-lg border border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-[#2d3548]">
        <h3 className="text-white text-sm">Time</h3>
        <div className="flex items-center gap-1.5">
          <button className="px-2.5 py-0.5 text-xs border border-[#00bcd4] text-[#00bcd4] rounded hover:bg-[#00bcd4]/10 transition-colors">
            Apply
          </button>
          <button
            onClick={onClose}
            className="p-0.5 hover:bg-[#252b3d] rounded transition-colors"
          >
            <X className="h-3.5 w-3.5 text-[#8b92a7] hover:text-white" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="px-3 py-2.5 space-y-2.5">
        {/* Starting Location */}
        <div className="space-y-1">
          <label className="text-[#8b92a7] text-xs">Starting location</label>
          <Input
            value={startingLocation}
            onChange={(e) => setStartingLocation(e.target.value)}
            className="h-7 bg-[#0f1219] border-[#2d3548] text-white text-xs"
          />
        </div>

        {/* Travel Mode Toggle */}
        <div className="space-y-1">
          <label className="text-[#8b92a7] text-xs">Travel mode</label>
          <div className="flex gap-1">
            {[
              { id: "driving", label: "Driving" },
              { id: "walking", label: "Walking" },
              { id: "biking", label: "Biking" },
            ].map((mode) => (
              <button
                key={mode.id}
                onClick={() => setTravelMode(mode.id as any)}
                className={`flex-1 px-2 py-1 text-xs rounded transition-colors ${
                  travelMode === mode.id
                    ? "bg-[#00bcd4] text-white"
                    : "bg-[#0f1219] text-[#8b92a7] border border-[#2d3548] hover:border-[#00bcd4]/50"
                }`}
              >
                {mode.label}
              </button>
            ))}
          </div>
        </div>

        {/* Travel Time */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-[#8b92a7] text-xs">Travel time</label>
            <div className="flex items-center gap-1">
              <Input
                type="number"
                value={travelTime}
                onChange={(e) => setTravelTime(Number(e.target.value))}
                className="h-6 w-12 bg-[#0f1219] border-[#2d3548] text-white text-xs px-1.5 text-center"
              />
              <span className="text-[#8b92a7] text-xs">mi</span>
            </div>
          </div>
          <Slider
            value={[travelTime]}
            onValueChange={([val]) => setTravelTime(val)}
            min={0}
            max={60}
            step={1}
            className="[&_[role=slider]]:bg-[#00bcd4] [&_[role=slider]]:border-[#00bcd4] [&_.bg-primary]:bg-[#00bcd4]"
          />
        </div>
      </div>
    </div>
  );

  const renderDistancePanel = () => (
    <div className="w-[280px] bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md rounded-lg border border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-[#2d3548]">
        <h3 className="text-white text-sm">Distance</h3>
        <div className="flex items-center gap-1.5">
          <button className="px-2.5 py-0.5 text-xs border border-[#00bcd4] text-[#00bcd4] rounded hover:bg-[#00bcd4]/10 transition-colors">
            Apply
          </button>
          <button
            onClick={onClose}
            className="p-0.5 hover:bg-[#252b3d] rounded transition-colors"
          >
            <X className="h-3.5 w-3.5 text-[#8b92a7] hover:text-white" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="px-3 py-2.5 space-y-2.5">
        {/* Starting Location */}
        <div className="space-y-1">
          <label className="text-[#8b92a7] text-xs">Starting location</label>
          <Input
            value={startingLocation}
            onChange={(e) => setStartingLocation(e.target.value)}
            className="h-7 bg-[#0f1219] border-[#2d3548] text-white text-xs"
          />
        </div>

        {/* Distance Mode Toggle */}
        <div className="space-y-1">
          <label className="text-[#8b92a7] text-xs">Distance mode</label>
          <div className="flex gap-1">
            {[
              { id: "driving", label: "Driving" },
              { id: "radius", label: "Radius" },
            ].map((mode) => (
              <button
                key={mode.id}
                onClick={() => setDistanceMode(mode.id as any)}
                className={`flex-1 px-2 py-1 text-xs rounded transition-colors ${
                  distanceMode === mode.id
                    ? "bg-[#00bcd4] text-white"
                    : "bg-[#0f1219] text-[#8b92a7] border border-[#2d3548] hover:border-[#00bcd4]/50"
                }`}
              >
                {mode.label}
              </button>
            ))}
          </div>
        </div>

        {/* Distance */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-[#8b92a7] text-xs">Distance</label>
            <div className="flex items-center gap-1">
              <Input
                type="number"
                value={distance}
                onChange={(e) => setDistance(Number(e.target.value))}
                className="h-6 w-12 bg-[#0f1219] border-[#2d3548] text-white text-xs px-1.5 text-center"
              />
              <span className="text-[#8b92a7] text-xs">mi</span>
            </div>
          </div>
          <Slider
            value={[distance]}
            onValueChange={([val]) => setDistance(val)}
            min={0}
            max={100}
            step={1}
            className="[&_[role=slider]]:bg-[#00bcd4] [&_[role=slider]]:border-[#00bcd4] [&_.bg-primary]:bg-[#00bcd4]"
          />
        </div>
      </div>
    </div>
  );

  const renderAreaSelectorPanel = () => (
    <div className="w-[280px] bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md rounded-lg border border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-[#2d3548]">
        <h3 className="text-white text-sm">Area Type</h3>
        <div className="flex items-center gap-1.5">
          <button 
            onClick={() => {
              if (selectedAreaType && onAreaTypeApply) {
                onAreaTypeApply(selectedAreaType);
              }
            }}
            disabled={!selectedAreaType}
            className="px-2.5 py-0.5 text-xs border border-[#00bcd4] text-[#00bcd4] rounded hover:bg-[#00bcd4]/10 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Apply
          </button>
          <button
            onClick={onClose}
            className="p-0.5 hover:bg-[#252b3d] rounded transition-colors"
          >
            <X className="h-3.5 w-3.5 text-[#8b92a7] hover:text-white" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="px-3 py-2.5 space-y-2">
        {/* Area Type Options */}
        <div className="space-y-1">
          <label className="text-[#8b92a7] text-xs">Select area type</label>
          <div className="grid grid-cols-2 gap-1.5">
            {[
              { id: "zipcode", label: "Zip Code", icon: Hash },
              { id: "county", label: "County", icon: Building2 },
              { id: "state", label: "State", icon: MapIcon },
              { id: "city", label: "City", icon: Building },
            ].map((type) => (
              <button
                key={type.id}
                onClick={() => setSelectedAreaType(type.id)}
                className={`flex items-center gap-1.5 px-2 py-1.5 text-xs rounded transition-colors ${
                  selectedAreaType === type.id
                    ? "bg-[#00bcd4] text-white"
                    : "bg-[#0f1219] text-[#8b92a7] border border-[#2d3548] hover:border-[#00bcd4]/50"
                }`}
              >
                <type.icon className="h-3.5 w-3.5" />
                {type.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderDrawPanel = () => {
    const drawTools = [
      { id: "polygon", icon: Pentagon, label: "Polygon" },
      { id: "rectangle", icon: Square, label: "Rectangle" },
      { id: "circle", icon: Circle, label: "Circle" },
    ];

    return (
      <div className="bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md rounded-lg border border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20">
        {/* Horizontal Layout */}
        <div className="flex items-center gap-2 px-2.5 py-2">
          <span className="text-white text-xs flex-shrink-0">Draw:</span>
          
          {/* Drawing Tools - Horizontal */}
          <div className="flex gap-1.5">
            {drawTools.map((tool) => (
              <button
                key={tool.id}
                onClick={() => setSelectedDrawTool(tool.id)}
                className={`flex items-center gap-1.5 py-1.5 px-2.5 rounded transition-all ${
                  selectedDrawTool === tool.id
                    ? "bg-[#00bcd4] text-white"
                    : "bg-[#0f1219] text-[#8b92a7] border border-[#2d3548] hover:border-[#00bcd4]/50"
                }`}
              >
                <tool.icon className="h-3.5 w-3.5" />
                <span className="text-xs whitespace-nowrap">{tool.label}</span>
              </button>
            ))}
          </div>

          <button
            onClick={onClose}
            className="p-1 hover:bg-[#252b3d] rounded transition-colors ml-1 flex-shrink-0"
          >
            <X className="h-3.5 w-3.5 text-[#8b92a7] hover:text-white" />
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="fixed bottom-[120px] left-1/2 -translate-x-1/2 z-40 animate-in slide-in-from-bottom-4 duration-300">
      {activeTool === "draw" && renderDrawPanel()}
      {activeTool === "history" && renderTimePanel()}
      {activeTool === "measure" && renderDistancePanel()}
      {activeTool === "grid" && renderAreaSelectorPanel()}
    </div>
  );
}

