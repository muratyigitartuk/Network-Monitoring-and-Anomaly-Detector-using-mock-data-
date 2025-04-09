import { AlertTriangle, CheckCircle2 } from 'lucide-react';
import { Alert } from '../types';
import { format } from 'date-fns';

interface Props {
  alerts: Alert[];
  onAcknowledge: (id: string) => void;
}

export function AlertList({ alerts, onAcknowledge }: Props) {
  if (alerts.length === 0) return null;

  return (
    <div className="mb-6 space-y-2">
      {alerts.map(alert => (
        <div 
          key={alert.id} 
          className={`flex items-center gap-2 p-3 rounded-lg ${
            alert.type === 'critical' 
              ? 'bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-700' 
              : 'bg-yellow-50 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-700'
          } border`}
        >
          <AlertTriangle className={`w-5 h-5 ${
            alert.type === 'critical' 
              ? 'text-red-500 dark:text-red-400' 
              : 'text-yellow-500 dark:text-yellow-400'
          }`} />
          <div className="flex-1">
            <span className={`${
              alert.type === 'critical' 
                ? 'text-red-800 dark:text-red-200' 
                : 'text-yellow-800 dark:text-yellow-200'
            }`}>
              {alert.message}
            </span>
            <span className={`ml-2 text-sm ${
              alert.type === 'critical' 
                ? 'text-red-600 dark:text-red-400' 
                : 'text-yellow-600 dark:text-yellow-400'
            }`}>
              {format(alert.timestamp, 'HH:mm:ss')}
            </span>
          </div>
          {!alert.acknowledged && (
            <button
              onClick={() => onAcknowledge(alert.id)}
              className="p-1 hover:bg-white/10 rounded"
              title="Acknowledge alert"
            >
              <CheckCircle2 className="w-5 h-5 text-green-500 dark:text-green-400" />
            </button>
          )}
        </div>
      ))}
    </div>
  );
}