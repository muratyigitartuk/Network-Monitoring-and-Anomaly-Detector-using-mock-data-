import { NetworkMetrics } from '../types';

const LOCATIONS = [
  'New York, US',
  'London, UK',
  'Tokyo, JP',
  'Sydney, AU',
  'Singapore, SG'
];

function generateRandomIP() {
  return Array.from({ length: 4 }, () => Math.floor(Math.random() * 256)).join('.');
}

function generateRandomPort() {
  return Math.floor(Math.random() * 65535);
}

function generateRandomLocation() {
  return LOCATIONS[Math.floor(Math.random() * LOCATIONS.length)];
}

export function generateNetworkMetrics(): NetworkMetrics {
  const baseTraffic = Math.random() * 1000;
  const baseLatency = 50 + Math.random() * 100;
  
  return {
    timestamp: Date.now(),
    incomingTraffic: baseTraffic + Math.random() * 200,
    outgoingTraffic: baseTraffic * 0.8 + Math.random() * 150,
    activeConnections: Math.floor(Math.random() * 1000),
    averageLatency: baseLatency,
    packetLoss: Math.random() * 2,
    topSourceIPs: Array.from({ length: 5 }, () => ({
      ip: generateRandomIP(),
      count: Math.floor(Math.random() * 1000),
      location: generateRandomLocation(),
      latency: baseLatency + (Math.random() - 0.5) * 50
    })),
    topDestIPs: Array.from({ length: 5 }, () => ({
      ip: generateRandomIP(),
      count: Math.floor(Math.random() * 1000),
      location: generateRandomLocation(),
      latency: baseLatency + (Math.random() - 0.5) * 50
    })),
    protocols: {
      tcp: Math.random() * 800,
      udp: Math.random() * 200
    },
    portTraffic: Array.from({ length: 5 }, () => ({
      port: generateRandomPort(),
      bytes: Math.floor(Math.random() * 100000)
    }))
  };
}