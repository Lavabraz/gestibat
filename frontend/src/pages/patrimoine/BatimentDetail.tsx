import { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import SkeletonLoader from '../../components/dashboard/SkeletonLoader';
import { Building, BuildingDetailResponse } from '../../types/patrimoine';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const statusColors = {
  active: 'bg-green-500/10 text-green-600 border-green-500',
  inactive: 'bg-slate-500/10 text-slate-600 border-slate-500',
  maintenance: 'bg-orange-500/10 text-orange-600 border-orange-500',
};

export default function BatimentDetail() {
  const { id } = useParams<{ id: string }>();
  const [building, setBuilding] = useState<Building | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      fetchBuildingDetail();
    }
  }, [id]);

  const fetchBuildingDetail = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(API_URL + '/patrimoine/batiments/' + id, {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      });

      const data: BuildingDetailResponse = response.data;
      setBuilding(data.data);
    } catch (err) {
      console.error('Failed to fetch building detail:', err);
      setError('Batiment introuvable');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id) return;
    if (!window.confirm('Etes-vous sur de vouloir supprimer ce batiment ?')) return;

    try {
      const token = localStorage.getItem('token');
      await axios.delete(API_URL + '/patrimoine/batiments/' + id, {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      });
      navigate('/patrimoine/batiments');
    } catch (err) {
      console.error('Failed to delete building:', err);
      setError('Echec de la suppression');
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-primary">Details du batiment</h1>
          <SkeletonLoader type="text" className="w-48 h-10" />
        </div>
        <SkeletonLoader type="card" count={3} className="space-y-4" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-alert-red/10 text-alert-red p-4 rounded-card">
        {error}
        <Link
          to="/patrimoine/batiments"
          className="ml-4 bg-alert-red text-white px-4 py-1 rounded-input text-sm"
        >
          Retour a la liste
        </Link>
      </div>
    );
  }

  if (!building) {
    return (
      <div className="bg-card-bg rounded-card p-8 text-center text-slate-500">
        <p>Batiment introuvable</p>
        <Link
          to="/patrimoine/batiments"
          className="mt-4 inline-block bg-primary text-white px-4 py-2 rounded-input"
        >
          Retour a la liste
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-primary">{building.name}</h1>
        <div className="flex gap-2">
          <Link
            to={id + '/edit'}
            className="bg-slate-200 hover:bg-slate-300 text-slate-800 px-4 py-2 rounded-input transition-colors"
          >
            Editer
          </Link>
          <button
            onClick={handleDelete}
            className="bg-alert-red hover:bg-red-600 text-white px-4 py-2 rounded-input transition-colors"
          >
            Supprimer
          </button>
        </div>
      </div>

      <div className="bg-card-bg rounded-card p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-800 mb-4">
          Informations generales
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-slate-500 mb-1">Adresse</p>
            <p className="font-medium">
              {building.address}, {building.postalCode} {building.city}
            </p>
          </div>
          <div>
            <p className="text-sm text-slate-500 mb-1">Statut</p>
            <span
              className={'px-3 py-1 rounded-full text-sm font-medium border ' +
                statusColors[building.status]}
            >
              {building.status}
            </span>
          </div>
          <div>
            <p className="text-sm text-slate-500 mb-1">Annee de construction</p>
            <p>{building.yearBuilt || 'Non specifiee'}</p>
          </div>
          <div>
            <p className="text-sm text-slate-500 mb-1">Surface</p>
            <p>{building.surfaceArea ? building.surfaceArea + ' m2' : 'Non specifiee'}</p>
          </div>
        </div>
        {building.description && (
          <div className="mt-4 pt-4 border-t border-slate-200">
            <p className="text-sm text-slate-500 mb-1">Description</p>
            <p>{building.description}</p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-card-bg rounded-card p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Documents
          </h2>
          {building.documents && building.documents.length > 0 ? (
            <ul className="space-y-2">
              {building.documents.map((doc, index) => (
                <li key={index} className="text-sm">
                  <a
                    href={doc}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:text-primary-dark"
                  >
                    Document {index + 1}
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-500 text-sm">Aucun document</p>
          )}
        </div>

        <div className="bg-card-bg rounded-card p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Images
          </h2>
          {building.images && building.images.length > 0 ? (
            <div className="grid grid-cols-2 gap-2">
              {building.images.map((img, index) => (
                <img
                  key={index}
                  src={img}
                  alt={building.name + ' - ' + index}
                  className="w-full h-24 object-cover rounded"
                />
              ))}
            </div>
          ) : (
            <p className="text-slate-500 text-sm">Aucune image</p>
          )}
        </div>
      </div>

      <Link
        to="/patrimoine/batiments"
        className="inline-block bg-slate-200 hover:bg-slate-300 text-slate-800 px-6 py-2 rounded-input transition-colors"
      >
        &larr; Retour a la liste
      </Link>
    </div>
  );
}
