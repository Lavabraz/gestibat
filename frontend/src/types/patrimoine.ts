export interface Building {
  id: string;
  name: string;
  address: string;
  city: string;
  postalCode: string;
  description?: string;
  yearBuilt?: number;
  surfaceArea?: number;
  status: 'active' | 'inactive' | 'maintenance';
  createdAt: string;
  updatedAt: string;
  images?: string[];
  documents?: string[];
}

export interface BuildingFilter {
  status?: Building['status'];
  city?: string;
  search?: string;
  yearMin?: number;
  yearMax?: number;
}

export interface BuildingListResponse {
  data: Building[];
  pagination: {
    page: number;
    perPage: number;
    total: number;
    totalPages: number;
  };
}

export interface BuildingDetailResponse {
  data: Building;
  related: {
    agents: string[];
    maintenanceRecords: any[];
    inspections: any[];
  };
}

export interface PaginationParams {
  page?: number;
  perPage?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}