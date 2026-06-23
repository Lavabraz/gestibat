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
      padding: '1.5rem',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      cursor: 'pointer',
      transition: 'box-shadow 0.2s',
    }}>
      <div style={{ display: 'flex', items: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
        <p style={{ fontSize: '0.875rem', color: '#64748b' }}>{kpi.label}</p>
        {kpi.icon && <span style={{ fontSize: '1.5rem' }}>{kpi.icon}</span>}
      </div>
      <div style={{ display: 'flex', items: 'baseline', gap: '0.5rem' }}>
        <h3 style={{ fontSize: '1.875rem', fontWeight: 'bold', color: '#007179' }}>{kpi.value}</h3>
        {kpi.trend && (
          <span style={{ fontSize: '0.875rem', fontWeight: '500', color: getTrendColor() }}>
            {getTrendIcon()} {kpi.change}%
          </span>
        )}
      </div>
    </div>
  );
}