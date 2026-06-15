"""
manna.py  MANNA Budget Layer
Budget allocation, Inventor's Covenant (1%), ledger logging, vault tracking.
"""
from datetime import datetime
from typing import List, Dict

class MANNABudgetLayer:
      COVENANT_RATE = 0.01

    def __init__(self, total_budget: float):
              self.total_budget  = total_budget
              self.vault_balance = total_budget
              self.covenant_fund = 0.0
              self.ledger: List[Dict] = []

    def allocate(self, amount: float) -> bool:
              covenant = amount * self.COVENANT_RATE
              total    = amount + covenant
              if total > self.vault_balance:
                            self.ledger.append({"ts": datetime.utcnow().isoformat(), "event": "REJECTED", "amount": amount})
                            return False
                        self.vault_balance  -= total
        self.covenant_fund  += covenant
        self.ledger.append({"ts": datetime.utcnow().isoformat(), "event": "ALLOCATED",
                                                        "amount": amount, "covenant": covenant, "balance": self.vault_balance})
        return True

    def summary(self) -> Dict:
              return {"total_budget": self.total_budget, "vault_balance": self.vault_balance,
                                      "covenant_fund": self.covenant_fund, "transactions": len(self.ledger)}
