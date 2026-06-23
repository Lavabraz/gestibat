import { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import SkeletonLoader from '../components/dashboard/SkeletonLoader';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface Contact {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  role: string;
  company?: string;
  address?: string;
  city?: string;
  postalCode?: string;
  type: 'entreprise' | 'artisan' | 'fournisseur' | 'autre';
}

const getTypeBadgeClass = (type: string) => {
  switch (type) {
    case 'entreprise': return 'bg-blue-100 text-blue-800';
    case 'artisan': return 'bg-orange-100 text-orange-800';
    case 'fournisseur': return 'bg-green-100 text-green-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

const getTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    entreprise: 'Entreprises',
    artisan: 'Artisans',
    fournisseur: 'Fournisseurs',
    autre: 'Autres',
  };
  return labels[type] || type;
};

export default function ContactsList() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterType, setFilterType] = useState<string | null>(null);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const typeFilter = searchParams.get('type');
    if (typeFilter) setFilterType(typeFilter);
    fetchContacts(typeFilter || null);
  }, [location.search]);

  const fetchContacts = async (typeFilter: string | null = null) => {
    setIsLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const params = typeFilter ? { type: typeFilter } : {};
      const response = await axios.get(API_URL + '/contacts/', {
        headers: { Authorization: 'Bearer ' + token },
        params,
      });
      setContacts(response.data || []);
    } catch (err) {
      console.error('Failed to fetch contacts:', err);
      setError('Echec du chargement des contacts');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (type: string | null) => {
    setFilterType(type);
    navigate(type ? '/contacts?type=' + type : '/contacts');
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-primary">Contacts</h1>
        <SkeletonLoader type="table" count={10} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-alert-red/10 text-alert-red p-4 rounded-card">
        {error}
        <button onClick={() => fetchContacts(filterType || null)} className="ml-4 bg-alert-red text-white px-4 py-1 rounded-input text-sm">
          Reessayer
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-primary">Contacts</h1>
        <div className="flex gap-2">
          <button onClick={() => handleFilterChange(null)} className={'px-4 py-2 rounded-input text-sm ' + (filterType === null ? 'bg-primary text-white' : 'bg-card-bg text-slate-700 hover:bg-slate-200')}>Tous</button>
          <button onClick={() => handleFilterChange('entreprise')} className={'px-4 py-2 rounded-input text-sm ' + (filterType === 'entreprise' ? 'bg-primary text-white' : 'bg-card-bg text-slate-700 hover:bg-slate-200')}>Entreprises</button>
          <button onClick={() => handleFilterChange('artisan')} className={'px-4 py-2 rounded-input text-sm ' + (filterType === 'artisan' ? 'bg-primary text-white' : 'bg-card-bg text-slate-700 hover:bg-slate-200')}>Artisans</button>
          <button onClick={() => handleFilterChange('fournisseur')} className={'px-4 py-2 rounded-input text-sm ' + (filterType === 'fournisseur' ? 'bg-primary text-white' : 'bg-card-bg text-slate-700 hover:bg-slate-200')}>Fournisseurs</button>
        </div>
      </div>

      {filterType && <div className="bg-slate-100 p-3 rounded-card text-sm text-slate-600">Filtre actif: {getTypeLabel(filterType)} ({contacts.length} resultats)</div>}

      <div className="bg-card-bg rounded-card shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-200">
            <tr>
              <th className="text-left p-4 font-semibold text-slate-700">Nom</th>
              <th className="text-left p-4 font-semibold text-slate-700">Email</th>
              <th className="text-left p-4 font-semibold text-slate-700">Telephone</th>
              <th className="text-left p-4 font-semibold text-slate-700">Type</th>
              <th className="text-left p-4 font-semibold text-slate-700">Role</th>
              <th className="text-left p-4 font-semibold text-slate-700">Entreprise</th>
            </tr>
          </thead>
          <tbody>
            {contacts.length === 0 ? (
              <tr><td colSpan={6} className="text-center p-8 text-slate-500">Aucun contact trouve</td></tr>
            ) : (
              contacts.map((contact) => (
                <tr key={contact.id} className="border-t border-slate-200 hover:bg-slate-50">
                  <td className="p-4"><div className="font-medium">{contact.lastName}</div><div className="text-sm text-slate-500">{contact.firstName}</div></td>
                  <td className="p-4 text-sm">{contact.email}</td>
                  <td className="p-4 text-sm">{contact.phone}</td>
                  <td className="p-4"><span className={"px-2 py-1 rounded-full text-xs " + getTypeBadgeClass(contact.type)}>{getTypeLabel(contact.type)}</span></td>
                  <td className="p-4 text-sm">{contact.role}</td>
                  <td className="p-4 text-sm">{contact.company || '-'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}