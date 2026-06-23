export const apiBase = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

export type LoginPayload = {
  username: string | FormDataEntryValue | null
  password: string | FormDataEntryValue | null
}

export async function checkBackend(): Promise<string> {
  try {
    const response = await fetch(`${apiBase}/openapi.json`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    })
    if (!response.ok) {
      return `Backend returned ${response.status} when loading OpenAPI description.`
    }
    return 'Backend API is reachable. OpenAPI description loaded successfully.'
  } catch {
    return `Backend unreachable. Start the API server at ${apiBase}`
  }
}

export async function loginUser(payload: LoginPayload): Promise<string> {
  if (!payload.username || !payload.password) {
    return 'Username and password are required.'
  }

  try {
    const response = await fetch(`${apiBase}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: String(payload.username),
        password: String(payload.password),
      }),
    })

    if (!response.ok) {
      const errorBody = await response.json().catch(() => null)
      return `Login failed: ${response.status} ${errorBody?.detail ?? ''}`
    }

    const data = await response.json()
    console.log('Login response:', data)
    return 'Login successful. Token received.'
  } catch {
    return 'Login request failed. Check backend status and CORS settings.'
  }
}
