import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

function App() {
  const [activeTab, setActiveTab] = useState('hide')
  const [secretText, setSecretText] = useState('')
  const [key, setKey] = useState('')
  const [revealedText, setRevealedText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [generatedKey, setGeneratedKey] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const handleHide = async (e) => {
    e.preventDefault()
    if (!secretText.trim()) {
      setError('Please enter some text to hide')
      return
    }

    setLoading(true)
    setError('')
    setSuccessMessage('')
    
    try {
      const response = await axios.post(`${API_URL}/hide/`, {
        text: secretText
      })
      
      setGeneratedKey(response.data.key)
      setSuccessMessage('Secret hidden successfully!')
      setSecretText('')
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to hide the secret. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleReveal = async (e) => {
    e.preventDefault()
    if (!key.trim()) {
      setError('Please enter a key to reveal')
      return
    }

    setLoading(true)
    setError('')
    setSuccessMessage('')
    
    try {
      const response = await axios.get(`${API_URL}/reveal/${key}/`)
      setRevealedText(response.data.text)
      setSuccessMessage('Secret revealed successfully!')
      setKey('')
    } catch (err) {
      if (err.response?.status === 404) {
        setError('Secret not found or already viewed')
      } else {
        setError(err.response?.data?.error || 'Failed to reveal the secret. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('Copied to clipboard!')
  }

  const resetForms = () => {
    setSecretText('')
    setKey('')
    setRevealedText('')
    setGeneratedKey('')
    setError('')
    setSuccessMessage('')
  }

  const handleTabChange = (tab) => {
    setActiveTab(tab)
    resetForms()
  }

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>🔒 Secure Message Sharing</h1>
          <p>Share secrets that self-destruct after being viewed once</p>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'hide' ? 'active' : ''}`}
            onClick={() => handleTabChange('hide')}
          >
            🎁 Hide Secret
          </button>
          <button
            className={`tab ${activeTab === 'reveal' ? 'active' : ''}`}
            onClick={() => handleTabChange('reveal')}
          >
            🔓 Reveal Secret
          </button>
        </div>

        <div className="content">
          {activeTab === 'hide' && (
            <div className="tab-content">
              <form onSubmit={handleHide}>
                <div className="form-group">
                  <label htmlFor="secretText">Enter your secret message:</label>
                  <textarea
                    id="secretText"
                    value={secretText}
                    onChange={(e) => setSecretText(e.target.value)}
                    placeholder="Type your secret message here... It will be destroyed after first view."
                    disabled={loading}
                    rows="6"
                  />
                </div>
                
                <button 
                  type="submit" 
                  className="btn-primary"
                  disabled={loading || !secretText.trim()}
                >
                  {loading ? '🔄 Hiding Secret...' : '🔒 Hide Secret'}
                </button>
              </form>

              {generatedKey && (
                <div className="result success">
                  <h3>✅ Secret Hidden Successfully!</h3>
                  <p>Your secret key (copy this and share it):</p>
                  <div 
                    className="key-display"
                    onClick={() => copyToClipboard(generatedKey)}
                    title="Click to copy"
                  >
                    {generatedKey}
                  </div>
                  <p className="url-display">
                    ⏰ This secret will expire in 24 hours or after first view
                  </p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'reveal' && (
            <div className="tab-content">
              <form onSubmit={handleReveal}>
                <div className="form-group">
                  <label htmlFor="key">Enter the secret key:</label>
                  <textarea
                    id="key"
                    value={key}
                    onChange={(e) => setKey(e.target.value)}
                    placeholder="Paste the secret key here to reveal the message..."
                    disabled={loading}
                    rows="4"
                  />
                </div>
                
                <button 
                  type="submit" 
                  className="btn-primary"
                  disabled={loading || !key.trim()}
                >
                  {loading ? '🔄 Revealing Secret...' : '🔓 Reveal Secret'}
                </button>
              </form>

              {revealedText && (
                <div className="result success">
                  <h3>🎉 Secret Revealed!</h3>
                  <p>The secret message was:</p>
                  <div className="secret-display">
                    {revealedText}
                  </div>
                  <p className="warning-message">
                    ⚠️ This secret has been destroyed and cannot be viewed again
                  </p>
                </div>
              )}
            </div>
          )}

          {error && (
            <div className="result error">
              <h3>❌ Error</h3>
              <p>{error}</p>
            </div>
          )}

          {successMessage && !generatedKey && !revealedText && (
            <div className="result success">
              <h3>✅ Success</h3>
              <p>{successMessage}</p>
            </div>
          )}
        </div>

        <div className="footer">
          <p>Built with Django, React & Redis • Messages self-destruct after viewing</p>
        </div>
      </div>
    </div>
  )
}

export default App