import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);

  const handleSearch = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    if (query) formData.append('query_text', query);
    if (file) formData.append('file', file);

    try {
      // Points to the FastAPI backend container
      const res = await fetch('http://localhost:8000/search', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      console.error("Search failed:", err);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem', fontFamily: 'sans-serif' }}>
      <h2>Multimodal Search</h2>
      <form onSubmit={handleSearch} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <input 
          type="text" 
          placeholder="Search by text (e.g. 'A red car')..." 
          value={query} 
          onChange={e => { setQuery(e.target.value); setFile(null); }} 
        />
        <div style={{ textAlign: 'center' }}>OR</div>
        <input 
          type="file" 
          accept="image/*" 
          onChange={e => { setFile(e.target.files[0]); setQuery(''); }} 
        />
        <button type="submit" style={{ padding: '0.5rem', background: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}>
          Search Database
        </button>
      </form>

      <div style={{ marginTop: '2rem' }}>
        {results.length === 0 ? <p>No results yet.</p> : results.map((hit, i) => (
          <div key={i} style={{ borderBottom: '1px solid #eee', padding: '1rem 0' }}>
            <p><strong>Match Score:</strong> {(hit.score * 100).toFixed(1)}%</p>
            <p><strong>Image File:</strong> {hit.data?.filename}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;