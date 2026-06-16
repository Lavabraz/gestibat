import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface Agent {
  id_agent: number;
  nom_complet: string;
  email: string;
  statut: string;
  date_embauche: string;
  role: string;
  telephone?: string;
}

export default function AgentsList() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchAgents();
  }, [filter]);

  const fetchAgents = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      let url = API_URL + '/users/agents/';
      if (filter) {
        url += '?statut=' + encodeURIComponent(filter);
      }
      const response = await axios.get(url, {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      });
      setAgents(response.data.results || []);
    } catch (err) {
      console.error('Failed to fetch agents:', err);
      setError('Echec du chargement des agents');
    } finally {
      setIsLoading(false);
    }
  };

  const getStatutColor = (statut: string) => {
    const normalized = statut.toLowerCase().replace(/s/g, '');
    if (normalized === 'actif') return 'bg-green-100 text-green-800';
    if (normalized === 'inactif') return 'bg-red-100 text-red-800';
    if (normalized === 'vacataire') return 'bg-yellow-100 text-yellow-800';
    if (normalized === 'remplacant') return 'bg-blue-100 text-blue-800';
    return 'bg-slate-100 text-slate-800';
  };

  const getRoleColor = (role: string) => {
    const normalized = role.toLowerCase().replace(/s/g, '');
    if (normalized === 'admin' || normalized === 'administrateur') return 'bg-purple-100 text-purple-800';
    if (normalized === 'superadmin') return 'bg-red-100 text-red-800';
    if (normalized === 'editeur' || normalized === 'editor') return 'bg-blue-100 text-blue-800';
    return 'bg-slate-100 text-slate-800';
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold text-primary mb-6">Liste des agents</h1>
        <div className="animate-pulse space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-12 bg-slate-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-100 text-red-800 p-4 rounded">
          {error}
          <button
            onClick={fetchAgents}
            className="ml-4 bg-red-500 text-white px-4 py-1 rounded"
          >
            Reessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-primary">Liste des agents</h1>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-4 py-2 border rounded"
        >
          <option value="">Tous les statuts</option>
          <option value="Actif">Actif</option>
          <option value="Inactif">Inactif</option>
          <option value="Vacataire">Vacataire</option>
          <option value="Remplacant">Remplaçant</option>
        </select>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Nom
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Rôle
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Statut
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Téléphone
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Date embauche
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {agents.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-4 text-center text-slate-500">
                  Aucun agent trouvé
                </td>
              </tr>
            ) : (
              agents.map((agent) => {
                const statutClass = getStatutColor(agent.statut);
                const roleClass = getRoleColor(agent.role);
                return (
                  <tr key={agent.id_agent} className="hover:bg-slate-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-slate-900">
                        {agent.nom_complet}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-slate-600">{agent.email}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={"px-2 py-1 rounded-full text-xs font-medium " + roleClass}>
                        {agent.role}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={"px-2 py-1 rounded-full text-xs font-medium " + statutClass}>
                        {agent.statut}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {agent.telephone || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                      {new Date(agent.date_embauche).toLocaleDateString()}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}