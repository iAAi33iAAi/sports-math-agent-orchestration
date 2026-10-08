"""MANNA budget allocation and covenant tracking."""
from datetime import datetime, timezone
from typing import Dict, List


class MANNABudgetLayer:
    COVENANT_RATE = 0.01

    def __init__(self, total_budget: float) -> None:
        if total_budget < 0:
            raise ValueError("total_budget must be non-negative.")
        self.total_budget = total_budget
        self.vault_balance = total_budget
        self.covenant_fund = 0.0
        self.ledger: List[Dict] = []

    def allocate(self, amount: float) -> bool:
        if amount < 0:
            raise ValueError("amount must be non-negative.")
        covenant = amount * self.COVENANT_RATE
        total = amount + covenant
        if total > self.vault_balance:
            self.ledger.append(
                {"ts": datetime.now(timezone.utc).isoformat(), "event": "REJECTED", "amount": amount}
            )
            return False

        self.vault_balance -= total
        self.covenant_fund += covenant
        self.ledger.append(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "event": "ALLOCATED",
                "amount": amount,
                "covenant": covenant,
                "balance": self.vault_balance,
            }
        )
        return True

    def summary(self) -> Dict:
        return {
            "total_budget": self.total_budget,
            "vault_balance": self.vault_balance,
            "covenant_fund": self.covenant_fund,
            "transactions": len(self.ledger),
        }
