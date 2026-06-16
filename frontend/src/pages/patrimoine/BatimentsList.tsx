import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import SkeletonLoader from '../../components/dashboard/SkeletonLoader';
import { Building, BuildingListResponse } from '../../types/patrimoine';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const statusColors = {
  active: 'bg-green-500/10 text-green-600',
  inactive: 'bg-slate-500/10 text-slate-600',
  maintenance: 'bg-orange-500/10 text-orange-600',
};

export default function BatimentsList() {
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchParams, setSearchParams] = useSearchParams();
  const [pagination, setPagination] = useState({
    page: 1,
    perPage: 10,
    total: 0,
    totalPages: 0,
  });

  const search = searchParams.get('search') || '';
  const statusFilter = searchParams.get('status') as Building['status'] | '';
  const cityFilter = searchParams.get('city') || '';

  useEffect(() => {
    fetchBuildings();
  }, [search, statusFilter, cityFilter, pagination.page]);

  const fetchBuildings = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const params: Record<string, any> = {
        page: pagination.page,
        per_page: pagination.perPage,
      };

      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;
      if (cityFilter) params.city = cityFilter;

      const response = await axios.get(API_URL + '/patrimoine/batiments/', {
        headers: {
          Authorization: 'Bearer ' + token,
        },
        params,
      });

      const data: BuildingListResponse = response.data;
      setBuildings(data.data);
      setPagination(data.pagination);
    } catch (err) {
      console.error('Failed to fetch buildings:', err);
      setError('Echec du chargement des batiments');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPagination({ ...pagination, page: 1 });
  };

  const handleStatusChange = (status: Building['status'] | '') => {
    setSearchParams({
      ...Object.fromEntries(searchParams),
      status: status || undefined,
    });
    setPagination({ ...pagination, page: 1 });
  };

  const handlePageChange = (page: number) => {
    setPagination({ ...pagination, page });
  };

  if (isLoading && pagination.page === 1) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-primary">Gestion du Patrimoine</h1>
        <SkeletonLoader type="list" count={5} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-alert-red/10 text-alert-red p-4 rounded-card">
        {error}
        <button
          onClick={fetchBuildings}
          className="ml-4 bg-alert-red text-white px-4 py-1 rounded-input text-sm"
        >
          Reessayer
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-primary">Gestion du Patrimoine</h1>
        <Link
          to="/patrimoine/batiments/new"
          className="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-input transition-colors"
        >
          + Ajouter un batiment
        </Link>
      </div>

      <div className="bg-card-bg rounded-card p-4 shadow-sm">
        <form onSubmit={handleSearch} className="flex flex-wrap gap-4 items-end">
          <div className="flex-1 min-w-64">
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Recherche
            </label>
            <input
              type="search"
              value={search}
              onChange={(e) => setSearchParams({
                ...Object.fromEntries(searchParams),
                search: e.target.value || undefined,
              })}
              placeholder="Nom, adresse, ville..."
              className="w-full px-4 py-2 border border-slate-300 rounded-input focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div className="min-w-48">
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Statut
            </label>
            <select
              value={statusFilter}
              onChange={(e) => handleStatusChange(e.target.value as Building['status'] | '')}
              className="w-full px-4 py-2 border border-slate-300 rounded-input focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Tous les statuts</option>
              <option value="active">Actif</option>
              <option value="inactive">Inactif</option>
              <option value="maintenance">En maintenance</option>
            </select>
          </div>

          <div className="min-w-48">
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Ville
            </label>
            <input
              type="text"
              value={cityFilter}
              onChange={(e) => setSearchParams({
                ...Object.fromEntries(searchParams),
                city: e.target.value || undefined,
              })}
              placeholder="Filtrer par ville"
              className="w-full px-4 py-2 border border-slate-300 rounded-input focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <button
            type="submit"
            className="bg-primary hover:bg-primary-dark text-white px-6 py-2 rounded-input transition-colors"
          >
            Filtrer
          </button>
        </form>
      </div>

      {buildings.length === 0 ? (
        <div className="bg-card-bg rounded-card p-8 text-center text-slate-500">
          <p>Aucun batiment trouve</p>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="bg-card-bg rounded-card p-6 shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-200">
                    <th className="text-left py-3 px-4 font-semibold text-slate-700">
                      Batiment
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-slate-700">
                      Adresse
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-slate-700">
                      Ville
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-slate-700">
                      Statut
                    </th>
                    <th className="text-right py-3 px-4 font-semibold text-slate-700">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {buildings.map((building) => (
                    <tr
                      key={building.id}
                      className="border-b border-slate-100 hover:bg-slate-50 transition-colors"
                    >
                      <td className="py-4 px-4">
                        <Link
                          to={building.id}
                          className="font-medium text-primary hover:text-primary-dark"
                        >
                          {building.name}
                        </Link>
                      </td>
                      <td className="py-4 px-4 text-slate-600">
                        {building.address}
                      </td>
                      <td className="py-4 px-4 text-slate-600">
                        {building.postalCode} {building.city}
                      </td>
                      <td className="py-4 px-4">
                        <span
                          className={'px-2 py-1 rounded-full text-xs font-medium ' +
                            statusColors[building.status]}
                        >
                          {building.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-right">
                        <Link
                          to={building.id}
                          className="text-primary hover:text-primary-dark mr-2"
                        >
                          Voir
                        </Link>
                        <Link
                          to={building.id + '/edit'}
                          className="text-slate-600 hover:text-primary mr-2"
                        >
                          Editer
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {pagination.totalPages > 1 && (
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-500">
                Page {pagination.page} sur {pagination.totalPages} ({pagination.total} resultats)
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => handlePageChange(Math.max(1, pagination.page - 1))}
                  disabled={pagination.page <= 1}
                  className="px-4 py-2 bg-card-bg rounded-input text-slate-700 hover:bg-slate-200 disabled:opacity-50"
                >
                  Precedent
                </button>
                <button
                  onClick={() => handlePageChange(Math.min(pagination.totalPages, pagination.page + 1))}
                  disabled={pagination.page >= pagination.totalPages}
                  className="px-4 py-2 bg-card-bg rounded-input text-slate-700 hover:bg-slate-200 disabled:opacity-50"
                >
                  Suivant
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
