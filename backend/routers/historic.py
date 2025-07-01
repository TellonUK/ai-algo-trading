from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from services.history_loader import load_history_data, OHLCData

router = APIRouter()


@router.get("/history", response_model=List[OHLCData])
async def get_historic_data(
    symbol: str = Query(..., description="Stock symbol (e.g., TSLA)"),
    timeframe: str = Query(..., description="Timeframe (1min, 5min, 30min, 1day)"),
    start: Optional[str] = Query(None, description="Start date in ISO 8601 format"),
    end: Optional[str] = Query(None, description="End date in ISO 8601 format"),
    limit: int = Query(500, ge=1, le=5000, description="Maximum number of records to return")
):
    try:
        valid_timeframes = ["1min", "5min", "30min", "1day"]
        if timeframe not in valid_timeframes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timeframe. Must be one of: {', '.join(valid_timeframes)}"
            )
        
        data = load_history_data(symbol, timeframe, start, end, limit)
        return data
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Historical data not found for symbol {symbol} with timeframe {timeframe}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")