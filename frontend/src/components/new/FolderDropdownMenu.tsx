import { useState } from "react";
import {
  ChevronDown,
  ChevronRight,
  Eye,
  Trash2,
  Edit2,
  MapPin,
  Search,
  FolderPlus,
  Plus,
  Folder as FolderIcon,
  EyeOff,
  GripVertical,
} from "lucide-react";
import { useFolders } from "@/contexts/FolderContext";
import { Input } from "@/components/ui/input";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

interface FolderDropdownMenuProps {
  title?: string;
  onAddArea?: () => void;
  onCreateFolder?: () => void;
}

// Area colors
const AREA_COLORS = [
  "#00bcd4", // Cyan
  "#f59e0b", // Amber
  "#8b5cf6", // Purple
  "#ef4444", // Red
  "#10b981", // Green
  "#3b82f6", // Blue
  "#ec4899", // Pink
  "#f97316", // Orange
  "#14b8a6", // Teal
  "#a855f7", // Violet
];

export function FolderDropdownMenu({
  title = "My Territories",
  onAddArea,
  onCreateFolder,
}: FolderDropdownMenuProps) {
  const {
    folders,
    toggleFolderVisibility,
    deleteFolder,
    updateFolder,
    removeItemFromFolder,
    updateItemInFolder,
  } = useFolders();
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());
  const [editingFolderId, setEditingFolderId] = useState<string | null>(null);
  const [editingFolderName, setEditingFolderName] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [hoveredFolder, setHoveredFolder] = useState<string | null>(null);
  const [editingItemId, setEditingItemId] = useState<string | null>(null);
  const [editingItemName, setEditingItemName] = useState("");
  const [hoveredArea, setHoveredArea] = useState<string | null>(null);

  const toggleFolder = (folderId: string) => {
    setExpandedFolders((prev) => {
      const next = new Set(prev);
      if (next.has(folderId)) {
        next.delete(folderId);
      } else {
        next.add(folderId);
      }
      return next;
    });
  };

  const handleSaveFolderName = (folderId: string) => {
    if (editingFolderName.trim()) {
      updateFolder(folderId, { name: editingFolderName });
    }
    setEditingFolderId(null);
    setEditingFolderName("");
  };

  const handleKeyDown = (e: React.KeyboardEvent, callback: () => void) => {
    if (e.key === "Enter") {
      callback();
    } else if (e.key === "Escape") {
      setEditingFolderId(null);
      setEditingFolderName("");
      setEditingItemId(null);
      setEditingItemName("");
    }
  };

  const handleEditItem = (itemId: string, currentName: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingItemId(itemId);
    setEditingItemName(currentName);
  };

  const handleSaveItemName = (folderId: string, itemId: string) => {
    if (editingItemName.trim()) {
      updateItemInFolder(folderId, itemId, { name: editingItemName });
    }
    setEditingItemId(null);
    setEditingItemName("");
  };

  const filteredFolders = folders.filter((folder) =>
    folder?.name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="w-full bg-gradient-to-br from-[#1a2332]/95 to-[#151d2b]/95 backdrop-blur-md border border-[#2d3548]/50 rounded-lg shadow-xl">
      {/* Header */}
      <div className="px-4 py-3 border-b border-[#2d3548]/50">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-white">{title}</h3>
          <div className="flex items-center gap-2">
            <button
              onClick={onCreateFolder}
              className="p-1.5 hover:bg-[#252b3d] rounded transition-colors group"
              title="Add Folder"
            >
              <FolderPlus className="h-4 w-4 text-[#8b92a7] group-hover:text-[#00bcd4] transition-colors" />
            </button>
            <button
              onClick={onAddArea}
              className="p-1.5 hover:bg-[#252b3d] rounded transition-colors group"
              title="Add Area"
            >
              <Plus className="h-4 w-4 text-[#8b92a7] group-hover:text-[#00bcd4] transition-colors" />
            </button>
          </div>
        </div>
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6b7280]" />
          <Input
            type="text"
            placeholder="Search territories..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 h-9 bg-[#0f1219] border-[#2d3548] text-white placeholder:text-[#6b7280]"
          />
        </div>
      </div>

      {/* Folders List */}
      <div className="px-3 py-2 max-h-[400px] overflow-y-auto">
        {filteredFolders.map((folder) => {
          const filteredItems = (folder.items || []).filter((item: any) =>
            item?.name?.toLowerCase().includes(searchTerm.toLowerCase())
          );

          return (
            <div key={folder.id} className="mb-1">
              {/* Folder Header */}
              <div
                className="flex items-center gap-2 px-2 py-2 hover:bg-[#252b3d] rounded-md transition-colors group cursor-pointer"
                onMouseEnter={() => setHoveredFolder(folder.id)}
                onMouseLeave={() => setHoveredFolder(null)}
              >
                <GripVertical className="h-4 w-4 text-[#6b7280] flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity cursor-grab" />
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleFolderVisibility(folder.id);
                  }}
                  className="flex-shrink-0"
                  title="Toggle visibility"
                >
                  {(folder as any).isVisible !== false ? (
                    <Eye className="h-4 w-4 text-[#8b92a7] hover:text-[#00bcd4] transition-colors" />
                  ) : (
                    <EyeOff className="h-4 w-4 text-[#6b7280] hover:text-[#00bcd4] transition-colors" />
                  )}
                </button>
                <FolderIcon
                  className="h-4 w-4 flex-shrink-0"
                  style={{ color: folder.color || "#8b92a7" }}
                />
                {editingFolderId === folder.id ? (
                  <Input
                    value={editingFolderName}
                    onChange={(e) => setEditingFolderName(e.target.value)}
                    onBlur={() => handleSaveFolderName(folder.id)}
                    onKeyDown={(e) => handleKeyDown(e, () => handleSaveFolderName(folder.id))}
                    className="h-6 text-sm flex-1 bg-[#0f1219] border-[#2d3548] text-white"
                    autoFocus
                  />
                ) : (
                  <span
                    className="text-white text-sm flex-1 truncate"
                    onClick={() => toggleFolder(folder.id)}
                  >
                    {folder.name}
                  </span>
                )}
                <button onClick={() => toggleFolder(folder.id)} className="flex-shrink-0">
                  {expandedFolders.has(folder.id) ? (
                    <ChevronDown className="h-4 w-4 text-[#8b92a7] hover:text-[#00bcd4] transition-colors" />
                  ) : (
                    <ChevronRight className="h-4 w-4 text-[#8b92a7] hover:text-[#00bcd4] transition-colors" />
                  )}
                </button>

                {/* Hover Actions */}
                {hoveredFolder === folder.id && editingFolderId !== folder.id && (
                  <div className="flex items-center gap-1 flex-shrink-0">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setEditingFolderId(folder.id);
                        setEditingFolderName(folder.name);
                      }}
                      className="p-1 hover:bg-[#2d3548] rounded transition-colors"
                      title="Rename"
                    >
                      <Edit2 className="h-3.5 w-3.5 text-[#8b92a7] hover:text-[#00bcd4]" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteFolder(folder.id);
                      }}
                      className="p-1 hover:bg-[#2d3548] rounded transition-colors"
                      title="Delete"
                    >
                      <Trash2 className="h-3.5 w-3.5 text-[#8b92a7] hover:text-red-400" />
                    </button>
                  </div>
                )}
              </div>

              {/* Folder Items */}
              {expandedFolders.has(folder.id) && (
                <div className="ml-6 mt-1 space-y-1">
                  {filteredItems.map((item: any) => (
                    <div
                      key={item.id}
                      className="flex items-center gap-2 px-2 py-1.5 hover:bg-[#252b3d] rounded-md transition-colors group cursor-pointer"
                      onMouseEnter={() => setHoveredArea(item.id)}
                      onMouseLeave={() => setHoveredArea(null)}
                    >
                      <GripVertical className="h-4 w-4 text-[#6b7280] flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity cursor-grab" />
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          updateItemInFolder(folder.id, item.id, { visible: !item.visible });
                        }}
                        className="flex-shrink-0"
                        title="Toggle visibility"
                      >
                        {item.isVisible !== false ? (
                          <Eye className="h-4 w-4 text-[#8b92a7] hover:text-[#00bcd4] transition-colors" />
                        ) : (
                          <EyeOff className="h-4 w-4 text-[#6b7280] hover:text-[#00bcd4] transition-colors" />
                        )}
                      </button>

                      {/* Area Type Icon */}
                      <div className="flex-shrink-0">
                        <MapPin className="h-3.5 w-3.5 text-[#8b92a7]" />
                      </div>

                      {/* Color Circle with Picker */}
                      <Popover>
                        <PopoverTrigger asChild>
                          <button
                            onClick={(e) => e.stopPropagation()}
                            className="w-3 h-3 rounded-full flex-shrink-0 border border-[#2d3548] hover:border-[#00bcd4] transition-colors cursor-pointer"
                            style={{ backgroundColor: item.color || "#00bcd4" }}
                          />
                        </PopoverTrigger>
                        <PopoverContent 
                          className="w-auto p-2 bg-[#1a1f2e] border-[#2d3548]"
                          side="right"
                          sideOffset={8}
                        >
                          <div className="grid grid-cols-5 gap-2">
                            {AREA_COLORS.map((color) => (
                              <button
                                key={color}
                                onClick={(e) => {
                                  e.stopPropagation();
                                  updateItemInFolder(folder.id, item.id, { color });
                                }}
                                className="w-6 h-6 rounded-full border-2 hover:scale-110 transition-transform"
                                style={{ 
                                  backgroundColor: color,
                                  borderColor: item.color === color ? "#00bcd4" : "#2d3548"
                                }}
                              />
                            ))}
                          </div>
                        </PopoverContent>
                      </Popover>

                      {/* Item Name */}
                      {editingItemId === item.id ? (
                        <Input
                          value={editingItemName}
                          onChange={(e) => setEditingItemName(e.target.value)}
                          onBlur={() => handleSaveItemName(folder.id, item.id)}
                          onKeyDown={(e) => handleKeyDown(e, () => handleSaveItemName(folder.id, item.id))}
                          className="h-6 text-sm flex-1 bg-[#0f1219] border-[#2d3548] text-white"
                          autoFocus
                        />
                      ) : (
                        <span className="text-white text-sm flex-1 truncate">{item.name}</span>
                      )}

                      {/* Hover Actions */}
                      {hoveredArea === item.id && editingItemId !== item.id && (
                        <div className="flex items-center gap-1 flex-shrink-0">
                          <button
                            onClick={(e) => handleEditItem(item.id, item.name, e)}
                            className="p-1 hover:bg-[#2d3548] rounded transition-colors"
                            title="Rename"
                          >
                            <Edit2 className="h-3.5 w-3.5 text-[#8b92a7] hover:text-[#00bcd4]" />
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              removeItemFromFolder(folder.id, item.id);
                            }}
                            className="p-1 hover:bg-[#2d3548] rounded transition-colors"
                            title="Delete"
                          >
                            <Trash2 className="h-3.5 w-3.5 text-[#8b92a7] hover:text-red-400" />
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}

        {filteredFolders.length === 0 && (
          <div className="text-center py-8 text-[#6b7280] text-sm">
            No territories found
          </div>
        )}
      </div>
    </div>
  );
}

