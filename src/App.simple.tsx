import React, { useEffect, useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { Header } from './components/Header';
import { StatusCard } from './components/StatusCard';
import { TimeRangeSelector } from './components/TimeRangeSelector';
import { ExportButton } from './components/ExportButton';
import { TimeRange } from './types';

// Simple mock data
const mockData = {
  incomingTraffic: 125.45,
  outgoingTraffic: 67.89,
  activeConnections: 42,
  timestamp: new Date()
};

function App() {
  console.log('App rendering');
  const [timeRange, setTimeRange] = useState<TimeRange>(TimeRange.FIFTEEN_MIN);
  
  // Log when component mounts
  useEffect(() => {
    console.log('App mounted');
    return () => console.log('App unmounted');
  }, []);

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6 transition-colors">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <Header />
            <div className="flex items-center gap-4">
              <TimeRangeSelector value={timeRange} onChange={setTimeRange} />
              <ExportButton timeRange={timeRange} />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <StatusCard
              title="Incoming Traffic"
              value={`${mockData.incomingTraffic.toFixed(2)} Mbps`}
              icon="arrow-down"
              color="blue"
            />
            <StatusCard
              title="Outgoing Traffic"
              value={`${mockData.outgoingTraffic.toFixed(2)} Mbps`}
              icon="arrow-up"
              color="green"
            />
            <StatusCard
              title="Active Connections"
              value={mockData.activeConnections.toString()}
              icon="network"
              color="purple"
            />
          </div>

          <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">
              Network Monitoring Dashboard
            </h2>
            <p className="text-gray-600 dark:text-gray-300">
              This is a simplified version of the dashboard showing basic metrics.
              The full dashboard with charts and detailed metrics will be implemented soon.
            </p>
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
