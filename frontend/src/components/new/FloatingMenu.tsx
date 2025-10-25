import { Card } from "@/components/ui/card";
import { MapPin, Building2, Database, TrendingUp, Users } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const menuItems = [
  {
    id: "demographics",
    label: "Demographics",
    description: "Population, age, income, and more",
    icon: Users,
  },
  {
    id: "points-of-interest",
    label: "Points of Interest",
    description: "Businesses & Services",
    icon: MapPin,
  },
  {
    id: "administrative",
    label: "Administrative boundaries",
    description: "Postal codes, municipalities, provinces/territories",
    icon: Building2,
  },
  {
    id: "customer-metrics-data",
    label: "Custom Metrics & Your Data",
    description: "Custom metrics and data management",
    icon: Database,
  },
  {
    id: "demand-research",
    label: "Demand Research",
    description: "SEO, keywords, rankings",
    icon: TrendingUp,
  },
];

interface FloatingMenuProps {
  onMenuItemClick: (id: string) => void;
  activeItem: string | null;
}

export function FloatingMenu({ onMenuItemClick, activeItem }: FloatingMenuProps) {
  const handleMenuClick = (itemId: string) => {
    onMenuItemClick(itemId);
  };

  return (
    <div className="fixed left-6 top-20 z-30">
      <Card className="flex flex-row items-center gap-2 px-2 py-2 backdrop-blur-md bg-[#1a1f2e]/90 border-[#2d3548] shadow-xl rounded-3xl">
        <TooltipProvider delayDuration={200}>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeItem === item.id;
            
            return (
              <Tooltip key={item.id}>
                <TooltipTrigger asChild>
                  <button
                    onClick={() => handleMenuClick(item.id)}
                    className={`p-2.5 rounded-lg transition-all cursor-pointer group ${
                      isActive 
                        ? "bg-[#00bcd4]/20 border border-[#00bcd4]/50" 
                        : "bg-[#0f1219] border border-[#2d3548] hover:bg-[#252b3d] hover:border-[#00bcd4]/30"
                    }`}
                    aria-label={item.label}
                  >
                    <Icon 
                      className={`h-5 w-5 transition-all ${
                        isActive
                          ? "text-[#00bcd4] drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]"
                          : "text-[#8b92a7] group-hover:text-[#00bcd4] group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]"
                      }`}
                    />
                  </button>
                </TooltipTrigger>
                <TooltipContent 
                  side="top" 
                  className="bg-[#1a1f2e] border-[#2d3548] px-3 py-2 max-w-[280px]"
                  sideOffset={8}
                >
                  <div className="space-y-0.5">
                    <p className="text-white">{item.label}</p>
                    <p className="text-[#8b92a7] text-sm">{item.description}</p>
                  </div>
                </TooltipContent>
              </Tooltip>
            );
          })}
        </TooltipProvider>
      </Card>
    </div>
  );
}

