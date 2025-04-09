import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { NetworkMetrics } from '../types';
import { useTheme } from '../context/ThemeContext';
import { format } from 'date-fns';

interface Props {
  data: NetworkMetrics[];
}

export function LatencyChart({ data }: Props) {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  const formattedData = data.map(metric => ({
    time: format(metric.timestamp, 'HH:mm:ss'),
    latency: Math.round(metric.averageLatency),
    packetLoss: metric.packetLoss
  }));

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Network Latency</h2>
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={formattedData}>
            <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
            <XAxis 
              dataKey="time" 
              stroke={isDark ? '#9ca3af' : '#4b5563'}
            />
            <YAxis 
              stroke={isDark ? '#9ca3af' : '#4b5563'}
              yAxisId="left"
              label={{ value: 'Latency (ms)', angle: -90, position: 'insideLeft' }}
            />
            <YAxis 
              stroke={isDark ? '#9ca3af' : '#4b5563'}
              yAxisId="right"
              orientation="right"
              label={{ value: 'Packet Loss (%)', angle: 90, position: 'insideRight' }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: isDark ? '#1f2937' : '#ffffff',
                borderColor: isDark ? '#374151' : '#e5e7eb',
                color: isDark ? '#ffffff' : '#000000'
              }}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="latency" 
              stroke="#8b5cf6" 
              name="Latency"
              yAxisId="left"
              strokeWidth={2}
            />
            <Line 
              type="monotone" 
              dataKey="packetLoss" 
              stroke="#ef4444" 
              name="Packet Loss"
              yAxisId="right"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}