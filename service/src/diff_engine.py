from typing import List, Dict, Any
from src.models import GrantRequirement

class DiffEngine:
    """
    Logic for comparing grant requirements to identify changes.
    """
    
    def compare_requirements(self, old_reqs: List[GrantRequirement], new_reqs: List[GrantRequirement]) -> List[Dict[str, Any]]:
        """
        Compares two lists of requirements and returns differences.
        
        Args:
            old_reqs: Requirements from a previous cycle.
            new_reqs: Requirements from the current cycle.
            
        Returns:
            List[Dict]: A list of changes detected.
        """
        changes = []
        
        # Simple map by category for comparison
        old_map = {r.category: r for r in old_reqs}
        new_map = {r.category: r for r in new_reqs}
        
        all_categories = set(old_map.keys()) | set(new_map.keys())
        
        for cat in all_categories:
            if cat not in old_map:
                changes.append({
                    "category": cat,
                    "type": "ADDED",
                    "detail": "New requirement category introduced."
                })
            elif cat not in new_map:
                changes.append({
                    "category": cat,
                    "type": "REMOVED",
                    "detail": "Requirement category removed."
                })
            else:
                # Compare details
                old_r = old_map[cat]
                new_r = new_map[cat]
                
                if old_r.max_words != new_r.max_words:
                    changes.append({
                        "category": cat,
                        "type": "MODIFIED",
                        "field": "max_words",
                        "old_value": old_r.max_words,
                        "new_value": new_r.max_words,
                        "detail": f"Word limit changed from {old_r.max_words} to {new_r.max_words}"
                    })
                    
        return changes
