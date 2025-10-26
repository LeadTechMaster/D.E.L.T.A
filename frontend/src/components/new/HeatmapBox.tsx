import { Card } from "@/components/ui/card";
import { Flame, X } from "lucide-react";
import { useState } from "react";
import { Switch } from "@/components/ui/switch";
import { Dialog, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Search, Star, Users, TrendingUp, ChevronRight, ChevronDown, Check, BarChart3, User, Home, DollarSign, GraduationCap, Heart, Baby, Plus, MapPin, Target } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Collapsible, CollapsibleTrigger, CollapsibleContent } from "@/components/ui/collapsible";

interface HeatmapBoxProps {
  offsetTop?: number;
  isOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  onOpenMyMetrics?: () => void;
  onOpenMyData?: () => void;
  onOpenPointsOfInterest?: () => void;
  onOpenCompetitiveAnalysis?: () => void;
  onOpenDemandResearch?: () => void;
}

interface DataTypeSection {
  id: string;
  name: string;
  count: number;
  icon: typeof Star;
  items: string[];
  subcategories?: {
    id: string;
    name: string;
    icon: typeof User;
    items: string[];
  }[];
}

interface HeatmapLayer {
  id: string;
  data: string;
}

export function HeatmapBox({ 
  isOpen: externalIsOpen, 
  onOpenChange,
  onOpenMyMetrics,
  onOpenMyData,
  onOpenPointsOfInterest,
  onOpenCompetitiveAnalysis,
  onOpenDemandResearch
}: HeatmapBoxProps) {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentLayerIndex, setCurrentLayerIndex] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [expandedSection, setExpandedSection] = useState<string>("demographics");
  const [activeSubcategory, setActiveSubcategory] = useState<string | null>("all");
  const [internalIsOpen, setInternalIsOpen] = useState(false);
  const [isHeatmapEnabled, setIsHeatmapEnabled] = useState(true);
  const [layers, setLayers] = useState<HeatmapLayer[]>([
    { id: "1", data: "Population Density" },
  ]);

  // Use external state if provided, otherwise use internal state
  const isOpen = externalIsOpen !== undefined ? externalIsOpen : internalIsOpen;
  const setIsOpen = onOpenChange || setInternalIsOpen;

  const dataTypeSections: DataTypeSection[] = [
    {
      id: "my-metrics",
      name: "MY METRICS",
      count: 0,
      icon: Star,
      items: []
    },
    {
      id: "demographics",
      name: "DEMOGRAPHICS",
      count: 588,
      icon: Users,
      items: [],
      subcategories: [
        {
          id: "population",
          name: "Population",
          icon: Users,
          items: [
            "Population",
            "Population Density",
            "Population under 4 years",
            "Population 5 to 9 years",
            "Population 10 to 14 years",
            "Population under 14 years",
            "Population 15 to 64 years",
            "Population 65 years and over"
          ]
        },
        {
          id: "age",
          name: "Age",
          icon: Baby,
          items: [
            "Average age of the population",
            "Median age of the population",
            "Age Distribution"
          ]
        },
        {
          id: "households",
          name: "Households",
          icon: Home,
          items: [
            "Total Households",
            "Average Household Size",
            "Housing Units",
            "Median Home Value"
          ]
        },
        {
          id: "income",
          name: "Income",
          icon: DollarSign,
          items: [
            "Median total income",
            "Median after-tax income"
          ]
        },
        {
          id: "education",
          name: "Education & Work",
          icon: GraduationCap,
          items: [
            "Educational Attainment",
            "Employment Rate",
            "Unemployment Rate",
            "Commute Times"
          ]
        },
        {
          id: "diversity",
          name: "Diversity",
          icon: Heart,
          items: [
            "Diversity Index",
            "Gender Ratio"
          ]
        }
      ]
    },
    {
      id: "custom-metrics",
      name: "CUSTOM METRICS DATA",
      count: 6,
      icon: TrendingUp,
      items: [
        "Custom Index 1",
        "Custom Index 2",
        "Composite Score",
        "Trend Analysis",
        "Growth Rate",
        "Market Score"
      ]
    },
    {
      id: "points-of-interest",
      name: "POINTS OF INTEREST",
      count: 0,
      icon: MapPin,
      items: []
    },
    {
      id: "competitor",
      name: "COMPETITOR",
      count: 0,
      icon: Target,
      items: []
    },
    {
      id: "demand-seo",
      name: "DEMAND / SEO",
      count: 0,
      icon: TrendingUp,
      items: []
    }
  ];

  const getFilteredSections = () => {
    if (!searchTerm) return dataTypeSections;
    
    return dataTypeSections.map(section => {
      if (section.subcategories) {
        // For sections with subcategories (Demographics)
        const filteredSubcategories = section.subcategories.map(subcat => ({
          ...subcat,
          items: subcat.items.filter(item =>
            item.toLowerCase().includes(searchTerm.toLowerCase())
          )
        })).filter(subcat => subcat.items.length > 0);
        
        return {
          ...section,
          subcategories: filteredSubcategories
        };
      } else {
        // For sections without subcategories
        return {
          ...section,
          items: section.items.filter(item =>
            item.toLowerCase().includes(searchTerm.toLowerCase())
          )
        };
      }
    }).filter(section => {
      if (section.subcategories) {
        return section.subcategories.length > 0;
      }
      return section.items.length > 0;
    });
  };

  const handleAddLayer = () => {
    if (layers.length >= 3) return; // Limit to 3 layers
    const newLayer: HeatmapLayer = {
      id: (layers.length + 1).toString(),
      data: "Population Density",
    };
    setLayers([...layers, newLayer]);
  };

  const handleRemoveLayer = (index: number) => {
    const newLayers = layers.filter((_, i) => i !== index);
    setLayers(newLayers);
  };

  const openDialog = (index: number) => {
    setIsDialogOpen(true);
    setCurrentLayerIndex(index);
  };

  const handleSelectData = (item: string) => {
    const newLayers = layers.map((layer, index) => {
      if (index === currentLayerIndex) {
        return { ...layer, data: item };
      }
      return layer;
    });
    setLayers(newLayers);
    setIsDialogOpen(false);
  };

  return (
    <div className={`fixed top-[252px] transition-all duration-300 ${isOpen ? 'right-[68px] z-50' : 'right-4 z-40'}`}>
      <Card 
        onClick={() => !isOpen && (onOpenChange ? onOpenChange(true) : setIsOpen(true))}
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
              onOpenChange ? onOpenChange(false) : setIsOpen(false);
            }}
            className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-[#1a1f2e] border-2 border-[#00bcd4] flex items-center justify-center hover:bg-[#00bcd4] transition-colors cursor-pointer group z-10"
          >
            <X className="h-4 w-4 text-[#00bcd4] group-hover:text-white" />
          </button>
        )}
        
        {/* Header */}
        {isOpen ? (
          // Open state - horizontal layout
          <div className="flex items-center justify-between gap-6 px-4 py-1.5 w-[240px]">
            <div className="cursor-pointer group flex-shrink-0">
              <Flame className={`h-9 w-9 transition-all ${
                isHeatmapEnabled 
                  ? "text-[#00bcd4] drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]" 
                  : "text-[#6b7280]"
              }`} />
            </div>
            <button 
              onClick={(e) => {
                e.stopPropagation();
                onOpenChange ? onOpenChange(false) : setIsOpen(false);
              }}
              className="text-white flex-1 text-center cursor-pointer hover:text-[#00bcd4] transition-colors"
            >
              Heatmap
            </button>
            <Switch 
              checked={isHeatmapEnabled} 
              onCheckedChange={(checked) => {
                setIsHeatmapEnabled(checked);
              }}
              onClick={(e) => e.stopPropagation()}
              className={`flex-shrink-0 scale-110 ${isHeatmapEnabled ? '!bg-[#00bcd4] drop-shadow-[0_0_8px_rgba(0,188,212,0.8)]' : ''}`}
            />
          </div>
        ) : (
          // Collapsed state
          <div className="p-2.5 rounded-lg">
            <div className="cursor-pointer group">
              <Flame className={`h-5 w-5 transition-all ${
                isHeatmapEnabled 
                  ? "text-[#00bcd4] drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]" 
                  : "text-[#8b92a7]"
              }`} />
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
            <div className="px-2.5 pb-2.5 pt-2 w-[240px]">
              {/* Data Type Label */}
              <div className="flex items-center justify-between mb-1">
                <label className="text-[#9ca3af] text-xs">Data Type</label>
              </div>
          
          {/* Data Type Layers */}
          <div className="space-y-1.5 mb-2">
            {layers.map((layer, index) => (
              <div key={layer.id} className="flex items-center gap-1.5">
                <button 
                  onClick={() => openDialog(index)}
                  className="flex-1 flex items-center justify-between p-2 bg-[#0f1219] rounded-lg border border-[#2d3548] hover:border-[#00bcd4]/50 transition-colors cursor-pointer"
                >
                  <span className="text-white text-xs">{layer.data}</span>
                  <Search className="h-3.5 w-3.5 text-[#00bcd4] hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)] transition-all" />
                </button>
                {layers.length > 1 && (
                  <button
                    onClick={() => handleRemoveLayer(index)}
                    className="p-2 bg-[#0f1219] rounded-lg border border-[#2d3548] hover:border-red-500 transition-colors cursor-pointer"
                  >
                    <span className="text-[#9ca3af] hover:text-red-500 transition-colors text-xs">✕</span>
                  </button>
                )}
              </div>
            ))}
          </div>

          {/* Add HeatMap Layer Button */}
          <button
            onClick={handleAddLayer}
            disabled={layers.length >= 3}
            className={`w-full flex items-center justify-center gap-1.5 p-1.5 rounded-lg border transition-all cursor-pointer mb-2 ${
              layers.length >= 3
                ? "text-[#6b7280] bg-[#1a1f2e] border-[#2d3548] cursor-not-allowed opacity-50"
                : "text-[#00bcd4] hover:text-white hover:bg-[#252b3d] border-[#2d3548] hover:border-[#00bcd4]"
            }`}
          >
            <span className="text-lg">+</span>
            <span className="text-xs">HeatMap Layer {layers.length >= 3 && "(Max 3)"}</span>
          </button>

          {/* Density Gradient */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-[#9ca3af] text-sm">Density by km²</label>
            </div>
            <div className="space-y-2">
              {/* Gradient Bar */}
              <div
                className="h-2 rounded-full"
                style={{
                  background: "linear-gradient(to right, #1e88e5, #00bcd4, #26c6da, #ffeb3b, #ff9800, #f44336)",
                }}
              />
              {/* Min/Max Labels */}
              <div className="flex justify-between text-[#9ca3af] text-xs">
                <span>0</span>
                <span>14,998</span>
              </div>
            </div>
          </div>
            </div>
          </>
        )}
      </Card>

      {/* Dialog for selecting heatmap data */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-[#1a1f2e] border-[#2d3548] max-w-2xl p-0">
          <div className="sr-only">
            <DialogTitle>Select Heatmap Data</DialogTitle>
            <DialogDescription>
              Choose data to visualize on the map
            </DialogDescription>
          </div>

          {/* Search Bar */}
          <div className="sticky top-0 bg-[#1a1f2e] border-b border-[#2d3548] p-4 z-10">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6b7280]" />
              <Input
                type="text"
                placeholder="Search for data to display on the heatmap"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-[#0f1219] border-[#2d3548] text-white placeholder:text-[#6b7280]"
              />
              <button
                onClick={() => setIsDialogOpen(false)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#6b7280] hover:text-white transition-colors cursor-pointer"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Data Type Sections */}
          <ScrollArea className="h-[500px]">
            <div className="p-4 space-y-2">
              {getFilteredSections().map((section) => {
                const Icon = section.icon;
                const isExpanded = expandedSection === section.id;
                const hasNoData = section.count === 0;
                
                return (
                  <Collapsible
                    key={section.id}
                    open={isExpanded}
                    onOpenChange={(open) => setExpandedSection(open ? section.id : "")}
                  >
                    <CollapsibleTrigger className="flex items-center justify-between w-full p-3 rounded-lg hover:bg-[#252b3d] transition-colors cursor-pointer group">
                      <div className="flex items-center gap-3">
                        <Icon className={`h-4 w-4 ${hasNoData ? 'text-[#6b7280]' : 'text-[#00bcd4]'}`} />
                        <span className={`text-sm ${hasNoData ? 'text-[#6b7280]' : 'text-[#8b92a7]'}`}>
                          {section.name} {hasNoData ? '(NO DATA)' : `(${section.count} DATA)`}
                        </span>
                      </div>
                      {isExpanded ? (
                        <ChevronDown className="h-4 w-4 text-[#6b7280]" />
                      ) : (
                        <ChevronRight className="h-4 w-4 text-[#6b7280]" />
                      )}
                    </CollapsibleTrigger>
                    
                    <CollapsibleContent className="mt-1">
                      {/* Special handling for MY METRICS */}
                      {section.id === "my-metrics" && (
                        <div className="ml-2 mb-2">
                          <button
                            onClick={() => {
                              setIsDialogOpen(false);
                              onOpenMyData?.();
                            }}
                            className="w-full flex items-center gap-2 p-2.5 rounded-lg bg-[#0f1219] border border-[#2d3548] hover:border-[#00bcd4]/50 text-[#00bcd4] hover:bg-[#252b3d] transition-all cursor-pointer"
                          >
                            <Plus className="h-4 w-4" />
                            <span className="text-sm">Add Data</span>
                          </button>
                        </div>
                      )}

                      {/* Special handling for CUSTOM METRICS */}
                      {section.id === "custom-metrics" && (
                        <div className="ml-2 mb-2">
                          <button
                            onClick={() => {
                              setIsDialogOpen(false);
                              onOpenMyMetrics?.();
                            }}
                            className="w-full flex items-center gap-2 p-2.5 rounded-lg bg-[#0f1219] border border-[#2d3548] hover:border-[#00bcd4]/50 text-[#00bcd4] hover:bg-[#252b3d] transition-all cursor-pointer"
                          >
                            <Plus className="h-4 w-4" />
                            <span className="text-sm">Create</span>
                          </button>
                        </div>
                      )}

                      {/* Special handling for POINTS OF INTEREST */}
                      {section.id === "points-of-interest" && (
                        <div className="ml-2 mb-2">
                          <button
                            onClick={() => {
                              setIsDialogOpen(false);
                              onOpenPointsOfInterest?.();
                            }}
                            className="w-full flex items-center gap-2 p-2.5 rounded-lg bg-[#0f1219] border border-[#2d3548] hover:border-[#00bcd4]/50 text-[#00bcd4] hover:bg-[#252b3d] transition-all cursor-pointer"
                          >
                            <MapPin className="h-4 w-4" />
                            <span className="text-sm">Browse Points of Interest</span>
                          </button>
                        </div>
                      )}

                      {/* Special handling for COMPETITOR */}
                      {section.id === "competitor" && (
                        <div className="ml-2 mb-2">
                          <button
                            onClick={() => {
                              setIsDialogOpen(false);
                              onOpenCompetitiveAnalysis?.();
                            }}
                            className="w-full flex items-center gap-2 p-2.5 rounded-lg bg-[#0f1219] border border-[#2d3548] hover:border-[#00bcd4]/50 text-[#00bcd4] hover:bg-[#252b3d] transition-all cursor-pointer"
                          >
                            <Target className="h-4 w-4" />
                            <span className="text-sm">View Competitors</span>
                          </button>
                        </div>
                      )}

                      {/* Special handling for DEMAND / SEO */}
                      {section.id === "demand-seo" && (
                        <div className="ml-2 mb-2">
                          <button
                            onClick={() => {
                              setIsDialogOpen(false);
                              onOpenDemandResearch?.();
                            }}
                            className="w-full flex items-center gap-2 p-2.5 rounded-lg bg-[#0f1219] border border-[#2d3548] hover:border-[#00bcd4]/50 text-[#00bcd4] hover:bg-[#252b3d] transition-all cursor-pointer"
                          >
                            <TrendingUp className="h-4 w-4" />
                            <span className="text-sm">Research Demand</span>
                          </button>
                        </div>
                      )}

                      {/* Horizontal Subcategories for Demographics */}
                      {section.id === "demographics" && section.subcategories ? (
                        <div className="ml-2 space-y-3">
                          {/* Subcategory Pills - Horizontal */}
                          <div className="flex flex-wrap gap-2 mb-3">
                            {/* All option */}
                            <button
                              onClick={() => setActiveSubcategory("all")}
                              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                                activeSubcategory === "all"
                                  ? "bg-[#00bcd4]/20 border border-[#00bcd4]/50 text-[#00bcd4]"
                                  : "bg-[#0f1219] border border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/30 hover:text-[#00bcd4]"
                              }`}
                            >
                              <Users className="h-3 w-3" />
                              <span className="text-xs">All</span>
                            </button>
                            {section.subcategories.map((subcat) => {
                              const SubIcon = subcat.icon;
                              const isActive = activeSubcategory === subcat.id;
                              
                              return (
                                <button
                                  key={subcat.id}
                                  onClick={() => setActiveSubcategory(subcat.id)}
                                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                                    isActive
                                      ? "bg-[#00bcd4]/20 border border-[#00bcd4]/50 text-[#00bcd4]"
                                      : "bg-[#0f1219] border border-[#2d3548] text-[#8b92a7] hover:border-[#00bcd4]/30 hover:text-[#00bcd4]"
                                  }`}
                                >
                                  <SubIcon className="h-3 w-3" />
                                  <span className="text-xs">{subcat.name}</span>
                                </button>
                              );
                            })}
                          </div>

                          {/* Items for Active Subcategory */}
                          <div className="space-y-0.5">
                            {(activeSubcategory === "all"
                              ? section.subcategories.flatMap((subcat) => subcat.items)
                              : section.subcategories
                                  .filter((subcat) => subcat.id === activeSubcategory)
                                  .flatMap((subcat) => subcat.items)
                            ).map((item) => {
                              const isSelected = layers[currentLayerIndex]?.data === item;
                              
                              return (
                                <button
                                  key={item}
                                  onClick={() => handleSelectData(item)}
                                  className="w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-[#252b3d] transition-colors cursor-pointer group text-left"
                                >
                                  <BarChart3 className="h-4 w-4 text-[#00bcd4] flex-shrink-0" />
                                  <span className={`flex-1 text-sm ${isSelected ? 'text-white' : 'text-[#e0e0e0]'}`}>
                                    {item}
                                  </span>
                                  {isSelected && (
                                    <Check className="h-4 w-4 text-[#00bcd4] flex-shrink-0" />
                                  )}
                                </button>
                              );
                            })}
                          </div>
                        </div>
                      ) : (
                        /* Regular items for non-Demographics sections */
                        <div className="space-y-0.5 ml-2">
                          {section.items.map((item) => {
                            const isSelected = layers[currentLayerIndex]?.data === item;
                            
                            return (
                              <button
                                key={item}
                                onClick={() => handleSelectData(item)}
                                className="w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-[#252b3d] transition-colors cursor-pointer group text-left"
                              >
                                <BarChart3 className="h-4 w-4 text-[#00bcd4] flex-shrink-0" />
                                <span className={`flex-1 text-sm ${isSelected ? 'text-white' : 'text-[#e0e0e0]'}`}>
                                  {item}
                                </span>
                                {isSelected && (
                                  <Check className="h-4 w-4 text-[#00bcd4] flex-shrink-0" />
                                )}
                              </button>
                            );
                          })}
                        </div>
                      )}
                    </CollapsibleContent>
                  </Collapsible>
                );
              })}
            </div>
          </ScrollArea>
        </DialogContent>
      </Dialog>
    </div>
  );
}

