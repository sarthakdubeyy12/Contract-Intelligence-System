from typing import Dict, List

class ContractScoringService:
    """
    Provides scoring and gap analysis for parsed contracts.
    """

    def __init__(self):
        # Define expected clauses and weights
        self.expected_clauses = {
            "termination": 20,
            "confidentiality": 15,
            "governing_law": 10,
            "liability": 20,
            "payment_terms": 15,
            "force_majeure": 10,
            "dispute_resolution": 10,
        }

    def score_contract(self, parsed_data: Dict) -> Dict:
        """
        Scores a parsed contract and identifies missing/weak clauses.
        parsed_data: { "clauses": ["termination", "confidentiality", ...] }
        """
        found_clauses = parsed_data.get("clauses", [])
        total_score = 0
        max_score = sum(self.expected_clauses.values())
        missing_clauses: List[str] = []

        for clause, weight in self.expected_clauses.items():
            if clause in found_clauses:
                total_score += weight
            else:
                missing_clauses.append(clause)

        # percentage
        percentage = round((total_score / max_score) * 100, 2)

        return {
            "total_score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "missing_clauses": missing_clauses,
            "found_clauses": found_clauses,
        }