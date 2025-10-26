import { X, Download, Info } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";

interface ImportDataDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ImportDataDialog({ isOpen, onClose }: ImportDataDialogProps) {
  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 z-50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Dialog */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <Card className="bg-[#1a1f2e] border-[#2d3548] shadow-2xl w-full max-w-2xl">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-[#2d3548]">
            <h2 className="text-white">Import my data</h2>
            <button
              onClick={onClose}
              className="p-1 hover:bg-[#2d3548] rounded transition-colors"
            >
              <X className="h-5 w-5 text-[#8b92a7]" />
            </button>
          </div>

          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Info Alert */}
            <Alert className="bg-[#0f1219] border-[#2d3548]">
              <Info className="h-4 w-4 text-[#00bcd4]" />
              <AlertDescription className="text-[#e0e0e0] ml-2">
                <p className="mb-2">
                  D.E.L.T.A allows you to import your own data onto your map. You can
                  directly import a correctly formatted Excel file, or connect to
                  your CRM.
                </p>
                <p className="text-purple-400 text-sm">
                  Your plan allows you to import 10,000 points for free.
                </p>
              </AlertDescription>
            </Alert>

            {/* Import Options */}
            <div className="flex gap-3">
              <Button
                variant="outline"
                className="flex items-center gap-2 bg-[#0f1219] border-[#2d3548] text-white hover:bg-[#2d3548] hover:border-[#00bcd4] transition-colors"
              >
                <Download className="h-4 w-4" />
                Import file
              </Button>

              <Button
                variant="outline"
                className="flex items-center gap-2 bg-[#0f1219] border-[#2d3548] text-white hover:bg-[#2d3548] hover:border-[#00bcd4] transition-colors"
              >
                <svg
                  className="h-4 w-4"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2z"
                    fill="#FF7A59"
                  />
                  <path
                    d="M12 6a6 6 0 100 12 6 6 0 000-12z"
                    fill="#fff"
                  />
                </svg>
                Import from HubSpot
              </Button>
            </div>
          </div>

          {/* Footer */}
          <div className="flex justify-end p-6 border-t border-[#2d3548]">
            <Button
              variant="ghost"
              onClick={onClose}
              className="text-[#8b92a7] hover:text-white hover:bg-[#2d3548]"
            >
              Cancel
            </Button>
          </div>
        </Card>
      </div>
    </>
  );
}

