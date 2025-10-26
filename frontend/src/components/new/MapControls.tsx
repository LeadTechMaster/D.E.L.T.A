import { Save } from "lucide-react";
import { useState } from "react";
import { useFolders } from "@/contexts/FolderContext";
import { FolderDropdown } from "./FolderDropdown";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

export function MapControls() {
  const { saveCurrentView } = useFolders();
  const [isSaveDialogOpen, setIsSaveDialogOpen] = useState(false);
  const [saveForm, setSaveForm] = useState({ name: "", description: "", type: "map" as "map" | "dashboard" });

  const handleSaveView = () => {
    if (saveForm.name.trim()) {
      saveCurrentView(saveForm.name, saveForm.description, saveForm.type);
      setSaveForm({ name: "", description: "", type: "map" });
      setIsSaveDialogOpen(false);
    }
  };

  return (
    <>
      <div className="fixed top-20 right-4 z-30 flex items-center gap-2">
        {/* Save Button */}
        <button 
          onClick={() => setIsSaveDialogOpen(true)}
          className="p-2.5 bg-[#1a1f2e] border border-[#2d3548] rounded-lg shadow-xl hover:bg-[#252b3d] transition-all cursor-pointer group"
        >
          <Save className="h-5 w-5 text-[#8b92a7] group-hover:text-[#00bcd4] group-hover:drop-shadow-[0_0_8px_rgba(0,188,212,0.6)] transition-all" />
        </button>

        {/* Folder Button */}
        <FolderDropdown />
      </div>

      {/* Save Dialog */}
      <Dialog open={isSaveDialogOpen} onOpenChange={setIsSaveDialogOpen}>
        <DialogContent className="bg-[#1a1a1a] border-[#2d3548] max-w-md">
          <DialogTitle className="text-white">Save Current View</DialogTitle>
          <DialogDescription className="text-[#8b92a7]">
            Save your current map view to access it later in split screen
          </DialogDescription>
          
          <div className="space-y-4 mt-4">
            <div>
              <label className="text-[#8b92a7] text-sm mb-2 block">Name</label>
              <Input
                placeholder="View name"
                value={saveForm.name}
                onChange={(e) => setSaveForm({ ...saveForm, name: e.target.value })}
                className="bg-[#0f1219] border-[#2d3548] text-white"
              />
            </div>
            
            <div>
              <label className="text-[#8b92a7] text-sm mb-2 block">Description</label>
              <Textarea
                placeholder="Description"
                value={saveForm.description}
                onChange={(e) => setSaveForm({ ...saveForm, description: e.target.value })}
                className="bg-[#0f1219] border-[#2d3548] text-white resize-none"
                rows={3}
              />
            </div>
            
            <div className="flex gap-2 pt-2">
              <button
                onClick={handleSaveView}
                className="flex-1 px-4 py-2 bg-[#00bcd4] text-black rounded-lg hover:bg-[#00bcd4]/90 transition-all cursor-pointer"
              >
                Save to Folder
              </button>
              <button
                onClick={() => {
                  setIsSaveDialogOpen(false);
                  setSaveForm({ name: "", description: "", type: "map" });
                }}
                className="px-4 py-2 bg-[#2d3548] text-white rounded-lg hover:bg-[#3d4558] transition-all cursor-pointer"
              >
                Cancel
              </button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}

