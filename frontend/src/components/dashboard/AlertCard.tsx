import { Alert } from '../../types/dashboard';

interface AlertCardProps {
  alert: Alert;
}

const alertColors = {
  warning: 'bg-alert-orange/10 border-alert-orange text-alert-orange',
  error: 'bg-alert-red/10 border-alert-red text-alert-red',
  success: 'bg-alert-green/10 border-alert-green text-alert-green',
  info: 'bg-blue-500/10 border-blue-500 text-blue-500',
};

const alertIcons = {
  warning: '⚠️',
  error: '❌',
  success: '✅',
  info: 'ℹ️',
};

export default function AlertCard({ alert }: AlertCardProps) {
  const colorClass = alertColors[alert.type] || alertColors.info;

  return (
    <div className={'border-l-4 p-4 rounded-r-card ' + colorClass}>
      <div className="flex items-start gap-3">
        <span className="text-xl">{alertIcons[alert.type]}</span>
        <div className="flex-1">
          <h4 className="font-semibold">{alert.title}</h4>
          <p className="text-sm mt-1">{alert.message}</p>
          <p className="text-xs text-slate-500 mt-2">
            {new Date(alert.timestamp).toLocaleString('fr-FR')}
          </p>
        </div>
      </div>
    </div>
  );
}
