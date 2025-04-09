import { Clock } from 'lucide-react';
import { TimeRange } from '../types';

interface Props {
  value: TimeRange;
  onChange: (range: TimeRange) => void;
}

export function TimeRangeSelector({ value, onChange }: Props) {
  const ranges: { value: TimeRange; label: string }[] = [
    { value: '5m', label: '5 minutes' },
    { value: '15m', label: '15 minutes' },
    { value: '30m', label: '30 minutes' },
    { value: '1h', label: '1 hour' },
    { value: '6h', label: '6 hours' },
    { value: '24h', label: '24 hours' },
  ];

  return (
    <div className="flex items-center gap-2">
      <Clock className="w-5 h-5 text-gray-600 dark:text-gray-400" />
      <select
        value={value}
        onChange={(e) => onChange(e.target.value as TimeRange)}
        className="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 text-sm"
      >
        {ranges.map(range => (
          <option key={range.value} value={range.value}>
            {range.label}
          </option>
        ))}
      </select>
    </div>
  );
}