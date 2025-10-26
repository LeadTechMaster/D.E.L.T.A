// Mapbox Configuration
// To use this application, you need to:
// 1. Sign up for a free Mapbox account at https://account.mapbox.com/
// 2. Get your access token from https://account.mapbox.com/access-tokens/
// 3. Replace 'YOUR_MAPBOX_TOKEN_HERE' below with your actual token
// 4. Or set it as an environment variable VITE_MAPBOX_TOKEN

export const MAPBOX_ACCESS_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || 'pk.eyJ1Ijoic3VwcG9ydG1vdmVkaW4iLCJhIjoiY21kZmdxdHh6MGQ2aDJqcHE2YTIwbTFrMiJ9.I1xkq82JXLMlgB02xT8LMw';

console.log('🗺️ Mapbox Token Loaded:', MAPBOX_ACCESS_TOKEN.substring(0, 30) + '...');

// Default map configuration
export const DEFAULT_MAP_STYLE = 'mapbox://styles/mapbox/dark-v11';
export const DEFAULT_CENTER: [number, number] = [-122.3321, 47.6062]; // Seattle
export const DEFAULT_ZOOM = 11;