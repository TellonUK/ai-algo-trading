import { useEffect, useRef, useState } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

const CandlestickChart = ({ historicalData, decisions, onChartReady }) => {
  const chartContainerRef = useRef();
  const chartRef = useRef();
  const candlestickSeriesRef = useRef();
  const [isChartReady, setIsChartReady] = useState(false);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: 'rgba(42, 46, 57, 0.1)' },
        horzLines: { color: 'rgba(42, 46, 57, 0.1)' },
      },
      crosshair: {
        mode: 1,
      },
      rightPriceScale: {
        borderColor: 'rgba(42, 46, 57, 0.1)',
      },
      timeScale: {
        borderColor: 'rgba(42, 46, 57, 0.1)',
        timeVisible: true,
        secondsVisible: false,
      },
      handleScroll: {
        mouseWheel: true,
        pressedMouseMove: true,
      },
      handleScale: {
        axisPressedMouseMove: true,
        mouseWheel: true,
        pinch: true,
      },
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350'
    });

    chartRef.current = chart;
    candlestickSeriesRef.current = candlestickSeries;
    setIsChartReady(true);

    if (onChartReady) {
      onChartReady({
        chart,
        candlestickSeries,
        addMarker: (marker) => addDecisionMarker(candlestickSeries, marker),
        updateCandle: (candle) => updateCurrentCandle(candlestickSeries, candle),
        appendCandle: (candle) => appendNewCandle(candlestickSeries, candle)
      });
    }

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
          height: chartContainerRef.current.clientHeight,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (chart) {
        chart.remove();
      }
    };
  }, [onChartReady]);

  useEffect(() => {
    if (isChartReady && historicalData && historicalData.length > 0) {
      const formattedData = historicalData.map(item => ({
        time: item.timestamp,
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close
      }));
      candlestickSeriesRef.current.setData(formattedData);
    }
  }, [historicalData, isChartReady]);

  useEffect(() => {
    if (isChartReady && decisions && decisions.length > 0 && candlestickSeriesRef.current) {
      decisions.forEach(decision => {
        addDecisionMarker(candlestickSeriesRef.current, decision);
      });
    }
  }, [decisions, isChartReady]);

  const addDecisionMarker = (series, decision) => {
    if (!decision || !decision.timestamp || !decision.decision || !decision.price) return;

    const marker = {
      time: decision.timestamp,
      position: decision.decision === 'buy' ? 'belowBar' : 'aboveBar',
      color: '#000000',
      shape: decision.decision === 'buy' ? 'arrowUp' : 'arrowDown',
      text: decision.decision.toUpperCase(),
      size: 1
    };

    series.setMarkers([marker]);
  };

  const updateCurrentCandle = (series, candleData) => {
    if (!candleData) return;
    
    const formattedCandle = {
      time: candleData.timestamp,
      open: candleData.open,
      high: candleData.high,
      low: candleData.low,
      close: candleData.close
    };

    series.update(formattedCandle);
  };

  const appendNewCandle = (series, candleData) => {
    if (!candleData) return;

    const formattedCandle = {
      time: candleData.timestamp,
      open: candleData.open,
      high: candleData.high,
      low: candleData.low,
      close: candleData.close
    };

    series.update(formattedCandle);
  };

  return (
    <div 
      ref={chartContainerRef} 
      style={{ 
        width: '60%', 
        height: '600px',
        margin: '0 auto',
        border: '1px solid #e0e0e0',
        borderRadius: '8px'
      }} 
    />
  );
};

export default CandlestickChart;