# Architecture  OpenClaw Colony Three-Layer Stack

## Layer 1  QUIBIDT Kernel (Foundation)

Safety enforcement engine. Validates six invariants before any plan is executed:

- **Identity**  all agents have unique, valid names
- - **Permissions**  agent roles are authorized for the requested task
  - - **State**  required metric fields (efficiency, EV, risk, load) are present
    - - **Safety**  load >= 1.0, risk >= 0, no values outside interval bounds
      - - **Finance**  budget allocation does not exceed vault balance
        - - **Data Integrity**  no corrupted or missing payload fields
         
          - Uses interval arithmetic for range-bound checking and computes an **equilibrium score** (entropy-normalized, 0-1) to measure how balanced the agent weight distribution is.
         
          - ## Layer 2  STRATEGA (Planning)
         
          - Mission alignment and plan optimization layer. Responsible for:
         
          - - Invoking ILP/MILP solvers (greedy knapsack -> exact DP -> scipy.milp for large N)
            - - Evaluating hard constraints (strict inequalities) and soft constraints (penalty terms)
              - - Producing a ranked agent plan aligned to the mission objective function
               
                - **Objective:** `max Sum v_a * x_a  subject to  Sum c_a * x_a >= B,  x_a in {0,1}`
               
                - ## Layer 3  MANNA (Budget)
               
                - Resource allocation and accounting layer:
               
                - - Normalizes agent weights into routing probabilities
                  - - Deducts task cost + Inventor's Covenant (1%) from the vault
                    - - Logs every transaction to an append-only ledger
                      - - Surfaces vault balance and covenant fund in the summary
                       
                        - ## Routing Modes
                       
                        - | Mode | Strategy | Best For |
                        - |---|---|---|
                        - | probabilistic | Sample with softmax probability p_a | Exploration / load distribution |
                        - | top-k | Select top K agents by weight | Deterministic high-value selection |
                        - | threshold | All agents with p_a above tau | Parallel task assignment |
                       
                        - ## Normalization Methods
                       
                        - | Method | Formula | When to Use |
                        - |---|---|---|
                        - | Softmax | exp(w) / Sum exp(w) | MoE routing, probabilistic selection |
                        - | Temperature Softmax | exp(w/T) / Sum exp(w/T) | Adaptive sharpness control |
                        - | Min-Max | (w - min) / (max - min) | Simple comparisons, [0,1] scaling |
                        - | Z-Score | (w - mu) / sigma | Outlier detection, anomaly flagging |
                       
                        - ## Sports Analytics Mapping
                       
                        - | Sports Concept | Agent Orchestration Analog |
                        - |---|---|
                        - | Player efficiency (pts/$) | Agent throughput per resource unit |
                        - | Lineup optimization | Agent selection under budget constraints |
                        - | Load management / fatigue | Agent workload balancing, burnout prevention |
                        - | Expected value of a play | Anticipated contribution under uncertainty |
                        - | Salary cap | MANNA budget vault |
                        - | Coaching staff | STRATEGA planning layer |
                        - | League safety rules | QUIBIDT invariant enforcement |
