import { checkBackend, loginUser } from './api'

const loginForm = document.getElementById('login-form') as HTMLFormElement | null
const statusMessage = document.getElementById('status-message') as HTMLElement | null

function renderStatus(text: string) {
  if (statusMessage) {
    statusMessage.textContent = text
  }
}

async function initializeApp() {
  renderStatus('Checking backend availability...')
  const status = await checkBackend()
  renderStatus(status)
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

  const status = await loginUser(payload)
  renderStatus(status)
}

if (loginForm) {
  loginForm.addEventListener('submit', handleLogin)
}

initializeApp()
