const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    credentials: 'include',
    ...options,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.error || 'Request failed')
  }

  return response.json()
}

export const getHealth = () => request('/health')
export const getItems = () => request('/items')
export const createItem = (item) => request('/items', {
  method: 'POST',
  body: JSON.stringify(item),
})
export const signup = (user) => request('/auth/signup', { method: 'POST', body: JSON.stringify(user) })
export const login = (credentials) => request('/auth/login', { method: 'POST', body: JSON.stringify(credentials) })
export const logout = () => request('/auth/logout', { method: 'POST' })
export const getCurrentUser = () => request('/auth/me')
export const updateProfile = (profile) => request('/auth/profile', { method: 'PATCH', body: JSON.stringify(profile) })
export const completeLesson = (lessonId) => request(`/auth/lessons/${lessonId}/complete`, { method: 'POST' })
export const getProgress = () => request('/auth/progress')

export async function uploadAvatar(file) {
  const formData = new FormData()
  formData.append('picture', file)
  const response = await fetch(`${API_URL}/auth/profile/avatar`, {
    method: 'POST',
    body: formData,
    credentials: 'include',
  })
  if (!response.ok) throw new Error((await response.json()).error || 'Upload failed')
  return response.json()
}
