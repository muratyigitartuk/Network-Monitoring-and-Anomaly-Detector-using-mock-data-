import { NetworkMetrics } from '../types';

interface Props {
  data: NetworkMetrics;
  type: 'source' | 'destination';
}

export function TopIPs({ data, type }: Props) {
  const ips = type === 'source' ? data.topSourceIPs : data.topDestIPs;
  const title = type === 'source' ? 'Top Source IPs' : 'Top Destination IPs';

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">{title}</h2>
      <div className="space-y-2">
        {ips.map((ip) => (
          <div key={ip.ip} className="flex justify-between items-center p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
            <span className="font-mono text-gray-800 dark:text-gray-200">{ip.ip}</span>
            <span className="text-gray-600 dark:text-gray-400">{ip.count.toLocaleString()} packets</span>
          </div>
        ))}
      </div>
    </div>
  );
}