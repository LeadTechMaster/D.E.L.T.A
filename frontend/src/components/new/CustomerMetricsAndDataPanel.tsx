import { useState } from "react";
import { X, Plus, ChevronDown, ChevronRight, Database, Star, TrendingUp, BarChart3, PieChart, Activity, Zap, Target, Award, Trophy, Sparkles, Layers, Users, DollarSign, Calendar, Home, Percent, HelpCircle } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { ImportDataDialog } from "./ImportDataDialog";
import { FolderDropdownMenu } from "./FolderDropdownMenu";

interface CustomerMetricsAndDataPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

// Available icons for section headers
const availableIcons = [
  { id: "star", Icon: Star, label: "Star" },
  { id: "database", Icon: Database, label: "Database" },
  { id: "trending-up", Icon: TrendingUp, label: "Trending" },
  { id: "bar-chart", Icon: BarChart3, label: "Bar Chart" },
  { id: "pie-chart", Icon: PieChart, label: "Pie Chart" },
  { id: "activity", Icon: Activity, label: "Activity" },
  { id: "zap", Icon: Zap, label: "Lightning" },
  { id: "target", Icon: Target, label: "Target" },
  { id: "award", Icon: Award, label: "Award" },
  { id: "trophy", Icon: Trophy, label: "Trophy" },
  { id: "sparkles", Icon: Sparkles, label: "Sparkles" },
  { id: "layers", Icon: Layers, label: "Layers" },
];

// Available icons for metric symbols
const metricSymbolIcons = [
  { id: "bar-chart", Icon: BarChart3, label: "Bar Chart" },
  { id: "pie-chart", Icon: PieChart, label: "Pie Chart" },
  { id: "activity", Icon: Activity, label: "Activity" },
  { id: "trending-up", Icon: TrendingUp, label: "Trending Up" },
  { id: "users", Icon: Users, label: "Users" },
  { id: "dollar", Icon: DollarSign, label: "Dollar" },
  { id: "calendar", Icon: Calendar, label: "Calendar" },
  { id: "home", Icon: Home, label: "Home" },
  { id: "percent", Icon: Percent, label: "Percent" },
  { id: "target", Icon: Target, label: "Target" },
  { id: "zap", Icon: Zap, label: "Lightning" },
  { id: "database", Icon: Database, label: "Database" },
];

export function CustomerMetricsAndDataPanel({ isOpen, onClose }: CustomerMetricsAndDataPanelProps) {
  const [isImportDialogOpen, setIsImportDialogOpen] = useState(false);
  const [isLocationDropdownOpen, setIsLocationDropdownOpen] = useState(false);
  const [isFormVisible, setIsFormVisible] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(["demographics"]));
  const [metricName, setMetricName] = useState("New metric");
  const [selectedSymbol, setSelectedSymbol] = useState("bar-chart");
  const [formula, setFormula] = useState("");
  const [metricsIcon, setMetricsIcon] = useState("star");
  const [dataIcon, setDataIcon] = useState("database");
  const [isMetricsIconPickerOpen, setIsMetricsIconPickerOpen] = useState(false);
  const [isDataIconPickerOpen, setIsDataIconPickerOpen] = useState(false);
  const [isSymbolPickerOpen, setIsSymbolPickerOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("custom-metrics");

  const toggleSection = (sectionId: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(sectionId)) {
      newExpanded.delete(sectionId);
    } else {
      newExpanded.add(sectionId);
    }
    setExpandedSections(newExpanded);
  };

  const handleAddFormula = (operator: string) => {
    setFormula(prev => prev + operator);
  };

  const demographicsData = [
    { id: 1, name: "Population", iconId: "users" },
    { id: 2, name: "Median total income", iconId: "dollar" },
    { id: 3, name: "Median after-tax income", iconId: "dollar" },
    { id: 4, name: "Average age of the population", iconId: "calendar" },
    { id: 5, name: "Median age of the population", iconId: "calendar" },
  ];

  if (!isOpen) return null;

  const MetricsIconComponent = availableIcons.find(i => i.id === metricsIcon)?.Icon || Star;
  const DataIconComponent = availableIcons.find(i => i.id === dataIcon)?.Icon || Database;
  const SelectedSymbolIcon = metricSymbolIcons.find(i => i.id === selectedSymbol)?.Icon || BarChart3;

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed left-4 top-36 z-40 w-[380px]">
            <Card className="bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20 overflow-hidden flex flex-col">
              {/* Header */}
              <div className="px-3 py-2.5 flex-shrink-0 flex items-center justify-between gap-3">
                <h2 className="text-white text-sm flex-shrink-0">Custom Data</h2>

                {/* Location Selector */}
                <Popover open={isLocationDropdownOpen} onOpenChange={setIsLocationDropdownOpen}>
                  <PopoverTrigger asChild>
                    <button className="flex-1 h-7 px-2.5 flex items-center gap-1.5 text-xs bg-[#0f1219] border border-[#2d3548] text-white rounded-md hover:border-[#00bcd4]/50 transition-colors cursor-pointer">
                      <div className="w-1.5 h-1.5 rounded-full bg-[#00bcd4] flex-shrink-0" />
                      <span className="truncate">Kitchener, ON, Canada</span>
                    </button>
                  </PopoverTrigger>
                  <PopoverContent 
                    align="start" 
                    className="w-[380px] p-0 border-0 shadow-xl"
                    sideOffset={4}
                  >
                    <FolderDropdownMenu 
                      title="Custom Metrics Locations"
                      onAddArea={() => {
                        console.log("Add area");
                        setIsLocationDropdownOpen(false);
                      }}
                      onCreateFolder={() => {
                        console.log("Create folder");
                      }}
                    />
                  </PopoverContent>
                </Popover>
                
                <div className="flex items-center gap-0.5 flex-shrink-0">
                  <button
                    onClick={onClose}
                    className="p-1 hover:bg-[#2d3548] rounded transition-colors"
                  >
                    <X className="h-3.5 w-3.5 text-[#8b92a7]" />
                  </button>
                </div>
              </div>

              {/* Neon Line */}
              <div
                className="h-[2px] bg-gradient-to-r from-transparent via-[#00bcd4] to-transparent flex-shrink-0"
                style={{
                  boxShadow: "0 0 8px rgba(0, 188, 212, 0.8), 0 0 4px rgba(0, 188, 212, 0.6)",
                }}
              />

              {/* Content */}
              <div className="overflow-hidden flex-1 flex flex-col">
          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col overflow-hidden">
            <div className="border-b border-[#2d3548] px-3 bg-[#0f1219]/50 flex-shrink-0">
              <TabsList className="bg-transparent h-auto p-0 gap-1 w-full">
                <TabsTrigger
                  value="custom-metrics"
                  className="flex-1 data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-[#00bcd4] rounded-none px-3 py-2.5 text-[#9ca3af] hover:text-[#00bcd4] transition-all cursor-pointer [&[data-state=active]]:text-[#00bcd4] [&[data-state=active]]:drop-shadow-[0_0_15px_rgba(0,188,212,0.8)] hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]"
                >
                  <div className="flex items-center gap-2">
                    <Popover open={isMetricsIconPickerOpen} onOpenChange={setIsMetricsIconPickerOpen}>
                      <PopoverTrigger asChild>
                        <button 
                          className="p-0.5 hover:bg-[#2d3548] rounded transition-colors cursor-pointer group"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <MetricsIconComponent className="h-3.5 w-3.5 group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]" />
                        </button>
                      </PopoverTrigger>
                      <PopoverContent 
                        side="right" 
                        align="start"
                        className="w-[200px] p-2 bg-[#1a1f2e] border-[#2d3548]"
                        sideOffset={8}
                      >
                        <p className="text-[#8b92a7] text-xs mb-2 px-1">Choose Icon</p>
                        <div className="grid grid-cols-4 gap-1">
                          {availableIcons.map((iconOption) => {
                            const IconComp = iconOption.Icon;
                            return (
                              <button
                                key={iconOption.id}
                                onClick={() => {
                                  setMetricsIcon(iconOption.id);
                                  setIsMetricsIconPickerOpen(false);
                                }}
                                className={`p-2 rounded transition-all cursor-pointer hover:bg-[#2d3548] ${
                                  metricsIcon === iconOption.id ? "bg-[#00bcd4]/20 text-[#00bcd4]" : "text-[#8b92a7]"
                                }`}
                                title={iconOption.label}
                              >
                                <IconComp className="h-4 w-4" />
                              </button>
                            );
                          })}
                        </div>
                      </PopoverContent>
                    </Popover>
                    <span className="text-xs">Custom Metrics</span>
                  </div>
                </TabsTrigger>
                <TabsTrigger
                  value="your-data"
                  className="flex-1 data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-[#00bcd4] rounded-none px-3 py-2.5 text-[#9ca3af] hover:text-[#00bcd4] transition-all cursor-pointer [&[data-state=active]]:text-[#00bcd4] [&[data-state=active]]:drop-shadow-[0_0_15px_rgba(0,188,212,0.8)] hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]"
                >
                  <div className="flex items-center gap-2">
                    <Popover open={isDataIconPickerOpen} onOpenChange={setIsDataIconPickerOpen}>
                      <PopoverTrigger asChild>
                        <button 
                          className="p-0.5 hover:bg-[#2d3548] rounded transition-colors cursor-pointer group"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <DataIconComponent className="h-3.5 w-3.5 group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]" />
                        </button>
                      </PopoverTrigger>
                      <PopoverContent 
                        side="right" 
                        align="start"
                        className="w-[200px] p-2 bg-[#1a1f2e] border-[#2d3548]"
                        sideOffset={8}
                      >
                        <p className="text-[#8b92a7] text-xs mb-2 px-1">Choose Icon</p>
                        <div className="grid grid-cols-4 gap-1">
                          {availableIcons.map((iconOption) => {
                            const IconComp = iconOption.Icon;
                            return (
                              <button
                                key={iconOption.id}
                                onClick={() => {
                                  setDataIcon(iconOption.id);
                                  setIsDataIconPickerOpen(false);
                                }}
                                className={`p-2 rounded transition-all cursor-pointer hover:bg-[#2d3548] ${
                                  dataIcon === iconOption.id ? "bg-[#00bcd4]/20 text-[#00bcd4]" : "text-[#8b92a7]"
                                }`}
                                title={iconOption.label}
                              >
                                <IconComp className="h-4 w-4" />
                              </button>
                            );
                          })}
                        </div>
                      </PopoverContent>
                    </Popover>
                    <span className="text-xs">Your Data</span>
                  </div>
                </TabsTrigger>
              </TabsList>
            </div>

            {/* Tab Content */}
            <div className="flex-1 overflow-y-auto">
              <TabsContent value="custom-metrics" className="px-3 py-2.5 space-y-2.5 mt-0">
                {/* Add a metric button */}
                {!isFormVisible && (
                  <Button
                    onClick={() => setIsFormVisible(true)}
                    className="w-full h-7 text-xs bg-[#00bcd4]/10 hover:bg-[#00bcd4]/20 text-[#00bcd4] border border-[#00bcd4]/30"
                  >
                    <Plus className="h-3 w-3 mr-1" />
                    Add a metric
                  </Button>
                )}

                {/* Metric Form */}
                {isFormVisible && (
                  <Card className="bg-[#0f1219] border-[#2d3548] p-3 space-y-3">
                    {/* NAME */}
                    <div className="space-y-1.5">
                      <label className="text-[#8b92a7] text-xs uppercase tracking-wide">Name</label>
                      <Input
                        value={metricName}
                        onChange={(e) => setMetricName(e.target.value)}
                        className="h-8 text-xs bg-[#1a1f2e] border-[#2d3548] text-white"
                      />
                    </div>

                    {/* SYMBOL */}
                    <div className="space-y-1.5">
                      <label className="text-[#8b92a7] text-xs uppercase tracking-wide">Symbol</label>
                      <Popover open={isSymbolPickerOpen} onOpenChange={setIsSymbolPickerOpen}>
                        <PopoverTrigger asChild>
                          <button className="w-10 h-10 bg-[#1a1f2e] border border-[#2d3548] rounded-lg hover:border-[#00bcd4]/50 transition-all flex items-center justify-center group">
                            <SelectedSymbolIcon className="h-5 w-5 text-[#8b92a7] group-hover:text-[#00bcd4] transition-colors" />
                          </button>
                        </PopoverTrigger>
                        <PopoverContent 
                          side="right" 
                          align="start"
                          className="w-[240px] p-3 bg-[#1a1f2e] border-[#2d3548]"
                          sideOffset={8}
                        >
                          <p className="text-[#8b92a7] text-xs mb-2 uppercase tracking-wide">Choose Symbol</p>
                          <div className="grid grid-cols-4 gap-2">
                            {metricSymbolIcons.map((iconOption) => {
                              const IconComp = iconOption.Icon;
                              return (
                                <button
                                  key={iconOption.id}
                                  onClick={() => {
                                    setSelectedSymbol(iconOption.id);
                                    setIsSymbolPickerOpen(false);
                                  }}
                                  className={`p-2.5 rounded-lg transition-all cursor-pointer hover:bg-[#2d3548] ${
                                    selectedSymbol === iconOption.id ? "bg-[#00bcd4]/20 border border-[#00bcd4]/50" : "border border-transparent"
                                  }`}
                                  title={iconOption.label}
                                >
                                  <IconComp className={`h-4 w-4 ${selectedSymbol === iconOption.id ? "text-[#00bcd4]" : "text-[#8b92a7]"}`} />
                                </button>
                              );
                            })}
                          </div>
                        </PopoverContent>
                      </Popover>
                    </div>

                    {/* FORMULA */}
                    <div className="space-y-2">
                      <label className="text-[#8b92a7] text-xs uppercase tracking-wide">Formula</label>
                      
                      {/* Operator buttons */}
                      <div className="flex items-center gap-2 flex-wrap">
                        {['+', '-', '*', '/', '(', ')'].map((op) => (
                          <button
                            key={op}
                            onClick={() => handleAddFormula(op)}
                            className="w-8 h-8 text-sm bg-[#1a1f2e] hover:bg-[#252b3d] border border-[#2d3548] hover:border-[#00bcd4]/50 text-[#00bcd4] rounded-lg transition-all cursor-pointer"
                          >
                            {op}
                          </button>
                        ))}
                        <button className="h-8 px-3 flex items-center gap-1 text-xs text-[#00bcd4] hover:bg-[#00bcd4]/10 rounded-lg transition-colors cursor-pointer">
                          <HelpCircle className="h-3.5 w-3.5" />
                          Help
                        </button>
                      </div>

                      {/* Search/Formula input */}
                      <Input
                        value={formula}
                        onChange={(e) => setFormula(e.target.value)}
                        placeholder="Type to search for data"
                        className="h-9 text-xs bg-[#1a1f2e] border-[#2d3548] text-white placeholder:text-[#6b7280]"
                      />

                      {/* Data sections */}
                      <div className="space-y-1 mt-2">
                        {/* My Metrics Section */}
                        <div>
                          <button
                            onClick={() => toggleSection("my-metrics")}
                            className="flex items-center justify-between w-full px-2 py-2 hover:bg-[#252b3d] rounded-lg transition-colors group"
                          >
                            <div className="flex items-center gap-2 text-[#8b92a7] text-xs">
                              {expandedSections.has("my-metrics") ? (
                                <ChevronDown className="h-3.5 w-3.5" />
                              ) : (
                                <ChevronRight className="h-3.5 w-3.5" />
                              )}
                              <Star className="h-3.5 w-3.5" />
                              <span className="uppercase tracking-wide">My Metrics (No Data)</span>
                            </div>
                            <ChevronRight className="h-3.5 w-3.5 text-[#8b92a7] opacity-0 group-hover:opacity-100 transition-opacity" />
                          </button>
                        </div>

                        {/* Demographics Section */}
                        <div>
                          <button
                            onClick={() => toggleSection("demographics")}
                            className="flex items-center justify-between w-full px-2 py-2 hover:bg-[#252b3d] rounded-lg transition-colors group"
                          >
                            <div className="flex items-center gap-2 text-[#8b92a7] text-xs">
                              {expandedSections.has("demographics") ? (
                                <ChevronDown className="h-3.5 w-3.5" />
                              ) : (
                                <ChevronRight className="h-3.5 w-3.5" />
                              )}
                              <Users className="h-3.5 w-3.5" />
                              <span className="uppercase tracking-wide">Demographics (588 Data)</span>
                            </div>
                          </button>
                          
                          {expandedSections.has("demographics") && (
                            <div className="mt-1 space-y-0.5 ml-6">
                              {demographicsData.map((item) => {
                                const ItemIcon = metricSymbolIcons.find(i => i.id === item.iconId)?.Icon || BarChart3;
                                return (
                                  <button
                                    key={item.id}
                                    onClick={() => handleAddFormula(`[${item.name}]`)}
                                    className="flex items-center gap-2 w-full px-2 py-1.5 hover:bg-[#252b3d] rounded-lg transition-colors text-left group"
                                  >
                                    <ItemIcon className="h-3.5 w-3.5 text-[#8b92a7] group-hover:text-[#00bcd4] transition-colors" />
                                    <span className="text-white text-xs">{item.name}</span>
                                  </button>
                                );
                              })}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex justify-between pt-2 border-t border-[#2d3548]">
                      <Button
                        variant="ghost"
                        onClick={() => {
                          setIsFormVisible(false);
                          setMetricName("New metric");
                          setFormula("");
                        }}
                        className="h-8 px-4 text-xs text-[#8b92a7] hover:text-[#00bcd4] hover:bg-[#252b3d]"
                      >
                        Cancel
                      </Button>
                      <Button className="h-8 px-4 text-xs bg-[#00bcd4] hover:bg-[#00d4e8] text-black">
                        Save
                      </Button>
                    </div>
                  </Card>
                )}
              </TabsContent>

              <TabsContent value="your-data" className="px-4 py-4 mt-0">
                {/* Add Data Button */}
                <div className="flex justify-center mb-5">
                  <Button
                    onClick={() => setIsImportDialogOpen(true)}
                    className="h-7 text-xs bg-[#00bcd4] hover:bg-[#00bcd4]/90 text-white px-4 py-1 flex items-center gap-1.5"
                  >
                    <Database className="h-3 w-3" />
                    Add your data
                  </Button>
                </div>

                {/* Empty State Illustration */}
                <div className="flex flex-col items-center text-center space-y-3">
                  {/* SVG Illustration - scaled down */}
                  <div className="relative w-[233px] h-[175px] flex items-center justify-center">
                    <svg
                      viewBox="0 0 320 240"
                      className="w-full h-full"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      {/* Background blobs */}
                      <ellipse cx="160" cy="180" rx="120" ry="40" fill="#2d3548" opacity="0.3" />
                      <ellipse cx="100" cy="140" rx="80" ry="60" fill="#2d3548" opacity="0.2" />
                      <ellipse cx="220" cy="140" rx="70" ry="50" fill="#2d3548" opacity="0.2" />
                      
                      {/* Map pin */}
                      <g transform="translate(80, 80)">
                        <path
                          d="M20 0C8.954 0 0 8.954 0 20c0 11.046 20 36 20 36s20-24.954 20-36C40 8.954 31.046 0 20 0z"
                          fill="#6b7280"
                        />
                        <circle cx="20" cy="18" r="8" fill="#9ca3af" />
                      </g>
                      
                      {/* Calendar/Table */}
                      <g transform="translate(140, 100)">
                        <rect x="0" y="0" width="60" height="50" rx="4" fill="#6b7280" />
                        <rect x="4" y="8" width="52" height="38" rx="2" fill="#9ca3af" />
                        {/* Grid lines */}
                        <line x1="8" y1="20" x2="52" y2="20" stroke="#6b7280" strokeWidth="2" />
                        <line x1="8" y1="30" x2="52" y2="30" stroke="#6b7280" strokeWidth="2" />
                        <line x1="26" y1="12" x2="26" y2="42" stroke="#6b7280" strokeWidth="2" />
                        <line x1="38" y1="12" x2="38" y2="42" stroke="#6b7280" strokeWidth="2" />
                        {/* Paperclip */}
                        <path
                          d="M48 -5 L55 2 L50 7 L56 13 L52 17 L46 11 L41 16 L34 9 L39 4 L44 -1 Z"
                          fill="#6b7280"
                          opacity="0.8"
                        />
                      </g>
                      
                      {/* Chart */}
                      <g transform="translate(40, 140)">
                        <rect x="0" y="30" width="50" height="30" rx="4" fill="#6b7280" />
                        {/* Pie chart representation */}
                        <circle cx="25" cy="45" r="15" fill="#9ca3af" />
                        <path
                          d="M25 30 L25 45 L40 45 A15 15 0 0 0 25 30 Z"
                          fill="#4b5563"
                        />
                      </g>
                      
                      {/* Hand pointer */}
                      <g transform="translate(200, 150)">
                        <path
                          d="M20 40 L15 30 L15 20 L18 17 L20 19 L20 10 L23 7 L25 9 L25 15 L28 13 L30 15 L30 20 L33 18 L35 20 L35 30 Z"
                          fill="#9ca3af"
                        />
                        <path
                          d="M15 30 L20 40 L35 40 L35 30"
                          fill="#6b7280"
                        />
                      </g>
                    </svg>
                  </div>

                  {/* Message */}
                  <p className="text-[#8b92a7] text-xs">
                    Import your data to analyze your area
                  </p>
                </div>
              </TabsContent>
            </div>
          </Tabs>
              </div>
            </Card>
          </div>

      {/* Import Dialog */}
      <ImportDataDialog
        isOpen={isImportDialogOpen}
        onClose={() => setIsImportDialogOpen(false)}
      />
    </>
  );
}

