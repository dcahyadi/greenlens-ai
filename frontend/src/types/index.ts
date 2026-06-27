export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface SourceDocument {
  content: string
  source_file: string
  regulation: string
  category: string
  year: number
  page: number
}

export interface QueryResponse {
  answer: string
  sources: SourceDocument[]
  model_used: string
}

export interface QueryRequest {
  question: string
  language: 'en' | 'id'
  category?: string | null
  chat_history: ChatMessage[]
}

export const CATEGORY_OPTIONS = [
  { value: '', label: 'All Documents' },
  { value: 'climate_commitment', label: 'NDC / Climate Commitments' },
  { value: 'energy_transition', label: 'JETP / Energy Transition' },
  { value: 'carbon_market', label: 'Carbon Market' },
  { value: 'renewable_energy', label: 'Renewable Energy (ESDM)' },
  { value: 'environmental_law', label: 'Environmental Law (KLHK)' },
  { value: 'green_finance', label: 'Green Finance (OJK)' },
]

export const CATEGORY_COLORS: Record<string, string> = {
  climate_commitment: 'bg-blue-100 text-blue-800',
  energy_transition: 'bg-yellow-100 text-yellow-800',
  carbon_market: 'bg-gray-100 text-gray-800',
  renewable_energy: 'bg-green-100 text-green-800',
  environmental_law: 'bg-emerald-100 text-emerald-800',
  green_finance: 'bg-teal-100 text-teal-800',
  unknown: 'bg-slate-100 text-slate-600',
}
