import { useEffect, useState } from 'react'
import { getCurrentUser, uploadAvatar, updateProfile } from './api'

const themes = [
  { id: 'paper', label: 'Paper', colors: ['#f3f0e8', '#1d2922'] },
  { id: 'dark', label: 'Dark', colors: ['#18201c', '#f3f0e8'] },
  { id: 'red', label: 'Red & white', colors: ['#f3e8e4', '#7e2f27'] },
  { id: 'blue', label: 'Blue & white', colors: ['#e8eff3', '#214d68'] },
  { id: 'mono', label: 'Black & white', colors: ['#f4f4f4', '#111111'] },
]

export default function Settings({ user, onUserChange, onBack }) {
  const [name, setName] = useState(user?.name || '')
  const [theme, setTheme] = useState(user?.theme || 'paper')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    if (!user) getCurrentUser().then((response) => onUserChange(response.user)).catch(() => {})
  }, [onUserChange, user])

  async function savePreferences() {
    setIsSaving(true)
    setError('')
    setMessage('')
    try {
      const response = await updateProfile({ name, theme })
      onUserChange(response.user)
      setMessage('Settings saved.')
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsSaving(false)
    }
  }

  async function handleAvatarChange(event) {
    const file = event.target.files?.[0]
    if (!file) return
    setError('')
    setMessage('')
    try {
      const response = await uploadAvatar(file)
      onUserChange(response.user)
      setMessage('Profile picture updated.')
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  return (
    <main className="settings-page">
      <nav className="learning-nav">
        <button className="learning-brand" onClick={onBack} type="button">blocky<span>.</span></button>
        <button className="settings-back" onClick={onBack} type="button">Back to learning -&gt;</button>
      </nav>
      <header className="settings-header">
        <p className="content-kicker">Your workspace</p>
        <h1>Settings</h1>
        <p>Shape Blocky around the way you learn.</p>
      </header>
      <section className="settings-grid">
        <div className="settings-section profile-section">
          <p className="section-number">01</p>
          <div><h2>Profile</h2><p>Make your learning space feel like yours.</p></div>
          <div className="profile-controls">
            <div className="avatar-wrap">
              {user?.profile_picture_url ? <img src={`${import.meta.env.VITE_API_URL || 'http://localhost:5000/api'}${user.profile_picture_url}`} alt="Profile" /> : <span>{(name || 'B').slice(0, 1).toUpperCase()}</span>}
              <label className="avatar-upload" htmlFor="avatar">Change<input id="avatar" type="file" accept="image/png,image/jpeg,image/webp" onChange={handleAvatarChange} /></label>
            </div>
            <label className="settings-field">Display name<input value={name} onChange={(event) => setName(event.target.value)} /></label>
          </div>
        </div>
        <div className="settings-section privacy-section">
          <p className="section-number">02</p>
          <div><h2>Privacy</h2><p>Your account uses secure server-side sessions. Passwords are never stored in plain text.</p></div>
          <div className="privacy-note"><span>Session security</span><strong>Active</strong></div>
        </div>
        <div className="settings-section points-section">
          <p className="section-number">03</p>
          <div><h2>Points</h2><p>Every completed lesson adds one point to your record.</p></div>
          <strong className="points-total">{user?.points || 0}<small> points</small></strong>
        </div>
        <div className="settings-section lessons-section">
          <p className="section-number">04</p>
          <div><h2>Lessons completed</h2><p>Keep moving forward, one clear idea at a time.</p></div>
          <strong className="points-total">{user?.lessons_completed || 0}<small> lessons</small></strong>
        </div>
        <div className="settings-section appearance-section">
          <p className="section-number">05</p>
          <div><h2>Appearance</h2><p>Choose a palette for your study sessions.</p></div>
          <div className="theme-grid">{themes.map((item) => <button className={theme === item.id ? 'theme-choice active' : 'theme-choice'} key={item.id} onClick={() => setTheme(item.id)} type="button"><span className="theme-swatch" style={{ background: item.colors[0], color: item.colors[1] }}>Aa</span><span>{item.label}</span>{theme === item.id && <b>Selected</b>}</button>)}</div>
        </div>
      </section>
      {(error || message) && <p className={error ? 'settings-feedback error' : 'settings-feedback success'}>{error || message}</p>}
      <button className="settings-save" onClick={savePreferences} type="button" disabled={isSaving}>{isSaving ? 'Saving...' : 'Save settings'} <span>-&gt;</span></button>
    </main>
  )
}
