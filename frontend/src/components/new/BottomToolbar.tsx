import { Pencil, Clock, Ruler, Grid3x3, X } from "lucide-react";

interface BottomToolbarProps {
  isOpen: boolean;
  onClose: () => void;
  onToolClick: (toolId: string) => void;
  activeTool: string | null;
}

export function BottomToolbar({ isOpen, onClose, onToolClick, activeTool }: BottomToolbarProps) {
  if (!isOpen) return null;

  const tools = [
    { id: "draw", icon: Pencil, label: "Draw" },
    { id: "history", icon: Clock, label: "Time" },
    { id: "measure", icon: Ruler, label: "Distance" },
    { id: "grid", icon: Grid3x3, label: "Area Type" },
  ];

  return (
    <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 animate-in slide-in-from-bottom-4 duration-300">
      <div className="backdrop-blur-md bg-gradient-to-br from-[#00bcd4]/90 to-[#0097a7]/90 border border-[#00bcd4] shadow-xl shadow-[#00bcd4]/40 px-4 py-3 rounded-3xl relative">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-[#1a1f2e] border-2 border-white flex items-center justify-center hover:bg-white transition-colors cursor-pointer group"
        >
          <X className="h-4 w-4 text-white group-hover:text-[#1a1f2e]" />
        </button>

        <div className="flex items-center gap-3">
          {tools.map((tool) => (
            <button
              key={tool.id}
              onClick={() => onToolClick(tool.id)}
              className={`group p-4 rounded-2xl transition-all cursor-pointer ${
                activeTool === tool.id
                  ? "bg-[#1a1f2e] border border-[#1a1f2e] shadow-[0_0_12px_rgba(0,0,0,0.3)]"
                  : "bg-[#00bcd4]/20 border border-white/30 hover:bg-[#1a1f2e]/80 hover:border-white/50 hover:shadow-[0_0_8px_rgba(0,0,0,0.2)]"
              }`}
            >
              <tool.icon className={`h-6 w-6 transition-all ${
                activeTool === tool.id
                  ? "text-[#00bcd4] drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]"
                  : "text-white group-hover:text-[#00bcd4] group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)]"
              }`} />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

