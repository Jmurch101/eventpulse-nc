import React, { useEffect, useMemo, useRef } from 'react';
import * as d3 from 'd3';

interface BubbleClusterProps {
  countsByType: Record<string, number>;
  onSelect: (eventType: string) => void;
}

const colors: Record<string, string> = {
  academic: '#3b82f6',
  government: '#10b981',
  community: '#8b5cf6',
  tech: '#f59e0b',
  holiday: '#ef4444',
};

const BubbleCluster: React.FC<BubbleClusterProps> = ({ countsByType, onSelect }) => {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const data = useMemo(() => Object.entries(countsByType).map(([type, value]) => ({ type, value })), [countsByType]);

  useEffect(() => {
    if (!svgRef.current) return;
    const width = 360, height = 260;
    const root = d3.hierarchy({ children: data } as any).sum((d: any) => d.value);
    const pack = d3.pack<any>().size([width, height]).padding(6);
    const nodes = pack(root).leaves();

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();
    const g = svg.attr('viewBox', `0 0 ${width} ${height}`).append('g');

    const node = g.selectAll('g').data(nodes).enter().append('g')
      .attr('transform', (d) => `translate(${d.x},${d.y})`)
      .style('cursor', 'pointer')
      .on('click', (_, d: any) => onSelect(d.data.type));

    node.append('circle')
      .attr('r', d => d.r)
      .attr('fill', (d: any) => colors[d.data.type] || '#64748b')
      .attr('fill-opacity', 0.8);

    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('font-size', '10px')
      .attr('fill', '#fff')
      .text((d: any) => d.data.type);
  }, [data, onSelect]);

  return (
    <div className="bg-white rounded-lg shadow p-3">
      <div className="text-sm font-semibold text-gray-800 mb-2">Event Types</div>
      <svg ref={svgRef} width="100%" height="260" />
    </div>
  );
};

export default BubbleCluster;

