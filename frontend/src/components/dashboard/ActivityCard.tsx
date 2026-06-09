import { Activity } from '../../types/dashboard';

interface ActivityCardProps {
  activity: Activity;
}

const statusColors = {
  completed: 'bg-green-500/10 text-green-600',
  pending: 'bg-orange-500/10 text-orange-600',
  failed: 'bg-red-500/10 text-red-600',
};

export default function ActivityCard({ activity }: ActivityCardProps) {
  const colorClass = statusColors[activity.status] || statusColors.pending;

  return (
    <div className="flex items-center gap-4 p-3 bg-card-bg rounded-input hover:bg-slate-200 transition-colors">
      <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
        <span className="text-primary">👤</span>
      </div>
      <div className="flex-1">
        <p className="font-medium text-slate-800">
          {activity.user} <span className="text-slate-500">{activity.action}</span> {activity.target}
        </p>
        <p className="text-xs text-slate-400 mt-1">
          {new Date(activity.timestamp).toLocaleString('fr-FR')}
        </p>
      </div>
      <span className={'px-2 py-1 rounded-full text-xs font-medium ' + colorClass}>
        {activity.status}
      </span>
    </div>
  );
}
