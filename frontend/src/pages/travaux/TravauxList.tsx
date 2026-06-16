import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface Travaux {
  id_travaux: number;
  titre_travaux: string;
  statut: string;
  date_demande: string;
  batiment?: {
    id_batiment: number;
    nom_batiment: string;
  };
  priorite: string;
  type_travaux: string;
}

export default function TravauxList() {
  const [travaux, setTravaux] = useState<Travaux[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchTravaux();
  }, [filter]);

  const fetchTravaux = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      let url = API_URL + '/travaux/travaux/';
      if (filter) {
        url += '?statut=' + encodeURIComponent(filter);
      }
      const response = await axios.get(url, {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      });
      setTravaux(response.data.results || []);
    } catch (err) {
      console.error('Failed to fetch travaux:', err);
      setError('Echec du chargement des travaux');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDetail = (id: number) => {
    navigate('/travaux/' + id);
  };

  const getStatutColor = (statut: string) => {
    const normalized = statut.toLowerCase().replace(/s/g, '');
    if (normalized === 'encours') return 'bg-blue-100 text-blue-800';
    if (normalized === 'terminé' || normalized === 'termine') return 'bg-green-100 text-green-800';
    if (normalized === 'proposé' || normalized === 'propose') return 'bg-yellow-100 text-yellow-800';
    if (normalized === 'validé' || normalized === 'valide') return 'bg-purple-100 text-purple-800';
    return 'bg-slate-100 text-slate-800';
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold text-primary mb-6">Liste des travaux</h1>
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
            onClick={fetchTravaux}
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
        <h1 className="text-2xl font-bold text-primary">Liste des travaux</h1>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-4 py-2 border rounded"
        >
          <option value="">Tous les statuts</option>
          <option value="En cours">En cours</option>
          <option value="Terminé">Terminé</option>
          <option value="Proposé">Proposé</option>
          <option value="Validé">Validé</option>
          <option value="Annulé">Annulé</option>
        </select>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Titre
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Bâtiment
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Statut
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Priorité
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Date
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {travaux.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-4 text-center text-slate-500">
                  Aucun travail trouvé
                </td>
              </tr>
            ) : (
              travaux.map((travail) => {
                const statutClass = getStatutColor(travail.statut);
                return (
                  <tr key={travail.id_travaux} className="hover:bg-slate-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-slate-900">
                        {travail.titre_travaux}
                      </div>
                      <div className="text-xs text-slate-500">
                        {travail.type_travaux}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {travail.batiment?.nom_batiment || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={"px-2 py-1 rounded-full text-xs font-medium " + statutClass}>
                        {travail.statut}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 py-1 bg-slate-100 text-slate-800 rounded-full text-xs font-medium">
                        {travail.priorite}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                      {new Date(travail.date_demande).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleDetail(travail.id_travaux)}
                        className="text-primary hover:text-primary-dark"
                      >
                        Voir
                      </button>
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