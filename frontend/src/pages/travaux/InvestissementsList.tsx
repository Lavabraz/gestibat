import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface Investissement {
  id_investissement: number;
  titre_projet: string;
  description: string;
  montant_previsionnel: number;
  annee_programmation: number;
  statut: string;
  date_creation: string;
  batiment?: {
    id_batiment: number;
    nom_batiment: string;
  };
  service_pilote?: {
    id_service: number;
    nom_service: string;
  };
}

export default function InvestissementsList() {
  const [investissements, setInvestissements] = useState<Investissement[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchInvestissements();
  }, [filter]);

  const fetchInvestissements = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      let url = API_URL + '/travaux/investissements/';
      if (filter) {
        url += '?statut=' + encodeURIComponent(filter);
      }
      const response = await axios.get(url, {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      });
      setInvestissements(response.data.results || []);
    } catch (err) {
      console.error('Failed to fetch investissements:', err);
      setError('Echec du chargement des investissements');
    } finally {
      setIsLoading(false);
    }
  };

  const getStatutColor = (statut: string) => {
    const normalized = statut.toLowerCase().replace(/s/g, '');
    if (normalized === 'valide' || normalized === 'validé') return 'bg-green-100 text-green-800';
    if (normalized === 'engage' || normalized === 'engagé') return 'bg-blue-100 text-blue-800';
    if (normalized === 'enattente' || normalized === 'enattente') return 'bg-yellow-100 text-yellow-800';
    if (normalized === 'annule' || normalized === 'annulé') return 'bg-red-100 text-red-800';
    return 'bg-slate-100 text-slate-800';
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold text-primary mb-6">Liste des investissements</h1>
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
            onClick={fetchInvestissements}
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
        <h1 className="text-2xl font-bold text-primary">Liste des investissements</h1>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-4 py-2 border rounded"
        >
          <option value="">Tous les statuts</option>
          <option value="Validé">Validé</option>
          <option value="Engagé">Engagé</option>
          <option value="En attente">En attente</option>
          <option value="Annulé">Annulé</option>
        </select>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Titre du projet
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Bâtiment
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Montant
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Année
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Statut
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                Service pilote
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {investissements.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-4 text-center text-slate-500">
                  Aucun investissement trouvé
                </td>
              </tr>
            ) : (
              investissements.map((inv) => {
                const statutClass = getStatutColor(inv.statut);
                return (
                  <tr key={inv.id_investissement} className="hover:bg-slate-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-slate-900">
                        {inv.titre_projet}
                      </div>
                      <div className="text-xs text-slate-500 truncate max-w-xs">
                        {inv.description}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {inv.batiment?.nom_batiment || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {inv.montant_previsionnel.toLocaleString()} €
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {inv.annee_programmation}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={"px-2 py-1 rounded-full text-xs font-medium " + statutClass}>
                        {inv.statut}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {inv.service_pilote?.nom_service || 'N/A'}
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