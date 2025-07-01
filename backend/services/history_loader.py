import os
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class OHLCData(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float


def load_history_data(
    symbol: str,
    timeframe: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 500
) -> List[OHLCData]:
    filename = f"dummyData/{symbol}_full_{timeframe}.txt"
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Data file not found for {symbol} {timeframe}")
    
    data = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(',')
            if len(parts) != 5:
                continue
                
            timestamp_str, open_price, high_price, low_price, close_price = parts
            
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace(' ', 'T'))
                
                if start:
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    if timestamp < start_dt:
                        continue
                
                if end:
                    end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    if timestamp > end_dt:
                        continue
                
                data.append(OHLCData(
                    timestamp=timestamp.isoformat(),
                    open=float(open_price),
                    high=float(high_price),
                    low=float(low_price),
                    close=float(close_price)
                ))
                
            except (ValueError, TypeError):
                continue
    
    return data[:limit]