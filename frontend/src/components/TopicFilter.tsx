import { Filter } from 'lucide-react'
import { CATEGORY_OPTIONS } from '../types'

interface Props {
  value: string
  onChange: (value: string) => void
}

export function TopicFilter({ value, onChange }: Props) {
  return (
    <div className="flex items-center gap-2">
      <Filter size={14} className="text-slate-400 shrink-0" />
      <select
        value={value}
        onChange={e => onChange(e.target.value)}
        className="text-sm border border-slate-200 rounded-lg px-2 py-1.5 bg-white text-slate-700
                   focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
      >
        {CATEGORY_OPTIONS.map(opt => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
    </div>
  )
}
