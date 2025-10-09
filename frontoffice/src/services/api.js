/**
 * Service API pour les appels HTTP REST au backend
 */

class ApiService {
  constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  }

  /**
   * Effectuer une requête GET
   */
  async get(endpoint) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error(`❌ Erreur GET ${endpoint}:`, error)
      throw error
    }
  }

  /**
   * Effectuer une requête POST
   */
  async post(endpoint, data) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`❌ Erreur POST ${endpoint}:`, error)
      throw error
    }
  }

  /**
   * Récupérer les statistiques d'une équipe
   */
  async getTeamStats(teamId) {
    return await this.get(`/teams/${teamId}/stats`)
  }

  /**
   * Récupérer le message de bienvenue
   */
  async getWelcomeMessage() {
    return await this.get('/')
  }

  /**
   * Vérifier que le backend est accessible
   */
  async checkBackend() {
    try {
      const response = await this.get('/')
      return {
        isAvailable: true,
        message: response.message
      }
    } catch (error) {
      return {
        isAvailable: false,
        error: error.message
      }
    }
  }
}

// Instance singleton
export const apiService = new ApiService()

export default apiService
