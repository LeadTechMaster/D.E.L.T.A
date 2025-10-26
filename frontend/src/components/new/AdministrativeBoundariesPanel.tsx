import { X } from "lucide-react";
import { Card } from "@/components/ui/card";
import { useState } from "react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { FolderDropdownMenu } from "./FolderDropdownMenu";

interface AdministrativeBoundariesPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const postalCodesData = [
  { code: "N0C", coverage: 100 },
  { code: "N0G", coverage: 100 },
  { code: "N4N", coverage: 100 },
  { code: "N4W", coverage: 100 },
];

const municipalitiesData = [
  { name: "Minto", coverage: 100 },
  { name: "Wellington North", coverage: 85 },
  { name: "Mapleton", coverage: 92 },
];

const provincesData = [
  { name: "Ontario", coverage: 100 },
];

export function AdministrativeBoundariesPanel({ isOpen, onClose }: AdministrativeBoundariesPanelProps) {
  const [isLocationDropdownOpen, setIsLocationDropdownOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("postal-codes");

  if (!isOpen) return null;

  return (
    <div className="fixed left-4 top-36 z-40 w-[380px]">
          <Card className="bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20 overflow-hidden">
            {/* Header */}
            <div className="px-3 py-2.5 flex items-center justify-between gap-3">
              <h2 className="text-white text-sm flex-shrink-0">Administrative boundaries</h2>

              {/* Location Selector */}
              <Popover open={isLocationDropdownOpen} onOpenChange={setIsLocationDropdownOpen}>
                <PopoverTrigger asChild>
                  <button className="flex-1 h-7 px-2.5 flex items-center gap-1.5 text-xs bg-[#0f1219] border border-[#2d3548] text-white rounded-md hover:border-[#00bcd4]/50 transition-colors cursor-pointer">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#00bcd4] flex-shrink-0" />
                    <span className="truncate">Minto, ON, Canada</span>
                  </button>
                </PopoverTrigger>
                <PopoverContent 
                  align="start" 
                  className="w-[380px] p-0 border-0 shadow-xl"
                  sideOffset={4}
                >
                  <FolderDropdownMenu 
                    title="Boundaries Locations"
                    onAddArea={() => {
                      console.log("Add boundaries area");
                      setIsLocationDropdownOpen(false);
                    }}
                    onCreateFolder={() => {
                      console.log("Create boundaries folder");
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
              className="h-[2px] bg-gradient-to-r from-transparent via-[#00bcd4] to-transparent"
              style={{
                boxShadow: "0 0 8px rgba(0, 188, 212, 0.8), 0 0 4px rgba(0, 188, 212, 0.6)",
              }}
            />

            {/* Content */}
            <div className="overflow-hidden">
              <div className="max-h-[calc(100vh-240px)] overflow-y-auto">
                {/* Tabs */}
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <div className="px-3 pt-2 border-b border-[#2d3548]">
                    <TabsList className="w-full bg-transparent h-auto p-0 gap-4">
                      <TabsTrigger 
                        value="postal-codes" 
                        className="bg-transparent data-[state=active]:bg-transparent px-0 pb-1.5 border-b-2 border-transparent data-[state=active]:border-[#00bcd4] text-[#8b92a7] data-[state=active]:text-[#00bcd4] rounded-none hover:text-[#00bcd4] transition-colors text-xs"
                      >
                        Postal codes
                      </TabsTrigger>
                      <TabsTrigger 
                        value="municipalities" 
                        className="bg-transparent data-[state=active]:bg-transparent px-0 pb-1.5 border-b-2 border-transparent data-[state=active]:border-[#00bcd4] text-[#8b92a7] data-[state=active]:text-[#00bcd4] rounded-none hover:text-[#00bcd4] transition-colors text-xs"
                      >
                        Municipalities
                      </TabsTrigger>
                      <TabsTrigger 
                        value="provinces" 
                        className="bg-transparent data-[state=active]:bg-transparent px-0 pb-1.5 border-b-2 border-transparent data-[state=active]:border-[#00bcd4] text-[#8b92a7] data-[state=active]:text-[#00bcd4] rounded-none hover:text-[#00bcd4] transition-colors text-xs"
                      >
                        Provinces/Territories
                      </TabsTrigger>
                    </TabsList>
                  </div>

                  {/* Postal Codes Tab */}
                  <TabsContent value="postal-codes" className="p-3 m-0">
                    <div className="space-y-3">
                      <div>
                        <h3 className="text-white mb-0.5 text-sm">List of postal codes</h3>
                        <p className="text-[#8b92a7] text-xs">Results: {postalCodesData.length}</p>
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center text-[#8b92a7] text-xs">
                          <span className="w-20">Postcode</span>
                          <span className="flex-1">% of coverage</span>
                        </div>
                        
                        {postalCodesData.map((item) => (
                          <div key={item.code} className="flex items-center gap-3">
                            <span className="text-white text-xs w-16">{item.code}</span>
                            <div className="flex-1 flex items-center gap-2">
                              <div className="flex-1 h-1.5 bg-[#0f1419] rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-[#00bcd4] rounded-full transition-all"
                                  style={{ width: `${item.coverage}%` }}
                                />
                              </div>
                              <span className="text-white text-xs w-10 text-right">{item.coverage}%</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </TabsContent>

                  {/* Municipalities Tab */}
                  <TabsContent value="municipalities" className="p-3 m-0">
                    <div className="space-y-3">
                      <div>
                        <h3 className="text-white mb-0.5 text-sm">List of municipalities</h3>
                        <p className="text-[#8b92a7] text-xs">Results: {municipalitiesData.length}</p>
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center text-[#8b92a7] text-xs">
                          <span className="w-32">Municipality</span>
                          <span className="flex-1">% of coverage</span>
                        </div>
                        
                        {municipalitiesData.map((item) => (
                          <div key={item.name} className="flex items-center gap-3">
                            <span className="text-white text-xs w-32">{item.name}</span>
                            <div className="flex-1 flex items-center gap-2">
                              <div className="flex-1 h-1.5 bg-[#0f1419] rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-[#00bcd4] rounded-full transition-all"
                                  style={{ width: `${item.coverage}%` }}
                                />
                              </div>
                              <span className="text-white text-xs w-10 text-right">{item.coverage}%</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </TabsContent>

                  {/* Provinces/Territories Tab */}
                  <TabsContent value="provinces" className="p-3 m-0">
                    <div className="space-y-3">
                      <div>
                        <h3 className="text-white mb-0.5 text-sm">List of provinces/territories</h3>
                        <p className="text-[#8b92a7] text-xs">Results: {provincesData.length}</p>
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center text-[#8b92a7] text-xs">
                          <span className="w-32">Province/Territory</span>
                          <span className="flex-1">% of coverage</span>
                        </div>
                        
                        {provincesData.map((item) => (
                          <div key={item.name} className="flex items-center gap-3">
                            <span className="text-white text-xs w-32">{item.name}</span>
                            <div className="flex-1 flex items-center gap-2">
                              <div className="flex-1 h-1.5 bg-[#0f1419] rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-[#00bcd4] rounded-full transition-all"
                                  style={{ width: `${item.coverage}%` }}
                                />
                              </div>
                              <span className="text-white text-xs w-10 text-right">{item.coverage}%</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
              </div>
            </div>
          </Card>
        </div>
  );
}

