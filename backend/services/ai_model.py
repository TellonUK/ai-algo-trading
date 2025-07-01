import random
from typing import Literal
from services.history_loader import OHLCData


DecisionType = Literal["buy", "sell", "hold"]


class AIModel:
    def __init__(self):
        self.decisions = ["buy", "sell", "hold"]
        self.weights = [0.3, 0.3, 0.4]  # Slightly favor hold
    
    def make_decision(self, ohlc_bar: OHLCData) -> DecisionType:
        price_change = ((ohlc_bar.close - ohlc_bar.open) / ohlc_bar.open) * 100
        
        if price_change > 0.5:
            return "buy"
        elif price_change < -0.5:
            return "sell"
        else:
            return random.choices(self.decisions, weights=self.weights)[0]


ai_model = AIModel()