import React, { useEffect, useRef } from 'react';
import { NetworkMetrics } from '../types';
import { Network } from 'vis-network';
import { DataSet } from 'vis-data';

interface Props {
  data: NetworkMetrics;
}

export function NetworkTopology({ data }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);

  useEffect(() => {
    if (!containerRef.current || !data) return;

    // Create nodes for source and destination IPs
    const nodes = new DataSet<any>([]);
    const edges = new DataSet<any>([]);

    // Add router node (center of the network)
    nodes.add({
      id: 'router',
      label: 'Router',
      shape: 'diamond',
      size: 30,
      color: {
        background: '#6366f1',
        border: '#4f46e5',
        highlight: {
          background: '#818cf8',
          border: '#6366f1'
        }
      },
      font: { color: '#ffffff' }
    });

    // Add source IP nodes
    data.topSourceIPs.forEach((ip, index) => {
      const id = `src_${ip.ip}`;
      nodes.add({
        id,
        label: `${ip.ip}\n${ip.count} packets`,
        shape: 'dot',
        size: 20 + (ip.count / 100),
        color: {
          background: '#10b981',
          border: '#059669',
          highlight: {
            background: '#34d399',
            border: '#10b981'
          }
        },
        title: `Source IP: ${ip.ip}<br>Packets: ${ip.count}<br>Location: ${ip.location || 'Unknown'}`
      });

      // Add edge from source to router
      edges.add({
        from: id,
        to: 'router',
        arrows: 'to',
        width: 1 + (ip.count / 200),
        color: { color: '#10b981', highlight: '#34d399' },
        title: `${Math.round(ip.count)} packets`
      });
    });

    // Add destination IP nodes
    data.topDestIPs.forEach((ip, index) => {
      const id = `dst_${ip.ip}`;
      nodes.add({
        id,
        label: `${ip.ip}\n${ip.count} packets`,
        shape: 'dot',
        size: 20 + (ip.count / 100),
        color: {
          background: '#f59e0b',
          border: '#d97706',
          highlight: {
            background: '#fbbf24',
            border: '#f59e0b'
          }
        },
        title: `Destination IP: ${ip.ip}<br>Packets: ${ip.count}<br>Location: ${ip.location || 'Unknown'}`
      });

      // Add edge from router to destination
      edges.add({
        from: 'router',
        to: id,
        arrows: 'to',
        width: 1 + (ip.count / 200),
        color: { color: '#f59e0b', highlight: '#fbbf24' },
        title: `${Math.round(ip.count)} packets`
      });
    });

    // Create network
    const network = new Network(
      containerRef.current,
      { nodes, edges },
      {
        physics: {
          stabilization: true,
          barnesHut: {
            gravitationalConstant: -5000,
            centralGravity: 0.3,
            springLength: 150,
            springConstant: 0.04,
            damping: 0.09
          }
        },
        interaction: {
          hover: true,
          tooltipDelay: 200
        },
        layout: {
          improvedLayout: true,
          hierarchical: {
            enabled: false
          }
        }
      }
    );

    networkRef.current = network;

    return () => {
      if (networkRef.current) {
        networkRef.current.destroy();
        networkRef.current = null;
      }
    };
  }, [data]);

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Network Topology</h2>
      <div ref={containerRef} className="h-[400px]" />
      <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 flex justify-between">
        <div className="flex items-center">
          <span className="inline-block w-3 h-3 rounded-full bg-green-500 mr-1"></span>
          <span>Source IPs</span>
        </div>
        <div className="flex items-center">
          <span className="inline-block w-3 h-3 rounded-full bg-indigo-500 mr-1"></span>
          <span>Router</span>
        </div>
        <div className="flex items-center">
          <span className="inline-block w-3 h-3 rounded-full bg-amber-500 mr-1"></span>
          <span>Destination IPs</span>
        </div>
      </div>
    </div>
  );
}
