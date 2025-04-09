import { NetworkMetrics } from '../types';

interface Props {
  metrics: NetworkMetrics;
}

export function StatusCard({ metrics }: Props) {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">Current Status</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Active Connections</p>
          <p className="text-2xl font-semibold text-gray-900 dark:text-white">
            {metrics.activeConnections}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Traffic</p>
          <p className="text-2xl font-semibold text-gray-900 dark:text-white">
            {Math.round(metrics.incomingTraffic + metrics.outgoingTraffic)} Mbps
          </p>
        </div>
      </div>
    </div>
  );
}