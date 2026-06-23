export const apiBase = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

export type LoginPayload = {
  username: string | FormDataEntryValue | null
  password: string | FormDataEntryValue | null
}

export type LoginResult = {
  success: boolean
  message: string
  token?: string
  username?: string
}

export type RoomResponse = {
  id_room: number
  dormitory_id: number
  floor: number
  number: number
  qty_person: number
  who: string
  corpus: string
  status: string
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

export async function loginUser(payload: LoginPayload): Promise<LoginResult> {
  if (!payload.username || !payload.password) {
    return { success: false, message: 'Username and password are required.' }
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
      return {
        success: false,
        message: `Login failed: ${response.status} ${errorBody?.detail ?? ''}`,
      }
    }

    const data = await response.json()
    console.log('Login response:', data)
    return {
      success: true,
      message: 'Login successful. Token received.',
      token: data.access_token,
      username: String(payload.username),
    }
  } catch (error) {
    console.error('Login request error:', error)
    return {
      success: false,
      message: 'Login request failed. Check backend status and CORS settings.',
    }
  }
}

export async function getAvailableRooms(): Promise<RoomResponse[] | null> {
  try {
    const response = await fetch(`${apiBase}/rooms/available/`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })

    if (!response.ok) {
      console.error('Failed to load rooms:', response.status)
      return null
    }

    return await response.json()
  } catch (error) {
    console.error('Error fetching available rooms:', error)
    return null
  }
}
