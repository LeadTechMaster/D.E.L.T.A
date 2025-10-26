import { X, TrendingUp, Search, BarChart3, Eye, Plus, Trash2 } from "lucide-react";
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

interface DemandResearchPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

interface KeywordData {
  id: string;
  keyword: string;
  volume: string;
  trend: string;
  trendPercent: number;
  yoyChange: string;
  competition: "High" | "Medium" | "Low";
  cpc: string;
  bidLow: string;
  bidHigh: string;
}

// Mock keyword data generator
const generateKeywordData = (keyword: string): KeywordData => {
  const volumes = ["135K", "89K", "67K", "45K", "54K", "38K", "28K", "92K", "71K", "103K"];
  const trends = ["+24%", "+18%", "+12%", "+8%", "+15%", "+6%", "-3%", "+21%", "+9%", "+11%"];
  const yoyChanges = ["+18%", "+12%", "+8%", "-5%", "+22%", "+3%", "-8%", "+16%", "+7%", "+14%"];
  const competitions: ("High" | "Medium" | "Low")[] = ["High", "Medium", "Low"];
  const cpcs = ["$2.45", "$1.89", "$1.34", "$0.98", "$1.12", "$1.56", "$2.10", "$1.75", "$0.85", "$1.95"];
  const bidLows = ["$1.20", "$0.95", "$0.70", "$0.50", "$0.60", "$0.85", "$1.10", "$0.90", "$0.45", "$1.00"];
  const bidHighs = ["$3.80", "$2.95", "$2.10", "$1.50", "$1.75", "$2.40", "$3.25", "$2.70", "$1.35", "$3.00"];
  
  const index = Math.floor(Math.random() * volumes.length);
  
  return {
    id: Math.random().toString(36).substr(2, 9),
    keyword,
    volume: volumes[index],
    trend: trends[index],
    trendPercent: parseFloat(trends[index]),
    yoyChange: yoyChanges[index],
    competition: competitions[Math.floor(Math.random() * competitions.length)],
    cpc: cpcs[index],
    bidLow: bidLows[index],
    bidHigh: bidHighs[index],
  };
};

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty) {
    case "High":
      return "text-red-400 bg-red-400/10 border-red-400/30";
    case "Medium":
      return "text-yellow-400 bg-yellow-400/10 border-yellow-400/30";
    case "Low":
      return "text-green-400 bg-green-400/10 border-green-400/30";
    default:
      return "text-[#8b92a7] bg-[#2d3548]/10 border-[#2d3548]/30";
  }
};

// Simple sparkline component
const Sparkline = ({ trend }: { trend: number }) => {
  const isPositive = trend >= 0;
  return (
    <svg width="60" height="20" className="inline-block">
      <polyline
        points="0,15 15,12 30,8 45,10 60,5"
        fill="none"
        stroke={isPositive ? "#4ade80" : "#f87171"}
        strokeWidth="1.5"
      />
    </svg>
  );
};

export function DemandResearchPanel({ isOpen, onClose }: DemandResearchPanelProps) {
  const [isLocationDropdownOpen, setIsLocationDropdownOpen] = useState(false);
  const [keywordInput, setKeywordInput] = useState("");
  const [keywords, setKeywords] = useState<KeywordData[]>([
    generateKeywordData("coffee shop near me"),
    generateKeywordData("best coffee in san francisco"),
    generateKeywordData("specialty coffee"),
  ]);

  const handleAddKeyword = () => {
    if (keywordInput.trim() && keywords.length < 10) {
      setKeywords([...keywords, generateKeywordData(keywordInput.trim())]);
      setKeywordInput("");
    }
  };

  const handleRemoveKeyword = (id: string) => {
    setKeywords(keywords.filter((k) => k.id !== id));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleAddKeyword();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed left-4 top-36 z-40 w-[600px] animate-in slide-in-from-left-4 duration-300">
      <Card className="bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20 overflow-hidden">
        {/* Header */}
        <div className="px-3 py-2.5 flex items-center justify-between gap-3">
          <h2 className="text-white text-sm flex-shrink-0">Demand Research</h2>

          {/* Location Selector */}
          <Popover open={isLocationDropdownOpen} onOpenChange={setIsLocationDropdownOpen}>
            <PopoverTrigger asChild>
              <button className="flex-1 h-7 px-2.5 flex items-center gap-1.5 text-xs bg-[#0f1219] border border-[#2d3548] text-white rounded-md hover:border-[#00bcd4]/50 transition-colors cursor-pointer">
                <div className="w-1.5 h-1.5 rounded-full bg-[#00bcd4] flex-shrink-0" />
                <span className="truncate">San Francisco, CA</span>
              </button>
            </PopoverTrigger>
            <PopoverContent 
              align="start" 
              className="w-[380px] p-0 border-0 shadow-xl"
              sideOffset={4}
            >
              <FolderDropdownMenu 
                title="Demand Research Locations"
                onAddArea={() => {
                  console.log("Add demand research area");
                  setIsLocationDropdownOpen(false);
                }}
                onCreateFolder={() => {
                  console.log("Create demand research folder");
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
          {/* Keyword Input */}
          <div className="px-3 py-2.5 border-b border-[#2d3548]">
            <div className="flex items-center gap-2">
              <Search className="h-3.5 w-3.5 text-[#8b92a7]" />
              <Input
                placeholder={`Enter keyword... (${keywords.length}/10)`}
                value={keywordInput}
                onChange={(e) => setKeywordInput(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={keywords.length >= 10}
                className="flex-1 h-7 bg-[#0f1219] border-[#2d3548] text-white text-xs placeholder:text-[#6b7280] disabled:opacity-50"
              />
              <Button
                onClick={handleAddKeyword}
                disabled={!keywordInput.trim() || keywords.length >= 10}
                className="h-7 px-2 bg-[#00bcd4] hover:bg-[#00bcd4]/90 text-black disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Plus className="h-3.5 w-3.5" />
              </Button>
            </div>
          </div>

          {/* Stats Summary */}
          {keywords.length > 0 && (
            <div className="px-3 py-3 border-b border-[#2d3548] bg-[#0f1219]/50">
              <div className="grid grid-cols-3 gap-3">
                <div className="flex flex-col items-center gap-1 p-2 bg-[#1a1f2e] rounded border border-[#2d3548]">
                  <Search className="h-3.5 w-3.5 text-[#00bcd4]" />
                  <span className="text-white text-xs">{keywords.length} Keywords</span>
                  <span className="text-[#8b92a7] text-[10px]">Tracked</span>
                </div>
                <div className="flex flex-col items-center gap-1 p-2 bg-[#1a1f2e] rounded border border-[#2d3548]">
                  <TrendingUp className="h-3.5 w-3.5 text-green-400" />
                  <span className="text-white text-xs">
                    {(keywords.reduce((sum, k) => sum + k.trendPercent, 0) / keywords.length).toFixed(1)}%
                  </span>
                  <span className="text-[#8b92a7] text-[10px]">Avg Trend</span>
                </div>
                <div className="flex flex-col items-center gap-1 p-2 bg-[#1a1f2e] rounded border border-[#2d3548]">
                  <Eye className="h-3.5 w-3.5 text-[#00bcd4]" />
                  <span className="text-white text-xs">
                    ${(keywords.reduce((sum, k) => sum + parseFloat(k.cpc.replace("$", "")), 0) / keywords.length).toFixed(2)}
                  </span>
                  <span className="text-[#8b92a7] text-[10px]">Avg CPC</span>
                </div>
              </div>
            </div>
          )}

          {/* Keywords Table */}
          <div className="max-h-[500px] overflow-auto">
            {keywords.length === 0 ? (
              <div className="px-3 py-8 text-center">
                <Search className="h-8 w-8 text-[#8b92a7] mx-auto mb-2" />
                <p className="text-[#8b92a7] text-sm">Add keywords to start researching demand</p>
                <p className="text-[#6b7280] text-xs mt-1">You can add up to 10 keywords</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead className="sticky top-0 bg-[#1a1f2e] border-b border-[#2d3548]">
                    <tr>
                      <th className="text-left px-3 py-2 text-[#8b92a7] font-medium">Keyword</th>
                      <th className="text-right px-2 py-2 text-[#8b92a7] font-medium">Monthly Searches</th>
                      <th className="text-center px-2 py-2 text-[#8b92a7] font-medium">Trend</th>
                      <th className="text-right px-2 py-2 text-[#8b92a7] font-medium">YoY Change</th>
                      <th className="text-center px-2 py-2 text-[#8b92a7] font-medium">Competition</th>
                      <th className="text-right px-2 py-2 text-[#8b92a7] font-medium">CPC</th>
                      <th className="text-right px-2 py-2 text-[#8b92a7] font-medium">Bid Range</th>
                      <th className="text-center px-2 py-2 text-[#8b92a7] font-medium w-8"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {keywords.map((item, index) => (
                      <tr 
                        key={item.id}
                        className={`border-b border-[#2d3548] hover:bg-[#252b3d] transition-colors ${
                          index % 2 === 0 ? "bg-[#0f1219]/30" : "bg-[#0f1219]/10"
                        }`}
                      >
                        <td className="px-3 py-2.5 text-white max-w-[140px] truncate" title={item.keyword}>
                          {item.keyword}
                        </td>
                        <td className="px-2 py-2.5 text-right text-white">
                          {item.volume}
                        </td>
                        <td className="px-2 py-2.5 text-center">
                          <Sparkline trend={item.trendPercent} />
                        </td>
                        <td className={`px-2 py-2.5 text-right ${
                          item.trendPercent >= 0 ? "text-green-400" : "text-red-400"
                        }`}>
                          {item.yoyChange}
                        </td>
                        <td className="px-2 py-2.5 text-center">
                          <Badge 
                            variant="outline" 
                            className={`text-[10px] ${getDifficultyColor(item.competition)}`}
                          >
                            {item.competition}
                          </Badge>
                        </td>
                        <td className="px-2 py-2.5 text-right text-white">
                          {item.cpc}
                        </td>
                        <td className="px-2 py-2.5 text-right text-[#8b92a7]">
                          {item.bidLow} - {item.bidHigh}
                        </td>
                        <td className="px-2 py-2.5 text-center">
                          <button
                            onClick={() => handleRemoveKeyword(item.id)}
                            className="p-1 hover:bg-[#2d3548] rounded transition-colors group"
                            title="Remove keyword"
                          >
                            <Trash2 className="h-3 w-3 text-[#8b92a7] group-hover:text-red-400" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Footer Actions */}
          <div className="px-3 py-2.5 border-t border-[#2d3548] flex items-center gap-2">
            <Button 
              className="flex-1 h-8 bg-[#00bcd4] hover:bg-[#00bcd4]/90 text-black text-xs"
            >
              <BarChart3 className="h-3.5 w-3.5 mr-1.5" />
              View Full Report
            </Button>
            <Button 
              variant="outline"
              className="h-8 bg-transparent border-[#2d3548] hover:bg-[#2d3548] text-[#8b92a7] hover:text-white text-xs"
            >
              Export
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}

