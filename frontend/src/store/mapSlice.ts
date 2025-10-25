import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
import type { ViewMode, MapLayer, DrawingTool } from '../types/enums';
import type { DrawnShape, FilterState, Coordinates } from '../types/schema';

interface MapState {
  activeViewMode: ViewMode;
  activeLayers: MapLayer[];
  selectedDrawingTool: DrawingTool | null;
  drawnShapes: DrawnShape[];
  selectedShapeId: string | null;
  comparisonTerritories: string[];
  filters: FilterState;
  mapCenter: Coordinates;
  mapZoom: number;
  mapStyle: string;
  searchQuery: string;
  distanceMeasurement: {
    mode: 'driving' | 'walking' | 'cycling' | 'circle';
    distance: number;
    unit: 'km' | 'mi';
  };
  heatmapDataType: string;
}

const initialState: MapState = {
  activeViewMode: 'map' as ViewMode,
  activeLayers: [],
  selectedDrawingTool: null,
  drawnShapes: [],
  selectedShapeId: null,
  comparisonTerritories: [],
  filters: {
    incomeRange: [0, 200000],
    minSearchVolume: 0,
    radius: 10,
    businessType: ''
  },
  mapCenter: { lat: 47.6062, lng: -122.3321 },
  mapZoom: 11,
  mapStyle: 'dark',
  searchQuery: '',
  distanceMeasurement: {
    mode: 'cycling',
    distance: 5,
    unit: 'km'
  },
  heatmapDataType: 'population'
};

const mapSlice = createSlice({
  name: 'map',
  initialState,
  reducers: {
    setViewMode: (state, action: PayloadAction<ViewMode>) => {
      state.activeViewMode = action.payload;
    },
    toggleLayer: (state, action: PayloadAction<MapLayer>) => {
      const index = state.activeLayers.indexOf(action.payload);
      if (index > -1) {
        state.activeLayers.splice(index, 1);
      } else {
        state.activeLayers.push(action.payload);
      }
    },
    setDrawingTool: (state, action: PayloadAction<DrawingTool | null>) => {
      state.selectedDrawingTool = action.payload;
    },
    addShape: (state, action: PayloadAction<DrawnShape>) => {
      state.drawnShapes.push(action.payload);
    },
    updateShape: (state, action: PayloadAction<{ id: string; updates: Partial<DrawnShape> }>) => {
      const shape = state.drawnShapes.find(s => s.id === action.payload.id);
      if (shape) {
        Object.assign(shape, action.payload.updates);
      }
    },
    deleteShape: (state, action: PayloadAction<string>) => {
      state.drawnShapes = state.drawnShapes.filter(s => s.id !== action.payload);
      if (state.selectedShapeId === action.payload) {
        state.selectedShapeId = null;
      }
    },
    setSelectedShapeId: (state, action: PayloadAction<string | null>) => {
      state.selectedShapeId = action.payload;
    },
    addToComparison: (state, action: PayloadAction<string>) => {
      if (!state.comparisonTerritories.includes(action.payload)) {
        state.comparisonTerritories.push(action.payload);
      }
    },
    removeFromComparison: (state, action: PayloadAction<string>) => {
      state.comparisonTerritories = state.comparisonTerritories.filter(id => id !== action.payload);
    },
    updateFilters: (state, action: PayloadAction<Partial<FilterState>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    resetFilters: (state) => {
      state.filters = initialState.filters;
    },
    setMapCenter: (state, action: PayloadAction<Coordinates>) => {
      state.mapCenter = action.payload;
    },
    setMapZoom: (state, action: PayloadAction<number>) => {
      state.mapZoom = action.payload;
    },
    setMapStyle: (state, action: PayloadAction<string>) => {
      state.mapStyle = action.payload;
    },
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
    setDistanceMeasurement: (state, action: PayloadAction<Partial<MapState['distanceMeasurement']>>) => {
      state.distanceMeasurement = { ...state.distanceMeasurement, ...action.payload };
    },
    setHeatmapDataType: (state, action: PayloadAction<string>) => {
      state.heatmapDataType = action.payload;
    }
  }
});

export const {
  setViewMode,
  toggleLayer,
  setDrawingTool,
  addShape,
  updateShape,
  deleteShape,
  setSelectedShapeId,
  addToComparison,
  removeFromComparison,
  updateFilters,
  resetFilters,
  setMapCenter,
  setMapZoom,
  setMapStyle,
  setSearchQuery,
  setDistanceMeasurement,
  setHeatmapDataType
} = mapSlice.actions;

export default mapSlice.reducer;