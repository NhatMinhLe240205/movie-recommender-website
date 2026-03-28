import { useState } from "react"

function SearchBar({ onMovieSelect }) {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState([])

  async function handleSearch(e) {
    const value = e.target.value
    setQuery(value)
    if (value.length < 2) { setResults([]); return }
    const res = await fetch(`http://localhost:5000/api/search?q=${value}`)
    const data = await res.json()
    setResults(data)
  }

  function handleSelect(movie) {
    onMovieSelect(movie)
    setQuery(movie.title)
    setResults([])
  }

  return (
    <div className="search-wrap">
      <input
        className="input"
        type="text"
        placeholder="Search a movie..."
        value={query}
        onChange={handleSearch}
      />
      {results.length > 0 && (
        <div className="dropdown">
          {results.map(movie => (
            <div
              key={movie.movieId}
              className="drop-item"
              onClick={() => handleSelect(movie)}
            >
              <span className="drop-title">{movie.title}</span>
              <span className="drop-meta">{movie.genres}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default SearchBar