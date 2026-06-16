export interface KpiData {
  label: string;
  value: number | string;
  icon?: string;
  trend?: 'up' | 'down' | 'stable';
  change?: number;
}

export interface Alert {
  id: string;
  type: 'warning' | 'error' | 'success' | 'info';
  title: string;
  message: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high';
}

export interface Activity {
  id: string;
  action: string;
  user: string;
  target: string;
  timestamp: string;
  status: 'completed' | 'pending' | 'failed';
}

export interface DashboardData {
  kpis: KpiData[];
  alerts: Alert[];
  recentActivities: Activity[];
  stats: {
    totalUsers: number;
    totalBuildings: number;
    totalAgents: number;
    pendingRequests: number;
  };
}

export interface DashboardResponse {
  data: DashboardData;
  lastUpdated: string;
}