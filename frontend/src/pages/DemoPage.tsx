import { useState } from "react";
import { SearchBar } from "@/components/new/SearchBar";
import { FloatingMenu } from "@/components/new/FloatingMenu";
import { DemographicsPanel } from "@/components/new/DemographicsPanel";

export function DemoPage() {
  const [activePanel, setActivePanel] = useState<string | null>(null);
  const [selectedZipcode, setSelectedZipcode] = useState<string>("94103");
  const [selectedLocation, setSelectedLocation] = useState<{
    lat: number;
    lng: number;
    name: string;
  } | null>(null);

  const handleLocationSelect = (location: { lat: number; lng: number; name: string }) => {
    setSelectedLocation(location);
    console.log("Location selected:", location);
  };

  const handleZipcodeSelect = (zipcode: string) => {
    setSelectedZipcode(zipcode);
    console.log("ZIP code selected:", zipcode);
    // Auto-open demographics panel when ZIP code is selected
    setActivePanel("demographics");
  };

  const handleMenuItemClick = (itemId: string) => {
    if (activePanel === itemId) {
      // Close if clicking the same item
      setActivePanel(null);
    } else {
      setActivePanel(itemId);
    }
  };

  return (
    <div className="relative w-full h-screen bg-[#0a0a0a] overflow-hidden">
      {/* Background gradient effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#00bcd4]/5 via-transparent to-[#26c6da]/5 pointer-events-none" />

      {/* Demo Map Placeholder */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="text-[#00bcd4] text-6xl font-bold animate-pulse">
            🗺️
          </div>
          <h1 className="text-3xl font-bold text-white">
            D.E.L.T.A 2 Demo
          </h1>
          <p className="text-[#8b92a7] text-lg max-w-md">
            Map visualization will go here. For now, testing new UI components:
          </p>
          <div className="space-y-2 text-sm text-[#8b92a7]">
            <p>✅ SearchBar with Mapbox integration</p>
            <p>✅ FloatingMenu with 5 categories</p>
            <p>✅ DemographicsPanel with real Census data</p>
          </div>
          
          {selectedLocation && (
            <div className="mt-8 p-4 bg-[#1a1f2e] border border-[#2d3548] rounded-lg max-w-md mx-auto">
              <p className="text-white font-semibold mb-2">📍 Selected Location:</p>
              <p className="text-[#00bcd4] text-sm">{selectedLocation.name}</p>
              <p className="text-[#8b92a7] text-xs mt-1">
                Lat: {selectedLocation.lat.toFixed(4)}, Lng: {selectedLocation.lng.toFixed(4)}
              </p>
              {selectedZipcode && (
                <p className="text-[#26c6da] text-sm mt-2">
                  ZIP Code: {selectedZipcode}
                </p>
              )}
            </div>
          )}

          <div className="mt-6 p-3 bg-[#1a1f2e]/50 border border-[#2d3548]/50 rounded-lg max-w-sm mx-auto">
            <p className="text-[#fbbf24] text-sm font-medium">💡 Try it out:</p>
            <p className="text-[#8b92a7] text-xs mt-1">
              1. Search for a ZIP code (e.g., "94103")<br/>
              2. Click Demographics icon (left menu)<br/>
              3. See real Census data in the panel!
            </p>
          </div>
        </div>
      </div>

      {/* SearchBar Component */}
      <SearchBar
        onLocationSelect={handleLocationSelect}
        onZipcodeSelect={handleZipcodeSelect}
      />

      {/* FloatingMenu Component */}
      <FloatingMenu
        onMenuItemClick={handleMenuItemClick}
        activeItem={activePanel}
      />

      {/* DemographicsPanel Component */}
      <DemographicsPanel
        isOpen={activePanel === "demographics"}
        onClose={() => setActivePanel(null)}
        zipcode={selectedZipcode}
      />

      {/* Info Panel for other menu items (placeholder) */}
      {activePanel && activePanel !== "demographics" && (
        <div className="fixed right-0 top-0 h-screen w-[480px] z-40 bg-[#1a1f2e]/95 backdrop-blur-md border-l border-[#2d3548] shadow-2xl flex items-center justify-center">
          <div className="text-center space-y-4 p-8">
            <div className="text-5xl">🚧</div>
            <h3 className="text-xl font-semibold text-white capitalize">
              {activePanel.replace(/-/g, " ")}
            </h3>
            <p className="text-[#8b92a7]">
              This panel is coming soon!
            </p>
            <button
              onClick={() => setActivePanel(null)}
              className="mt-4 px-4 py-2 bg-[#00bcd4] text-white rounded-lg hover:bg-[#00bcd4]/80 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Debug Info (bottom-left corner) */}
      <div className="fixed bottom-4 left-4 z-50 p-3 bg-[#1a1f2e]/90 border border-[#2d3548] rounded-lg text-xs text-[#8b92a7] max-w-xs">
        <p className="font-semibold text-white mb-2">🔧 Debug Info:</p>
        <p>Active Panel: {activePanel || "None"}</p>
        <p>Selected ZIP: {selectedZipcode || "None"}</p>
        <p>Backend: http://localhost:8001</p>
        <p className="mt-2 text-[#00bcd4]">
          {activePanel === "demographics" ? "✅ Fetching real data..." : "⏸️ Waiting for interaction"}
        </p>
      </div>
    </div>
  );
}

