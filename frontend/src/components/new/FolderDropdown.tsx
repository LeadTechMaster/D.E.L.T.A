import { useState } from "react";
import { Folder, X } from "lucide-react";
import { Card } from "@/components/ui/card";
import { FolderDropdownMenu } from "./FolderDropdownMenu";

interface FolderDropdownProps {
  isOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  onAddArea?: () => void;
}

export function FolderDropdown({ isOpen: externalIsOpen, onOpenChange, onAddArea }: FolderDropdownProps) {
  const [internalIsOpen, setInternalIsOpen] = useState(false);

  // Use external state if provided, otherwise use internal state
  const isOpen = externalIsOpen !== undefined ? externalIsOpen : internalIsOpen;
  const setIsOpen = onOpenChange || setInternalIsOpen;

  return (
    <div className="relative">
      <Card 
        onClick={() => !isOpen && setIsOpen(true)}
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
              setIsOpen(false);
            }}
            className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-[#1a1f2e] border-2 border-[#00bcd4] flex items-center justify-center hover:bg-[#00bcd4] transition-colors cursor-pointer group z-10"
          >
            <X className="h-4 w-4 text-[#00bcd4] group-hover:text-white" />
          </button>
        )}
        
        {/* Header */}
        {isOpen ? (
          // Open state - horizontal layout
          <div className="flex items-center justify-between gap-6 px-4 py-1.5 w-[280px]">
            <div className="cursor-pointer group flex-shrink-0">
              <Folder className="h-9 w-9 text-[#00bcd4] drop-shadow-[0_0_8px_rgba(0,188,212,0.6)] transition-all" />
            </div>
            <button 
              onClick={(e) => {
                e.stopPropagation();
                setIsOpen(false);
              }}
              className="text-white flex-1 text-center cursor-pointer hover:text-[#00bcd4] transition-colors"
            >
              Folders
            </button>
            <div className="w-9 flex-shrink-0" /> {/* Spacer for balance */}
          </div>
        ) : (
          // Collapsed state - same size as map layer button
          <div className="p-2.5 rounded-lg">
            <div className="cursor-pointer group">
              <Folder className="h-5 w-5 text-[#8b92a7] transition-all group-hover:text-[#00bcd4] group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]" />
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
            <div className="w-[280px] pt-2">
              <FolderDropdownMenu 
                title="Map Folders"
                onAddArea={() => {
                  if (onAddArea) {
                    onAddArea();
                  }
                  setIsOpen(false);
                }}
                onCreateFolder={() => {
                  console.log("Create map folder");
                }}
              />
            </div>
          </>
        )}
      </Card>
    </div>
  );
}

