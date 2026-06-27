import { FileText, ExternalLink } from 'lucide-react'
import { SourceDocument, CATEGORY_COLORS } from '../types'

interface Props {
  source: SourceDocument
  index: number
}

export function SourceCard({ source, index }: Props) {
  const colorClass = CATEGORY_COLORS[source.category] || CATEGORY_COLORS.unknown
  const fileName = source.source_file.split('/').pop() || source.source_file

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-3 text-sm hover:border-green-300 transition-colors">
      <div className="flex items-start gap-2 mb-2">
        <FileText size={14} className="text-green-600 mt-0.5 shrink-0" />
        <div className="flex-1 min-w-0">
          <p className="font-medium text-slate-800 truncate">{source.regulation}</p>
          <p className="text-slate-400 text-xs truncate">{fileName} · p.{source.page}</p>
        </div>
        <span className={`text-xs px-1.5 py-0.5 rounded-full font-medium shrink-0 ${colorClass}`}>
          {source.year}
        </span>
      </div>
      <p className="text-slate-600 text-xs leading-relaxed line-clamp-3">{source.content}</p>
    </div>
  )
}
