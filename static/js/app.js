// EduAgent Web Interface JavaScript

class EduAgentClient {
  constructor() {
    this.agentAddress = null
    this.questionHistory = []
    this.init()
  }

  async init() {
    this.setupEventListeners()
    await this.checkAgentStatus()
    this.loadHistory()
  }

  setupEventListeners() {
    const form = document.getElementById("questionForm")
    form.addEventListener("submit", (e) => this.handleSubmit(e))
  }

  async checkAgentStatus() {
    try {
      const response = await fetch("/api/agent/info")
      const data = await response.json()

      this.agentAddress = data.address
      this.updateAgentStatus(true)
    } catch (error) {
      console.error("Error checking agent status:", error)
      this.updateAgentStatus(false)
    }
  }

  updateAgentStatus(isOnline) {
    const statusElement = document.getElementById("agentStatus")
    const indicator = statusElement.querySelector(".status-indicator")
    const text = statusElement.querySelector(".status-text")

    if (isOnline) {
      indicator.style.backgroundColor = "#10B981"
      text.textContent = "Agent Online"
    } else {
      indicator.style.backgroundColor = "#EF4444"
      text.textContent = "Agent Offline"
    }
  }

  async handleSubmit(e) {
    e.preventDefault()

    const question = document.getElementById("question").value
    const conceptType = document.getElementById("conceptType").value
    const difficultyLevel = document.getElementById("difficultyLevel").value
    const studentId = document.getElementById("studentId").value

    if (!question.trim()) {
      alert("Please enter a question")
      return
    }

    this.submitQuestion(question, conceptType, difficultyLevel, studentId)
  }

  async submitQuestion(question, conceptType, difficultyLevel, studentId) {
    const submitBtn = document.getElementById("submitBtn")
    const btnText = submitBtn.querySelector(".btn-text")
    const btnLoader = submitBtn.querySelector(".btn-loader")

    // Show loading state
    submitBtn.disabled = true
    btnText.style.display = "none"
    btnLoader.style.display = "inline-block"

    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          concept_type: conceptType,
          difficulty_level: difficultyLevel,
          student_id: studentId || null,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        // Generate mock response for demo
        this.displayResponse(question, conceptType, difficultyLevel)
        this.addToHistory(question)
        document.getElementById("questionForm").reset()
      } else {
        alert("Error: " + data.error)
      }
    } catch (error) {
      console.error("Error submitting question:", error)
      alert("Error submitting question. Please try again.")
    } finally {
      // Hide loading state
      submitBtn.disabled = false
      btnText.style.display = "inline"
      btnLoader.style.display = "none"
    }
  }

  displayResponse(question, conceptType, difficultyLevel) {
    const responseContainer = document.getElementById("responseContainer")

    // Generate mock response based on concept type
    const mockResponse = this.generateMockResponse(question, conceptType, difficultyLevel)

    responseContainer.innerHTML = `
            <div class="response-content">
                <div class="response-section">
                    <h3>Explanation</h3>
                    <p>${mockResponse.explanation}</p>
                </div>

                <div class="response-section">
                    <h3>Key Points</h3>
                    <ul class="key-points">
                        ${mockResponse.keyPoints.map((point) => `<li>${point}</li>`).join("")}
                    </ul>
                </div>

                <div class="response-section">
                    <h3>Examples</h3>
                    <ul class="examples">
                        ${mockResponse.examples.map((example) => `<li>${example}</li>`).join("")}
                    </ul>
                </div>

                <div class="response-section">
                    <h3>Practice Problems</h3>
                    <ul class="practice-problems">
                        ${mockResponse.practiceProblems.map((problem) => `<li>${problem}</li>`).join("")}
                    </ul>
                </div>
            </div>
        `
  }

  generateMockResponse(question, conceptType, difficultyLevel) {
    const responses = {
      mathematics: {
        explanation:
          "Mathematics is the study of numbers, quantities, and shapes. Your question touches on fundamental concepts that are essential for understanding more advanced topics.",
        keyPoints: [
          "Focus on understanding the core concept",
          "Practice with multiple examples",
          "Connect to real-world applications",
        ],
        examples: [
          "Example 1: Basic application",
          "Example 2: Intermediate use case",
          "Example 3: Advanced application",
        ],
        practiceProblems: [
          "Practice Problem 1: Apply the concept to a new scenario",
          "Practice Problem 2: Solve a variation",
          "Practice Problem 3: Combine with related concepts",
        ],
      },
      programming: {
        explanation:
          "Programming is the art of writing instructions for computers. Your question relates to important programming concepts that will help you write better code.",
        keyPoints: [
          "Understand the syntax and semantics",
          "Practice writing code regularly",
          "Study existing code examples",
        ],
        examples: ["Example 1: Simple implementation", "Example 2: Real-world use case", "Example 3: Advanced pattern"],
        practiceProblems: [
          "Practice Problem 1: Write a simple program",
          "Practice Problem 2: Refactor existing code",
          "Practice Problem 3: Build a project",
        ],
      },
      algorithm: {
        explanation:
          "Algorithms are step-by-step procedures for solving problems. Understanding algorithms is crucial for writing efficient code.",
        keyPoints: [
          "Understand the algorithm's logic",
          "Analyze time and space complexity",
          "Practice implementing variations",
        ],
        examples: ["Example 1: Linear search", "Example 2: Binary search", "Example 3: Sorting algorithms"],
        practiceProblems: [
          "Practice Problem 1: Implement the algorithm",
          "Practice Problem 2: Optimize for performance",
          "Practice Problem 3: Apply to new problems",
        ],
      },
      data_structure: {
        explanation:
          "Data structures are ways to organize and store data efficiently. Choosing the right data structure is key to writing performant code.",
        keyPoints: [
          "Understand the structure's properties",
          "Know when to use each structure",
          "Practice implementing them",
        ],
        examples: ["Example 1: Array operations", "Example 2: Linked list traversal", "Example 3: Tree operations"],
        practiceProblems: [
          "Practice Problem 1: Implement the structure",
          "Practice Problem 2: Solve problems using it",
          "Practice Problem 3: Compare with alternatives",
        ],
      },
    }

    return responses[conceptType] || responses.mathematics
  }

  addToHistory(question) {
    this.questionHistory.unshift({
      question: question.substring(0, 50) + (question.length > 50 ? "..." : ""),
      timestamp: new Date().toLocaleTimeString(),
    })

    this.updateHistoryDisplay()
    this.saveHistory()
  }

  updateHistoryDisplay() {
    const historyList = document.getElementById("historyList")

    if (this.questionHistory.length === 0) {
      historyList.innerHTML = '<li class="empty-history">No questions asked yet</li>'
      return
    }

    historyList.innerHTML = this.questionHistory
      .map(
        (item, index) => `
                <li onclick="client.selectHistoryItem(${index})">
                    <strong>${item.question}</strong>
                    <br>
                    <small>${item.timestamp}</small>
                </li>
            `,
      )
      .join("")
  }

  selectHistoryItem(index) {
    const item = this.questionHistory[index]
    document.getElementById("question").value = item.question
    document.getElementById("question").focus()
  }

  saveHistory() {
    localStorage.setItem("eduagent_history", JSON.stringify(this.questionHistory))
  }

  loadHistory() {
    const saved = localStorage.getItem("eduagent_history")
    if (saved) {
      this.questionHistory = JSON.parse(saved)
      this.updateHistoryDisplay()
    }
  }
}

// Initialize the client when DOM is ready
let client
document.addEventListener("DOMContentLoaded", () => {
  client = new EduAgentClient()
})
