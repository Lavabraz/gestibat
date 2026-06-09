import { KpiData } from '../../types/dashboard';

interface KpiCardProps {
  kpi: KpiData;
}

export default function KpiCard({ kpi }: KpiCardProps) {
  const getTrendColor = () => {
    switch (kpi.trend) {
      case 'up':
        return 'text-alert-green';
      case 'down':
        return 'text-alert-red';
      default:
        return 'text-slate-600';
    }
  };

  const getTrendIcon = () => {
    switch (kpi.trend) {
      case 'up':
        return '↑';
      case 'down':
        return '↓';
      default:
        return '→';
    }
  };

  return (
    <div className="bg-card-bg rounded-card p-6 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm text-slate-600">{kpi.label}</p>
        {kpi.icon && <span className="text-2xl">{kpi.icon}</span>}
      </div>
      <div className="flex items-baseline gap-2">
        <h3 className="text-3xl font-bold text-primary">{kpi.value}</h3>
        {kpi.trend && (
          <span className={'text-sm font-medium ' + getTrendColor()}>
            {getTrendIcon()} {kpi.change}%
          </span>
        )}
      </div>
    </div>
  );
}
