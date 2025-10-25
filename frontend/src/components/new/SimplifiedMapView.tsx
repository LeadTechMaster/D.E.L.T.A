import { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { MAPBOX_ACCESS_TOKEN } from '@/config/mapbox';

mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;

interface SimplifiedMapViewProps {
  center?: { lat: number; lng: number };
  zoom?: number;
}

export function SimplifiedMapView({ center = { lat: 37.7749, lng: -122.4194 }, zoom = 12 }: SimplifiedMapViewProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/satellite-streets-v12',
      center: [center.lng, center.lat],
      zoom: zoom
    });

    map.current.addControl(new mapboxgl.NavigationControl(), 'bottom-right');

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

  return (
    <div className="fixed inset-0 pt-14">
      <div ref={mapContainer} className="w-full h-full" />
    </div>
  );
}

