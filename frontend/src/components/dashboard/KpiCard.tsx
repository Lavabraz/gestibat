import { KpiData } from '../../types/dashboard';

interface KpiCardProps {
  kpi: KpiData;
}

export default function KpiCard({ kpi }: KpiCardProps) {
  const getTrendColor = () => {
    switch (kpi.trend) {
      case 'up': return '#0de218';
      case 'down': return '#ff0004';
      default: return '#64748b';
    }
  };

  const getTrendIcon = () => {
    switch (kpi.trend) {
      case 'up': return '↑';
      case 'down': return '↓';
      default: return '→';
    }
  };

  return (
    <div style={{
      backgroundColor: '#e2e2e2',
      borderRadius: '20px',
      padding: '24px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      cursor: 'pointer',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <p style={{ fontSize: '14px', color: '#64748b', margin: 0 }}>{kpi.label}</p>
        {kpi.icon && <span style={{ fontSize: '24px' }}>{kpi.icon}</span>}
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
        <h3 style={{ fontSize: '30px', fontWeight: 'bold', color: '#007179', margin: 0 }}>{kpi.value}</h3>
        {kpi.trend && (
          <span style={{ fontSize: '14px', fontWeight: '500', color: getTrendColor() }}>
            {getTrendIcon()} {kpi.change}%
          </span>
        )}
      </div>
    </div>
  );
}