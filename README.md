# VWMA-Based Traction Strength Strategy

## 1) Strategy Title
**VWMA-Based Traction Strength Strategy**

---

## 2) Strategy Description

This strategy is designed to analyze **market traction** using the **Volume-Weighted Moving Average (VWMA)** of recent low prices. It attempts to measure whether the market is showing **sustained positive or negative pressure** and the **strength of that pressure**.

---

### Step 1 – Data Collection
- For every new bulk data feed, the strategy records the **low price** and **volume** into a rolling 20-period window (using `deque`).  
- Only the most recent 20 periods are kept, ensuring the VWMA reflects up-to-date market activity.  

---

### Step 2 – VWMA Calculation
- VWMA is computed as the weighted average of the last 20 low prices, where each price is weighted by its corresponding trading volume.  

**Formula (VWMA):**

VWMA<sub>t</sub> = ( Σ p<sub>i</sub> · v<sub>i</sub> ) / ( Σ v<sub>i</sub> )

where the sums run over the last N = 20 periods,
p<sub>i</sub> = low price at period i, v<sub>i</sub> = volume at period i.


- If fewer than 20 data points are available, the VWMA is not calculated.  

---

### Step 3 – Traction Detection
- The current market price is compared with the VWMA to determine traction:  
  - **Positive traction** → current price > VWMA.  
  - **Negative traction** → current price < VWMA.  
  - **Unchanged** → if current price equals VWMA, the previous traction is retained.  

---

### Step 4 – Strength Measurement
- For each tick, the strategy computes `price × volume` and adds it to a **running strength sum**.  
- This sum represents how much volume is backing the current traction, i.e., the **momentum strength** of the trend.  

---

### Step 5 – Traction Switch Handling
- When traction changes direction (positive → negative or vice versa):  
  - The event is logged with timestamp, old traction, new traction, and current price.  
  - The **final strength value** for the completed traction phase is reported.  
  - The strength sum is then reset to begin tracking the new traction phase.  

---

### Step 6 – Continuous Monitoring
- Even without a traction switch, the strategy continuously logs the current traction and its growing strength.  
- This provides an evolving view of the **market’s conviction** in the current direction.  

---

### Trading Interpretation
Although the code is designed as a **monitoring tool** rather than an automated trading system, traders could apply the signals in the following ways:  

**1. Entry Signals**  
- A switch to **positive traction** (price > VWMA) with strong accumulated strength may signal the start of an **uptrend**, making it a potential **buy entry**.  
- Conversely, a switch to **negative traction** (price < VWMA) with strong strength could signal the start of a **downtrend**, making it a potential **short/sell entry**.  

**2. Exit Signals**  
- If traction switches direction, it may indicate a **trend reversal**, which traders could use as an **exit point** for existing positions.  

**3. Strength as Confirmation**  
- A **higher accumulated strength value** suggests **volume-backed conviction**, increasing confidence in the traction direction.  
- A **weak or low strength value** may suggest a **false breakout or weak trend**, so traders may wait for more confirmation before acting.  

**4. Risk Management**  
- By observing traction changes early, traders can potentially **reduce losses** from staying too long in a weakening trend.  

---

## 3) Library Used
- **AlgoAPI (AlgoAPIUtil, AlgoAPI_Backtest)** → Provides the algorithmic trading framework, event handling, and logging.  
- **collections.deque** → Efficient fixed-length rolling window for storing recent low prices and volumes for VWMA calculation.  
