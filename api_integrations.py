"""
External API integrations for EduAgent
Fetches educational content, practice problems, and learning resources
"""
import aiohttp
import asyncio
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class QuizAPIClient:
    """Client for fetching quiz and practice problems"""
    
    BASE_URL = "https://quizapi.io/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    async def get_practice_problems(self, 
                                   category: str, 
                                   difficulty: str = "medium",
                                   limit: int = 3) -> List[Dict]:
        """
        Fetch practice problems from QuizAPI
        
        Args:
            category: Topic category (e.g., 'programming', 'mathematics')
            difficulty: Problem difficulty level
            limit: Number of problems to fetch
        
        Returns:
            List of practice problems
        """
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "category": category,
                    "difficulty": difficulty,
                    "limit": limit
                }
                
                if self.api_key:
                    params["apiKey"] = self.api_key
                
                async with session.get(f"{self.BASE_URL}/questions", params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self._format_problems(data)
                    else:
                        logger.error(f"QuizAPI error: {resp.status}")
                        return []
        
        except Exception as e:
            logger.error(f"Error fetching practice problems: {str(e)}")
            return []
    
    def _format_problems(self, raw_data: List[Dict]) -> List[Dict]:
        """Format raw API response into standardized format"""
        formatted = []
        
        for problem in raw_data:
            formatted.append({
                "question": problem.get("question", ""),
                "options": problem.get("answers", {}),
                "correct_answer": problem.get("correct_answer", ""),
                "explanation": problem.get("explanation", ""),
                "difficulty": problem.get("difficulty", "medium")
            })
        
        return formatted


class WikipediaAPIClient:
    """Client for fetching educational content from Wikipedia"""
    
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    
    async def search_concept(self, concept: str, max_results: int = 3) -> List[Dict]:
        """
        Search for educational concepts on Wikipedia
        
        Args:
            concept: The concept to search for
            max_results: Maximum number of results
        
        Returns:
            List of search results with summaries
        """
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": concept,
                    "srwhat": "text",
                    "srlimit": max_results,
                    "format": "json"
                }
                
                async with session.get(self.BASE_URL, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self._format_search_results(data)
                    else:
                        logger.error(f"Wikipedia API error: {resp.status}")
                        return []
        
        except Exception as e:
            logger.error(f"Error searching Wikipedia: {str(e)}")
            return []
    
    async def get_page_summary(self, page_title: str) -> Optional[str]:
        """
        Get a summary of a Wikipedia page
        
        Args:
            page_title: Title of the Wikipedia page
        
        Returns:
            Page summary or None if not found
        """
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "action": "query",
                    "titles": page_title,
                    "prop": "extracts",
                    "explaintext": True,
                    "exintro": True,
                    "format": "json"
                }
                
                async with session.get(self.BASE_URL, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        pages = data.get("query", {}).get("pages", {})
                        
                        for page_id, page_data in pages.items():
                            if "extract" in page_data:
                                return page_data["extract"][:500]  # Return first 500 chars
                    
                    return None
        
        except Exception as e:
            logger.error(f"Error fetching Wikipedia page: {str(e)}")
            return None
    
    def _format_search_results(self, raw_data: Dict) -> List[Dict]:
        """Format Wikipedia search results"""
        formatted = []
        
        search_results = raw_data.get("query", {}).get("search", [])
        
        for result in search_results:
            formatted.append({
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "page_id": result.get("pageid", "")
            })
        
        return formatted


class CodeExamplesAPIClient:
    """Client for fetching code examples and snippets"""
    
    BASE_URL = "https://api.github.com"
    
    async def search_code_examples(self, 
                                  language: str, 
                                  topic: str,
                                  max_results: int = 5) -> List[Dict]:
        """
        Search for code examples on GitHub
        
        Args:
            language: Programming language (e.g., 'python', 'javascript')
            topic: Topic to search for
            max_results: Maximum number of results
        
        Returns:
            List of code examples
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Search for repositories with the topic
                search_query = f"language:{language} topic:{topic}"
                params = {
                    "q": search_query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": max_results
                }
                
                async with session.get(f"{self.BASE_URL}/search/repositories", params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self._format_code_examples(data)
                    else:
                        logger.error(f"GitHub API error: {resp.status}")
                        return []
        
        except Exception as e:
            logger.error(f"Error fetching code examples: {str(e)}")
            return []
    
    def _format_code_examples(self, raw_data: Dict) -> List[Dict]:
        """Format GitHub search results into code examples"""
        formatted = []
        
        repos = raw_data.get("items", [])
        
        for repo in repos:
            formatted.append({
                "name": repo.get("name", ""),
                "description": repo.get("description", ""),
                "url": repo.get("html_url", ""),
                "language": repo.get("language", ""),
                "stars": repo.get("stargazers_count", 0)
            })
        
        return formatted


class EducationalResourceAggregator:
    """
    Aggregates multiple educational APIs to provide comprehensive learning resources
    """
    
    def __init__(self, quiz_api_key: Optional[str] = None):
        self.quiz_client = QuizAPIClient(quiz_api_key)
        self.wiki_client = WikipediaAPIClient()
        self.code_client = CodeExamplesAPIClient()
    
    async def get_comprehensive_learning_resources(self,
                                                   concept: str,
                                                   language: str = "python",
                                                   difficulty: str = "medium") -> Dict:
        """
        Fetch comprehensive learning resources for a concept
        
        Args:
            concept: The concept to learn about
            language: Programming language (if applicable)
            difficulty: Difficulty level
        
        Returns:
            Dictionary with multiple types of learning resources
        """
        # Fetch resources in parallel
        wiki_results, practice_problems, code_examples = await asyncio.gather(
            self.wiki_client.search_concept(concept),
            self.quiz_client.get_practice_problems(concept, difficulty),
            self.code_client.search_code_examples(language, concept)
        )
        
        # Get detailed Wikipedia summary if available
        wiki_summary = None
        if wiki_results:
            wiki_summary = await self.wiki_client.get_page_summary(wiki_results[0]["title"])
        
        return {
            "concept": concept,
            "wikipedia_results": wiki_results,
            "wikipedia_summary": wiki_summary,
            "practice_problems": practice_problems,
            "code_examples": code_examples,
            "difficulty": difficulty
        }
    
    async def get_practice_problems(self, 
                                   concept: str,
                                   difficulty: str = "medium",
                                   limit: int = 3) -> List[Dict]:
        """Get practice problems for a concept"""
        return await self.quiz_client.get_practice_problems(concept, difficulty, limit)
    
    async def get_concept_explanation(self, concept: str) -> Optional[str]:
        """Get a Wikipedia-based explanation for a concept"""
        results = await self.wiki_client.search_concept(concept, max_results=1)
        
        if results:
            return await self.wiki_client.get_page_summary(results[0]["title"])
        
        return None
    
    async def get_code_examples(self, 
                               language: str,
                               topic: str,
                               max_results: int = 5) -> List[Dict]:
        """Get code examples for a topic"""
        return await self.code_client.search_code_examples(language, topic, max_results)
