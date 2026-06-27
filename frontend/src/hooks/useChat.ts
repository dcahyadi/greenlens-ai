import { useState, useCallback } from 'react'
import { ChatMessage, QueryResponse, QueryRequest } from '../types'

const API_URL = import.meta.env.VITE_API_URL || ''

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastSources, setLastSources] = useState<QueryResponse['sources']>([])

  const sendMessage = useCallback(async (
    question: string,
    language: 'en' | 'id' = 'en',
    category?: string | null,
  ) => {
    setIsLoading(true)
    setError(null)

    const userMsg: ChatMessage = { role: 'user', content: question }
    const updatedMessages = [...messages, userMsg]
    setMessages(updatedMessages)

    try {
      const body: QueryRequest = {
        question,
        language,
        category: category || null,
        chat_history: messages.slice(-8), // last 8 messages = 4 turns context
      }

      const res = await fetch(`${API_URL}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(err.detail || `HTTP ${res.status}`)
      }

      const data: QueryResponse = await res.json()
      setMessages([...updatedMessages, { role: 'assistant', content: data.answer }])
      setLastSources(data.sources)
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Failed to get response'
      setError(msg)
      setMessages([...updatedMessages, {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${msg}. Please try again.`,
      }])
    } finally {
      setIsLoading(false)
    }
  }, [messages])

  const clearChat = useCallback(() => {
    setMessages([])
    setLastSources([])
    setError(null)
  }, [])

  return { messages, isLoading, error, lastSources, sendMessage, clearChat }
}
