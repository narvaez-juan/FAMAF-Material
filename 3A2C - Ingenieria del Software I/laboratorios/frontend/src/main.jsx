import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './containers/App/index.css'
import App from './containers/App/App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
