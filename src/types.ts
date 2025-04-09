export interface NetworkMetrics {
  timestamp: number;
  incomingTraffic: number;
  outgoingTraffic: number;
  activeConnections: number;
  topSourceIPs: { ip: string; count: number; location?: string; latency?: number }[];
  topDestIPs: { ip: string; count: number; location?: string; latency?: number }[];
  protocols: {
    tcp: number;
    udp: number;
  };
  portTraffic: { port: number; bytes: number }[];
  averageLatency: number;
  packetLoss: number;
}

export interface Alert {
  id: string;
  message: string;
  timestamp: number;
  type: 'warning' | 'critical';
  acknowledged: boolean;
}

export interface Threshold {
  id: string;
  name: string;
  metric: 'incomingTraffic' | 'outgoingTraffic' | 'activeConnections' | 'averageLatency' | 'packetLoss';
  value: number;
  type: 'warning' | 'critical';
  enabled: boolean;
}

export interface Filter {
  port?: number;
  protocol?: 'tcp' | 'udp';
  minTraffic?: number;
  maxLatency?: number;
}

export type TimeRange = '5m' | '15m' | '30m' | '1h' | '6h' | '24h';
export type Theme = 'light' | 'dark';