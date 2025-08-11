export interface Event {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  location_name: string;
  latitude: number;
  longitude: number;
  organization_id: number;
  event_type: 'academic' | 'government' | 'holiday' | 'city';
  source_url: string;
  created_at: string;
  tags?: string; // comma-separated from backend; optional
}

export interface EventFilters {
  eventType?: string;
  organization?: string;
  dateRange?: {
    start: Date;
    end: Date;
  };
  search?: string;
}

export interface Organization {
  id: number;
  name: string;
  type: string;
  location: string;
} 