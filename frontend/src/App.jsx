import { useState, useEffect, useRef } from 'react'
import CandlestickChart from './components/CandlestickChart'
import { fetchHistoricalData, fetchAIDecisions } from './services/api'
import websocketService from './services/websocket'
import './App.css'

function App() {
  const [historicalData, setHistoricalData] = useState([])
  const [decisions, setDecisions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [connectionStatus, setConnectionStatus] = useState('disconnected')
  const chartApiRef = useRef(null)

  useEffect(() => {
    loadInitialData()
    setupWebSocket()

    return () => {
      websocketService.disconnect()
    }
  }, [])

  const loadInitialData = async () => {
    try {
      setLoading(true)
      const [historyData, decisionsData] = await Promise.all([
        fetchHistoricalData(),
        fetchAIDecisions()
      ])
      
      setHistoricalData(historyData)
      setDecisions(decisionsData)
      setError(null)
    } catch (err) {
      setError(`Failed to load data: ${err.message}`)
      console.error('Error loading initial data:', err)
    } finally {
      setLoading(false)
    }
  }

  const setupWebSocket = () => {
    websocketService.on('connected', () => {
      setConnectionStatus('connected')
      console.log('WebSocket connected')
    })

    websocketService.on('disconnected', () => {
      setConnectionStatus('disconnected')
      console.log('WebSocket disconnected')
    })

    websocketService.on('error', (error) => {
      setConnectionStatus('error')
      console.error('WebSocket error:', error)
    })

    websocketService.on('priceUpdate', (priceData) => {
      if (chartApiRef.current && chartApiRef.current.updateCandle) {
        chartApiRef.current.updateCandle(priceData)
      }
    })

    websocketService.on('candleComplete', (candleData) => {
      if (chartApiRef.current && chartApiRef.current.appendCandle) {
        chartApiRef.current.appendCandle(candleData.candle)
        
        if (candleData.decision && (candleData.decision.decision === 'buy' || candleData.decision.decision === 'sell')) {
          chartApiRef.current.addMarker(candleData.decision)
          setDecisions(prev => [...prev, candleData.decision])
        }
      }
    })

    websocketService.connect()
  }

  const handleChartReady = (chartApi) => {
    chartApiRef.current = chartApi
  }

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return '#4CAF50'
      case 'disconnected': return '#f44336'
      case 'error': return '#ff9800'
      default: return '#9e9e9e'
    }
  }

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <h2>Loading market data...</h2>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={loadInitialData}>Retry</button>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Denique AI Market Analysis</h1>
        <div className="status-indicator">
          <span 
            className="status-dot" 
            style={{ backgroundColor: getStatusColor() }}
          ></span>
          <span className="status-text">
            {connectionStatus === 'connected' ? 'Live' : 'Offline'}
          </span>
        </div>
      </header>
      
      <main className="app-main">
        <CandlestickChart 
          historicalData={historicalData}
          decisions={decisions}
          onChartReady={handleChartReady}
        />
      </main>
    </div>
  )
}

export default App
