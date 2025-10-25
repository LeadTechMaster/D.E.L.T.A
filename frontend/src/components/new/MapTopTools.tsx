import { Plus, Folder } from "lucide-react";

interface MapTopToolsProps {
  onFolderClick?: () => void;
  isFolderActive?: boolean;
  onPlusClick?: () => void;
}

export function MapTopTools({ onFolderClick, isFolderActive, onPlusClick }: MapTopToolsProps) {
  return (
    <>
      {/* Top Right - Plus and Folder Buttons */}
      <div className="fixed right-4 top-20 z-40 flex gap-2">
        {/* Plus Button */}
        <button 
          onClick={onPlusClick}
          className="p-2.5 rounded-lg transition-all cursor-pointer group backdrop-blur-md bg-[#1a1f2e] border border-[#2d3548] text-[#8b92a7] hover:text-[#00bcd4] hover:bg-[#252b3d] hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)] shadow-xl"
        >
          <Plus className="h-5 w-5 transition-all group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]" />
        </button>
        
        {/* Folder Button */}
        <button 
          onClick={onFolderClick}
          className={`p-2.5 rounded-lg transition-all cursor-pointer group backdrop-blur-md border shadow-xl ${
            isFolderActive
              ? "bg-[#00bcd4]/20 border-[#00bcd4] text-[#00bcd4]"
              : "bg-[#1a1f2e] border-[#2d3548] text-[#8b92a7] hover:text-[#00bcd4] hover:bg-[#252b3d] hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]"
          }`}
        >
          <Folder className={`h-5 w-5 transition-all ${isFolderActive ? "drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]" : "group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]"}`} />
        </button>
      </div>
    </>
  );
}

