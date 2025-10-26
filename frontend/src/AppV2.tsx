import { useState } from "react";
import { SearchBar } from "@/components/new/SearchBar";
import { FloatingMenu } from "@/components/new/FloatingMenu";
import { DemographicsPanel } from "@/components/new/DemographicsPanel";
import { PointsOfInterestPanel } from "@/components/new/PointsOfInterestPanel";
import { CustomerMetricsAndDataPanel } from "@/components/new/CustomerMetricsAndDataPanel";
import { CompetitiveAnalysisPanel } from "@/components/new/CompetitiveAnalysisPanel";
import { DemandResearchPanel } from "@/components/new/DemandResearchPanel";
import { AdministrativeBoundariesPanel } from "@/components/new/AdministrativeBoundariesPanel";
import { MapTopTools } from "@/components/new/MapTopTools";
import { MapToolbar } from "@/components/new/MapToolbar";
import { MapLayerSelector } from "@/components/new/MapLayerSelector";
import { HeatmapBox } from "@/components/new/HeatmapBox";
import { BottomToolbar } from "@/components/new/BottomToolbar";
import { ToolPanels } from "@/components/new/ToolPanels";
import { PolygonDrawing } from "@/components/new/PolygonDrawing";
import { MassSelector } from "@/components/new/MassSelector";
import { FolderDropdown } from "@/components/new/FolderDropdown";
import { SimplifiedMapView } from "@/components/new/SimplifiedMapView";
import { FolderProvider } from "@/contexts/FolderContext";
import { DashboardProvider } from "@/contexts/DashboardContext";

export function AppV2() {
  const [activePanel, setActivePanel] = useState<string | null>(null);
  const [selectedZipcode, setSelectedZipcode] = useState<string>("94103");
  const [mapCenter, setMapCenter] = useState({ lat: 37.7749, lng: -122.4194 });
  const [mapZoom, setMapZoom] = useState(12);
  const [isPlusOpen, setIsPlusOpen] = useState(false);
  const [isFolderOpen, setIsFolderOpen] = useState(false);
  const [isDemographicsOpen, setIsDemographicsOpen] = useState(false);
  const [isPointsOfInterestOpen, setIsPointsOfInterestOpen] = useState(false);
  const [isCustomerMetricsDataOpen, setIsCustomerMetricsDataOpen] = useState(false);
  const [isCompetitiveAnalysisOpen, setIsCompetitiveAnalysisOpen] = useState(false);
  const [isDemandResearchOpen, setIsDemandResearchOpen] = useState(false);
  const [isAdministrativeBoundariesOpen, setIsAdministrativeBoundariesOpen] = useState(false);
  const [toolbarPanelHeight, setToolbarPanelHeight] = useState(0);
  const [isHeatmapOpen, setIsHeatmapOpen] = useState(false);
  const [isBottomToolbarOpen, setIsBottomToolbarOpen] = useState(false);
  const [activeToolbarItem, setActiveToolbarItem] = useState<string | null>(null);
  const [isMapLayerOpen, setIsMapLayerOpen] = useState(false);
  const [isTerritoriesOpen, setIsTerritoriesOpen] = useState(false);
  const [isMassSelectorMode, setIsMassSelectorMode] = useState(false);
  const [selectedAreaType, setSelectedAreaType] = useState<string | null>(null);

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
    // Toggle behavior - if clicking the same item, close it
    if (activePanel === itemId) {
      setActivePanel(null);
      setIsDemographicsOpen(false);
      setIsPointsOfInterestOpen(false);
      setIsCustomerMetricsDataOpen(false);
      setIsCompetitiveAnalysisOpen(false);
      setIsDemandResearchOpen(false);
      setIsAdministrativeBoundariesOpen(false);
      return;
    }

    setActivePanel(itemId);

    // Close all panels first
    setIsDemographicsOpen(false);
    setIsPointsOfInterestOpen(false);
    setIsCustomerMetricsDataOpen(false);
    setIsCompetitiveAnalysisOpen(false);
    setIsDemandResearchOpen(false);
    setIsAdministrativeBoundariesOpen(false);

    // Open the appropriate panel
    if (itemId === "demographics") {
      setIsDemographicsOpen(true);
    } else if (itemId === "points-of-interest") {
      setIsPointsOfInterestOpen(true);
    } else if (itemId === "customer-metrics-data") {
      setIsCustomerMetricsDataOpen(true);
    } else if (itemId === "competitive-analysis") {
      setIsCompetitiveAnalysisOpen(true);
    } else if (itemId === "demand-research") {
      setIsDemandResearchOpen(true);
    } else if (itemId === "administrative") {
      setIsAdministrativeBoundariesOpen(true);
    }
  };

  const handleCloseDemographics = () => {
    setIsDemographicsOpen(false);
    setActivePanel(null);
  };

  const handleClosePointsOfInterest = () => {
    setIsPointsOfInterestOpen(false);
    setActivePanel(null);
  };

  const handleCloseCustomerMetricsData = () => {
    setIsCustomerMetricsDataOpen(false);
    setActivePanel(null);
  };

  const handleCloseCompetitiveAnalysis = () => {
    setIsCompetitiveAnalysisOpen(false);
    setActivePanel(null);
  };

  const handleCloseDemandResearch = () => {
    setIsDemandResearchOpen(false);
    setActivePanel(null);
  };

  const handleCloseAdministrativeBoundaries = () => {
    setIsAdministrativeBoundariesOpen(false);
    setActivePanel(null);
  };

  const handleOpenCustomerMetricsDataFromHeatmap = () => {
    setActivePanel("customer-metrics-data");
    setIsCustomerMetricsDataOpen(true);
    setIsHeatmapOpen(false);
  };

  const handleOpenPointsOfInterestFromHeatmap = () => {
    setActivePanel("points-of-interest");
    setIsPointsOfInterestOpen(true);
    setIsHeatmapOpen(false);
  };

  const handleOpenCompetitiveAnalysisFromHeatmap = () => {
    setActivePanel("competitive-analysis");
    setIsCompetitiveAnalysisOpen(true);
    setIsHeatmapOpen(false);
  };

  const handleOpenDemandResearchFromHeatmap = () => {
    setActivePanel("demand-research");
    setIsDemandResearchOpen(true);
    setIsHeatmapOpen(false);
  };

  const handleOpenAdministrativeBoundariesFromHeatmap = () => {
    setActivePanel("administrative");
    setIsAdministrativeBoundariesOpen(true);
    setIsHeatmapOpen(false);
  };

  const handleToolbarClick = (id: string) => {
    // Toggle behavior
    if (activeToolbarItem === id) {
      setActiveToolbarItem(null);
    } else {
      setActiveToolbarItem(id);
    }
  };

  const handleToolbarPanelChange = (isOpen: boolean, panelHeight: number) => {
    setToolbarPanelHeight(isOpen ? panelHeight : 0);
  };

  // Handler for MapLayerSelector - close other panels when opened
  const handleMapLayerOpenChange = (open: boolean) => {
    setIsMapLayerOpen(open);
    if (open) {
      setIsHeatmapOpen(false);
      setIsTerritoriesOpen(false);
      setIsBottomToolbarOpen(false);
      setActiveToolbarItem(null);
    }
  };

  // Handler for HeatmapBox - close other panels when opened
  const handleHeatmapOpenChange = (open: boolean) => {
    setIsHeatmapOpen(open);
    if (open) {
      setIsMapLayerOpen(false);
      setIsTerritoriesOpen(false);
      setIsBottomToolbarOpen(false);
      setActiveToolbarItem(null);
    }
  };

  // Handler for FolderDropdown - close other panels when opened
  const handleFolderOpenChange = (open: boolean) => {
    setIsFolderOpen(open);
    if (open) {
      setIsBottomToolbarOpen(false);
      setActiveToolbarItem(null);
    }
  };

  // Handler for Territories dropdown - close other panels when opened
  const handleTerritoriesToggle = () => {
    const newState = !isTerritoriesOpen;
    setIsTerritoriesOpen(newState);
    if (newState) {
      setIsHeatmapOpen(false);
      setIsMapLayerOpen(false);
      setIsBottomToolbarOpen(false);
      setActiveToolbarItem(null);
    }
  };

  const handleAddFolder = () => {
    console.log("Add new folder");
  };

  const handleAddArea = () => {
    // Close territories panel and open bottom toolbar to select area type
    setIsTerritoriesOpen(false);
    setIsBottomToolbarOpen(true);
    setActiveToolbarItem("grid"); // Open area type selector
  };

  const handleAreaTypeApply = (areaType: string) => {
    // When Apply is clicked in Area Type Selector
    setSelectedAreaType(areaType);
    setIsMassSelectorMode(true);
    setActiveToolbarItem(null); // Close the area type panel
  };

  const handleMassSelectorFinish = () => {
    // Handle finishing the mass selector
    setIsMassSelectorMode(false);
    setSelectedAreaType(null);
    setIsTerritoriesOpen(true); // Reopen territories panel
  };

  const handleMassSelectorCancel = () => {
    // Handle canceling the mass selector
    setIsMassSelectorMode(false);
    setSelectedAreaType(null);
  };

  // Handler for Plus button / BottomToolbar - close other panels when opened
  const handlePlusClick = () => {
    const newState = !isBottomToolbarOpen;
    setIsBottomToolbarOpen(newState);
    if (newState) {
      setIsMapLayerOpen(false);
      setIsHeatmapOpen(false);
      setIsFolderOpen(false);
    } else {
      // When closing the toolbar, also close any open tool panels
      setActiveToolbarItem(null);
    }
  };

  // Heatmap position calculation:
  // - MapToolbar is at top-20 (80px)
  // - Toolbar Card height is ~48px
  // - Gap of 12px after toolbar
  const toolbarTop = 80; // top-20
  const toolbarHeight = 48;
  const gapAfterToolbar = 12;

  const heatmapTopPosition = toolbarTop + toolbarHeight + gapAfterToolbar;

  return (
    <FolderProvider>
      <DashboardProvider>
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
            isFolderOpen={isFolderOpen}
            onFolderOpenChange={handleFolderOpenChange}
            onFolderClick={handleTerritoriesToggle}
            isFolderActive={isTerritoriesOpen}
          />

          {/* Folder Dropdown */}
          <FolderDropdown
            isOpen={isTerritoriesOpen}
            onClose={handleTerritoriesToggle}
            onAddFolder={handleAddFolder}
            onAddArea={handleAddArea}
            isHeatmapOpen={isHeatmapOpen}
          />

          {/* Tool Panels */}
          <ToolPanels 
            activeTool={activeToolbarItem}
            onClose={() => setActiveToolbarItem(null)}
            onAreaTypeApply={handleAreaTypeApply}
          />

          {/* Mass Selector */}
          <MassSelector
            isActive={isMassSelectorMode}
            areaType={selectedAreaType || "area"}
            onFinish={handleMassSelectorFinish}
            onCancel={handleMassSelectorCancel}
          />

          {/* Bottom Toolbar */}
          <BottomToolbar 
            isOpen={isBottomToolbarOpen} 
            onClose={() => {
              setIsBottomToolbarOpen(false);
              setActiveToolbarItem(null);
            }}
            onToolClick={handleToolbarClick}
            activeTool={activeToolbarItem}
          />

          {/* Map Toolbar */}
          <MapToolbar
            onPanelChange={handleToolbarPanelChange}
          />

          {/* Map Layer Selector */}
          <MapLayerSelector 
            isOpen={isMapLayerOpen} 
            onOpenChange={handleMapLayerOpenChange} 
          />

          {/* Polygon Drawing */}
          <PolygonDrawing 
            isActive={activeToolbarItem === "draw"} 
          />

          {/* Heatmap Box */}
          <HeatmapBox
            offsetTop={heatmapTopPosition}
            isOpen={isHeatmapOpen}
            onOpenChange={handleHeatmapOpenChange}
            onOpenMyMetrics={handleOpenCustomerMetricsDataFromHeatmap}
            onOpenMyData={handleOpenCustomerMetricsDataFromHeatmap}
            onOpenPointsOfInterest={handleOpenPointsOfInterestFromHeatmap}
            onOpenCompetitiveAnalysis={handleOpenCompetitiveAnalysisFromHeatmap}
            onOpenDemandResearch={handleOpenDemandResearchFromHeatmap}
            onOpenAdministrativeBoundaries={handleOpenAdministrativeBoundariesFromHeatmap}
          />

          {/* Left Side Menu */}
          <FloatingMenu
            onMenuItemClick={handleMenuItemClick}
            activeItem={activePanel}
          />

          {/* All Panels */}
          <DemographicsPanel
            isOpen={isDemographicsOpen}
            onClose={handleCloseDemographics}
            zipcode={selectedZipcode}
          />

          <PointsOfInterestPanel
            isOpen={isPointsOfInterestOpen}
            onClose={handleClosePointsOfInterest}
          />

          <CustomerMetricsAndDataPanel
            isOpen={isCustomerMetricsDataOpen}
            onClose={handleCloseCustomerMetricsData}
          />

          <CompetitiveAnalysisPanel
            isOpen={isCompetitiveAnalysisOpen}
            onClose={handleCloseCompetitiveAnalysis}
          />

          <DemandResearchPanel
            isOpen={isDemandResearchOpen}
            onClose={handleCloseDemandResearch}
          />

          <AdministrativeBoundariesPanel
            isOpen={isAdministrativeBoundariesOpen}
            onClose={handleCloseAdministrativeBoundaries}
          />
        </div>
      </DashboardProvider>
    </FolderProvider>
  );
}

