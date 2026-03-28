function MethodPicker({ method, onMethodChange }) {
  return (
    <div className="method-picker">
      <button
        className={`method-btn ${method === 'content' ? 'active' : ''}`}
        onClick={() => onMethodChange('content')}
      >
        <strong>Content Based</strong>
        By genre similarity
      </button>
      <button
        className={`method-btn ${method === 'collaborative' ? 'active' : ''}`}
        onClick={() => onMethodChange('collaborative')}
      >
        <strong>Collaborative</strong>
        By user ratings
      </button>
    </div>
  )
}

export default MethodPicker