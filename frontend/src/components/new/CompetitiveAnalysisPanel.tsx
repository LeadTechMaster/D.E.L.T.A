import { X, Target, TrendingUp, DollarSign, MapPin, BarChart3, Filter } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { FolderDropdownMenu } from "./FolderDropdownMenu";
import { Badge } from "@/components/ui/badge";

interface CompetitiveAnalysisPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

// Mock competitor data
const competitors = [
  { id: 1, name: "Starbucks Coffee", category: "Coffee Shop", distance: "0.3 mi", revenue: "$2.1M", customers: "15.2K", growth: "+12%" },
  { id: 2, name: "Peet's Coffee", category: "Coffee Shop", distance: "0.5 mi", revenue: "$1.8M", customers: "12.5K", growth: "+8%" },
  { id: 3, name: "Blue Bottle Coffee", category: "Coffee Shop", distance: "0.8 mi", revenue: "$1.5M", customers: "9.8K", growth: "+15%" },
  { id: 4, name: "Local Café", category: "Coffee Shop", distance: "0.4 mi", revenue: "$890K", customers: "6.2K", growth: "+5%" },
  { id: 5, name: "Philz Coffee", category: "Coffee Shop", distance: "1.2 mi", revenue: "$2.3M", customers: "18.1K", growth: "+18%" },
];

export function CompetitiveAnalysisPanel({ isOpen, onClose }: CompetitiveAnalysisPanelProps) {
  const [isFolderDropdownOpen, setIsFolderDropdownOpen] = useState(false);

  if (!isOpen) return null;

  return (
    <div className="fixed left-4 top-36 z-40 w-[380px] animate-in slide-in-from-left-4 duration-300">
      <Card className="bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20 max-h-[calc(100vh-180px)] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between px-3 py-2.5 border-b border-[#2d3548]">
          <h2 className="text-white text-sm">Competitive Analysis</h2>
          <button
            onClick={onClose}
            className="p-0.5 hover:bg-[#2d3548] rounded transition-colors"
          >
            <X className="h-4 w-4 text-[#8b92a7]" />
          </button>
        </div>

        {/* Location Selector */}
        <div className="px-3 py-2.5 border-b border-[#2d3548]">
          <Popover open={isFolderDropdownOpen} onOpenChange={setIsFolderDropdownOpen}>
            <PopoverTrigger asChild>
              <button className="w-full px-3 py-1.5 bg-[#0f1219] border border-[#2d3548] rounded text-white text-sm text-left hover:border-[#00bcd4]/50 transition-colors flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <MapPin className="h-3.5 w-3.5 text-[#00bcd4]" />
                  <span>San Francisco, CA</span>
                </div>
                <span className="text-[#8b92a7]">▼</span>
              </button>
            </PopoverTrigger>
            <PopoverContent 
              className="w-[397px] p-0 bg-[#1a1f2e] border-[#2d3548]" 
              align="start"
              side="bottom"
              sideOffset={4}
            >
              <FolderDropdownMenu />
            </PopoverContent>
          </Popover>
        </div>

        {/* Filter Bar */}
        <div className="px-3 py-2.5 border-b border-[#2d3548]">
          <div className="flex items-center gap-2">
            <Filter className="h-3.5 w-3.5 text-[#8b92a7]" />
            <Input
              placeholder="Search competitors..."
              className="flex-1 h-7 bg-[#0f1219] border-[#2d3548] text-white text-xs placeholder:text-[#6b7280]"
            />
          </div>
        </div>

        {/* Stats Summary */}
        <div className="px-3 py-3 border-b border-[#2d3548] bg-[#0f1219]/50">
          <div className="grid grid-cols-3 gap-3">
            <div className="flex flex-col items-center gap-1 p-2 bg-[#1a1f2e] rounded border border-[#2d3548]">
              <Target className="h-3.5 w-3.5 text-[#00bcd4]" />
              <span className="text-white text-xs">5</span>
              <span className="text-[#8b92a7] text-[10px]">Competitors</span>
            </div>
            <div className="flex flex-col items-center gap-1 p-2 bg-[#1a1f2e] rounded border border-[#2d3548]">
              <DollarSign className="h-3.5 w-3.5 text-[#00bcd4]" />
              <span className="text-white text-xs">$8.6M</span>
              <span className="text-[#8b92a7] text-[10px]">Total Revenue</span>
            </div>
            <div className="flex flex-col items-center gap-1 p-2 bg-[#1a1f2e] rounded border border-[#2d3548]">
              <TrendingUp className="h-3.5 w-3.5 text-green-400" />
              <span className="text-white text-xs">+11.6%</span>
              <span className="text-[#8b92a7] text-[10px]">Avg Growth</span>
            </div>
          </div>
        </div>

        {/* Competitors List */}
        <div className="max-h-[400px] overflow-auto">
          <div className="px-3 py-2 space-y-2">
            {competitors.map((competitor) => (
              <Card 
                key={competitor.id}
                className="bg-[#0f1219] border-[#2d3548] hover:border-[#00bcd4]/50 transition-colors p-3"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1">
                    <h4 className="text-white text-sm">{competitor.name}</h4>
                    <p className="text-[#8b92a7] text-xs">{competitor.category}</p>
                  </div>
                  <Badge variant="outline" className="bg-[#00bcd4]/10 border-[#00bcd4]/30 text-[#00bcd4] text-[10px]">
                    {competitor.distance}
                  </Badge>
                </div>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <span className="text-[#8b92a7] text-[10px]">Revenue</span>
                    <p className="text-white">{competitor.revenue}</p>
                  </div>
                  <div>
                    <span className="text-[#8b92a7] text-[10px]">Customers</span>
                    <p className="text-white">{competitor.customers}</p>
                  </div>
                  <div>
                    <span className="text-[#8b92a7] text-[10px]">Growth</span>
                    <p className="text-green-400">{competitor.growth}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Footer Actions */}
        <div className="px-3 py-2.5 border-t border-[#2d3548] flex items-center gap-2">
          <Button 
            className="flex-1 h-8 bg-[#00bcd4] hover:bg-[#00bcd4]/90 text-black text-xs"
          >
            <BarChart3 className="h-3.5 w-3.5 mr-1.5" />
            Compare Selected
          </Button>
          <Button 
            variant="outline"
            className="h-8 bg-transparent border-[#2d3548] hover:bg-[#2d3548] text-[#8b92a7] hover:text-white text-xs"
          >
            Export
          </Button>
        </div>
      </Card>
    </div>
  );
}

