import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { NetworkMetrics } from '../types';
import { useTheme } from '../context/ThemeContext';

interface Props {
  data: NetworkMetrics;
}

export function ProtocolDistribution({ data }: Props) {
  const { theme } = useTheme();
  
  const protocols = [
    { name: 'TCP', value: data.protocols.tcp },
    { name: 'UDP', value: data.protocols.udp }
  ];

  const COLORS = ['#8b5cf6', '#10b981'];

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Protocol Distribution</h2>
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={protocols}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              label
            >
              {protocols.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ 
                backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff',
                borderColor: theme === 'dark' ? '#374151' : '#e5e7eb',
                color: theme === 'dark' ? '#ffffff' : '#000000'
              }}
            />
            <Legend 
              formatter={(value) => (
                <span className={theme === 'dark' ? 'text-gray-200' : 'text-gray-800'}>
                  {value}
                </span>
              )}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}