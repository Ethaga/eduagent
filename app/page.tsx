"use client"

import type React from "react"

import { useState, useEffect } from "react"

interface AgentInfo {
  name: string
  address: string
  status: string
  capabilities: string[]
}

interface Concept {
  value: string
  label: string
}

interface DifficultyLevel {
  value: string
  label: string
}

interface ExplanationResponse {
  explanation: string
  keyPoints: string[]
  examples: string[]
  practiceProblems: string[]
}

export default function Home() {
  const [agentInfo, setAgentInfo] = useState<AgentInfo | null>(null)
  const [concepts, setConcepts] = useState<Concept[]>([])
  const [difficultyLevels, setDifficultyLevels] = useState<DifficultyLevel[]>([])
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState<ExplanationResponse | null>(null)
  const [history, setHistory] = useState<string[]>([])

  const [formData, setFormData] = useState({
    question: "",
    conceptType: "algebra",
    difficultyLevel: "intermediate",
    studentId: "",
  })

  useEffect(() => {
    fetchAgentInfo()
    fetchConcepts()
    fetchDifficultyLevels()
    loadHistory()
  }, [])

  const fetchAgentInfo = async () => {
    try {
      const res = await fetch("/api/agent/info")
      if (!res.ok) throw new Error("Failed to fetch agent info")
      const data = await res.json()
      setAgentInfo(data)
    } catch (error) {
      console.error("Error fetching agent info:", error)
      setAgentInfo({
        name: "EduAgent",
        address: "agent1qf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvq",
        status: "offline",
        capabilities: ["Mathematical Concept Explanation", "Programming Tutorials"],
      })
    }
  }

  const fetchConcepts = async () => {
    try {
      const res = await fetch("/api/concepts")
      if (!res.ok) throw new Error("Failed to fetch concepts")
      const data = await res.json()
      const conceptsData = data.concepts.map((concept: string) => ({
        value: concept,
        label: concept.charAt(0).toUpperCase() + concept.slice(1).replace("-", " "),
      }))
      setConcepts(conceptsData)
    } catch (error) {
      console.error("Error fetching concepts:", error)
      setConcepts([
        { value: "algebra", label: "Algebra" },
        { value: "calculus", label: "Calculus" },
        { value: "geometry", label: "Geometry" },
        { value: "python", label: "Python" },
        { value: "javascript", label: "JavaScript" },
        { value: "data-structures", label: "Data Structures" },
        { value: "algorithms", label: "Algorithms" },
      ])
    }
  }

  const fetchDifficultyLevels = async () => {
    try {
      const res = await fetch("/api/difficulty-levels")
      if (!res.ok) throw new Error("Failed to fetch difficulty levels")
      const data = await res.json()
      const levelsData = data.levels.map((level: string) => ({
        value: level,
        label: level.charAt(0).toUpperCase() + level.slice(1),
      }))
      setDifficultyLevels(levelsData)
    } catch (error) {
      console.error("Error fetching difficulty levels:", error)
      setDifficultyLevels([
        { value: "beginner", label: "Beginner" },
        { value: "intermediate", label: "Intermediate" },
        { value: "advanced", label: "Advanced" },
      ])
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: formData.question,
          concept_type: formData.conceptType,
          difficulty_level: formData.difficultyLevel,
          student_id: formData.studentId || null,
        }),
      })

      const data = await res.json()

      if (res.ok) {
        setResponse(data)
        addToHistory(formData.question)
        setFormData({ ...formData, question: "" })
      } else {
        console.error("Error:", data.error)
        setResponse(null)
      }
    } catch (error) {
      console.error("Error submitting question:", error)
      setResponse(null)
    } finally {
      setLoading(false)
    }
  }

  const addToHistory = (question: string) => {
    const newHistory = [question.substring(0, 50) + (question.length > 50 ? "..." : ""), ...history.slice(0, 9)]
    setHistory(newHistory)
    localStorage.setItem("eduagent_history", JSON.stringify(newHistory))
  }

  const loadHistory = () => {
    const saved = localStorage.getItem("eduagent_history")
    if (saved) {
      setHistory(JSON.parse(saved))
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-2">EduAgent</h1>
          <p className="text-blue-100 mb-4">AI-Powered Educational Tutor</p>
          <div className="flex items-center gap-2">
            <div
              className={`w-3 h-3 rounded-full animate-pulse ${agentInfo?.status === "active" ? "bg-green-400" : "bg-red-400"}`}
            ></div>
            <span className="text-sm">
              {agentInfo ? `Agent ${agentInfo.status} - ${agentInfo.address?.slice(0, 20)}...` : "Connecting..."}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Question Panel */}
          <section className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Ask a Question</h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Question Input */}
              <div>
                <label htmlFor="question" className="block text-sm font-semibold text-gray-700 mb-2">
                  Your Question
                </label>
                <textarea
                  id="question"
                  value={formData.question}
                  onChange={(e) => setFormData({ ...formData, question: e.target.value })}
                  placeholder="Ask me anything about mathematics, programming, algorithms, or data structures..."
                  rows={4}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Concept Type */}
              <div>
                <label htmlFor="conceptType" className="block text-sm font-semibold text-gray-700 mb-2">
                  Concept Type
                </label>
                <select
                  id="conceptType"
                  value={formData.conceptType}
                  onChange={(e) => setFormData({ ...formData, conceptType: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {concepts.map((concept) => (
                    <option key={concept.value} value={concept.value}>
                      {concept.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Difficulty Level */}
              <div>
                <label htmlFor="difficultyLevel" className="block text-sm font-semibold text-gray-700 mb-2">
                  Difficulty Level
                </label>
                <select
                  id="difficultyLevel"
                  value={formData.difficultyLevel}
                  onChange={(e) => setFormData({ ...formData, difficultyLevel: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {difficultyLevels.map((level) => (
                    <option key={level.value} value={level.value}>
                      {level.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Student ID */}
              <div>
                <label htmlFor="studentId" className="block text-sm font-semibold text-gray-700 mb-2">
                  Student ID (Optional)
                </label>
                <input
                  type="text"
                  id="studentId"
                  value={formData.studentId}
                  onChange={(e) => setFormData({ ...formData, studentId: e.target.value })}
                  placeholder="Enter your student ID for progress tracking"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 rounded-lg transition-colors"
              >
                {loading ? "Processing..." : "Ask EduAgent"}
              </button>
            </form>
          </section>

          {/* Response Panel */}
          <section className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Response</h2>

            <div className="bg-gray-50 rounded-lg p-6 min-h-96 max-h-96 overflow-y-auto mb-6">
              {response ? (
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-blue-600 mb-2">Explanation</h3>
                    <p className="text-gray-700 whitespace-pre-wrap">{response.explanation}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-blue-600 mb-2">Key Points</h3>
                    <ul className="list-disc list-inside space-y-1 text-gray-700">
                      {response.keyPoints.map((point, index) => (
                        <li key={index}>{point}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="font-semibold text-blue-600 mb-2">Examples</h3>
                    <ul className="list-disc list-inside space-y-1 text-gray-700">
                      {response.examples.map((example, index) => (
                        <li key={index}>{example}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500">
                  <p>Ask a question to get started!</p>
                </div>
              )}
            </div>

            {/* History */}
            <div className="border-t pt-6">
              <h3 className="font-semibold text-gray-800 mb-3">Recent Questions</h3>
              <ul className="space-y-2">
                {history.length > 0 ? (
                  history.map((item, index) => (
                    <li
                      key={index}
                      onClick={() => setFormData({ ...formData, question: item })}
                      className="p-2 bg-gray-100 rounded cursor-pointer hover:bg-gray-200 text-sm text-gray-700"
                    >
                      {item}
                    </li>
                  ))
                ) : (
                  <li className="text-gray-500 italic">No questions asked yet</li>
                )}
              </ul>
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12 py-8">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p>&copy; 2025 EduAgent - ASI Alliance Innovation Lab</p>
          <div className="flex justify-center gap-4 mt-4">
            <a href="#" className="hover:text-blue-400">
              Documentation
            </a>
            <a href="#" className="hover:text-blue-400">
              GitHub
            </a>
            <a href="#" className="hover:text-blue-400">
              Agentverse
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}
