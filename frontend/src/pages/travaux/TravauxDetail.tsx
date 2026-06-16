import { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface Travaux {
  id_travaux: number;
  titre_travaux: string;
  description: string;
  statut: string;
  date_demande: string;
  date_fin_previsionnelle: string;
  date_fin_reelle: string;
  priorite: string;
  type_travaux: string;
  cout_estime: number;
  domaine_metier: string;
  batiment?: {
    id_batiment: number;
    nom_batiment: string;
    code_patrimoine: string;
  };
  service_demandeur?: {
    id_service: number;
    nom_service: string;
  };
  responsable_interne?: {
    id_agent: number;
    nom_complet: string;
  };
  investissement?: {
    id_investissement: number;
    titre_projet: string;
  };
}

export default function TravauxDetail() {
  const { id } = useParams<{ id: string }>();
  const [travail, setTravail] = useState<Travaux | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      fetchTravail(parseInt(id));
    }
  }, [id]);

  const fetchTravail = async (travailId: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(API_URL + '/travaux/travaux/' + travailId, {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      });
      setTravail(response.data);
    } catch (err) {
      console.error('Failed to fetch travail:', err);
      setError('Echec du chargement du travail');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCloturer = async () => {
    if (!id) return;
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        API_URL + '/travaux/travaux/' + id + '/cloturer/',
        {},
        {
          headers: {
            Authorization: 'Bearer ' + token,
          },
        }
      );
      fetchTravail(parseInt(id));
    } catch (err) {
      console.error('Failed to cloturer travail:', err);
      setError('Echec de la clôture du travail');
    }
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold text-primary mb-6">Détail du travail</h1>
        <div className="animate-pulse">
          <div className="h-8 bg-slate-200 rounded mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="h-6 bg-slate-200 rounded"></div>
            <div className="h-6 bg-slate-200 rounded"></div>
            <div className="h-6 bg-slate-200 rounded"></div>
            <div className="h-6 bg-slate-200 rounded"></div>
          </div>
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
            onClick={() => navigate('/travaux')}
            className="ml-4 bg-red-500 text-white px-4 py-1 rounded"
          >
            Retour
          </button>
        </div>
      </div>
    );
  }

  if (!travail) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold text-primary mb-6">Travail non trouvé</h1>
        <button
          onClick={() => navigate('/travaux')}
          className="bg-primary text-white px-4 py-2 rounded"
        >
          Retour à la liste
        </button>
      </div>
    );
  }

  const getStatutColor = (statut: string) => {
    const normalized = statut.toLowerCase().replace(/s/g, '');
    if (normalized === 'encours') return 'bg-blue-100 text-blue-800';
    if (normalized === 'terminé' || normalized === 'termine') return 'bg-green-100 text-green-800';
    if (normalized === 'proposé' || normalized === 'propose') return 'bg-yellow-100 text-yellow-800';
    if (normalized === 'validé' || normalized === 'valide') return 'bg-purple-100 text-purple-800';
    return 'bg-slate-100 text-slate-800';
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-primary">Détail du travail</h1>
        <button
          onClick={() => navigate('/travaux')}
          className="bg-slate-200 text-slate-800 px-4 py-2 rounded hover:bg-slate-300"
        >
          Retour
        </button>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-slate-900">{travail.titre_travaux}</h2>
          <span className={"inline-block mt-2 px-3 py-1 rounded-full text-sm font-medium " + getStatutColor(travail.statut)}>
            {travail.statut}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-2">
              Informations générales
            </h3>
            <div className="space-y-2">
              <div>
                <span className="text-slate-500">Type: </span>
                <span className="text-slate-900">{travail.type_travaux}</span>
              </div>
              <div>
                <span className="text-slate-500">Priorité: </span>
                <span className="text-slate-900">{travail.priorite}</span>
              </div>
              <div>
                <span className="text-slate-500">Domaine: </span>
                <span className="text-slate-900">{travail.domaine_metier}</span>
              </div>
              <div>
                <span className="text-slate-500">Coût estimé: </span>
                <span className="text-slate-900">{travail.cout_estime} €</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-2">
              Bâtiment
            </h3>
            <div className="space-y-2">
              <div>
                <span className="text-slate-500">Nom: </span>
                <span className="text-slate-900">{travail.batiment?.nom_batiment || 'N/A'}</span>
              </div>
              <div>
                <span className="text-slate-500">Code patrimoine: </span>
                <span className="text-slate-900">{travail.batiment?.code_patrimoine || 'N/A'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-2">
            Description
          </h3>
          <p className="text-slate-700 bg-slate-50 p-4 rounded">{travail.description || 'Aucune description'}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-2">
              Dates
            </h3>
            <div className="space-y-2">
              <div>
                <span className="text-slate-500">Demande: </span>
                <span className="text-slate-900">{new Date(travail.date_demande).toLocaleDateString()}</span>
              </div>
              <div>
                <span className="text-slate-500">Fin prévisionnelle: </span>
                <span className="text-slate-900">
                  {travail.date_fin_previsionnelle ? new Date(travail.date_fin_previsionnelle).toLocaleDateString() : 'N/A'}
                </span>
              </div>
              <div>
                <span className="text-slate-500">Fin réelle: </span>
                <span className="text-slate-900">
                  {travail.date_fin_reelle ? new Date(travail.date_fin_reelle).toLocaleDateString() : 'N/A'}
                </span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-2">
              Responsables
            </h3>
            <div className="space-y-2">
              <div>
                <span className="text-slate-500">Service demandeur: </span>
                <span className="text-slate-900">{travail.service_demandeur?.nom_service || 'N/A'}</span>
              </div>
              <div>
                <span className="text-slate-500">Responsable: </span>
                <span className="text-slate-900">{travail.responsable_interne?.nom_complet || 'N/A'}</span>
              </div>
              {travail.investissement && (
                <div>
                  <span className="text-slate-500">Investissement: </span>
                  <span className="text-slate-900">{travail.investissement.titre_projet}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {travail.statut.toLowerCase().replace(/s/g, '') !== 'terminé' && (
          <div className="flex justify-end">
            <button
              onClick={handleCloturer}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              Clôturer ce travail
            </button>
          </div>
        )}
      </div>
    </div>
  );
}