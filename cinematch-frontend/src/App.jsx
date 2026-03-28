import { useState } from "react"
import SearchBar from "./components/SearchBar"
import MethodPicker from "./components/MethodPicker"
import "./App.css"

function App() {
  const [selectedMovie, setSelectedMovie] = useState(null)
  const [method, setMethod] = useState('content')
  const [year, setYear] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  function handleMovieSelect(movie) {
    setSelectedMovie(movie)
    setResults([])  // clear old results when new movie selected
  }

  async function handleRecommend() {
    setLoading(true)

    const body = {
      movieId: selectedMovie.movieId,
      method: method,
      year: method === 'content' ? parseInt(year) : null
    }

    const res = await fetch('http://localhost:5000/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })

    const data = await res.json()
    setResults(data)
    setLoading(false)
  }

  return (
    <div>
      <h1>CineMatch</h1>
      <SearchBar onMovieSelect={handleMovieSelect} />

      {selectedMovie && (
        <div>
          <p>You selected: {selectedMovie.title}</p>

          <MethodPicker method={method} onMethodChange={setMethod} />

          {method === 'content' && (
            <input
              type="number"
              placeholder="Enter a year e.g. 1995"
              value={year}
              onChange={e => setYear(e.target.value)}
            />
          )}

          <button onClick={handleRecommend} disabled={loading}>
            {loading ? 'Loading...' : 'Get Recommendations'}
          </button>
        </div>
      )}

      {results.length > 0 && (
        <div>
          <h2>Recommendations</h2>
          {results.map((movie, index) => (
            <div key={index}>
              <p>{movie.title}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App