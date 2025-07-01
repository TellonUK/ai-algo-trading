from fastapi import APIRouter, HTTPException, Query
from typing import List
from services.polygon_client import polygon_client
from services.history_loader import OHLCData

router = APIRouter()


@router.get("/history", response_model=List[OHLCData])
async def get_current_data(
    symbol: str = Query(..., description="Stock symbol (e.g., TSLA)"),
    timeframe: str = Query(..., description="Timeframe (1min, 5min, 30min, 1day)"),
    start: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end: str = Query(..., description="End date in YYYY-MM-DD format"),
    limit: int = Query(500, ge=1, le=5000, description="Maximum number of records to return")
):
    try:
        valid_timeframes = ["1min", "5min", "30min", "1day"]
        if timeframe not in valid_timeframes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timeframe. Must be one of: {', '.join(valid_timeframes)}"
            )
        
        data = await polygon_client.get_aggregates(symbol, timeframe, start, end, limit)
        return data
        
    except ValueError as e:
        if "POLYGON_API_KEY" in str(e):
            raise HTTPException(
                status_code=500,
                detail="Polygon API key not configured"
            )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching data from Polygon.io: {str(e)}"
        )