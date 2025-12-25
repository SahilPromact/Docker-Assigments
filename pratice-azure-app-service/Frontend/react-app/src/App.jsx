import { useState, useEffect } from 'react'
import './App.css'

// API Configuration - Update this based on your environment
const API_BASE_URL = import.meta.env.VITE_API_URL

function App() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({ name: '', source: '' })
  const [submitting, setSubmitting] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

  // Fetch items from backend
  const fetchItems = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE_URL}/items`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setItems(data.items || [])
    } catch (err) {
      setError(`Failed to fetch items: ${err.message}`)
      console.error('Error fetching items:', err)
    } finally {
      setLoading(false)
    }
  }

  // Load items on component mount
  useEffect(() => {
    fetchItems()
  }, [])

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validate form
    if (!formData.name.trim() || !formData.source.trim()) {
      setError('Both name and source are required')
      return
    }

    setSubmitting(true)
    setError(null)
    setSuccessMessage('')

    try {
      const response = await fetch(`${API_BASE_URL}/add-item`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name.trim(),
          source: formData.source.trim()
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // Show success message
      setSuccessMessage(`✅ Successfully added "${data.item.name}"!`)
      
      // Clear form
      setFormData({ name: '', source: '' })
      
      // Refresh items list
      await fetchItems()
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(''), 3000)
      
    } catch (err) {
      setError(`Failed to add item: ${err.message}`)
      console.error('Error adding item:', err)
    } finally {
      setSubmitting(false)
    }
  }

  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>Item Manager</h1>
        <p>Add and manage your items with ease</p>
      </header>

      {/* Main Content */}
      <div className="app-content">
        {/* Add Item Form */}
        <section className="add-item-section">
          <div className="form-card">
            <h2>Add New Item</h2>
            
            {error && <div className="error">{error}</div>}
            {successMessage && <div className="success-message">{successMessage}</div>}
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="item-name">Item Name</label>
                <input
                  id="item-name"
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Enter item name..."
                  disabled={submitting}
                  autoComplete="off"
                />
              </div>

              <div className="form-group">
                <label htmlFor="item-source">Source</label>
                <input
                  id="item-source"
                  type="text"
                  name="source"
                  value={formData.source}
                  onChange={handleInputChange}
                  placeholder="Enter source..."
                  disabled={submitting}
                  autoComplete="off"
                />
              </div>

              <button 
                type="submit" 
                className="submit-btn"
                disabled={submitting}
              >
                {submitting ? 'Adding...' : '+ Add Item'}
              </button>
            </form>
          </div>
        </section>

        {/* Items List */}
        <section className="items-section">
          <div className="section-header">
            <h2>All Items</h2>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <span className="items-count">
                {items.length} {items.length === 1 ? 'Item' : 'Items'}
              </span>
              <button 
                className="refresh-btn" 
                onClick={fetchItems}
                disabled={loading}
              >
                <span style={{ transform: loading ? 'rotate(360deg)' : 'none', display: 'inline-block', transition: 'transform 0.5s' }}>
                  🔄
                </span>
                Refresh
              </button>
            </div>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>Loading items...</p>
            </div>
          )}

          {/* Empty State */}
          {!loading && items.length === 0 && (
            <div className="empty-state">
              <div className="empty-state-icon">📭</div>
              <h3>No items yet</h3>
              <p>Add your first item using the form on the left</p>
            </div>
          )}

          {/* Items Grid */}
          {!loading && items.length > 0 && (
            <div className="items-grid">
              {items.map((item, index) => (
                <div 
                  key={item.id} 
                  className="item-card"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <div className="item-header">
                    <span className="item-id">#{item.id}</span>
                  </div>
                  <h3 className="item-name">{item.name}</h3>
                  <div className="item-source">{item.source}</div>
                  <div className="item-date">
                    {formatDate(item.created_at)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}

export default App
