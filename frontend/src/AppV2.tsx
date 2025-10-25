import { useState } from "react";
import { SearchBar } from "@/components/new/SearchBar";
import { FloatingMenu } from "@/components/new/FloatingMenu";
import { DemographicsPanel } from "@/components/new/DemographicsPanel";
import { MapTopTools } from "@/components/new/MapTopTools";
import { SimplifiedMapView } from "@/components/new/SimplifiedMapView";

export function AppV2() {
  const [activePanel, setActivePanel] = useState<string | null>(null);
  const [selectedZipcode, setSelectedZipcode] = useState<string>("94103");
  const [mapCenter, setMapCenter] = useState({ lat: 37.7749, lng: -122.4194 });
  const [mapZoom, setMapZoom] = useState(12);
  const [isPlusOpen, setIsPlusOpen] = useState(false);
  const [isFolderOpen, setIsFolderOpen] = useState(false);

  const handleLocationSelect = (location: { lat: number; lng: number; name: string }) => {
    setMapCenter({ lat: location.lat, lng: location.lng });
    setMapZoom(13);
    console.log("Location selected:", location);
  };

  const handleZipcodeSelect = (zipcode: string) => {
    setSelectedZipcode(zipcode);
    console.log("ZIP code selected:", zipcode);
    setActivePanel("demographics");
  };

  const handleMenuItemClick = (itemId: string) => {
    if (activePanel === itemId) {
      setActivePanel(null);
    } else {
      setActivePanel(itemId);
    }
  };

  const handlePlusClick = () => {
    setIsPlusOpen(!isPlusOpen);
    console.log("Plus clicked");
  };

  const handleFolderClick = () => {
    setIsFolderOpen(!isFolderOpen);
    console.log("Folder clicked");
  };

  return (
    <div className="min-h-screen bg-background dark">
      {/* Map Background - Full Screen with Mapbox */}
      <SimplifiedMapView center={mapCenter} zoom={mapZoom} />

      {/* SearchBar at Top Center */}
      <SearchBar
        onLocationSelect={handleLocationSelect}
        onZipcodeSelect={handleZipcodeSelect}
      />

      {/* Top Right Tools - Plus & Folder */}
      <MapTopTools
        onPlusClick={handlePlusClick}
        onFolderClick={handleFolderClick}
        isFolderActive={isFolderOpen}
      />

      {/* Left Side Menu */}
      <FloatingMenu
        onMenuItemClick={handleMenuItemClick}
        activeItem={activePanel}
      />

      {/* Demographics Panel */}
      <DemographicsPanel
        isOpen={activePanel === "demographics"}
        onClose={() => setActivePanel(null)}
        zipcode={selectedZipcode}
      />

      {/* Placeholder panels for other menu items */}
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
    </div>
  );
}

