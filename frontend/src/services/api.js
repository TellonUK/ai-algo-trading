const API_BASE_URL = '';

export const fetchHistoricalData = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/history`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching historical data:', error);
    throw error;
  }
};

export const fetchAIDecisions = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/decisions`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching AI decisions:', error);
    throw error;
  }
};