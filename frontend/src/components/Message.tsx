import { User, Bot } from 'lucide-react'
import { ChatMessage } from '../types'

interface Props {
  message: ChatMessage
}

export function Message({ message }: Props) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
        isUser ? 'bg-green-600' : 'bg-slate-700'
      }`}>
        {isUser
          ? <User size={16} className="text-white" />
          : <Bot size={16} className="text-white" />
        }
      </div>
      <div className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
        isUser
          ? 'bg-green-600 text-white rounded-tr-sm'
          : 'bg-white border border-slate-200 text-slate-800 rounded-tl-sm'
      }`}>
        {message.content.split('\n').map((line, i) => (
          <p key={i} className={line === '' ? 'mt-2' : ''}>{line}</p>
        ))}
      </div>
    </div>
  )
}
