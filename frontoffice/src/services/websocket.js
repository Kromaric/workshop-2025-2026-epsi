/**
 * Service WebSocket pour gérer la connexion au backend
 */

class WebSocketService {
  constructor() {
    this.ws = null
    this.isConnected = false
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 3000
    this.messageHandlers = []
    this.teamId = null
    this.playerId = null
  }

  /**
   * Se connecter au WebSocket
   */
  connect(teamId, playerId) {
    this.teamId = teamId
    this.playerId = playerId

    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
    const fullUrl = `${wsUrl}/ws/${teamId}/${playerId}`

    console.log('🔌 Connexion WebSocket à:', fullUrl)

    this.ws = new WebSocket(fullUrl)

    this.ws.onopen = () => {
      this.isConnected = true
      this.reconnectAttempts = 0
      console.log('✅ WebSocket connecté')
      this.notifyHandlers({ type: 'connection', status: 'connected' })
    }

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('📨 Message reçu:', data.type)
        this.notifyHandlers(data)
      } catch (error) {
        console.error('❌ Erreur parsing message:', error)
      }
    }

    this.ws.onclose = () => {
      this.isConnected = false
      console.log('❌ WebSocket déconnecté')
      this.notifyHandlers({ type: 'connection', status: 'disconnected' })
      this.attemptReconnect()
    }

    this.ws.onerror = (error) => {
      console.error('❌ Erreur WebSocket:', error)
    }

    return this.ws
  }

  /**
   * Tenter une reconnexion
   */
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`🔄 Reconnexion... (tentative ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      
      setTimeout(() => {
        this.connect(this.teamId, this.playerId)
      }, this.reconnectDelay)
    } else {
      console.error('❌ Nombre maximum de tentatives de reconnexion atteint')
    }
  }

  /**
   * Envoyer un message au serveur
   */
  send(data) {
    if (this.ws && this.isConnected) {
      this.ws.send(JSON.stringify(data))
      return true
    }
    console.warn('⚠️ WebSocket non connecté')
    return false
  }

  /**
   * Valider l'énigme Chardin
   */
  validateChardin(code) {
    return this.send({
      action: 'validate_chardin',
      code
    })
  }

  /**
   * Cliquer sur le bouton
   */
  clickButton() {
    return this.send({
      action: 'button_click'
    })
  }

  /**
   * Envoyer un message de chat
   */
  sendMessage(message) {
    return this.send({
      action: 'send_message',
      message
    })
  }

  /**
   * S'abonner aux messages
   */
  onMessage(handler) {
    this.messageHandlers.push(handler)
    return () => {
      this.messageHandlers = this.messageHandlers.filter(h => h !== handler)
    }
  }

  /**
   * Notifier tous les handlers
   */
  notifyHandlers(data) {
    this.messageHandlers.forEach(handler => {
      try {
        handler(data)
      } catch (error) {
        console.error('❌ Erreur dans le handler:', error)
      }
    })
  }

  /**
   * Déconnecter
   */
  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
      this.isConnected = false
    }
  }

  /**
   * Vérifier si connecté
   */
  getConnectionStatus() {
    return this.isConnected
  }
}

// Instance singleton
export const wsService = new WebSocketService()

export default wsService
