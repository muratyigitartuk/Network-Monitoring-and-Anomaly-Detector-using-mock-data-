import React, { useEffect, useState, useCallback } from 'react';
import { NetworkMetrics, Alert, Threshold, TimeRange, Filter } from './types';
import { ThemeProvider } from './context/ThemeContext';
import { Header } from './components/Header';
import { AlertList } from './components/AlertList';
import { TrafficChart } from './components/TrafficChart';
import { LatencyChart } from './components/LatencyChart';
import { ProtocolDistribution } from './components/ProtocolDistribution';
import { PortTrafficChart } from './components/PortTrafficChart';
import { TopIPs } from './components/TopIPs';
import { StatusCard } from './components/StatusCard';
import { TimeRangeSelector } from './components/TimeRangeSelector';
import { NetworkFilters } from './components/NetworkFilters';
import { ThresholdManager } from './components/ThresholdManager';
import { ExportButton } from './components/ExportButton';
import { NetworkTopology } from './components/NetworkTopology';
import { AnomalyDetection } from './components/AnomalyDetection';
// Login form removed - no authentication required
import { fetchCurrentMetrics, fetchHistoricalMetrics, fetchThresholds, acknowledgeAlert as apiAcknowledgeAlert, generateMockMetrics } from './services/api';

const UPDATE_INTERVAL = 2000;
const MAX_HISTORY = 30;

// Debug function to log component renders and state changes
function debugLog(message: string, data?: any) {
  const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
  console.log(`[${timestamp}] ${message}`, data ? data : '');
}

function App() {
  debugLog('App component rendering');

  const [metrics, setMetrics] = useState<NetworkMetrics[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [currentMetrics, setCurrentMetrics] = useState<NetworkMetrics | null>(null);
  const [thresholds, setThresholds] = useState<Threshold[]>([]);
  const [timeRange, setTimeRange] = useState<TimeRange>(TimeRange.FIFTEEN_MIN);
  const [filters, setFilters] = useState<Filter[]>([]);
  // Always authenticated, no login required
  const [isAuthenticated] = useState<boolean>(true);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [user] = useState<{ username: string; role: string }>({ username: 'admin', role: 'admin' });

  // Fetch metrics from API
  const fetchMetrics = useCallback(async () => {
    try {
      debugLog('Fetching current metrics');
      const data = await fetchCurrentMetrics();
      debugLog('Current metrics fetched', { timestamp: data.timestamp });

      setCurrentMetrics(data);
      setMetrics(prev => {
        const updated = [...prev, data].slice(-MAX_HISTORY);
        return updated;
      });
    } catch (error) {
      debugLog('Failed to fetch metrics', error);

      // Fallback to mock data if API fails
      const mockMetrics = generateMockMetrics();
      setCurrentMetrics(mockMetrics);
      setMetrics(prev => {
        const updated = [...prev, mockMetrics].slice(-MAX_HISTORY);
        return updated;
      });
    }
  }, []);

  // Acknowledge alert
  const acknowledgeAlert = async (id: string) => {
    try {
      await apiAcknowledgeAlert(id);
      setAlerts(prev => prev.map(alert =>
        alert.id === id ? { ...alert, acknowledged: true } : alert
      ));
    } catch (error) {
      console.error('Failed to acknowledge alert:', error);
    }
  };

  // Initialize the app on mount and generate initial mock data
  useEffect(() => {
    debugLog('App initialization');
    setIsLoading(true);

    try {
      // Generate initial mock data
      debugLog('Generating initial mock data');
      const mockMetrics = generateMockMetrics();

      // Set metrics first
      setMetrics([mockMetrics]);

      // Set current metrics
      setCurrentMetrics(mockMetrics);

      debugLog('Initial data generation complete');
    } catch (error) {
      debugLog('Error generating initial mock data', error);
    } finally {
      setIsLoading(false);
    }

    return () => {
      debugLog('App cleanup');
    };
  }, []);

  // Fetch thresholds from API
  useEffect(() => {
    if (!isAuthenticated) return;

    const loadThresholds = async () => {
      try {
        const data = await fetchThresholds();
        setThresholds(data);
      } catch (error) {
        console.error('Failed to fetch thresholds:', error);
      }
    };

    loadThresholds();
  }, [isAuthenticated]);

  // Fetch historical metrics based on time range
  useEffect(() => {
    if (!isAuthenticated) return;

    const loadHistoricalMetrics = async () => {
      try {
        const data = await fetchHistoricalMetrics(timeRange);
        if (data.length > 0) {
          setMetrics(data);
          setCurrentMetrics(data[data.length - 1]);
        }
      } catch (error) {
        console.error('Failed to fetch historical metrics:', error);
      }
    };

    loadHistoricalMetrics();
  }, [timeRange, isAuthenticated]);

  // Generate initial mock data when authenticated
  useEffect(() => {
    debugLog('Initial data useEffect running', { isAuthenticated, hasCurrentMetrics: !!currentMetrics });

    if (!isAuthenticated) {
      debugLog('Not authenticated, skipping initial data generation');
      return;
    }

    // Only generate mock data if we don't have any yet
    if (!currentMetrics) {
      debugLog('No current metrics, generating initial mock data');
      try {
        const mockMetrics = generateMockMetrics();
        debugLog('Mock metrics generated', { timestamp: mockMetrics.timestamp });

        // Set metrics first
        debugLog('Setting metrics array');
        setMetrics([mockMetrics]);

        // Set current metrics last
        debugLog('Setting currentMetrics');
        setCurrentMetrics(mockMetrics);

        debugLog('Initial data generation complete');
      } catch (error) {
        debugLog('Error generating mock metrics', error);
      }
    }

    return () => {
      debugLog('Initial data useEffect cleanup');
    };
  }, [isAuthenticated, currentMetrics]);

  // Set up polling interval for real-time updates
  useEffect(() => {
    debugLog('Polling useEffect running', { isAuthenticated, hasCurrentMetrics: !!currentMetrics });

    if (!isAuthenticated) {
      debugLog('Not authenticated, skipping polling setup');
      return;
    }

    // Only start polling if we already have initial data
    if (currentMetrics) {
      debugLog('Starting metrics polling');

      // Create a flag to track if component is still mounted
      let isMounted = true;

      // Define a safe fetch function that checks if component is still mounted
      const safeFetchMetrics = async () => {
        if (!isMounted) return;
        debugLog('Fetching metrics');
        try {
          await fetchMetrics();
          debugLog('Metrics fetched successfully');
        } catch (error) {
          debugLog('Error fetching metrics', error);
        }
      };

      // Fetch immediately on mount
      safeFetchMetrics();

      debugLog('Setting up polling interval');
      const interval = setInterval(() => {
        safeFetchMetrics();
      }, UPDATE_INTERVAL);

      return () => {
        debugLog('Polling useEffect cleanup');
        isMounted = false;
        clearInterval(interval);
      };
    } else {
      debugLog('No current metrics yet, not starting polling');
    }
  }, [fetchMetrics, isAuthenticated, currentMetrics]);

  // Determine what to render based on state
  const renderContent = () => {
    debugLog('Determining what to render', { isLoading, hasCurrentMetrics: !!currentMetrics });

    if (isLoading) {
      debugLog('Rendering loading state');
      return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
          <div className="text-lg text-gray-600 dark:text-gray-400">Loading...</div>
        </div>
      );
    }

    // If no metrics yet, show loading
    if (!currentMetrics) {
      debugLog('Rendering metrics loading state');
      return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
          <div className="text-lg text-gray-600 dark:text-gray-400">Loading metrics...</div>
        </div>
      );
    }

    // If we have metrics, render the dashboard
    debugLog('Rendering dashboard');
    return (
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
              value={`${currentMetrics.incomingTraffic.toFixed(2)} Mbps`}
              icon="arrow-down"
              color="blue"
            />
            <StatusCard
              title="Outgoing Traffic"
              value={`${currentMetrics.outgoingTraffic.toFixed(2)} Mbps`}
              icon="arrow-up"
              color="green"
            />
            <StatusCard
              title="Active Connections"
              value={currentMetrics.activeConnections.toString()}
              icon="network"
              color="purple"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <TrafficChart metrics={metrics} />
            <LatencyChart metrics={metrics} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <ProtocolDistribution protocols={currentMetrics.protocols} />
            <PortTrafficChart portTraffic={currentMetrics.portTraffic} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <TopIPs ips={currentMetrics.topSourceIPs} title="Top Source IPs" />
            <TopIPs ips={currentMetrics.topDestIPs} title="Top Destination IPs" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <NetworkTopology />
            <AnomalyDetection metrics={metrics} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AlertList alerts={alerts} onAcknowledge={acknowledgeAlert} />
            <ThresholdManager thresholds={thresholds} setThresholds={setThresholds} />
          </div>
        </div>
      </div>
    );
  };

  // Wrap the rendered content in ThemeProvider
  return (
    <ThemeProvider>
      {renderContent()}
    </ThemeProvider>
  );
}

export default App;
