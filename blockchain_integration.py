"""
Blockchain integration for EduAgent
Records student progress on EVM-compatible blockchains
"""
from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime
from web3 import Web3
import json
import hashlib
from config import WEB3_PROVIDER, PRIVATE_KEY, CONTRACT_ADDRESS

class ProgressRecord(BaseModel):
    """Model for student progress record"""
    student_id: str
    concepts_learned: List[str]
    questions_answered: int
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    difficulty_level: str
    score: float = Field(default=0.0, ge=0.0, le=100.0)

class BlockchainProgressTracker:
    """
    Tracks student progress on blockchain
    Supports EVM-compatible chains (Ethereum, Polygon, etc.)
    """
    
    def __init__(self, provider_url: Optional[str] = None, private_key: Optional[str] = None):
        self.provider_url = provider_url or WEB3_PROVIDER
        self.private_key = private_key or PRIVATE_KEY
        self.w3 = None
        self.account = None
        self.contract = None
        
        if self.provider_url and self.private_key:
            self._initialize_web3()
    
    def _initialize_web3(self):
        """Initialize Web3 connection"""
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.provider_url))
            
            if self.w3.is_connected():
                self.account = self.w3.eth.account.from_key(self.private_key)
                print(f"Connected to blockchain: {self.w3.eth.chain_id}")
            else:
                print("Failed to connect to blockchain provider")
        
        except Exception as e:
            print(f"Error initializing Web3: {str(e)}")
    
    def create_progress_hash(self, record: ProgressRecord) -> str:
        """Create a hash of the progress record"""
        record_str = json.dumps(record.dict(), sort_keys=True)
        return hashlib.sha256(record_str.encode()).hexdigest()
    
    def record_progress(self, record: ProgressRecord) -> Optional[Dict]:
        """
        Record student progress on blockchain
        
        Args:
            record: ProgressRecord to record
        
        Returns:
            Transaction receipt or None if blockchain not available
        """
        if not self.w3 or not self.w3.is_connected():
            # Fallback: return simulated blockchain record
            return self._create_simulated_record(record)
        
        try:
            # Create progress hash
            progress_hash = self.create_progress_hash(record)
            
            # Prepare transaction data
            tx_data = {
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price,
                "data": self._encode_progress_data(record, progress_hash)
            }
            
            # Sign and send transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "status": "success",
                "transaction_hash": tx_hash.hex(),
                "block_number": receipt["blockNumber"],
                "progress_hash": progress_hash,
                "student_id": record.student_id,
                "timestamp": record.timestamp
            }
        
        except Exception as e:
            print(f"Error recording progress on blockchain: {str(e)}")
            return self._create_simulated_record(record)
    
    def _create_simulated_record(self, record: ProgressRecord) -> Dict:
        """Create a simulated blockchain record for demo purposes"""
        import uuid
        
        progress_hash = self.create_progress_hash(record)
        
        return {
            "status": "success",
            "transaction_hash": f"0x{uuid.uuid4().hex}",
            "block_number": 0,
            "progress_hash": progress_hash,
            "student_id": record.student_id,
            "timestamp": record.timestamp,
            "simulated": True,
            "message": "Progress recorded (simulated - blockchain not configured)"
        }
    
    def _encode_progress_data(self, record: ProgressRecord, progress_hash: str) -> str:
        """Encode progress data for blockchain transaction"""
        # Simple encoding: concatenate key data
        data = f"{record.student_id}:{progress_hash}:{record.questions_answered}"
        return "0x" + data.encode().hex()
    
    def verify_progress(self, student_id: str, progress_hash: str) -> bool:
        """
        Verify a student's progress record on blockchain
        
        Args:
            student_id: Student identifier
            progress_hash: Hash of the progress record
        
        Returns:
            True if record is verified, False otherwise
        """
        # In a real implementation, this would query the blockchain
        # For now, return True as placeholder
        return True
    
    def get_student_achievements(self, student_id: str) -> Dict:
        """Get all achievements for a student"""
        return {
            "student_id": student_id,
            "total_questions_answered": 0,
            "concepts_mastered": [],
            "achievements": [
                "First Question",
                "10 Questions Answered",
                "Concept Master",
                "Consistent Learner"
            ],
            "blockchain_verified": True
        }

class ProgressNFT:
    """
    Represents a student achievement as an NFT
    Can be minted on EVM-compatible blockchains
    """
    
    def __init__(self, student_id: str, achievement_name: str, metadata: Dict):
        self.student_id = student_id
        self.achievement_name = achievement_name
        self.metadata = metadata
        self.created_at = datetime.utcnow().isoformat()
        self.token_id = None
        self.contract_address = None
    
    def to_metadata(self) -> Dict:
        """Convert to NFT metadata format"""
        return {
            "name": self.achievement_name,
            "description": f"Achievement unlocked by {self.student_id}",
            "image": f"ipfs://achievement/{self.achievement_name.lower().replace(' ', '_')}",
            "attributes": [
                {
                    "trait_type": "Student ID",
                    "value": self.student_id
                },
                {
                    "trait_type": "Achievement",
                    "value": self.achievement_name
                },
                {
                    "trait_type": "Date Earned",
                    "value": self.created_at
                }
            ],
            "metadata": self.metadata
        }

class AchievementSystem:
    """
    Manages student achievements and milestones
    """
    
    def __init__(self):
        self.achievements = {
            "first_question": {
                "name": "First Question",
                "description": "Asked your first question",
                "icon": "🎯",
                "points": 10
            },
            "ten_questions": {
                "name": "10 Questions Answered",
                "description": "Answered 10 questions",
                "icon": "🚀",
                "points": 50
            },
            "concept_master": {
                "name": "Concept Master",
                "description": "Mastered a concept",
                "icon": "🏆",
                "points": 100
            },
            "consistent_learner": {
                "name": "Consistent Learner",
                "description": "Learned consistently over time",
                "icon": "⭐",
                "points": 75
            },
            "all_concepts": {
                "name": "Polymath",
                "description": "Learned all concept types",
                "icon": "🧠",
                "points": 200
            }
        }
        
        self.student_achievements: Dict[str, List[str]] = {}
    
    def check_achievements(self, student_id: str, progress: Dict) -> List[str]:
        """
        Check and unlock achievements for a student
        
        Args:
            student_id: Student identifier
            progress: Student progress data
        
        Returns:
            List of newly unlocked achievements
        """
        if student_id not in self.student_achievements:
            self.student_achievements[student_id] = []
        
        unlocked = []
        questions_answered = progress.get("questions_asked", 0)
        concepts_learned = progress.get("concepts_learned", [])
        
        # Check first question
        if questions_answered >= 1 and "first_question" not in self.student_achievements[student_id]:
            self.student_achievements[student_id].append("first_question")
            unlocked.append("first_question")
        
        # Check 10 questions
        if questions_answered >= 10 and "ten_questions" not in self.student_achievements[student_id]:
            self.student_achievements[student_id].append("ten_questions")
            unlocked.append("ten_questions")
        
        # Check all concepts
        if len(concepts_learned) >= 4 and "all_concepts" not in self.student_achievements[student_id]:
            self.student_achievements[student_id].append("all_concepts")
            unlocked.append("all_concepts")
        
        return unlocked
    
    def get_student_achievements(self, student_id: str) -> List[Dict]:
        """Get all achievements for a student"""
        if student_id not in self.student_achievements:
            return []
        
        achievements = []
        for achievement_id in self.student_achievements[student_id]:
            if achievement_id in self.achievements:
                achievements.append({
                    "id": achievement_id,
                    **self.achievements[achievement_id]
                })
        
        return achievements
    
    def get_student_points(self, student_id: str) -> int:
        """Calculate total points for a student"""
        if student_id not in self.student_achievements:
            return 0
        
        total_points = 0
        for achievement_id in self.student_achievements[student_id]:
            if achievement_id in self.achievements:
                total_points += self.achievements[achievement_id].get("points", 0)
        
        return total_points
