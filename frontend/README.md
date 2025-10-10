# D.E.L.T.A Market Intelligence Dashboard

A comprehensive market intelligence platform featuring interactive maps, real-time analytics, and business insights.

## Features

- 🗺️ **Interactive Mapbox Map** - Full-screen map with dynamic overlays and heatmaps
- 📊 **Analytics Dashboard** - Demographics, keyword demand, competitor analysis, and opportunity scoring
- 🎯 **Drawing Tools** - Circle, polygon, drive-time zones, and ZIP selection
- 📈 **Data Visualization** - Bar charts, line charts, pie charts, and radar charts
- 🔍 **Territory Comparison** - Compare multiple territories side-by-side
- 🎨 **Modern UI** - Dark mode with vibrant accents, glassmorphism effects

## Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool (with Rolldown)
- **Material-UI v7** - Component library
- **MUI X Charts** - Data visualization
- **Redux Toolkit** - State management
- **Mapbox GL JS** - Interactive maps
- **Emotion** - CSS-in-JS styling

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Mapbox account and access token

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

4. Add your Mapbox token to `.env`:
   ```
   VITE_MAPBOX_TOKEN=your_actual_mapbox_token_here
   ```

   Get your free token at: https://account.mapbox.com/access-tokens/

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5176`

### Build

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Dashboard/
│   │       ├── Dashboard.tsx           # Main dashboard component
│   │       ├── DashboardHeader.tsx     # Header with view mode toggles
│   │       ├── MapView.tsx             # Mapbox map component
│   │       ├── DemographicsPanel.tsx   # Demographics analytics
│   │       ├── DemandPanel.tsx         # Keyword demand analytics
│   │       ├── CompetitorPanel.tsx     # Competitor analysis
│   │       └── OpportunityPanel.tsx    # Opportunity scoring
│   ├── store/
│   │   ├── store.ts                    # Redux store configuration
│   │   ├── mapSlice.ts                 # Map state management
│   │   └── hooks.ts                    # Typed Redux hooks
│   ├── types/
│   │   ├── enums.ts                    # TypeScript enums
│   │   └── schema.ts                   # TypeScript interfaces
│   ├── utils/
│   │   └── formatters.ts               # Formatting utilities
│   ├── data/
│   │   └── dashboardMockData.ts        # Mock data for development
│   ├── theme/
│   │   └── theme.ts                    # MUI theme configuration
│   ├── config/
│   │   └── mapbox.ts                   # Mapbox configuration
│   ├── App.tsx                         # Root component
│   └── main.tsx                        # Entry point
├── public/                             # Static assets
├── index.html                          # HTML template
├── package.json                        # Dependencies
├── tsconfig.json                       # TypeScript configuration
└── vite.config.ts                      # Vite configuration
```

## Available View Modes

- **Map View** - Full-screen interactive map
- **Dashboard View** - Analytics panels only
- **Split View** - Map and dashboard side-by-side

## Mock Data

The application currently uses mock data for demonstration. To connect to the real backend API:

1. Ensure the backend server is running at `http://localhost:8001`
2. Implement RTK Query endpoints in `src/api/` (TODO)
3. Replace mock data with API calls in components

## Expanding the ESLint Configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      tseslint.configs.recommendedTypeChecked,
      tseslint.configs.strictTypeChecked,
      tseslint.configs.stylisticTypeChecked,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
])
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

Proprietary - All rights reserved