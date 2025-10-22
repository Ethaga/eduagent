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
    setAgentInfo({
      name: "EduAgent",
      address: "agent1qf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvq",
      status: "active",
      capabilities: [
        "Mathematical Concept Explanation",
        "Programming Tutorials",
        "Algorithm Explanation",
        "Data Structure Guidance",
      ],
    })

    setConcepts([
      { value: "algebra", label: "Algebra" },
      { value: "calculus", label: "Calculus" },
      { value: "geometry", label: "Geometry" },
      { value: "python", label: "Python" },
      { value: "javascript", label: "JavaScript" },
      { value: "data-structures", label: "Data Structures" },
      { value: "algorithms", label: "Algorithms" },
    ])

    setDifficultyLevels([
      { value: "beginner", label: "Beginner" },
      { value: "intermediate", label: "Intermediate" },
      { value: "advanced", label: "Advanced" },
    ])

    loadHistory()
  }, [])

  const generateMockResponse = (question: string, conceptType: string, difficulty: string): ExplanationResponse => {
    const responses: Record<string, Record<string, ExplanationResponse>> = {
      algebra: {
        beginner: {
          explanation:
            "Algebra is the branch of mathematics that uses letters (variables) to represent unknown numbers. It helps us solve problems by creating equations.",
          keyPoints: [
            "Variables represent unknown values",
            "Equations show relationships between numbers",
            "We solve by isolating the variable",
            "Balance both sides of the equation",
          ],
          examples: ["x + 5 = 12 → x = 7", "2x = 10 → x = 5", "x - 3 = 7 → x = 10"],
          practiceProblems: ["Solve: x + 8 = 15", "Solve: 3x = 21", "Solve: x - 4 = 6"],
        },
        intermediate: {
          explanation:
            "Intermediate algebra involves working with polynomials, factoring, and quadratic equations. These concepts build on basic algebraic principles.",
          keyPoints: [
            "Polynomials have multiple terms with variables",
            "Factoring breaks expressions into simpler parts",
            "Quadratic equations have x² terms",
            "Use the quadratic formula or factoring to solve",
          ],
          examples: [
            "x² + 5x + 6 = (x + 2)(x + 3)",
            "x² - 4 = (x - 2)(x + 2)",
            "Using quadratic formula: x = (-b ± √(b² - 4ac)) / 2a",
          ],
          practiceProblems: ["Factor: x² + 7x + 12", "Solve: x² - 9 = 0", "Factor: 2x² + 8x + 6"],
        },
        advanced: {
          explanation:
            "Advanced algebra covers complex polynomials, systems of equations, matrices, and abstract algebraic structures.",
          keyPoints: [
            "Systems of equations can be solved using matrices",
            "Eigenvalues and eigenvectors are important in linear algebra",
            "Abstract algebra studies algebraic structures",
            "Group theory and ring theory are key concepts",
          ],
          examples: [
            "Matrix multiplication: [a b] × [e f] = [ae+bg af+bh]",
            "Determinant calculation for 2×2 matrix",
            "Solving systems using Gaussian elimination",
          ],
          practiceProblems: [
            "Find the determinant of a 3×3 matrix",
            "Solve a system of 3 equations with 3 unknowns",
            "Find eigenvalues of a given matrix",
          ],
        },
      },
      python: {
        beginner: {
          explanation:
            "Python is a beginner-friendly programming language. It uses simple syntax and is great for learning programming concepts.",
          keyPoints: [
            "Python uses indentation for code blocks",
            "Variables store data without declaring types",
            "Print function displays output",
            "Comments start with #",
          ],
          examples: [
            "print('Hello, World!')",
            "x = 10; y = 20; print(x + y)",
            "name = 'Alice'; print(f'Hello, {name}')",
          ],
          practiceProblems: [
            "Write a program that prints your name",
            "Create variables and print their sum",
            "Use a loop to print numbers 1 to 10",
          ],
        },
        intermediate: {
          explanation:
            "Intermediate Python covers functions, lists, dictionaries, and file handling. These are essential for building real applications.",
          keyPoints: [
            "Functions organize code into reusable blocks",
            "Lists store multiple values",
            "Dictionaries use key-value pairs",
            "File I/O allows reading and writing data",
          ],
          examples: [
            "def greet(name): return f'Hello, {name}'",
            "my_list = [1, 2, 3]; my_list.append(4)",
            "my_dict = {'name': 'Alice', 'age': 25}",
          ],
          practiceProblems: [
            "Write a function that calculates factorial",
            "Create a list and filter even numbers",
            "Read from a file and count lines",
          ],
        },
        advanced: {
          explanation:
            "Advanced Python includes decorators, generators, async programming, and metaprogramming for building complex applications.",
          keyPoints: [
            "Decorators modify function behavior",
            "Generators use yield for memory efficiency",
            "Async/await enables concurrent programming",
            "Metaclasses control class creation",
          ],
          examples: [
            "@decorator def func(): pass",
            "def gen(): yield 1; yield 2",
            "async def fetch(): await asyncio.sleep(1)",
          ],
          practiceProblems: [
            "Create a decorator that logs function calls",
            "Write a generator for Fibonacci sequence",
            "Build an async web scraper",
          ],
        },
      },
      "data-structures": {
        beginner: {
          explanation:
            "Data structures are ways to organize and store data. Arrays and lists are the simplest data structures.",
          keyPoints: [
            "Arrays store elements in contiguous memory",
            "Lists are dynamic arrays that can grow",
            "Access elements by index (0-based)",
            "Common operations: insert, delete, search",
          ],
          examples: [
            "Array: [1, 2, 3, 4, 5]",
            "List in Python: my_list = [10, 20, 30]",
            "Access: my_list[0] returns 10",
          ],
          practiceProblems: [
            "Create a list and access the third element",
            "Add and remove elements from a list",
            "Find the maximum value in a list",
          ],
        },
        intermediate: {
          explanation:
            "Intermediate data structures include stacks, queues, linked lists, and trees. These are crucial for algorithm design.",
          keyPoints: [
            "Stacks follow LIFO (Last In First Out)",
            "Queues follow FIFO (First In First Out)",
            "Linked lists use pointers to connect nodes",
            "Trees have hierarchical structure",
          ],
          examples: [
            "Stack: push(5), push(10), pop() returns 10",
            "Queue: enqueue(1), enqueue(2), dequeue() returns 1",
            "Binary Tree: root with left and right children",
          ],
          practiceProblems: [
            "Implement a stack using a list",
            "Implement a queue using a list",
            "Create a simple binary tree",
          ],
        },
        advanced: {
          explanation:
            "Advanced data structures include hash tables, graphs, heaps, and tries. These optimize specific operations.",
          keyPoints: [
            "Hash tables provide O(1) average lookup",
            "Graphs represent networks and relationships",
            "Heaps maintain partial ordering",
            "Tries efficiently store strings",
          ],
          examples: [
            "Hash table: {'key': 'value'}",
            "Graph: nodes connected by edges",
            "Min-heap: parent ≤ children",
            "Trie: tree of characters for prefix search",
          ],
          practiceProblems: [
            "Implement a hash table with collision handling",
            "Build a graph and perform DFS/BFS",
            "Implement a min-heap",
            "Build a trie for autocomplete",
          ],
        },
      },
    }

    return (
      responses[conceptType]?.[difficulty] || {
        explanation: `This is a ${difficulty} level explanation for ${conceptType}.`,
        keyPoints: ["Key point 1", "Key point 2", "Key point 3"],
        examples: ["Example 1", "Example 2"],
        practiceProblems: ["Problem 1", "Problem 2"],
      }
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const mockResponse = generateMockResponse(formData.question, formData.conceptType, formData.difficultyLevel)

      setResponse(mockResponse)
      addToHistory(formData.question)
      setFormData({ ...formData, question: "" })
    } catch (error) {
      console.error("Error processing question:", error)
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
