import React, { useState, useEffect } from 'react';
import { NetworkMetrics } from '../types';
import { AlertTriangle, CheckCircle } from 'lucide-react';

interface Props {
  data: NetworkMetrics[];
  thresholdSensitivity?: number; // 0-1, where 1 is most sensitive
}

interface AnomalyResult {
  isAnomaly: boolean;
  score: number;
  metric: string;
  value: number;
  timestamp: number;
}

export function AnomalyDetection({ data, thresholdSensitivity = 0.7 }: Props) {
  const [anomalies, setAnomalies] = useState<AnomalyResult[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!data || data.length < 10) {
      setLoading(false);
      return;
    }

    // Detect anomalies using a simple statistical approach
    // In a real implementation, this would call the backend ML service
    const detectAnomalies = () => {
      setLoading(true);
      
      // Calculate mean and standard deviation for each metric
      const metrics = ['incomingTraffic', 'outgoingTraffic', 'activeConnections', 'averageLatency', 'packetLoss'];
      const stats = metrics.reduce((acc, metric) => {
        const values = data.map(d => d[metric as keyof NetworkMetrics] as number);
        const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
        const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
        const stdDev = Math.sqrt(variance);
        
        acc[metric] = { mean, stdDev };
        return acc;
      }, {} as Record<string, { mean: number; stdDev: number }>);
      
      // Detect anomalies (values more than X standard deviations from mean)
      // thresholdSensitivity controls how many standard deviations to use
      const stdDevThreshold = 3 - (2 * thresholdSensitivity); // Maps 0.7 to 1.6 std deviations
      
      const newAnomalies: AnomalyResult[] = [];
      
      // Check only the most recent data points
      const recentData = data.slice(-5);
      
      recentData.forEach(metric => {
        metrics.forEach(metricName => {
          const value = metric[metricName as keyof NetworkMetrics] as number;
          const { mean, stdDev } = stats[metricName];
          
          // Calculate z-score (how many standard deviations from mean)
          const zScore = Math.abs((value - mean) / stdDev);
          
          // If z-score exceeds threshold, it's an anomaly
          if (zScore > stdDevThreshold) {
            newAnomalies.push({
              isAnomaly: true,
              score: zScore,
              metric: metricName,
              value,
              timestamp: metric.timestamp
            });
          }
        });
      });
      
      setAnomalies(newAnomalies);
      setLoading(false);
    };
    
    detectAnomalies();
  }, [data, thresholdSensitivity]);

  const formatMetricName = (name: string): string => {
    switch (name) {
      case 'incomingTraffic': return 'Incoming Traffic';
      case 'outgoingTraffic': return 'Outgoing Traffic';
      case 'activeConnections': return 'Active Connections';
      case 'averageLatency': return 'Average Latency';
      case 'packetLoss': return 'Packet Loss';
      default: return name;
    }
  };

  const formatMetricValue = (name: string, value: number): string => {
    switch (name) {
      case 'incomingTraffic':
      case 'outgoingTraffic':
        return `${Math.round(value)} Mbps`;
      case 'activeConnections':
        return `${value} connections`;
      case 'averageLatency':
        return `${Math.round(value)} ms`;
      case 'packetLoss':
        return `${value.toFixed(2)}%`;
      default:
        return `${value}`;
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Anomaly Detection</h2>
      
      {loading ? (
        <div className="flex justify-center items-center h-32">
          <div className="text-gray-500 dark:text-gray-400">Analyzing network patterns...</div>
        </div>
      ) : anomalies.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-32 text-green-600 dark:text-green-400">
          <CheckCircle className="w-8 h-8 mb-2" />
          <div>No anomalies detected</div>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="text-amber-600 dark:text-amber-400 font-medium mb-2">
            {anomalies.length} potential {anomalies.length === 1 ? 'anomaly' : 'anomalies'} detected
          </div>
          
          {anomalies.map((anomaly, index) => (
            <div 
              key={index}
              className="flex items-start p-3 rounded-md bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800"
            >
              <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 mt-0.5 mr-2 flex-shrink-0" />
              <div>
                <div className="font-medium text-amber-800 dark:text-amber-300">
                  Unusual {formatMetricName(anomaly.metric)}
                </div>
                <div className="text-sm text-amber-700 dark:text-amber-400">
                  Current value: {formatMetricValue(anomaly.metric, anomaly.value)}
                </div>
                <div className="text-xs text-amber-600 dark:text-amber-500 mt-1">
                  Anomaly score: {anomaly.score.toFixed(2)}
                </div>
              </div>
            </div>
          ))}
          
          <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Anomaly detection uses statistical analysis to identify unusual patterns in network traffic.
          </div>
        </div>
      )}
    </div>
  );
}
