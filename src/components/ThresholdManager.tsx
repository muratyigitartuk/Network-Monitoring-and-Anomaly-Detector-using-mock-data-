import { useState } from 'react';
import { Settings2, Plus, Trash2 } from 'lucide-react';
import { Threshold } from '../types';

interface Props {
  thresholds: Threshold[];
  onThresholdChange: (thresholds: Threshold[]) => void;
}

export function ThresholdManager({ thresholds, onThresholdChange }: Props) {
  const [isOpen, setIsOpen] = useState(false);

  const addThreshold = () => {
    const newThreshold: Threshold = {
      id: Date.now().toString(),
      name: 'New Threshold',
      metric: 'incomingTraffic',
      value: 1000,
      type: 'warning',
      enabled: true
    };
    onThresholdChange([...thresholds, newThreshold]);
  };

  const removeThreshold = (id: string) => {
    onThresholdChange(thresholds.filter(t => t.id !== id));
  };

  const updateThreshold = (id: string, updates: Partial<Threshold>) => {
    onThresholdChange(
      thresholds.map(t => t.id === id ? { ...t, ...updates } : t)
    );
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      >
        <Settings2 className="w-5 h-5 text-gray-700 dark:text-gray-200" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-96 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 z-10">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Thresholds</h3>
            <button
              onClick={addThreshold}
              className="p-2 rounded-lg bg-blue-500 hover:bg-blue-600 text-white transition-colors"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>

          <div className="space-y-4">
            {thresholds.map(threshold => (
              <div key={threshold.id} className="flex items-center gap-4 p-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <input
                  type="checkbox"
                  checked={threshold.enabled}
                  onChange={e => updateThreshold(threshold.id, { enabled: e.target.checked })}
                  className="w-4 h-4"
                />
                <input
                  type="text"
                  value={threshold.name}
                  onChange={e => updateThreshold(threshold.id, { name: e.target.value })}
                  className="flex-1 bg-transparent border-b border-gray-300 dark:border-gray-600 focus:outline-none focus:border-blue-500"
                />
                <select
                  value={threshold.metric}
                  onChange={e => updateThreshold(threshold.id, { metric: e.target.value as Threshold['metric'] })}
                  className="bg-transparent border border-gray-300 dark:border-gray-600 rounded"
                >
                  <option value="incomingTraffic">Incoming Traffic</option>
                  <option value="outgoingTraffic">Outgoing Traffic</option>
                  <option value="activeConnections">Active Connections</option>
                </select>
                <input
                  type="number"
                  value={threshold.value}
                  onChange={e => updateThreshold(threshold.id, { value: Number(e.target.value) })}
                  className="w-24 bg-transparent border border-gray-300 dark:border-gray-600 rounded"
                />
                <button
                  onClick={() => removeThreshold(threshold.id)}
                  className="text-red-500 hover:text-red-600"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}