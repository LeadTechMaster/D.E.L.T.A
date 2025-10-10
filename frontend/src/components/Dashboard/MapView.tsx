import { useEffect, useRef, useState } from 'react';
import { Box, Paper } from '@mui/material';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { MAPBOX_ACCESS_TOKEN } from '../../config/mapbox';
import { generateMapboxHeatmapGeoJSON, generateBusinessHeatmap, generateCompetitionHeatmap, generateOpportunityHeatmap } from '../../services/heatmapService';
import { fetchHeatmapData, type HeatmapDataType as ApiHeatmapDataType } from '../../services/heatmapApiService';
import { getIsochrone, getZipCodeFromCoordinates } from '../../services/mapboxService';
import { useZipcodeData } from '../../hooks/useZipcodeData';
import MapStyleSwitcher, { type MapStyle } from './MapStyleSwitcher';
import SearchLocationBar from './SearchLocationBar';
import DistanceMeasurementPanel, { type TravelMode, type DistanceUnit } from './DistanceMeasurementPanel';
import HeatmapPanel, { type HeatmapDataType } from './HeatmapPanel';
import DrawingToolsToolbar, { type DrawingTool } from './DrawingToolsToolbar';
import MapLayersToggle from './MapLayersToggle';
import ZipcodeInfoPanel from './ZipcodeInfoPanel';

mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;

// Map style URLs
const MAP_STYLES: Record<MapStyle, string> = {
  street: 'mapbox://styles/mapbox/streets-v12',
  outdoor: 'mapbox://styles/mapbox/outdoors-v12',
  light: 'mapbox://styles/mapbox/light-v11',
  dark: 'mapbox://styles/mapbox/dark-v11',
  satellite: 'mapbox://styles/mapbox/satellite-v9',
  hybrid: 'mapbox://styles/mapbox/satellite-streets-v12',
};

interface BusinessLocation {
  name: string;
  rating: number;
  user_ratings_total: number;
  coordinates: {
    latitude: number;
    longitude: number;
  };
}

interface MapViewProps {
  center: { lat: number; lng: number };
  zoom: number;
  businesses?: BusinessLocation[];
  onMapLoad?: (map: mapboxgl.Map) => void;
}

export default function MapView({ center, zoom, businesses, onMapLoad }: MapViewProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapStyle, setMapStyle] = useState<MapStyle>('dark');
  const [showDistancePanel, setShowDistancePanel] = useState(false);
  const [showHeatmapPanel, setShowHeatmapPanel] = useState(true);
  const [activeTool, setActiveTool] = useState<DrawingTool>(null);
  const [heatmapDataType, setHeatmapDataType] = useState<HeatmapDataType>('population');
  const [selectedPoint, setSelectedPoint] = useState<{ lat: number; lng: number } | null>(null);
  
  // ZIP code integration
  const { 
    currentZipcode, 
    zipcodeData, 
    setCurrentZipcode, 
    generateIsochrone,
    clearZipcodeData 
  } = useZipcodeData();
  const [currentMode, setCurrentMode] = useState<TravelMode>('cycling');
  const [currentDistance, setCurrentDistance] = useState(1);
  const [currentUnit, setCurrentUnit] = useState<DistanceUnit>('km');

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: MAP_STYLES[mapStyle],
      center: [center.lng, center.lat],
      zoom: zoom
    });

    map.current.addControl(new mapboxgl.NavigationControl(), 'bottom-right');
    map.current.addControl(new mapboxgl.FullscreenControl(), 'bottom-right');

    map.current.on('load', () => {
      if (map.current && onMapLoad) {
        onMapLoad(map.current);
      }
      
      // Add heatmap sources and layers if businesses are available
      if (map.current && businesses && businesses.length > 0) {
        addHeatmapLayers(map.current, businesses, getHeatmapTypeFromDataType(heatmapDataType));
      }
    });

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  useEffect(() => {
    if (map.current) {
      map.current.flyTo({
        center: [center.lng, center.lat],
        zoom: zoom,
        essential: true
      });
    }
  }, [center, zoom]);

  // Update map style
  useEffect(() => {
    if (map.current) {
      try {
        map.current.setStyle(MAP_STYLES[mapStyle]);
      } catch (error) {
        console.warn('Mapbox style loading warning (normal):', error);
      }
      
      // Re-add heatmap layers after style change
      map.current.once('styledata', () => {
        if (map.current && businesses && businesses.length > 0) {
          addHeatmapLayers(map.current, businesses, getHeatmapTypeFromDataType(heatmapDataType));
        }
      });
    }
  }, [mapStyle]);

  // Update heatmap when businesses or heatmap data type changes
  useEffect(() => {
    if (map.current && businesses && businesses.length > 0) {
      updateHeatmapLayers(map.current, businesses, getHeatmapTypeFromDataType(heatmapDataType));
    }
  }, [businesses, heatmapDataType]);

  const getHeatmapTypeFromDataType = (dataType: HeatmapDataType): 'business' | 'competition' | 'opportunity' => {
    switch (dataType) {
      case 'business_competition':
        return 'competition';
      case 'market_opportunity':
        return 'opportunity';
      default:
        return 'business';
    }
  };

  const handleLocationSelect = (location: { lat: number; lng: number; name: string }) => {
    if (map.current) {
      map.current.flyTo({
        center: [location.lng, location.lat],
        zoom: 12,
        essential: true,
        duration: 2000,
      });
    }
  };

  const handleToolChange = (tool: DrawingTool) => {
    setActiveTool(tool);
    
    // Show/hide panels based on tool
    if (tool === 'ruler') {
      setShowDistancePanel(true);
      // Enable map click listener
      if (map.current) {
        map.current.getCanvas().style.cursor = 'crosshair';
      }
    } else {
      setShowDistancePanel(false);
      setSelectedPoint(null);
      if (map.current) {
        map.current.getCanvas().style.cursor = '';
      }
    }
  };

  // Handle map clicks for distance tool
  useEffect(() => {
    if (!map.current || activeTool !== 'ruler') return;

    const handleMapClick = (e: mapboxgl.MapMouseEvent) => {
      const { lng, lat } = e.lngLat;
      setSelectedPoint({ lat, lng });
      
      // Update visualization immediately
      updateDistanceVisualization(lat, lng, currentMode, currentDistance, currentUnit);
    };

    map.current.on('click', handleMapClick);

    return () => {
      if (map.current) {
        map.current.off('click', handleMapClick);
      }
    };
  }, [activeTool, currentMode, currentDistance, currentUnit]);

  // Handle ZIP code isochrone visualization
  useEffect(() => {
    if (map.current && zipcodeData.isochrone && currentZipcode) {
      // Remove existing ZIP isochrone layers
      if (map.current.getLayer('zipcode-isochrone-layer')) {
        map.current.removeLayer('zipcode-isochrone-layer');
      }
      if (map.current.getSource('zipcode-isochrone-source')) {
        map.current.removeSource('zipcode-isochrone-source');
      }

      // Add ZIP code isochrone layer
      map.current.addSource('zipcode-isochrone-source', {
        type: 'geojson',
        data: zipcodeData.isochrone,
      });

      map.current.addLayer({
        id: 'zipcode-isochrone-layer',
        type: 'fill',
        source: 'zipcode-isochrone-source',
        paint: {
          'fill-color': '#00D9FF',
          'fill-opacity': 0.3,
        },
      });

      map.current.addLayer({
        id: 'zipcode-isochrone-outline',
        type: 'line',
        source: 'zipcode-isochrone-source',
        paint: {
          'line-color': '#00D9FF',
          'line-width': 2,
        },
      });

      // Center map on ZIP code if we have coordinates
      if (zipcodeData.coordinates) {
        map.current.flyTo({
          center: [zipcodeData.coordinates.lng, zipcodeData.coordinates.lat],
          zoom: 12,
          duration: 2000,
        });
      }
    }
  }, [zipcodeData.isochrone, currentZipcode, zipcodeData.coordinates]);

  const handleModeChange = async (mode: TravelMode) => {
    setCurrentMode(mode);
    
    // If we have a ZIP code selected, use ZIP code isochrone
    if (currentZipcode && mode !== 'circle') {
      try {
        // Convert distance to minutes for isochrone (approximate)
        const minutes = currentUnit === 'km' ? Math.round(currentDistance * 1.5) : Math.round(currentDistance * 2.5);
        await generateIsochrone(currentZipcode, minutes, mode);
      } catch (error) {
        console.error('Error generating ZIP code isochrone:', error);
      }
    } else if (selectedPoint) {
      // Fallback to point-based visualization
      await updateDistanceVisualization(
        selectedPoint.lat,
        selectedPoint.lng,
        mode,
        currentDistance,
        currentUnit
      );
    }
  };

  const handleDistanceChange = (distance: number, unit: DistanceUnit) => {
    setCurrentDistance(distance);
    setCurrentUnit(unit);
    
    // If we have a ZIP code selected, regenerate isochrone
    if (currentZipcode && currentMode !== 'circle') {
      try {
        // Convert distance to minutes for isochrone (approximate)
        const minutes = unit === 'km' ? Math.round(distance * 1.5) : Math.round(distance * 2.5);
        generateIsochrone(currentZipcode, minutes, currentMode);
      } catch (error) {
        console.error('Error generating ZIP code isochrone:', error);
      }
    } else if (selectedPoint) {
      // Fallback to point-based visualization
      updateDistanceVisualization(
        selectedPoint.lat,
        selectedPoint.lng,
        currentMode,
        distance,
        unit
      );
    }
  };

  const updateDistanceVisualization = async (
    lat: number,
    lng: number,
    mode: TravelMode,
    distance: number,
    unit: DistanceUnit
  ) => {
    if (!map.current) return;

    const distanceInKm = unit === 'mi' ? distance * 1.60934 : distance;
    
    // Remove all existing distance layers and sources
    const layersToRemove = [
      'distance-circle', 'distance-circle-outline', 'isochrone-layer', 'isochrone-outline', 
      'distance-marker', 'distance-route', 'distance-route-outline', 'zip-code-label'
    ];
    
    const sourcesToRemove = [
      'distance-circle-source', 'isochrone-source', 'distance-marker-source', 
      'distance-route-source', 'zip-code-source'
    ];
    
    layersToRemove.forEach(layerId => {
      if (map.current?.getLayer(layerId)) {
        try {
          map.current.removeLayer(layerId);
        } catch (e) {
          console.warn(`Failed to remove layer ${layerId}:`, e);
        }
      }
    });
    
    sourcesToRemove.forEach(sourceId => {
      if (map.current?.getSource(sourceId)) {
        try {
          map.current.removeSource(sourceId);
        } catch (e) {
          console.warn(`Failed to remove source ${sourceId}:`, e);
        }
      }
    });

    // Small delay to ensure cleanup is complete
    await new Promise(resolve => setTimeout(resolve, 50));

    if (!map.current) return;

    // Add marker at selected point
    if (!map.current.getSource('distance-marker-source')) {
      map.current.addSource('distance-marker-source', {
        type: 'geojson',
        data: {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [lng, lat],
          },
          properties: {},
        },
      });

      map.current.addLayer({
        id: 'distance-marker',
        type: 'circle',
        source: 'distance-marker-source',
        paint: {
          'circle-radius': 8,
          'circle-color': '#FF0000',
          'circle-stroke-width': 2,
          'circle-stroke-color': '#FFFFFF',
        },
      });
    }

    // Get and display ZIP code
    try {
      const zipCode = await getZipCodeFromCoordinates(lat, lng);
      if (zipCode && map.current && !map.current.getSource('zip-code-source')) {
        map.current.addSource('zip-code-source', {
          type: 'geojson',
          data: {
            type: 'Feature',
            geometry: {
              type: 'Point',
              coordinates: [lng, lat],
            },
            properties: {
              zipCode: `ZIP: ${zipCode}`,
            },
          },
        });

        map.current.addLayer({
          id: 'zip-code-label',
          type: 'symbol',
          source: 'zip-code-source',
          layout: {
            'text-field': ['get', 'zipCode'],
            'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
            'text-size': 14,
            'text-offset': [0, -1.5],
          },
          paint: {
            'text-color': '#FFFFFF',
            'text-halo-color': '#000000',
            'text-halo-width': 2,
          },
        });
      }
    } catch (error) {
      console.error('Error fetching ZIP code:', error);
    }

    if (!map.current) return;

    if (mode === 'circle') {
      // Draw simple circle
      const circleGeoJSON = createCircle([lng, lat], distanceInKm);
      
      if (!map.current.getSource('distance-circle-source')) {
        map.current.addSource('distance-circle-source', {
          type: 'geojson',
          data: circleGeoJSON as any,
        });
        
        map.current.addLayer({
          id: 'distance-circle',
          type: 'fill',
          source: 'distance-circle-source',
          paint: {
            'fill-color': '#00D9FF',
            'fill-opacity': 0.15,
          },
        });
        
        map.current.addLayer({
          id: 'distance-circle-outline',
          type: 'line',
          source: 'distance-circle-source',
          paint: {
            'line-color': '#00D9FF',
            'line-width': 3,
            'line-dasharray': [2, 2],
          },
        });
      }
    } else {
      // Use isochrone for travel modes with real Mapbox API
      const profile = mode === 'driving' ? 'driving' : mode === 'walking' ? 'walking' : 'cycling';
      const minutes = Math.round((distanceInKm / getSpeedKmPerHour(mode)) * 60);
      
      try {
        const isochroneData = await getIsochrone({
          coordinates: [lng, lat],
          profile,
          contours_minutes: [Math.max(1, Math.min(60, minutes))], // Clamp between 1-60 minutes
          polygons: true,
        });
        
        if (isochroneData && isochroneData.features && isochroneData.features.length > 0 && map.current && !map.current.getSource('isochrone-source')) {
          map.current.addSource('isochrone-source', {
            type: 'geojson',
            data: isochroneData,
          });
          
          const modeColors = {
            driving: '#FF6B35',
            walking: '#4ECDC4',
            cycling: '#95E1D3',
          };
          
          map.current.addLayer({
            id: 'isochrone-layer',
            type: 'fill',
            source: 'isochrone-source',
            paint: {
              'fill-color': modeColors[mode] || '#00D9FF',
              'fill-opacity': 0.25,
            },
          });
          
          map.current.addLayer({
            id: 'isochrone-outline',
            type: 'line',
            source: 'isochrone-source',
            paint: {
              'line-color': modeColors[mode] || '#00D9FF',
              'line-width': 3,
            },
          });
        }
      } catch (error) {
        console.error('Error generating isochrone:', error);
        // Fallback to circle if isochrone fails
        const circleGeoJSON = createCircle([lng, lat], distanceInKm);
        
        if (map.current && !map.current.getSource('distance-circle-source')) {
          map.current.addSource('distance-circle-source', {
            type: 'geojson',
            data: circleGeoJSON as any,
          });
          
          map.current.addLayer({
            id: 'distance-circle',
            type: 'fill',
            source: 'distance-circle-source',
            paint: {
              'fill-color': '#FF6B35',
              'fill-opacity': 0.15,
            },
          });
          
          map.current.addLayer({
            id: 'distance-circle-outline',
            type: 'line',
            source: 'distance-circle-source',
            paint: {
              'line-color': '#FF6B35',
              'line-width': 2,
            },
          });
        }
      }
    }
  };

  const getSpeedKmPerHour = (mode: TravelMode): number => {
    switch (mode) {
      case 'driving':
        return 50; // 50 km/h average city driving
      case 'walking':
        return 5; // 5 km/h walking speed
      case 'cycling':
        return 15; // 15 km/h cycling speed
      default:
        return 15;
    }
  };

  const handleDataTypeChange = async (dataType: HeatmapDataType) => {
    setHeatmapDataType(dataType);
    
    // Fetch real heatmap data from backend
    if (map.current) {
      const mapCenter = map.current.getCenter();
      
      try {
        const heatmapData = await fetchHeatmapData(
          dataType as ApiHeatmapDataType,
          mapCenter.lat,
          mapCenter.lng,
          5,
          'motor boat'
        );
        
        if (heatmapData && heatmapData.features && map.current) {
          // Update the heatmap layer with real data
          const source = map.current.getSource('heatmap-source') as mapboxgl.GeoJSONSource;
          if (source) {
            source.setData(heatmapData);
          }
        }
      } catch (error) {
        console.error('Error fetching heatmap data:', error);
      }
    }
  };

  // Helper function to create circle GeoJSON
  const createCircle = (center: [number, number], radiusInKm: number) => {
    const points = 64;
    const coords = {
      latitude: center[1],
      longitude: center[0],
    };

    const km = radiusInKm;
    const ret = [];
    const distanceX = km / (111.32 * Math.cos((coords.latitude * Math.PI) / 180));
    const distanceY = km / 110.574;

    for (let i = 0; i < points; i++) {
      const theta = (i / points) * (2 * Math.PI);
      const x = distanceX * Math.cos(theta);
      const y = distanceY * Math.sin(theta);
      ret.push([coords.longitude + x, coords.latitude + y]);
    }
    ret.push(ret[0]);

    return {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'Polygon',
            coordinates: [ret],
          },
          properties: {},
        },
      ],
    };
  };

  // Function to add heatmap layers
  const addHeatmapLayers = (map: mapboxgl.Map, businesses: BusinessLocation[], type: string) => {
    const heatmapData = generateHeatmapData(businesses, type);
    const geoJSON = generateMapboxHeatmapGeoJSON(heatmapData);
    
    // Remove existing layers and sources
    if (map.getLayer('heatmap-layer')) map.removeLayer('heatmap-layer');
    if (map.getLayer('business-points')) map.removeLayer('business-points');
    if (map.getSource('heatmap-source')) map.removeSource('heatmap-source');
    
    // Add new source
    map.addSource('heatmap-source', {
      type: 'geojson',
      data: geoJSON
    });
    
    // Add heatmap layer
    map.addLayer({
      id: 'heatmap-layer',
      type: 'heatmap',
      source: 'heatmap-source',
      maxzoom: 15,
      paint: {
        'heatmap-weight': [
          'interpolate',
          ['linear'],
          ['get', 'intensity'],
          0, 0,
          1, 1
        ],
        'heatmap-intensity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          0, 1,
          15, 3
        ],
        'heatmap-color': [
          'interpolate',
          ['linear'],
          ['heatmap-density'],
          0, 'rgba(33,102,172,0)',
          0.2, 'rgb(103,169,207)',
          0.4, 'rgb(209,229,240)',
          0.6, 'rgb(253,219,199)',
          0.8, 'rgb(239,138,98)',
          1, 'rgb(178,24,43)'
        ],
        'heatmap-radius': [
          'interpolate',
          ['linear'],
          ['zoom'],
          0, 2,
          15, 20
        ]
      }
    });
    
    // Add business points layer
    map.addLayer({
      id: 'business-points',
      type: 'circle',
      source: 'heatmap-source',
      minzoom: 14,
      paint: {
        'circle-radius': [
          'interpolate',
          ['linear'],
          ['get', 'rating'],
          1, 4,
          5, 12
        ],
        'circle-color': [
          'interpolate',
          ['linear'],
          ['get', 'rating'],
          1, '#ff4444',
          2, '#ff8844',
          3, '#ffaa44',
          4, '#88ff44',
          5, '#44ff44'
        ],
        'circle-stroke-width': 2,
        'circle-stroke-color': '#ffffff',
        'circle-opacity': 0.8
      }
    });
    
    // Add click handler for business points
    map.on('click', 'business-points', (e) => {
      if (e.features && e.features[0]) {
        const feature = e.features[0];
        const properties = feature.properties;
        const geometry = feature.geometry;
        
        if (properties && geometry.type === 'Point') {
          new mapboxgl.Popup()
            .setLngLat([geometry.coordinates[0], geometry.coordinates[1]])
            .setHTML(`
              <div style="padding: 10px;">
                <h3 style="margin: 0 0 5px 0;">${properties.name || 'Unknown'}</h3>
                <p style="margin: 0;"><strong>Rating:</strong> ${properties.rating || 0}/5 (${properties.reviews || 0} reviews)</p>
                <p style="margin: 0;"><strong>Intensity:</strong> ${Math.round((properties.intensity || 0) * 100)}%</p>
              </div>
            `)
            .addTo(map);
        }
      }
    });
    
    // Change cursor on hover
    map.on('mouseenter', 'business-points', () => {
      map.getCanvas().style.cursor = 'pointer';
    });
    
    map.on('mouseleave', 'business-points', () => {
      map.getCanvas().style.cursor = '';
    });
  };

  // Function to update heatmap layers
  const updateHeatmapLayers = (map: mapboxgl.Map, businesses: BusinessLocation[], type: string) => {
    const heatmapData = generateHeatmapData(businesses, type);
    const geoJSON = generateMapboxHeatmapGeoJSON(heatmapData);
    
    if (map.getSource('heatmap-source')) {
      (map.getSource('heatmap-source') as mapboxgl.GeoJSONSource).setData(geoJSON);
    }
  };

  // Function to generate heatmap data based on type
  const generateHeatmapData = (businesses: BusinessLocation[], type: string) => {
    switch (type) {
      case 'competition':
        return generateCompetitionHeatmap(businesses);
      case 'opportunity':
        return generateOpportunityHeatmap(businesses);
      default:
        return generateBusinessHeatmap(businesses);
    }
  };

  return (
    <Paper 
      elevation={0} 
      sx={{ 
        position: 'relative',
        width: '100%',
        height: '100%',
        overflow: 'hidden',
        borderRadius: 0
      }}
    >
      <Box
        ref={mapContainer}
        sx={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: 0,
          right: 0
        }}
      />
      
      {/* Map Style Switcher */}
      <MapStyleSwitcher value={mapStyle} onChange={setMapStyle} />

      {/* Search Location Bar */}
        <SearchLocationBar 
          onLocationSelect={handleLocationSelect}
          onZipcodeSelect={setCurrentZipcode}
        />

      {/* Map Layers Toggle */}
      <MapLayersToggle onClick={() => setShowHeatmapPanel(!showHeatmapPanel)} />

      {/* Drawing Tools Toolbar */}
      <DrawingToolsToolbar activeTool={activeTool} onToolChange={handleToolChange} />

      {/* Distance Measurement Panel */}
      {showDistancePanel && (
        <DistanceMeasurementPanel
          onClose={() => {
            setShowDistancePanel(false);
            setActiveTool(null);
          }}
          onModeChange={handleModeChange}
          onDistanceChange={handleDistanceChange}
        />
      )}

      {/* Heatmap Panel */}
      {showHeatmapPanel && businesses && businesses.length > 0 && (
        <HeatmapPanel
          onClose={() => setShowHeatmapPanel(false)}
          onDataTypeChange={handleDataTypeChange}
        />
      )}

      {/* ZIP Code Info Panel */}
      {currentZipcode && (
        <ZipcodeInfoPanel onClose={() => {}} />
      )}
    </Paper>
  );
}