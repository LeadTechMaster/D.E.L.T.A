import { X, Eye, Download, MoreVertical } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { FolderDropdownMenu } from "./FolderDropdownMenu";

interface PointsOfInterestPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function PointsOfInterestPanel({ isOpen, onClose }: PointsOfInterestPanelProps) {
  const [isLocationDropdownOpen, setIsLocationDropdownOpen] = useState(false);

  if (!isOpen) return null;

  return (
    <div className="fixed left-4 top-36 z-40 w-[380px] animate-in slide-in-from-left-4 duration-300">
      <Card className="bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20 overflow-hidden">
        {/* Header */}
        <div className="px-3 py-2.5 flex items-center justify-between gap-3">
          <h2 className="text-white text-sm flex-shrink-0">Points of Interest</h2>

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
                title="Points of Interest Locations"
                onAddArea={() => {
                  console.log("Add POI area");
                  setIsLocationDropdownOpen(false);
                }}
                onCreateFolder={() => {
                  console.log("Create POI folder");
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
        <div className="max-h-[calc(100vh-240px)] overflow-y-auto">
          {/* Results Section */}
          <div className="px-3 py-2.5">
            <h3 className="text-[#8b92a7] text-xs mb-2">RESULTS</h3>

            {/* New Search Card */}
            <Card className="bg-[#0f1219] border-[#00bcd4]/30 p-2.5 space-y-2.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1.5">
                  <div className="w-2 h-2 rounded-full bg-[#22c55e]" />
                  <span className="text-white text-xs">New Search</span>
                </div>
                <div className="flex items-center gap-0.5">
                  <button className="p-1 hover:bg-[#2d3548] rounded transition-colors">
                    <Eye className="h-3 w-3 text-[#8b92a7] hover:text-[#00bcd4] transition-colors" />
                  </button>
                  <button className="p-1 hover:bg-[#2d3548] rounded transition-colors">
                    <Download className="h-3 w-3 text-[#8b92a7] hover:text-[#00bcd4] transition-colors" />
                  </button>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <button className="p-1 hover:bg-[#2d3548] rounded transition-colors">
                        <MoreVertical className="h-3 w-3 text-[#8b92a7] hover:text-[#00bcd4] transition-colors" />
                      </button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent className="bg-[#1a1f2e] border-[#2d3548]">
                      <DropdownMenuItem className="text-white hover:bg-[#2d3548] cursor-pointer text-xs">
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-white hover:bg-[#2d3548] cursor-pointer text-xs">
                        Duplicate
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-red-500 hover:bg-[#2d3548] cursor-pointer text-xs">
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>

              {/* Categories */}
              <div className="space-y-1">
                <label className="text-[#8b92a7] text-xs">CATEGORIES</label>
                <Input
                  placeholder="e.g. school, grocery store, restaurant..."
                  className="h-7 text-xs bg-[#1a1f2e] border-[#2d3548] text-white placeholder:text-[#8b92a7]/50"
                />
              </div>

              {/* Names */}
              <div className="space-y-1">
                <label className="text-[#8b92a7] text-xs">NAMES</label>
                <Input
                  placeholder="e.g. Walmart, McDonald's..."
                  className="h-7 text-xs bg-[#1a1f2e] border-[#2d3548] text-white placeholder:text-[#8b92a7]/50"
                />
              </div>

              {/* Actions */}
              <div className="flex justify-end gap-1.5 pt-1">
                <Button
                  variant="ghost"
                  className="h-7 px-3 text-xs text-[#00bcd4] hover:text-[#00bcd4] hover:bg-[#00bcd4]/10"
                >
                  Cancel
                </Button>
                <Button className="h-7 px-3 text-xs bg-[#00bcd4] hover:bg-[#00bcd4]/90 text-white">
                  Save
                </Button>
              </div>
            </Card>

            {/* New Search Button */}
            <Button className="w-full mt-2.5 h-7 text-xs bg-[#00bcd4] hover:bg-[#00bcd4]/90 text-white">
              New search
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}

