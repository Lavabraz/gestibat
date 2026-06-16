import { useState, useEffect } from 'react';
import axios from 'axios';
import KpiCard from '../components/dashboard/KpiCard';
import AlertCard from '../components/dashboard/AlertCard';
import ActivityCard from '../components/dashboard/ActivityCard';
import SkeletonLoader from '../components/dashboard/SkeletonLoader';
import { KpiData, Alert, Activity } from '../types/dashboard';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export default function Dashboard() {
  const [kpis, setKpis] = useState<KpiData[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(API_URL + '/dashboard/', {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      });

      const data = response.data;
      setKpis(data.kpis || []);
      setAlerts(data.alerts || []);
      setActivities(data.recentActivities || []);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Echec du chargement des donnees');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-primary">Tableau de bord</h1>
        <SkeletonLoader type="card" count={4} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h2 className="text-lg font-semibold text-slate-800 mb-4">Alertes</h2>
            <SkeletonLoader type="list" count={3} />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-slate-800 mb-4">Activite recente</h2>
            <SkeletonLoader type="list" count={5} />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-alert-red/10 text-alert-red p-4 rounded-card">
        {error}
        <button
          onClick={fetchDashboardData}
          className="ml-4 bg-alert-red text-white px-4 py-1 rounded-input text-sm"
        >
          Reessayer
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-primary">Tableau de bord</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi) => (
          <KpiCard key={kpi.label} kpi={kpi} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card-bg rounded-card p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Alertes recentes
          </h2>
          {alerts.length === 0 ? (
            <p className="text-slate-500 text-sm">Aucune alerte</p>
          ) : (
            <div className="space-y-3">
              {alerts.slice(0, 3).map((alert) => (
                <AlertCard key={alert.id} alert={alert} />
              ))}
            </div>
          )}
        </div>

        <div className="bg-card-bg rounded-card p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Activite recente
          </h2>
          {activities.length === 0 ? (
            <p className="text-slate-500 text-sm">Aucune activite</p>
          ) : (
            <div className="space-y-3">
              {activities.slice(0, 5).map((activity) => (
                <ActivityCard key={activity.id} activity={activity} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
