from dataclasses import dataclass, asdict
from typing import Optional, Dict

@dataclass
class Task:
    """Core data structure for a compliance/log task.
    Using dataclass because it gives us __init__, __repr__, and equality for free."""
    id: int
    date: str  # ISO format YYYY-MM-DD - sortable and standard
    description: str
    status: str  # pending | in_progress | completed
    notes: Optional[str] = None
    completed_date: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to plain dict for JSON serialization"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Task":
        """Factory method - reconstruct object from saved data"""
        return cls(**data)
