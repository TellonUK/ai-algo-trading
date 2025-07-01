import os
import httpx
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from services.history_loader import OHLCData

load_dotenv()


class PolygonClient:
    def __init__(self):
        self.api_key = os.getenv("POLYGON_API_KEY")
        self.base_url = "https://api.polygon.io"
    
    async def get_aggregates(
        self,
        symbol: str,
        timeframe: str,
        start: str,
        end: str,
        limit: int = 500
    ) -> List[OHLCData]:
        if not self.api_key:
            raise ValueError("POLYGON_API_KEY not found in environment variables")
        
        multiplier, timespan = self._parse_timeframe(timeframe)
        
        url = f"{self.base_url}/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{start}/{end}"
        params = {
            "apikey": self.api_key,
            "limit": min(limit, 5000)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "results" not in data:
                return []
            
            ohlc_data = []
            for result in data["results"]:
                timestamp = datetime.fromtimestamp(result["t"] / 1000)
                
                ohlc_data.append(OHLCData(
                    timestamp=timestamp.isoformat(),
                    open=result["o"],
                    high=result["h"],
                    low=result["l"],
                    close=result["c"]
                ))
            
            return ohlc_data
    
    def _parse_timeframe(self, timeframe: str) -> tuple[int, str]:
        if timeframe == "1min":
            return 1, "minute"
        elif timeframe == "5min":
            return 5, "minute"
        elif timeframe == "30min":
            return 30, "minute"
        elif timeframe == "1day":
            return 1, "day"
        else:
            raise ValueError(f"Unsupported timeframe: {timeframe}")


polygon_client = PolygonClient()