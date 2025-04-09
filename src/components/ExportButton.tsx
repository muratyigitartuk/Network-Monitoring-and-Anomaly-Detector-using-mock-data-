import { Download } from 'lucide-react';
import { NetworkMetrics, TimeRange } from '../types';
import { unparse } from 'papaparse';
import { exportData } from '../services/api';

interface Props {
  data: NetworkMetrics[];
  timeRange?: TimeRange;
}

export function ExportButton({ data, timeRange = '24h' }: Props) {
  const handleExport = async () => {
    try {
      // Try to use the API to export data
      const blob = await exportData(timeRange);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');

      link.setAttribute('href', url);
      link.setAttribute('download', `network-metrics-${new Date().toISOString()}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Failed to export data from API, falling back to local data:', error);

      // Fallback to local data if API fails
      const exportDataLocal = data.map(metric => ({
        timestamp: new Date(metric.timestamp).toISOString(),
        incomingTraffic: metric.incomingTraffic,
        outgoingTraffic: metric.outgoingTraffic,
        activeConnections: metric.activeConnections,
        tcpTraffic: metric.protocols.tcp,
        udpTraffic: metric.protocols.udp,
        averageLatency: metric.averageLatency,
        packetLoss: metric.packetLoss
      }));

      const csv = unparse(exportDataLocal);
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);

      link.setAttribute('href', url);
      link.setAttribute('download', `network-metrics-${new Date().toISOString()}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <button
      onClick={handleExport}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      title="Export data"
    >
      <Download className="w-5 h-5 text-gray-700 dark:text-gray-200" />
    </button>
  );
}