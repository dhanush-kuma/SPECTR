import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiFetch, parseApiError, setCsrfToken } from '../api'
import PasswordInput from '../components/PasswordInput'
import Header from '../components/Header'
import { INVESTIGATOR_LABEL } from '../labels'

function InvestigatorLogin() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleLogin(e) {
    e.preventDefault()
    setError(null)
    setSubmitting(true)

    try {
      const res = await apiFetch('/investigator/login', {
        method: 'POST',
        json: {
          username: username.trim(),
          password,
          remember_me: rememberMe,
        },
      })
      let data = {}
      try {
        data = await res.json()
      } catch {
        if (!res.ok) {
          setError('Login failed. Please try again.')
          return
        }
      }

      if (!res.ok) {
        setError(parseApiError(data.detail) || 'Login failed.')
        return
      }

      setCsrfToken(data.csrf_token)
      navigate('/investigator/home', { replace: true })
    } catch {
      setError('Could not connect to backend.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <>
      <Header />

      <main className="app">
        <h1>{INVESTIGATOR_LABEL} Login</h1>

        <div className="setup-card">
          <div className="setup-card__header">
            <span className="setup-badge">{INVESTIGATOR_LABEL} Portal</span>
            <h2>Sign In</h2>
            <p>Enter your username and password to continue.</p>
          </div>

          <form className="setup-form" onSubmit={handleLogin} noValidate>
            <div className="field">
              <label htmlFor="inv-login-username">Username</label>
              <input
                id="inv-login-username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g. K7M2P9"
                required
                autoFocus
                autoComplete="username"
              />
            </div>
            <div className="field">
              <label htmlFor="inv-login-password">Password</label>
              <PasswordInput
                id="inv-login-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
              />
            </div>
            <div className="field field-checkbox">
              <label htmlFor="inv-remember-me" className="checkbox-label">
                <input
                  id="inv-remember-me"
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                Keep me signed in for 30 days
              </label>
            </div>
            {error && <p className="error">{error}</p>}
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? 'Signing in…' : 'Sign In'}
            </button>
          </form>
        </div>
      </main>
    </>
  )
}

export default InvestigatorLogin
