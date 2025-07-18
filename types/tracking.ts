export interface InteractionTracking {
  started_at: number;
  field_interactions: Record<string, number>;
  total_fields_interacted: number;
  form_abandonment_point?: string;
}
