import { checkBackend, loginUser, getAvailableRooms, type LoginResult, type RoomResponse } from './api'

const loginForm = document.getElementById('login-form') as HTMLFormElement | null
const statusMessage = document.getElementById('status-message') as HTMLElement | null
const dashboard = document.getElementById('dashboard') as HTMLElement | null
const dashboardMessage = document.getElementById('dashboard-message') as HTMLElement | null
const logoutButton = document.getElementById('logout-button') as HTMLButtonElement | null
const roomsPanel = document.getElementById('rooms-panel') as HTMLElement | null
const roomsContainer = document.getElementById('rooms-container') as HTMLElement | null

function renderStatus(text: string) {
  if (statusMessage) {
    statusMessage.textContent = text
  }
}

function renderRooms(rooms: RoomResponse[]) {
  if (!roomsContainer) {
    return
  }

  if (rooms.length === 0) {
    roomsContainer.innerHTML = '<p>No available rooms found.</p>'
    return
  }

  const rows = rooms
    .map(
      (room) =>
        `<tr><td>${room.corpus}</td><td>${room.floor}</td><td>${room.number}</td><td>${room.qty_person}</td><td>${room.who}</td><td>${room.status}</td></tr>`
    )
    .join('')

  roomsContainer.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Corpus</th>
          <th>Floor</th>
          <th>Number</th>
          <th>Capacity</th>
          <th>Gender</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>
  `
}

function renderRoomsError() {
  if (roomsContainer) {
    roomsContainer.innerHTML = '<p>Unable to load available rooms.</p>'
  }
}

function showDashboard(username: string) {
  if (loginForm) {
    loginForm.style.display = 'none'
  }
  if (dashboard) {
    dashboard.style.display = 'block'
  }
  if (roomsPanel) {
    roomsPanel.style.display = 'block'
  }
  if (dashboardMessage) {
    dashboardMessage.textContent = `Welcome, ${username}! You are now logged in to the platform.`
  }
}

function hideDashboard() {
  if (loginForm) {
    loginForm.style.display = ''
  }
  if (dashboard) {
    dashboard.style.display = 'none'
  }
  if (roomsPanel) {
    roomsPanel.style.display = 'none'
  }
  if (dashboardMessage) {
    dashboardMessage.textContent = ''
  }
  if (roomsContainer) {
    roomsContainer.innerHTML = ''
  }
}

async function loadAvailableRooms() {
  if (roomsContainer) {
    roomsContainer.textContent = 'Loading available rooms...'
  }

  const rooms = await getAvailableRooms()
  if (rooms === null) {
    renderRoomsError()
    return
  }

  renderRooms(rooms)
}

async function initializeApp() {
  renderStatus('Checking backend availability...')
  const status = await checkBackend()
  renderStatus(status)

  const savedToken = sessionStorage.getItem('access_token')
  const savedUsername = sessionStorage.getItem('username')
  if (savedToken && savedUsername) {
    showDashboard(savedUsername)
    renderStatus('Already logged in from this browser session.')
    await loadAvailableRooms()
  }
}

async function handleLogin(event: Event) {
  event.preventDefault()
  if (!loginForm) {
    return
  }

  const formData = new FormData(loginForm)
  const payload = {
    username: formData.get('username'),
    password: formData.get('password'),
  }

  const result: LoginResult = await loginUser(payload)
  renderStatus(result.message)

  if (result.success && result.token && result.username) {
    sessionStorage.setItem('access_token', result.token)
    sessionStorage.setItem('username', result.username)
    showDashboard(result.username)
    await loadAvailableRooms()
  }
}

if (loginForm) {
  loginForm.addEventListener('submit', handleLogin)
}

if (logoutButton) {
  logoutButton.addEventListener('click', () => {
    sessionStorage.removeItem('access_token')
    sessionStorage.removeItem('username')
    hideDashboard()
    renderStatus('Logged out. Please log in again.')
  })
}

initializeApp()
