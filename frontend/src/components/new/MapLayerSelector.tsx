import { useState } from "react";
import { Layers, X } from "lucide-react";
import { Card } from "@/components/ui/card";

// Real Mapbox style URLs
const mapLayers = [
  { 
    id: "default", 
    name: "Streets", 
    preview: "https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/-122.4194,37.7749,11,0/100x100@2x?access_token=pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw",
    style: "mapbox://styles/mapbox/streets-v12"
  },
  { 
    id: "satellite", 
    name: "Satellite", 
    preview: "https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/static/-122.4194,37.7749,11,0/100x100@2x?access_token=pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw",
    style: "mapbox://styles/mapbox/satellite-streets-v12"
  },
  { 
    id: "terrain", 
    name: "Terrain", 
    preview: "https://api.mapbox.com/styles/v1/mapbox/outdoors-v12/static/-122.4194,37.7749,11,0/100x100@2x?access_token=pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw",
    style: "mapbox://styles/mapbox/outdoors-v12"
  },
];

interface MapLayerSelectorProps {
  isOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  onStyleChange?: (style: 'default' | 'satellite' | 'terrain') => void;
}

export function MapLayerSelector({ 
  isOpen: externalIsOpen, 
  onOpenChange,
  onStyleChange 
}: MapLayerSelectorProps) {
  const [selectedLayer, setSelectedLayer] = useState("default");
  const [internalIsOpen, setInternalIsOpen] = useState(false);

  // Use external state if provided, otherwise use internal state
  const isOpen = externalIsOpen !== undefined ? externalIsOpen : internalIsOpen;
  const setIsOpen = onOpenChange || setInternalIsOpen;

  const handleStyleSelect = (layerId: string) => {
    setSelectedLayer(layerId);
    if (onStyleChange) {
      onStyleChange(layerId as 'default' | 'satellite' | 'terrain');
    }
  };

  return (
    <div className={`fixed top-[196px] transition-all duration-300 ${isOpen ? 'right-[68px] z-50' : 'right-4 z-40'}`}>
      <Card 
        onClick={() => !isOpen && setIsOpen(true)}
        className={`backdrop-blur-md shadow-xl transition-all duration-300 ease-out cursor-pointer relative ${
          isOpen 
            ? "bg-[#1a1f2e]/40 border-[#2d3548]/50 hover:bg-[#1a1f2e] hover:border-[#2d3548]" 
            : "bg-[#1a1f2e] border-[#2d3548] hover:bg-[#252b3d]"
        }`}
      >
        {/* Close Button */}
        {isOpen && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setIsOpen(false);
            }}
            className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-[#1a1f2e] border-2 border-[#00bcd4] flex items-center justify-center hover:bg-[#00bcd4] transition-colors cursor-pointer group z-10"
          >
            <X className="h-3 w-3 text-[#00bcd4] group-hover:text-white" />
          </button>
        )}
        
        {/* Header */}
        {isOpen ? (
          // Open state
          <div className="flex items-center justify-between gap-3 px-2.5 py-1.5 w-[180px]">
            <div className="cursor-pointer group flex-shrink-0">
              <Layers className="h-5 w-5 text-[#00bcd4] drop-shadow-[0_0_6px_rgba(0,188,212,0.6)] transition-all" />
            </div>
            <button 
              onClick={(e) => {
                e.stopPropagation();
                setIsOpen(false);
              }}
              className="text-white flex-1 text-center cursor-pointer hover:text-[#00bcd4] transition-colors text-xs"
            >
              Map Style
            </button>
            <div className="w-5 flex-shrink-0" /> {/* Spacer for balance */}
          </div>
        ) : (
          // Collapsed state - same size as heatmap button
          <div className="p-2.5 rounded-lg">
            <div className="cursor-pointer group">
              <Layers className="h-5 w-5 text-[#8b92a7] transition-all group-hover:text-[#00bcd4] group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]" />
            </div>
          </div>
        )}

        {/* Expanded Content */}
        {isOpen && (
          <>
            {/* Laser Line */}
            <div
              className="h-[2px] bg-gradient-to-r from-transparent via-[#00bcd4] to-transparent"
              style={{
                boxShadow: "0 0 8px rgba(0, 188, 212, 0.8), 0 0 4px rgba(0, 188, 212, 0.6)",
              }}
            />
            
            {/* Content Box */}
            <div className="px-2.5 pb-2.5 pt-2 w-[180px]">
              <div className="space-y-1.5">
                {mapLayers.map((layer) => (
                  <button
                    key={layer.id}
                    onClick={() => handleStyleSelect(layer.id)}
                    className={`w-full flex items-center gap-2 p-1.5 rounded-lg transition-all duration-200 cursor-pointer ${
                      selectedLayer === layer.id
                        ? "bg-[#00bcd4]/10 border border-[#00bcd4]/50"
                        : "hover:bg-[#252b3d] border border-transparent"
                    }`}
                  >
                    <div
                      className="w-7 h-7 rounded border border-[#2d3548] bg-cover bg-center flex-shrink-0"
                      style={{ backgroundImage: `url(${layer.preview})` }}
                    />
                    <span className={`text-xs flex-1 text-left ${
                      selectedLayer === layer.id ? "text-[#00bcd4]" : "text-[#e0e0e0]"
                    }`}>
                      {layer.name}
                    </span>
                    {selectedLayer === layer.id && (
                      <div className="w-1.5 h-1.5 rounded-full bg-[#00bcd4]" />
                    )}
                  </button>
                ))}
              </div>
            </div>
          </>
        )}
      </Card>
    </div>
  );
}

