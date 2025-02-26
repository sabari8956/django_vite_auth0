import { useState, useEffect } from 'react'
import './App.css'

function getCookieValue(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

function App() {
  const [count, setCount] = useState(0)
  const [apiData, setApiData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/', {
          credentials: 'include', // This will include cookies in the request
          headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${getCookieValue('jwt_token')}`
          }
        });
        console.log(response);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setApiData(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <div>
        <h1>Django + Vite + Auth0</h1>
        {apiData && (
          <div className="auth-buttons">
            {!apiData.isAuthenticated ? (
              <a href={`http://127.0.0.1:8000/login?redirect=${encodeURIComponent(window.location.href)}`}>
                <button>Login</button>
              </a>
            ) : (
              <a href="http://127.0.0.1:8000/logout">
                <button>Logout</button>
              </a>
            )}
          </div>
        )}
        
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            count is {count}
          </button>
          <p>
            Edit <code>src/App.jsx</code> and save to test HMR
          </p>
        </div>
        
        <div className="api-data">
          <h2>API Data from Django Backend</h2>
          {loading && <p>Loading data...</p>}
          {error && <p>Error: {error}</p>}
          {apiData && (
            <div>
              <pre>{JSON.stringify(apiData, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default App
