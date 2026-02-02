'use client';

import React, { useEffect, useState } from 'react';
import { 
  Mail, 
  Phone, 
  MapPin, 
  Loader2, 
  AlertCircle, 
  ArrowUpDown, 
  User as UserIcon 
} from 'lucide-react';
import DashboardLayout from '../components/DashboardLayout';

// --- Types ---

interface UserAddress {
  id: string;
  street: string;
  city: string;
  state: string | null;
  postal_code: string;
  country: string;
  is_primary: boolean;
  label: string | null;
}

interface UserPhoneNumber {
  id: string;
  phone_number: string;
  is_primary: boolean;
  label: string | null;
  is_verified: boolean;
}

interface UserEmail {
  id: string;
  email: string;
  is_primary: boolean;
  label: string | null;
  verified_at: string | null;
}

interface User {
  id: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
  addresses: UserAddress[];
  phone_numbers: UserPhoneNumber[];
  emails: UserEmail[];
}

type SortOption = 'primary' | 'label';

// --- Components ---

const SectionHeader = ({ 
  title, 
  icon: Icon, 
  onSort, 
  currentSort 
}: { 
  title: string; 
  icon: React.ElementType; 
  onSort: (option: SortOption) => void;
  currentSort: SortOption;
}) => (
  <div className="flex items-center justify-between mb-2 pb-1 border-b border-gray-100">
    <div className="flex items-center gap-2 text-sm font-semibold text-gray-700">
      <Icon className="w-4 h-4" />
      <span>{title}</span>
    </div>
    <div className="relative group">
      <button 
        className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-800 transition-colors"
        title="Sort entries"
      >
        <span>Sort: {currentSort === 'primary' ? 'Primary' : 'Label'}</span>
        <ArrowUpDown className="w-3 h-3" />
      </button>
      
      {/* Dropdown */}
      <div className="absolute right-0 mt-1 w-32 bg-white rounded-md shadow-lg border border-gray-100 hidden group-hover:block z-10">
        <button 
          onClick={() => onSort('primary')}
          className={`block w-full text-left px-3 py-2 text-xs hover:bg-gray-50 ${currentSort === 'primary' ? 'font-medium text-blue-600' : 'text-gray-700'}`}
        >
          Primary First
        </button>
        <button 
          onClick={() => onSort('label')}
          className={`block w-full text-left px-3 py-2 text-xs hover:bg-gray-50 ${currentSort === 'label' ? 'font-medium text-blue-600' : 'text-gray-700'}`}
        >
          Label (A-Z)
        </button>
      </div>
    </div>
  </div>
);

const UserCard = ({ user }: { user: User }) => {
  const [addressSort, setAddressSort] = useState<SortOption>('primary');
  const [phoneSort, setPhoneSort] = useState<SortOption>('primary');
  const [emailSort, setEmailSort] = useState<SortOption>('primary');

  const sortItems = <T extends { is_primary: boolean; label: string | null }>(
    items: T[], 
    criterion: SortOption
  ) => {
    if (!items) return [];
    return [...items].sort((a, b) => {
      if (criterion === 'primary') {
        // Primary first
        if (a.is_primary && !b.is_primary) return -1;
        if (!a.is_primary && b.is_primary) return 1;
        return 0;
      } else {
        // Label A-Z
        const labelA = a.label || '';
        const labelB = b.label || '';
        return labelA.localeCompare(labelB);
      }
    });
  };

  const sortedAddresses = sortItems(user.addresses, addressSort);
  const sortedPhones = sortItems(user.phone_numbers, phoneSort);
  const sortedEmails = sortItems(user.emails, emailSort);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="p-5 bg-gray-50 border-b border-gray-200">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
              <UserIcon className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-gray-900">{user.full_name || 'Unnamed User'}</h3>
              <p className="text-sm text-gray-500">{user.email}</p>
            </div>
          </div>
          <span className={`px-2 py-1 text-xs rounded-full font-medium ${user.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
            {user.is_active ? 'Active' : 'Inactive'}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-5 grid gap-6">
        
        {/* Emails Section */}
        <div>
          <SectionHeader 
            title="Emails" 
            icon={Mail} 
            onSort={setEmailSort} 
            currentSort={emailSort} 
          />
          <div className="space-y-2">
            {sortedEmails.length > 0 ? sortedEmails.map((email) => (
              <div key={email.id} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2 overflow-hidden">
                  <span className="truncate text-gray-800" title={email.email}>{email.email}</span>
                  {email.is_primary && <span className="text-[10px] bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded border border-blue-100">Primary</span>}
                </div>
                {email.label && <span className="text-xs text-gray-400 bg-gray-50 px-2 py-0.5 rounded">{email.label}</span>}
              </div>
            )) : (
              <p className="text-xs text-gray-400 italic">No emails found</p>
            )}
          </div>
        </div>

        {/* Phones Section */}
        <div>
          <SectionHeader 
            title="Phone Numbers" 
            icon={Phone} 
            onSort={setPhoneSort} 
            currentSort={phoneSort} 
          />
          <div className="space-y-2">
            {sortedPhones.length > 0 ? sortedPhones.map((phone) => (
              <div key={phone.id} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <span className="text-gray-800">{phone.phone_number}</span>
                  {phone.is_primary && <span className="text-[10px] bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded border border-blue-100">Primary</span>}
                </div>
                {phone.label && <span className="text-xs text-gray-400 bg-gray-50 px-2 py-0.5 rounded">{phone.label}</span>}
              </div>
            )) : (
              <p className="text-xs text-gray-400 italic">No phone numbers found</p>
            )}
          </div>
        </div>

        {/* Addresses Section */}
        <div>
          <SectionHeader 
            title="Addresses" 
            icon={MapPin} 
            onSort={setAddressSort} 
            currentSort={addressSort} 
          />
          <div className="space-y-3">
            {sortedAddresses.length > 0 ? sortedAddresses.map((addr) => (
              <div key={addr.id} className="text-sm bg-gray-50 p-2.5 rounded-lg border border-gray-100">
                <div className="flex items-center justify-between mb-1">
                  {addr.label && <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">{addr.label}</span>}
                  {addr.is_primary && <span className="text-[10px] bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded border border-blue-100">Primary</span>}
                </div>
                <div className="text-gray-700">
                  <p>{addr.street}</p>
                  <p>{addr.city}, {addr.state} {addr.postal_code}</p>
                  <p>{addr.country}</p>
                </div>
              </div>
            )) : (
              <p className="text-xs text-gray-400 italic">No addresses found</p>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

// --- Main Page Component ---

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('/api/users');
        if (!response.ok) {
          throw new Error(`Failed to fetch users: ${response.statusText}`);
        }
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center h-full text-gray-500 min-h-[50vh]">
          <Loader2 className="w-8 h-8 animate-spin mb-2" />
          <p>Loading users...</p>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center h-full text-red-500 min-h-[50vh]">
          <AlertCircle className="w-10 h-10 mb-2" />
          <p className="font-medium">Error loading users</p>
          <p className="text-sm text-red-400 mt-1">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-white border border-red-200 rounded-md shadow-sm text-sm text-red-600 hover:bg-red-50 transition-colors"
          >
            Try Again
          </button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Users Directory</h1>
          <p className="text-gray-500 mt-1">Manage and view user contact information</p>
        </header>

        {users.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
            <UserIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <h3 className="text-lg font-medium text-gray-900">No users found</h3>
            <p className="text-gray-500">The user directory is currently empty.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {users.map((user) => (
              <UserCard key={user.id} user={user} />
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
