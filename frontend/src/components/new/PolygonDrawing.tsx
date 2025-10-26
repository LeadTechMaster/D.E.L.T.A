import { useEffect, useRef, useState } from "react";
import { X, Pencil } from "lucide-react";

interface Point {
  x: number;
  y: number;
}

interface Polygon {
  id: string;
  points: Point[];
  color: string;
  closed: boolean;
}

interface PolygonDrawingProps {
  isActive: boolean;
  onClose: () => void;
  onPolygonComplete?: (coordinates: [number, number][]) => void; // lat/lng coordinates
}

export function PolygonDrawing({ isActive, onClose: _onClose, onPolygonComplete }: PolygonDrawingProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const [polygons, setPolygons] = useState<Polygon[]>([]);
  const [currentPolygon, setCurrentPolygon] = useState<Point[]>([]);
  const [hoveredPoint, setHoveredPoint] = useState<Point | null>(null);

  // Find the map container on mount
  useEffect(() => {
    if (isActive) {
      // The map is in the parent component with class containing 'mapboxgl-map'
      const mapElement = document.querySelector('.mapboxgl-map') as HTMLDivElement;
      if (mapElement) {
        mapContainerRef.current = mapElement;
        console.log("Found map container for coordinate conversion");
      }
    }
  }, [isActive]);

  const redraw = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw completed polygons
    polygons.forEach((polygon) => {
      if (polygon.points.length < 2) return;

      ctx.beginPath();
      ctx.moveTo(polygon.points[0].x, polygon.points[0].y);
      
      for (let i = 1; i < polygon.points.length; i++) {
        ctx.lineTo(polygon.points[i].x, polygon.points[i].y);
      }
      
      if (polygon.closed) {
        ctx.closePath();
        ctx.fillStyle = polygon.color + "33"; // Add transparency
        ctx.fill();
      }
      
      ctx.strokeStyle = polygon.color;
      ctx.lineWidth = 2;
      ctx.stroke();

      // Draw points
      polygon.points.forEach((point) => {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 5, 0, Math.PI * 2);
        ctx.fillStyle = polygon.color;
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.stroke();
      });
    });

    // Draw current polygon being drawn
    if (currentPolygon.length > 0) {
      ctx.beginPath();
      ctx.moveTo(currentPolygon[0].x, currentPolygon[0].y);
      
      for (let i = 1; i < currentPolygon.length; i++) {
        ctx.lineTo(currentPolygon[i].x, currentPolygon[i].y);
      }
      
      // Draw preview line to cursor
      if (hoveredPoint) {
        ctx.lineTo(hoveredPoint.x, hoveredPoint.y);
        
        // If near first point and has enough points, show closing line
        if (currentPolygon.length >= 3 && isNearPoint(hoveredPoint, currentPolygon[0], 15)) {
          ctx.lineTo(currentPolygon[0].x, currentPolygon[0].y);
        }
      }
      
      ctx.strokeStyle = "#00bcd4";
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]); // Dashed line for preview
      ctx.stroke();
      ctx.setLineDash([]); // Reset to solid line

      // Draw solid lines for completed segments
      ctx.beginPath();
      ctx.moveTo(currentPolygon[0].x, currentPolygon[0].y);
      for (let i = 1; i < currentPolygon.length; i++) {
        ctx.lineTo(currentPolygon[i].x, currentPolygon[i].y);
      }
      ctx.strokeStyle = "#00bcd4";
      ctx.lineWidth = 2;
      ctx.stroke();

      // Draw points
      currentPolygon.forEach((point, index) => {
        ctx.beginPath();
        ctx.arc(point.x, point.y, index === 0 ? 7 : 5, 0, Math.PI * 2);
        ctx.fillStyle = "#00bcd4";
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.stroke();

        // Glow effect for first point if hovering near it
        if (index === 0 && hoveredPoint && isNearPoint(hoveredPoint, point, 15)) {
          ctx.beginPath();
          ctx.arc(point.x, point.y, 10, 0, Math.PI * 2);
          ctx.strokeStyle = "#00bcd4";
          ctx.lineWidth = 2;
          ctx.stroke();
        }
      });
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Set canvas size to match window
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight - 56; // Account for top nav
      redraw();
    };

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    return () => window.removeEventListener("resize", resizeCanvas);
  }, []);

  useEffect(() => {
    redraw();
  }, [polygons, currentPolygon, hoveredPoint, isActive]);

  const isNearPoint = (p1: Point, p2: Point, threshold: number): boolean => {
    const distance = Math.sqrt(
      Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2)
    );
    return distance < threshold;
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isActive) {
      console.log("Canvas clicked but tool not active");
      return;
    }

    const canvas = canvasRef.current;
    if (!canvas) {
      console.log("Canvas ref not available");
      return;
    }

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const point: Point = { x, y };
    
    console.log("Canvas clicked at:", point, "isActive:", isActive);

    // Check if clicking near the first point to close polygon
    if (currentPolygon.length >= 3 && isNearPoint(point, currentPolygon[0], 15)) {
      // Close the polygon
      const newPolygon: Polygon = {
        id: Date.now().toString(),
        points: [...currentPolygon],
        color: "#00bcd4",
        closed: true,
      };
      setPolygons([...polygons, newPolygon]);
      setCurrentPolygon([]);
      
      // Notify parent with lat/lng coordinates
      if (onPolygonComplete) {
        console.log("Polygon completed, calling onPolygonComplete");
        // Note: For now, we pass canvas coordinates. Parent will need to convert to lat/lng
        // using the Mapbox map instance
        const coords: [number, number][] = currentPolygon.map(p => [p.y, p.x]);
        onPolygonComplete(coords);
      }
      
      return;
    }

    // Add point to current polygon
    setCurrentPolygon([...currentPolygon, point]);
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isActive || currentPolygon.length === 0) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const point: Point = { x, y };

    setHoveredPoint(point);
  };

  const handleDoubleClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isActive || currentPolygon.length < 3) return;

    e.preventDefault();
    
    // Close the polygon on double-click
    const newPolygon: Polygon = {
      id: Date.now().toString(),
      points: [...currentPolygon],
      color: "#00bcd4",
      closed: true,
    };
    setPolygons([...polygons, newPolygon]);
    setCurrentPolygon([]);
    
    // Notify parent with coordinates
    if (onPolygonComplete) {
      console.log("Polygon completed via double-click");
      const coords: [number, number][] = currentPolygon.map(p => [p.y, p.x]);
      onPolygonComplete(coords);
    }
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (!isActive) return;

    // ESC key to cancel current polygon
    if (e.key === "Escape") {
      setCurrentPolygon([]);
    }

    // Backspace or Delete to remove last point
    if ((e.key === "Backspace" || e.key === "Delete") && currentPolygon.length > 0) {
      setCurrentPolygon(currentPolygon.slice(0, -1));
    }

    // Enter key to close polygon (if at least 3 points)
    if (e.key === "Enter" && currentPolygon.length >= 3) {
      const newPolygon: Polygon = {
        id: Date.now().toString(),
        points: [...currentPolygon],
        color: "#00bcd4",
        closed: true,
      };
      setPolygons([...polygons, newPolygon]);
      setCurrentPolygon([]);
      
      // Notify parent
      if (onPolygonComplete) {
        console.log("Polygon completed via Enter key");
        const coords: [number, number][] = currentPolygon.map(p => [p.y, p.x]);
        onPolygonComplete(coords);
      }
    }
  };

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isActive, currentPolygon]);

  const clearAllPolygons = () => {
    setPolygons([]);
    setCurrentPolygon([]);
  };

  if (!isActive) return null;

  return (
    <>
      {/* Semi-transparent overlay to show drawing mode is active */}
      <div 
        className="fixed inset-0 bg-transparent pointer-events-none"
        style={{ 
          top: "56px",
          zIndex: 34,
          border: "2px solid rgba(0, 188, 212, 0.3)"
        }}
      />
      
      <canvas
        ref={canvasRef}
        className="fixed left-0 right-0 bottom-0 cursor-crosshair bg-transparent"
        style={{ 
          pointerEvents: "auto", 
          top: "56px",
          zIndex: 35
        }}
        onClick={handleCanvasClick}
        onMouseMove={handleMouseMove}
        onDoubleClick={handleDoubleClick}
      />
      
      {/* Active Mode Indicator */}
      <div className="fixed top-20 left-1/2 -translate-x-1/2 bg-[#00bcd4]/90 backdrop-blur-md border border-[#00bcd4] px-4 py-2 rounded-lg shadow-xl animate-pulse"
        style={{ zIndex: 60 }}
      >
        <p className="text-white text-sm flex items-center gap-2">
          <Pencil className="h-4 w-4" />
          <span>Drawing Mode Active</span>
        </p>
      </div>

      {/* Clear Button */}
      {(polygons.length > 0 || currentPolygon.length > 0) && (
        <button
          onClick={clearAllPolygons}
          className="fixed top-24 left-1/2 -translate-x-1/2 bg-[#1a1f2e] border border-[#00bcd4] px-4 py-2 rounded-lg hover:bg-[#00bcd4] hover:text-black transition-colors text-white text-sm flex items-center gap-2"
          style={{ zIndex: 60 }}
        >
          <X className="h-4 w-4" />
          Clear All Polygons
        </button>
      )}
    </>
  );
}

