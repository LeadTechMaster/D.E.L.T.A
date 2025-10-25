import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { Provider } from 'react-redux';
import { store } from './store/store';
import theme from './theme/theme';
import Dashboard from './components/Dashboard/Dashboard';

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline enableColorScheme />
        <Dashboard
          projectName="Seattle Motor Boat Market Analysis"
          lastSaved={new Date('2025-01-09T14:30:00')}
          userName="John Doe"
        />
      </ThemeProvider>
    </Provider>
  );
}

export default App;