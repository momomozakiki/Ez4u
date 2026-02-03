'use client';

import React, { useEffect, useState } from 'react';
import { 
  Loader2, 
  AlertCircle, 
  Settings,
  Info,
  ChevronRight,
  ArrowLeft,
  Building,
  User as UserIcon,
  Phone,
  Mail,
  MapPin,
  Folder
} from 'lucide-react';
import DashboardLayout from '../components/DashboardLayout';
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

// --- Types ---

interface Tenant {
  id: string;
  name: string;
  slug: string;
  parent_tenant_id: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  type: 'tenant';
}

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

interface UserRole {
  tenant_name: string;
  role_name: string;
}

interface User {
  id: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  addresses: UserAddress[];
  phone_numbers: UserPhoneNumber[];
  emails: UserEmail[];
  roles: UserRole[];
  type: 'user';
}

type DirectoryItem = Tenant | User;

// --- Components ---

const DetailSheet = ({ item, open, onOpenChange }: { item: DirectoryItem | null, open: boolean, onOpenChange: (open: boolean) => void }) => {
  if (!item) return null;

  const isUser = item.type === 'user';
  const title = isUser ? (item as User).full_name || 'Unnamed User' : (item as Tenant).name;
  const icon = isUser ? <UserIcon className="w-6 h-6" /> : <Building className="w-6 h-6" />;

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="w-[400px] sm:w-[540px] overflow-y-auto">
        <SheetHeader className="mb-6">
          <SheetTitle className="flex items-center gap-2 text-2xl">
            <div className="p-2 bg-primary/10 rounded-full text-primary">
              {icon}
            </div>
            {title}
          </SheetTitle>
          <SheetDescription>
            ID: {item.id}
          </SheetDescription>
        </SheetHeader>

        <div className="space-y-6">
          {/* Status Badge */}
          <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
            <span className="font-medium">Status</span>
            <span className={cn(
              "px-2.5 py-0.5 rounded-full text-xs font-medium",
              item.is_active ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
            )}>
              {item.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>

          {isUser ? (
             // User Details
             <>
               <div>
                  <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-3">Contact Information</h3>
                  <div className="space-y-4">
                    <div className="flex items-start gap-3">
                      <Mail className="w-4 h-4 mt-1 text-muted-foreground" />
                      <div className="flex-1">
                        <p className="font-medium text-sm">Email Addresses</p>
                        <div className="mt-1 space-y-1">
                          {(item as User).emails.map(email => (
                            <div key={email.id} className="flex items-center gap-2 text-sm">
                              <span>{email.email}</span>
                              {email.is_primary && <span className="text-[10px] bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded border border-blue-100">Primary</span>}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <Phone className="w-4 h-4 mt-1 text-muted-foreground" />
                      <div className="flex-1">
                        <p className="font-medium text-sm">Phone Numbers</p>
                        <div className="mt-1 space-y-1">
                          {(item as User).phone_numbers.length > 0 ? (item as User).phone_numbers.map(phone => (
                            <div key={phone.id} className="flex items-center gap-2 text-sm">
                              <span>{phone.phone_number}</span>
                              {phone.is_primary && <span className="text-[10px] bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded border border-blue-100">Primary</span>}
                            </div>
                          )) : <p className="text-sm text-muted-foreground italic">No phone numbers</p>}
                        </div>
                      </div>
                    </div>
                  </div>
               </div>

               <div>
                 <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-3">Addresses</h3>
                 <div className="space-y-3">
                   {(item as User).addresses.length > 0 ? (item as User).addresses.map(addr => (
                     <div key={addr.id} className="flex items-start gap-3 text-sm bg-muted/30 p-3 rounded-md">
                       <MapPin className="w-4 h-4 mt-0.5 text-muted-foreground" />
                       <div>
                         <div className="flex items-center gap-2 mb-1">
                           {addr.label && <span className="font-medium">{addr.label}</span>}
                           {addr.is_primary && <span className="text-[10px] bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded border border-blue-100">Primary</span>}
                         </div>
                         <p>{addr.street}</p>
                         <p>{addr.city}, {addr.state} {addr.postal_code}</p>
                         <p>{addr.country}</p>
                       </div>
                     </div>
                   )) : <p className="text-sm text-muted-foreground italic">No addresses</p>}
                 </div>
               </div>
             </>
          ) : (
            // Tenant Details
            <div>
              <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-3">Tenant Details</h3>
              <div className="space-y-3">
                 <div className="flex items-start gap-3 text-sm bg-muted/30 p-3 rounded-md">
                    <div>
                      <p className="font-medium text-xs text-muted-foreground uppercase">Slug</p>
                      <p className="font-medium">{(item as Tenant).slug}</p>
                    </div>
                 </div>
                 <div className="flex items-start gap-3 text-sm bg-muted/30 p-3 rounded-md">
                    <div>
                      <p className="font-medium text-xs text-muted-foreground uppercase">Created At</p>
                      <p>{new Date((item as Tenant).created_at).toLocaleString()}</p>
                    </div>
                 </div>
              </div>
            </div>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
};

// --- Main Page Component ---

export default function UsersPage() {
  const [items, setItems] = useState<DirectoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalUsers, setTotalUsers] = useState<number>(0);
  
  // State for Table & Hierarchy
  const [selectedItem, setSelectedItem] = useState<DirectoryItem | null>(null);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [contextStack, setContextStack] = useState<{id: string, name: string}[]>([]);
  
  // Column Visibility State
  const [visibleColumns, setVisibleColumns] = useState<Record<string, boolean>>({
    name: true,
    address: true,
    phone: true,
    email: true,
    role: true,
    status: true,
    actions: true
  });

  const fetchData = async (parentId: string | null) => {
    setLoading(true);
    setError(null);
    try {
      // Fetch Tenants (Folders)
      const tenantQueryParams = parentId ? `?parent_id=${parentId}` : '';
      const tenantsRes = await fetch(`/api/tenants${tenantQueryParams}`);
      if (!tenantsRes.ok) throw new Error('Failed to fetch tenants');
      const tenantsData: Tenant[] = await tenantsRes.json();
      const formattedTenants = tenantsData.map(t => ({ ...t, type: 'tenant' as const }));

      // Fetch Users (Files) - Only if we are in a context (not root) or if root users are supported
      // Assuming we only show users if we are inside a tenant
      let formattedUsers: User[] = [];
      if (parentId) {
         const usersRes = await fetch(`/api/users?tenant_id=${parentId}`);
         if (!usersRes.ok) throw new Error('Failed to fetch users');
         const usersData: User[] = await usersRes.json();
         formattedUsers = usersData.map(u => ({ ...u, type: 'user' as const }));
      }

      setItems([...formattedTenants, ...formattedUsers]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Get the current context (last item in stack)
    const currentContext = contextStack.length > 0 ? contextStack[contextStack.length - 1] : null;
    const parentId = currentContext ? currentContext.id : null;
    
    fetchData(parentId);
  }, [contextStack]);

  useEffect(() => {
    // Fetch total global user count for the Root label
    const fetchTotalUsers = async () => {
      try {
        const res = await fetch('/api/users');
        if (res.ok) {
          const data = await res.json();
          setTotalUsers(data.length);
        }
      } catch (error) {
        console.error("Failed to fetch total user count", error);
      }
    };
    fetchTotalUsers();
  }, []);

  const handleDrillDown = (item: DirectoryItem) => {
    if (item.type === 'tenant') {
      setContextStack(prev => {
        if (prev.some(ctx => ctx.id === item.id)) return prev;
        return [...prev, { id: item.id, name: (item as Tenant).name }];
      });
    } else {
      openDetails(item);
    }
  };

  const handleGoBack = () => {
    setContextStack(prev => prev.slice(0, -1));
  };

  const handleGoToRoot = () => {
    setContextStack([]);
  };

  const handleBreadcrumbClick = (index: number) => {
    setContextStack(prev => prev.slice(0, index + 1));
  };

  const openDetails = (item: DirectoryItem) => {
    setSelectedItem(item);
    setIsDetailOpen(true);
  };

  const toggleColumn = (key: string) => {
    setVisibleColumns(prev => ({ ...prev, [key]: !prev[key] }));
  };

  if (error) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center h-[50vh] text-destructive">
          <AlertCircle className="w-10 h-10 mb-2" />
          <p className="font-medium">Error loading directory</p>
          <p className="text-sm opacity-80 mt-1">{error}</p>
          <Button 
            variant="outline" 
            className="mt-4 border-destructive/30 hover:bg-destructive/10"
            onClick={() => window.location.reload()}
          >
            Try Again
          </Button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto p-6">
        
        {/* Header Area */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">User Management</h1>
            <p className="text-muted-foreground mt-1">
              Navigate tenants and manage users.
            </p>
          </div>
          
          <div className="flex items-center gap-2">
             {/* Column Visibility Settings */}
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline" size="sm" className="gap-2">
                  <Settings className="w-4 h-4" />
                  View Settings
                </Button>
              </PopoverTrigger>
              <PopoverContent align="end" className="w-56">
                <div className="space-y-2">
                  <h4 className="font-medium leading-none mb-3">Toggle Columns</h4>
                  <div className="space-y-2">
                    {Object.keys(visibleColumns).filter(k => k !== 'actions').map((key) => (
                      <div key={key} className="flex items-center space-x-2">
                        <Checkbox 
                          id={`col-${key}`} 
                          checked={visibleColumns[key]} 
                          onCheckedChange={() => toggleColumn(key)}
                        />
                        <Label htmlFor={`col-${key}`} className="capitalize cursor-pointer">
                          {key}
                        </Label>
                      </div>
                    ))}
                  </div>
                </div>
              </PopoverContent>
            </Popover>
          </div>
        </div>

        {/* Breadcrumb Navigation for Hierarchy */}
        <div className="flex items-center gap-2 mb-4 text-sm h-8">
          <Button 
            variant="ghost" 
            size="sm" 
            className={cn("h-auto p-0 hover:bg-transparent hover:underline", contextStack.length === 0 ? "font-bold text-foreground" : "text-muted-foreground")}
            onClick={handleGoToRoot}
          >
            Root <span className="ml-1 text-muted-foreground font-normal">({totalUsers})</span>
          </Button>
          
          {contextStack.map((ctx, index) => (
            <React.Fragment key={ctx.id}>
              <ChevronRight className="w-4 h-4 text-muted-foreground" />
              <Button
                variant="ghost"
                size="sm"
                className={cn(
                  "h-auto p-0 hover:bg-transparent hover:underline", 
                  index === contextStack.length - 1 ? "font-bold text-foreground" : "text-muted-foreground"
                )}
                onClick={() => handleBreadcrumbClick(index)}
              >
                {ctx.name}
              </Button>
            </React.Fragment>
          ))}
          
          {contextStack.length > 0 && (
            <Button variant="ghost" size="icon" className="ml-auto h-6 w-6" onClick={handleGoBack}>
              <ArrowLeft className="w-4 h-4" />
            </Button>
          )}
        </div>

        {/* Directory Table */}
        <div className="rounded-md border bg-card shadow-sm">
          <Table>
            <TableHeader>
              <TableRow>
                {visibleColumns.name && <TableHead className="w-[300px]">Name</TableHead>}
                {visibleColumns.address && <TableHead>Address</TableHead>}
                {visibleColumns.phone && <TableHead>Phone</TableHead>}
                {visibleColumns.email && <TableHead>Email</TableHead>}
                {visibleColumns.role && <TableHead>Role</TableHead>}
                {visibleColumns.status && <TableHead>Status</TableHead>}
                <TableHead className="w-[100px] text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                 <TableRow>
                  <TableCell colSpan={7} className="h-24 text-center">
                    <div className="flex items-center justify-center text-muted-foreground">
                      <Loader2 className="w-6 h-6 animate-spin mr-2" />
                      Loading...
                    </div>
                  </TableCell>
                </TableRow>
              ) : items.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} className="h-24 text-center text-muted-foreground">
                    No items found in this level.
                  </TableCell>
                </TableRow>
              ) : (
                items.map((item) => {
                  const isTenant = item.type === 'tenant';
                  const primaryAddress = !isTenant ? (item as User).addresses.find(a => a.is_primary) : null;
                  const primaryPhone = !isTenant ? (item as User).phone_numbers.find(p => p.is_primary) : null;
                  const primaryEmail = !isTenant ? (item as User).emails.find(e => e.is_primary) : null;
                  const role = !isTenant && (item as User).roles.length > 0 ? (item as User).roles[0] : null;

                  return (
                    <TableRow key={item.id} className="group">
                      {visibleColumns.name && (
                        <TableCell className="font-medium">
                          <div className="flex items-center gap-3">
                            <div 
                              className={cn(
                                "w-8 h-8 rounded-full flex items-center justify-center cursor-pointer transition-colors",
                                isTenant ? "bg-amber-100 text-amber-700 hover:bg-amber-200" : "bg-primary/10 text-primary hover:bg-primary/20"
                              )}
                              onClick={() => handleDrillDown(item)}
                              title={isTenant ? "Open Tenant" : "View User Details"}
                            >
                              {isTenant ? <Folder className="w-4 h-4" /> : <UserIcon className="w-4 h-4" />}
                            </div>
                            <div>
                              <div 
                                className="font-medium text-foreground hover:underline cursor-pointer"
                                onClick={() => handleDrillDown(item)}
                              >
                                {isTenant ? (item as Tenant).name : (item as User).full_name || 'Unnamed User'}
                              </div>
                            </div>
                          </div>
                        </TableCell>
                      )}
                      
                      {visibleColumns.address && (
                        <TableCell>
                           {primaryAddress ? (
                             <div className="text-xs text-muted-foreground">
                               <p>{primaryAddress.city}, {primaryAddress.country}</p>
                             </div>
                           ) : (
                             <span className="text-muted-foreground text-xs italic">-</span>
                           )}
                        </TableCell>
                      )}

                      {visibleColumns.phone && (
                        <TableCell>
                          {primaryPhone ? (
                            <span className="text-xs text-muted-foreground">{primaryPhone.phone_number}</span>
                          ) : (
                            <span className="text-muted-foreground text-xs italic">-</span>
                          )}
                        </TableCell>
                      )}

                      {visibleColumns.email && (
                        <TableCell>
                          {primaryEmail ? (
                            <span className="text-xs text-muted-foreground">{primaryEmail.email}</span>
                          ) : (
                            <span className="text-muted-foreground text-xs italic">-</span>
                          )}
                        </TableCell>
                      )}

                      {visibleColumns.role && (
                        <TableCell>
                          {role ? (
                            <span className="inline-flex items-center justify-center min-w-[80px] px-2 py-0.5 rounded-full text-xs font-medium bg-secondary text-secondary-foreground">
                              {role.role_name}
                            </span>
                          ) : (
                            <span className="text-muted-foreground text-xs italic">-</span>
                          )}
                        </TableCell>
                      )}
                      
                      {visibleColumns.status && (
                        <TableCell>
                           <span className={cn(
                            "inline-flex items-center justify-center min-w-[80px] px-2 py-1 rounded-full text-xs font-medium ring-1 ring-inset",
                            item.is_active 
                              ? "bg-green-50 text-green-700 ring-green-600/20" 
                              : "bg-red-50 text-red-700 ring-red-600/10"
                          )}>
                            {item.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </TableCell>
                      )}
                      
                      <TableCell className="text-right">
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          onClick={() => openDetails(item)}
                          title="More Info"
                        >
                          <Info className="w-4 h-4 text-muted-foreground hover:text-foreground" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </div>

        <DetailSheet 
          item={selectedItem} 
          open={isDetailOpen} 
          onOpenChange={setIsDetailOpen} 
        />
        
      </div>
    </DashboardLayout>
  );
}
