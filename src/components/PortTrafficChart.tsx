import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { NetworkMetrics } from '../types';
import { useTheme } from '../context/ThemeContext';

interface Props {
  data: NetworkMetrics;
}

export function PortTrafficChart({ data }: Props) {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  const formattedData = data.portTraffic
    .sort((a, b) => b.bytes - a.bytes)
    .map(port => ({
      port: `Port ${port.port}`,
      traffic: Math.round(port.bytes / 1024 / 1024) // Convert to MB
    }));

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Port Traffic (MB)</h2>
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={formattedData}>
            <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
            <XAxis 
              dataKey="port" 
              stroke={isDark ? '#9ca3af' : '#4b5563'}
            />
            <YAxis 
              stroke={isDark ? '#9ca3af' : '#4b5563'}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: isDark ? '#1f2937' : '#ffffff',
                borderColor: isDark ? '#374151' : '#e5e7eb',
                color: isDark ? '#ffffff' : '#000000'
              }}
            />
            <Legend />
            <Bar dataKey="traffic" fill="#6366f1" name="Traffic" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}