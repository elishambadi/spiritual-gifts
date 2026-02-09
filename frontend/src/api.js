import axios from 'axios'

const API_BASE_URL = 'https://spiritualgifts.parklandssda.org/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

export const surveyAPI = {
  // Get all questions
  getQuestions() {
    return api.get('/questions/')
  },
  
  // Get all spiritual gifts
  getGifts() {
    return api.get('/spiritual-gifts/')
  },
  
  // Create a new survey response
  createSurveyResponse(data) {
    return api.post('/survey-responses/', data)
  },
  
  // Get survey response by ID
  getSurveyResponse(id) {
    return api.get(`/survey-responses/${id}/`)
  },
  
  // Update answers for a survey response
  updateAnswers(id, answers) {
    return api.patch(`/survey-responses/${id}/update_answers/`, { answers })
  },
  
  // Get results for a survey response
  getSurveyResults(id) {
    return api.get(`/survey-responses/${id}/results/`)
  },
  
  // Mark survey as complete
  completeSurvey(id) {
    return api.post(`/survey-responses/${id}/complete/`)
  },

  // Admin leaderboard: top 5 performers per gift
  getAdminLeaderboard() {
    return api.get('/survey-responses/admin_leaderboard/')
  },

  // Public summaries: top 3 gifts per completed response
  getPublicSummaries() {
    return api.get('/survey-responses/public_summaries/')
  }
}
