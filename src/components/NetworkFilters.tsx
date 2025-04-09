import { Filter } from 'lucide-react';
import { Filter as FilterType } from '../types';
import { useState } from 'react';

interface Props {
  filters: FilterType;
  onFilterChange: (filters: FilterType) => void;
}

export function NetworkFilters({ filters, onFilterChange }: Props) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      >
        <Filter className="w-5 h-5 text-gray-700 dark:text-gray-200" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 z-10">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Filters</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Port
              </label>
              <input
                type="number"
                value={filters.port || ''}
                onChange={e => onFilterChange({ ...filters, port: e.target.value ? Number(e.target.value) : undefined })}
                className="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded px-3 py-1"
                placeholder="Filter by port"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Protocol
              </label>
              <select
                value={filters.protocol || ''}
                onChange={e => onFilterChange({ ...filters, protocol: e.target.value as 'tcp' | 'udp' | undefined })}
                className="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded px-3 py-1"
              >
                <option value="">All protocols</option>
                <option value="tcp">TCP</option>
                <option value="udp">UDP</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Min Traffic (Mbps)
              </label>
              <input
                type="number"
                value={filters.minTraffic || ''}
                onChange={e => onFilterChange({ ...filters, minTraffic: e.target.value ? Number(e.target.value) : undefined })}
                className="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded px-3 py-1"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Max Latency (ms)
              </label>
              <input
                type="number"
                value={filters.maxLatency || ''}
                onChange={e => onFilterChange({ ...filters, maxLatency: e.target.value ? Number(e.target.value) : undefined })}
                className="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded px-3 py-1"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}