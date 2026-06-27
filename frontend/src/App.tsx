import { useRef, useEffect, useState } from 'react'
import { Leaf, RotateCcw, Globe } from 'lucide-react'
import { useChat } from './hooks/useChat'
import { Message } from './components/Message'
import { SourceCard } from './components/SourceCard'
import { TopicFilter } from './components/TopicFilter'
import { ChatInput } from './components/ChatInput'
import { SuggestedQuestions } from './components/SuggestedQuestions'

export default function App() {
  const { messages, isLoading, error, lastSources, sendMessage, clearChat } = useChat()
  const [language, setLanguage] = useState<'en' | 'id'>('en')
  const [category, setCategory] = useState<string>('')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleSend = (text: string) => {
    sendMessage(text, language, category || null)
  }

  const isEmpty = messages.length === 0

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <Leaf size={18} className="text-white" />
            </div>
            <div>
              <h1 className="font-semibold text-slate-900 text-sm leading-none">GreenLens AI</h1>
              <p className="text-xs text-slate-400">Indonesia Green Policy Q&A</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {/* Language toggle */}
            <button
              onClick={() => setLanguage(l => l === 'en' ? 'id' : 'en')}
              className="flex items-center gap-1.5 text-xs border border-slate-200 rounded-lg
                         px-2.5 py-1.5 hover:bg-slate-50 transition-colors text-slate-600"
            >
              <Globe size={13} />
              {language === 'en' ? 'EN' : 'ID'}
            </button>
            {/* Clear chat */}
            {!isEmpty && (
              <button
                onClick={clearChat}
                className="flex items-center gap-1.5 text-xs border border-slate-200 rounded-lg
                           px-2.5 py-1.5 hover:bg-slate-50 transition-colors text-slate-600"
              >
                <RotateCcw size={13} />
                {language === 'id' ? 'Baru' : 'Clear'}
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main */}
      <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-4 flex gap-4">
        {/* Chat column */}
        <div className="flex-1 flex flex-col min-h-0">
          {/* Filter bar */}
          <div className="flex items-center gap-3 mb-3 bg-white border border-slate-200 rounded-xl p-2.5">
            <TopicFilter value={category} onChange={setCategory} />
            {category && (
              <span className="text-xs text-green-600 font-medium">
                {language === 'id' ? '• Filter aktif' : '• Filter active'}
              </span>
            )}
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto scrollbar-thin space-y-4 pb-4 min-h-[400px]">
            {isEmpty ? (
              <div className="flex flex-col items-center justify-center h-full text-center py-12">
                <div className="w-16 h-16 bg-green-50 rounded-2xl flex items-center justify-center mb-4">
                  <Leaf size={32} className="text-green-600" />
                </div>
                <h2 className="text-lg font-semibold text-slate-800 mb-1">
                  {language === 'id' ? 'Selamat datang di GreenLens AI' : 'Welcome to GreenLens AI'}
                </h2>
                <p className="text-sm text-slate-500 max-w-sm">
                  {language === 'id'
                    ? 'Tanyakan tentang kebijakan hijau Indonesia — NDC, JETP, AMDAL, karbon, dan energi terbarukan.'
                    : 'Ask about Indonesia\'s green policies — NDC, JETP, AMDAL, carbon markets, and renewable energy.'
                  }
                </p>
              </div>
            ) : (
              messages.map((msg, i) => <Message key={i} message={msg} />)
            )}

            {isLoading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                  <Leaf size={16} className="text-white" />
                </div>
                <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm px-4 py-3">
                  <div className="flex gap-1.5 items-center h-5">
                    {[0, 1, 2].map(i => (
                      <span key={i} className="w-2 h-2 bg-green-400 rounded-full animate-bounce"
                            style={{ animationDelay: `${i * 0.15}s` }} />
                    ))}
                  </div>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="mt-3 bg-white border border-slate-200 rounded-xl p-3">
            <ChatInput onSend={handleSend} isLoading={isLoading} language={language} />
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-72 shrink-0 space-y-4 hidden lg:block">
          {/* Sources */}
          {lastSources.length > 0 && (
            <div>
              <p className="text-xs text-slate-400 font-medium uppercase tracking-wide mb-2">
                {language === 'id' ? 'Sumber Dokumen' : 'Source Documents'}
              </p>
              <div className="space-y-2">
                {lastSources.map((src, i) => (
                  <SourceCard key={i} source={src} index={i} />
                ))}
              </div>
            </div>
          )}

          {/* Suggested questions */}
          {isEmpty && (
            <SuggestedQuestions onSelect={handleSend} language={language} />
          )}

          {/* Document index */}
          <div className="bg-white border border-slate-200 rounded-xl p-3">
            <p className="text-xs text-slate-400 font-medium uppercase tracking-wide mb-2">
              {language === 'id' ? 'Korpus Dokumen' : 'Document Corpus'}
            </p>
            <div className="space-y-1 text-xs text-slate-600">
              {[
                ['🌍', 'NDC 2021/2022'],
                ['⚡', 'JETP CIPP 2023'],
                ['📊', 'JETP Progress 2025'],
                ['💰', 'Perpres 98/2021 & 110/2025'],
                ['🔋', 'Perpres 112/2022'],
                ['☀️', 'Permen ESDM 2/2024'],
                ['🌿', 'PP 22/2021 & PermenLHK'],
                ['🏦', 'OJK TKBI v3 2026'],
                ['📈', 'POJK 14/2023'],
              ].map(([icon, label]) => (
                <div key={label} className="flex items-center gap-1.5">
                  <span>{icon}</span>
                  <span>{label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
