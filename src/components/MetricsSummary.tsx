import { NetworkMetrics } from '../types';
import { formatBytes } from '../utils/format';

interface Props {
  metrics: NetworkMetrics;
}

export function MetricsSummary({ metrics }: Props) {
  const totalTraffic = metrics.incomingTraffic + metrics.outgoingTraffic;
  const tcpPercentage = (metrics.protocols.tcp / (metrics.protocols.tcp + metrics.protocols.udp) * 100).toFixed(1);
  const udpPercentage = (metrics.protocols.udp / (metrics.protocols.tcp + metrics.protocols.udp) * 100).toFixed(1);

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Network Summary</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Traffic</p>
          <p className="text-xl font-semibold text-gray-900 dark:text-white">
            {Math.round(totalTraffic)} Mbps
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Active Connections</p>
          <p className="text-xl font-semibold text-gray-900 dark:text-white">
            {metrics.activeConnections}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Protocol Distribution</p>
          <p className="text-xl font-semibold text-gray-900 dark:text-white">
            TCP: {tcpPercentage}% / UDP: {udpPercentage}%
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Most Active Port</p>
          <p className="text-xl font-semibold text-gray-900 dark:text-white">
            Port {metrics.portTraffic.sort((a, b) => b.bytes - a.bytes)[0].port}
          </p>
        </div>
      </div>
    </div>
  );
}