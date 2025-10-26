/**
 * Map Coordinate Conversion Service
 * 
 * Converts between screen coordinates and geographic coordinates (lat/lng)
 * using the Mapbox GL JS map instance.
 */

import type { Map } from 'mapbox-gl';

export class MapCoordinateService {
  private static mapInstance: Map | null = null;

  /**
   * Set the Mapbox map instance for coordinate conversion
   */
  static setMapInstance(map: Map) {
    this.mapInstance = map;
    console.log("Map instance registered for coordinate conversion");
  }

  /**
   * Convert screen pixel coordinates to geographic coordinates
   * @param screenX - X coordinate in pixels (from canvas or screen)
   * @param screenY - Y coordinate in pixels
   * @returns [lat, lng] or null if map not available
   */
  static screenToLatLng(screenX: number, screenY: number): [number, number] | null {
    if (!this.mapInstance) {
      console.error("Map instance not available for coordinate conversion");
      return null;
    }

    try {
      const lngLat = this.mapInstance.unproject([screenX, screenY]);
      return [lngLat.lat, lngLat.lng];
    } catch (error) {
      console.error("Error converting screen to lat/lng:", error);
      return null;
    }
  }

  /**
   * Convert geographic coordinates to screen pixel coordinates
   * @param lat - Latitude
   * @param lng - Longitude
   * @returns {x, y} or null if map not available
   */
  static latLngToScreen(lat: number, lng: number): { x: number; y: number } | null {
    if (!this.mapInstance) {
      console.error("Map instance not available for coordinate conversion");
      return null;
    }

    try {
      const point = this.mapInstance.project([lng, lat]);
      return { x: point.x, y: point.y };
    } catch (error) {
      console.error("Error converting lat/lng to screen:", error);
      return null;
    }
  }

  /**
   * Convert array of screen coordinates to lat/lng
   * @param screenCoords - Array of [x, y] screen coordinates
   * @returns Array of [lat, lng] coordinates
   */
  static screenArrayToLatLng(screenCoords: [number, number][]): [number, number][] {
    return screenCoords
      .map(([x, y]) => this.screenToLatLng(x, y))
      .filter((coord): coord is [number, number] => coord !== null);
  }

  /**
   * Get current map instance
   */
  static getMapInstance(): Map | null {
    return this.mapInstance;
  }
}

