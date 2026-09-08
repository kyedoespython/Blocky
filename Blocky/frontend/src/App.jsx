import { useEffect, useState } from 'react'
import { getCurrentUser, login, signup } from './api'
import SQLLearning from './SQLLearning'
import Settings from './Settings'
import Plans from './Plans'

function AuthForm({ mode, onModeChange, onAuthenticated }) {
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const isSignup = mode === 'signup'

  function switchMode(nextMode) {
    onModeChange(nextMode)
    setError('')
    setMessage('')
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setMessage('')
    setIsSubmitting(true)

    const formData = new FormData(event.currentTarget)
    const credentials = {
      email: formData.get('email'),
      password: formData.get('password'),
    }

    try {
      if (isSignup) {
        const response = await signup({ ...credentials, name: formData.get('name') })
        onAuthenticated(response.user)
        setMessage('Your account is ready. Welcome to Blocky.')
      } else {
        const response = await login(credentials)
        onAuthenticated(response.user)
        setMessage('You are now logged in.')
      }
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="auth-card">
      <div className="auth-tabs" role="tablist" aria-label="Authentication options">
        <button
          className={mode === 'login' ? 'active' : ''}
          onClick={() => switchMode('login')}
          role="tab"
          aria-selected={mode === 'login'}
          type="button"
        >
          Log in
        </button>
        <button
          className={mode === 'signup' ? 'active' : ''}
          onClick={() => switchMode('signup')}
          role="tab"
          aria-selected={mode === 'signup'}
          type="button"
        >
          Sign up
        </button>
      </div>

      <div className="card-heading">
        <p className="card-kicker">{isSignup ? 'Start learning' : 'Welcome back'}</p>
        <h2>{isSignup ? 'Create your account' : 'Pick up where you left off.'}</h2>
        <p>{isSignup ? 'Your next query is closer than you think.' : 'Your database practice is waiting.'}</p>
      </div>

      <form onSubmit={handleSubmit}>
        {isSignup && (
          <label htmlFor="name">
            Name
            <input id="name" name="name" type="text" autoComplete="name" placeholder="Alex Morgan" required />
          </label>
        )}
        <label htmlFor="email">
          Email address
          <input id="email" name="email" type="email" autoComplete="email" placeholder="you@example.com" required />
        </label>
        <label htmlFor="password">
          Password
          <div className="password-field">
            <input
              id="password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              autoComplete={isSignup ? 'new-password' : 'current-password'}
              placeholder="Enter your password"
              required
            />
            <button
              className="password-toggle"
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
        </label>
        {isSignup && (
          <label className="checkbox-label">
            <input type="checkbox" required />
            <span>I agree to the terms of use.</span>
          </label>
        )}
        {!isSignup && <a className="forgot-link" href="#forgot-password">Forgot your password?</a>}
        {error && <p className="form-message form-error" role="alert">{error}</p>}
        {message && <p className="form-message form-success" role="status">{message}</p>}
        <button className="submit-button" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Working...' : isSignup ? 'Create account' : 'Log in'}
          <span aria-hidden="true">-&gt;</span>
        </button>
      </form>

      <p className="switch-prompt">
        {isSignup ? 'Already have an account?' : 'New to Blocky?'}{' '}
        <button type="button" onClick={() => switchMode(isSignup ? 'login' : 'signup')}>
          {isSignup ? 'Log in' : 'Create an account'}
        </button>
      </p>
    </div>
  )
}

function AuthPage({ onOpenLearning, onOpenPlans, onAuthenticated }) {
  const [mode, setMode] = useState('login')

  return (
    <main className="auth-page">
      <nav className="site-nav" aria-label="Main navigation">
        <a className="wordmark" href="#home">blocky<span>.</span></a>
        <div className="auth-nav-links"><button className="nav-link" onClick={onOpenLearning} type="button">Explore SQL -&gt;</button><button className="nav-link" onClick={onOpenPlans} type="button">Plans</button></div>
      </nav>

      <section className="auth-layout">
        <div className="auth-intro">
          <p className="kicker">A better way to learn SQL</p>
          <h1>Make sense of<br /><em>your data.</em></h1>
          <p className="intro-copy">Learn databases by doing. Build your foundations, write better queries, and turn curiosity into practical confidence.</p>
          <div className="intro-note"><span className="note-mark">SQL</span><span>For students, solo developers,<br />and the endlessly curious.</span></div>
        </div>
        <AuthForm mode={mode} onModeChange={setMode} onAuthenticated={onAuthenticated} />
      </section>

      <footer className="site-footer"><span>Blocky</span><span>Learn at your own pace.</span><a href="#privacy">Privacy</a></footer>
    </main>
  )
}

export default function App() {
  const initialHash = window.location.hash
  const [page, setPage] = useState(initialHash === '#sql' ? 'learning' : initialHash === '#settings' ? 'settings' : initialHash === '#plans' ? 'plans' : 'auth')
  const [user, setUser] = useState(null)

  useEffect(() => {
    document.documentElement.dataset.theme = user?.theme || 'paper'
  }, [user?.theme])

  useEffect(() => {
    getCurrentUser().then((response) => setUser(response.user)).catch(() => {})
  }, [])

  function openLearning() {
    window.history.replaceState(null, '', '#sql')
    setPage('learning')
  }

  function openAuth() {
    window.history.replaceState(null, '', '#home')
    setPage('auth')
  }

  function openSettings() {
    window.history.replaceState(null, '', '#settings')
    setPage('settings')
  }

  function openPlans() {
    window.history.replaceState(null, '', '#plans')
    setPage('plans')
  }

  if (page === 'settings') return <Settings user={user} onUserChange={setUser} onBack={openLearning} />
  if (page === 'learning') return <SQLLearning user={user} onUserChange={setUser} onOpenSettings={openSettings} onOpenPlans={openPlans} onBack={openAuth} />
  if (page === 'plans') return <Plans onBack={openAuth} onOpenLearning={openLearning} onOpenSettings={openSettings} />
  return <AuthPage onOpenLearning={openLearning} onOpenPlans={openPlans} onAuthenticated={setUser} />
}
