import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleProcess = async () => {
    if (!input) return alert("Please enter a message!");
    setLoading(true);
    try {
      // আপনার FastAPI ব্যাকএন্ড এন্ডপয়েন্ট
      const res = await axios.post('http://localhost:8000/process-lead', { 
        message: input 
      });
      setResult(res.data);
    } catch (err) {
      console.error("Error connecting to backend:", err);
      alert("Backend is not running or connection failed!");
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1>🚀 AI Lead Handler</h1>
        <p>Analyze and respond to leads using LangChain & Hugging Face</p>
      </header>

      <main style={styles.main}>
        <div style={styles.inputSection}>
          <textarea 
            style={styles.textarea}
            placeholder="Paste lead message here... (e.g., I'm interested in your enterprise plan)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button 
            onClick={handleProcess} 
            disabled={loading} 
            style={loading ? styles.buttonDisabled : styles.button}
          >
            {loading ? 'Analyzing...' : 'Process Lead'}
          </button>
        </div>

        {result && (
          <div style={styles.resultCard}>
            <h3>Lead Category: 
              <span style={{ color: result.status === 'Hot Lead' ? '#27ae60' : '#e74c3c', marginLeft: '10px' }}>
                {result.status}
              </span>
            </h3>
            <div style={styles.aiBox}>
              <strong>AI Suggested Response:</strong>
              <p>{result.ai_response}</p>
            </div>
            <div style={styles.footerInfo}>
              <span>Confidence Score: {result.score}</span>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

// Simple Inline CSS for quick setup
const styles = {
  container: { maxWidth: '800px', margin: '0 auto', padding: '40px 20px', fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif', color: '#333' },
  header: { textAlign: 'center', marginBottom: '40px' },
  main: { display: 'flex', flexDirection: 'column', gap: '20px' },
  inputSection: { display: 'flex', flexDirection: 'column', gap: '15px' },
  textarea: { width: '100%', height: '120px', padding: '15px', borderRadius: '8px', border: '1px solid #ddd', fontSize: '16px', outlineColor: '#3498db' },
  button: { padding: '12px', borderRadius: '8px', border: 'none', backgroundColor: '#3498db', color: 'white', fontSize: '16px', cursor: 'pointer', fontWeight: 'bold' },
  buttonDisabled: { padding: '12px', borderRadius: '8px', border: 'none', backgroundColor: '#bdc3c7', color: 'white', cursor: 'not-allowed' },
  resultCard: { marginTop: '20px', padding: '25px', borderRadius: '12px', backgroundColor: '#f9f9f9', borderLeft: '5px solid #3498db', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
  aiBox: { marginTop: '15px', padding: '15px', backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #eee' },
  footerInfo: { marginTop: '15px', fontSize: '12px', color: '#95a5a6', textAlign: 'right' }
};

export default App;