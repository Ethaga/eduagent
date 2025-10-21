"""
Core reasoning engine for EduAgent
Handles concept analysis, explanation generation, and learning strategies
"""
import json
from typing import List, Dict, Optional
from models import ExplanationResponse, ConceptType

class ReasoningEngine:
    """
    Handles the core logic for understanding questions and generating explanations
    """
    
    def __init__(self):
        """Initialize the reasoning engine with knowledge base"""
        self.knowledge_base = self._initialize_knowledge_base()
        self.explanation_strategies = self._initialize_strategies()
    
    def _initialize_knowledge_base(self) -> Dict:
        """Initialize a basic knowledge base for concepts"""
        return {
            "mathematics": {
                "algebra": {
                    "description": "Study of mathematical symbols and rules",
                    "key_concepts": ["variables", "equations", "functions", "polynomials"],
                    "examples": ["2x + 3 = 7", "f(x) = x^2 + 2x + 1"]
                },
                "calculus": {
                    "description": "Study of change and motion",
                    "key_concepts": ["derivatives", "integrals", "limits", "continuity"],
                    "examples": ["d/dx(x^2) = 2x", "∫x dx = x^2/2 + C"]
                },
                "geometry": {
                    "description": "Study of shapes and spaces",
                    "key_concepts": ["angles", "triangles", "circles", "vectors"],
                    "examples": ["Area of circle = πr^2", "Pythagorean theorem: a^2 + b^2 = c^2"]
                }
            },
            "programming": {
                "python": {
                    "description": "High-level programming language",
                    "key_concepts": ["variables", "loops", "functions", "classes", "decorators"],
                    "examples": ["for i in range(10):", "def function_name(param):"]
                },
                "data_structures": {
                    "description": "Ways to organize and store data",
                    "key_concepts": ["arrays", "linked_lists", "trees", "graphs", "hash_tables"],
                    "examples": ["list = [1, 2, 3]", "dict = {'key': 'value'}"]
                },
                "algorithms": {
                    "description": "Step-by-step procedures for solving problems",
                    "key_concepts": ["sorting", "searching", "dynamic_programming", "greedy"],
                    "examples": ["Binary search", "Merge sort", "Dijkstra's algorithm"]
                }
            }
        }
    
    def _initialize_strategies(self) -> Dict:
        """Initialize explanation strategies"""
        return {
            "beginner": {
                "approach": "Simple, step-by-step with analogies",
                "depth": "surface",
                "examples_count": 2
            },
            "intermediate": {
                "approach": "Balanced explanation with theory and practice",
                "depth": "moderate",
                "examples_count": 3
            },
            "advanced": {
                "approach": "In-depth with mathematical rigor",
                "depth": "deep",
                "examples_count": 4
            }
        }
    
    def analyze_question(self, question: str, concept_type: ConceptType) -> Dict:
        """
        Analyze a question to extract key information
        """
        # Simple keyword extraction and concept identification
        keywords = question.lower().split()
        
        analysis = {
            "question": question,
            "keywords": keywords,
            "concept_type": concept_type.value,
            "identified_concepts": self._identify_concepts(keywords, concept_type),
            "complexity_score": self._calculate_complexity(question)
        }
        
        return analysis
    
    def _identify_concepts(self, keywords: List[str], concept_type: ConceptType) -> List[str]:
        """Identify relevant concepts from keywords"""
        concepts = []
        
        if concept_type == ConceptType.MATHEMATICS:
            math_keywords = ["algebra", "calculus", "geometry", "derivative", "integral", 
                           "equation", "function", "matrix", "vector"]
            concepts = [k for k in keywords if k in math_keywords]
        
        elif concept_type == ConceptType.PROGRAMMING:
            prog_keywords = ["python", "loop", "function", "class", "array", "list", 
                           "dictionary", "algorithm", "sorting", "searching"]
            concepts = [k for k in keywords if k in prog_keywords]
        
        return concepts if concepts else ["general"]
    
    def _calculate_complexity(self, question: str) -> float:
        """Calculate question complexity (0-1 scale)"""
        # Simple heuristic: longer questions tend to be more complex
        word_count = len(question.split())
        complexity = min(word_count / 50, 1.0)
        return complexity
    
    def generate_explanation(self, 
                            question: str,
                            concept_type: ConceptType,
                            difficulty_level: str = "intermediate") -> ExplanationResponse:
        """
        Generate a comprehensive explanation for a question
        """
        # Analyze the question
        analysis = self.analyze_question(question, concept_type)
        
        # Get strategy for difficulty level
        strategy = self.explanation_strategies.get(difficulty_level, 
                                                   self.explanation_strategies["intermediate"])
        
        # Generate explanation components
        explanation = self._build_explanation(analysis, strategy)
        key_points = self._extract_key_points(analysis, strategy)
        examples = self._generate_examples(analysis, strategy)
        practice_problems = self._suggest_practice_problems(analysis, strategy)
        
        return ExplanationResponse(
            question=question,
            explanation=explanation,
            key_points=key_points,
            examples=examples,
            practice_problems=practice_problems,
            difficulty_level=difficulty_level,
            concept_type=concept_type.value
        )
    
    def _build_explanation(self, analysis: Dict, strategy: Dict) -> str:
        """Build the main explanation text"""
        concepts = analysis.get("identified_concepts", ["general"])
        approach = strategy.get("approach", "")
        
        explanation = f"Based on your question about {', '.join(concepts)}, here's an explanation using a {approach} approach:\n\n"
        
        # Add concept-specific explanation
        if "algebra" in concepts:
            explanation += "Algebra is the branch of mathematics dealing with symbols and the rules for manipulating them. "
            explanation += "It allows us to write general rules and solve problems with unknown values.\n"
        
        elif "calculus" in concepts:
            explanation += "Calculus is the mathematical study of continuous change. "
            explanation += "It has two main branches: derivatives (rates of change) and integrals (accumulation).\n"
        
        elif "python" in concepts:
            explanation += "Python is a versatile, high-level programming language known for its readability. "
            explanation += "It's widely used in data science, web development, and automation.\n"
        
        else:
            explanation += "This is an interesting question that touches on fundamental concepts. "
            explanation += "Let me break it down into manageable parts.\n"
        
        return explanation
    
    def _extract_key_points(self, analysis: Dict, strategy: Dict) -> List[str]:
        """Extract key points from the analysis"""
        concepts = analysis.get("identified_concepts", ["general"])
        
        key_points = [
            f"Focus on understanding {concepts[0] if concepts else 'the core concept'}",
            "Practice with multiple examples to solidify understanding",
            "Connect this concept to real-world applications"
        ]
        
        return key_points
    
    def _generate_examples(self, analysis: Dict, strategy: Dict) -> List[str]:
        """Generate relevant examples"""
        examples_count = strategy.get("examples_count", 2)
        concepts = analysis.get("identified_concepts", ["general"])
        
        examples = []
        
        if "algebra" in concepts:
            examples = [
                "Example 1: Solving 2x + 5 = 13 → x = 4",
                "Example 2: Factoring x² + 5x + 6 = (x + 2)(x + 3)",
                "Example 3: Graphing linear functions y = mx + b"
            ]
        
        elif "python" in concepts:
            examples = [
                "Example 1: for loop - for i in range(5): print(i)",
                "Example 2: function definition - def greet(name): return f'Hello, {name}'",
                "Example 3: list comprehension - squares = [x**2 for x in range(10)]"
            ]
        
        else:
            examples = [
                f"Example 1: Basic application of {concepts[0] if concepts else 'the concept'}",
                f"Example 2: Intermediate use case",
                f"Example 3: Advanced application"
            ]
        
        return examples[:examples_count]
    
    def _suggest_practice_problems(self, analysis: Dict, strategy: Dict) -> List[str]:
        """Suggest practice problems"""
        concepts = analysis.get("identified_concepts", ["general"])
        
        problems = [
            f"Practice Problem 1: Apply {concepts[0] if concepts else 'this concept'} to a new scenario",
            f"Practice Problem 2: Solve a variation of the original problem",
            f"Practice Problem 3: Combine this concept with another related concept"
        ]
        
        return problems
