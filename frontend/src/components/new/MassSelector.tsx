import { Check, X, MousePointer2 } from "lucide-react";

interface MassSelectorProps {
  isActive: boolean;
  areaType: string;
  onFinish: () => void;
  onCancel: () => void;
}

export function MassSelector({ isActive, areaType, onFinish, onCancel }: MassSelectorProps) {
  if (!isActive) return null;

  return (
    <div className="fixed bottom-[120px] left-1/2 -translate-x-1/2 z-40 animate-in slide-in-from-bottom-4 duration-300">
      <div className="bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md rounded-lg border border-[#00bcd4]/30 shadow-xl shadow-[#00bcd4]/20">
        {/* Horizontal Layout */}
        <div className="flex items-center gap-2 px-2.5 py-2">
          <span className="text-white text-xs flex-shrink-0">
            Click to select {areaType}s:
          </span>
          
          {/* Mass Selector Button */}
          <button
            className="flex items-center gap-1.5 py-1.5 px-2.5 rounded bg-[#00bcd4] text-white"
          >
            <MousePointer2 className="h-3.5 w-3.5" />
            <span className="text-xs whitespace-nowrap">Mass Selector</span>
          </button>

          {/* Finish Button */}
          <button
            onClick={onFinish}
            className="flex items-center gap-1 py-1.5 px-2.5 rounded bg-[#4caf50] text-white hover:bg-[#45a049] transition-colors"
          >
            <Check className="h-3.5 w-3.5" />
            <span className="text-xs whitespace-nowrap">Finish</span>
          </button>

          {/* Cancel Button */}
          <button
            onClick={onCancel}
            className="flex items-center gap-1 py-1.5 px-2.5 rounded bg-[#f44336] text-white hover:bg-[#da190b] transition-colors"
          >
            <X className="h-3.5 w-3.5" />
            <span className="text-xs whitespace-nowrap">Cancel</span>
          </button>
        </div>
      </div>
    </div>
  );
}

