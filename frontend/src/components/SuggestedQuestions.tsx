interface Props {
  onSelect: (q: string) => void
  language: 'en' | 'id'
}

const QUESTIONS_EN = [
  "What is Indonesia's emission reduction target in the Enhanced NDC 2022?",
  "How much financing was committed under JETP Indonesia?",
  "What carbon pricing instruments does Perpres 98/2021 introduce?",
  "What is the PLTS Atap rooftop solar policy?",
  "How does OJK's TKBI v3 2026 classify renewable energy?",
  "What is IDX Carbon and how is it regulated?",
]

const QUESTIONS_ID = [
  "Berapa target pengurangan emisi Indonesia dalam NDC 2022?",
  "Apa itu JETP Indonesia dan berapa dana yang dijanjikan?",
  "Apa itu AMDAL dan siapa yang wajib membuatnya?",
  "Bagaimana regulasi PLTS Atap menurut Permen ESDM 2/2024?",
  "Apa instrumen perdagangan karbon dalam Perpres 98/2021?",
  "Apa itu Bursa Karbon Indonesia (IDX Carbon)?",
]

export function SuggestedQuestions({ onSelect, language }: Props) {
  const questions = language === 'id' ? QUESTIONS_ID : QUESTIONS_EN

  return (
    <div className="space-y-2">
      <p className="text-xs text-slate-400 font-medium uppercase tracking-wide">
        {language === 'id' ? 'Pertanyaan Populer' : 'Suggested Questions'}
      </p>
      <div className="grid grid-cols-1 gap-2">
        {questions.map((q, i) => (
          <button
            key={i}
            onClick={() => onSelect(q)}
            className="text-left text-sm text-slate-600 bg-white border border-slate-200
                       rounded-lg px-3 py-2 hover:border-green-400 hover:text-green-700
                       hover:bg-green-50 transition-colors"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  )
}
