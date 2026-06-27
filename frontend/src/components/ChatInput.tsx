import { useState, KeyboardEvent } from 'react'
import { Send, Loader2 } from 'lucide-react'

interface Props {
  onSend: (text: string) => void
  isLoading: boolean
  language: 'en' | 'id'
}

export function ChatInput({ onSend, isLoading, language }: Props) {
  const [value, setValue] = useState('')

  const placeholder = language === 'id'
    ? 'Tanyakan tentang kebijakan lingkungan Indonesia...'
    : 'Ask about Indonesia\'s green policies...'

  const handleSend = () => {
    const trimmed = value.trim()
    if (!trimmed || isLoading) return
    onSend(trimmed)
    setValue('')
  }

  const handleKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex gap-2 items-end">
      <textarea
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKey}
        placeholder={placeholder}
        rows={1}
        disabled={isLoading}
        className="flex-1 resize-none border border-slate-200 rounded-xl px-4 py-3 text-sm
                   focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent
                   disabled:bg-slate-50 disabled:cursor-not-allowed max-h-32 overflow-y-auto
                   scrollbar-thin"
        style={{ minHeight: '48px' }}
        onInput={e => {
          const el = e.currentTarget
          el.style.height = 'auto'
          el.style.height = Math.min(el.scrollHeight, 128) + 'px'
        }}
      />
      <button
        onClick={handleSend}
        disabled={!value.trim() || isLoading}
        className="w-12 h-12 bg-green-600 hover:bg-green-700 disabled:bg-slate-200
                   rounded-xl flex items-center justify-center transition-colors shrink-0"
        aria-label="Send message"
      >
        {isLoading
          ? <Loader2 size={18} className="text-white animate-spin" />
          : <Send size={18} className="text-white" />
        }
      </button>
    </div>
  )
}
