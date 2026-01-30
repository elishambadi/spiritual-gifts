<template>
  <div class="survey-container">
    <div v-if="loading" class="loading">
      <p>Loading survey questions...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-else>
      <!-- User Information Form -->
      <div v-if="!surveyStarted" class="card">
        <h2>Welcome to the Spiritual Gifts Survey</h2>
        <p style="margin: 1rem 0; color: var(--text-secondary);">
          This survey will help you identify your spiritual gifts. Please answer all 80 questions 
          honestly based on how characteristic each statement is of you.
        </p>
        
        <p style="margin: 1rem 0; padding: 1rem; background: var(--background); border-radius: 6px; font-size: 0.9rem;">
          <strong>Rating Scale:</strong><br/>
          5 = Highly characteristic of me / definitely true for me<br/>
          4 = Most of the time this would describe me<br/>
          3 = Frequently characteristic (about 50% of the time)<br/>
          2 = Occasionally characteristic (about 25% of the time)<br/>
          1 = Not at all characteristic of me
        </p>
        
        <div class="form-group">
          <label for="name">Your Name *</label>
          <input 
            type="text" 
            id="name" 
            v-model="userName" 
            placeholder="Enter your name"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="email">Your Email (Optional)</label>
          <input 
            type="email" 
            id="email" 
            v-model="userEmail" 
            placeholder="Enter your email"
          />
        </div>
        
        <button class="btn btn-primary" @click="startSurvey">
          Start Survey
        </button>
      </div>

      <!-- Survey Questions -->
      <div v-else>
        <!-- Progress and Page Info -->
        <div class="card">
          <div class="progress-bar">
            <div 
              class="progress-bar-fill" 
              :style="{ width: progressPercentage + '%' }"
            ></div>
          </div>
          <p style="text-align: center; color: var(--text-secondary); margin-top: 0.5rem;">
            {{ pagesRemaining }} page{{ pagesRemaining !== 1 ? 's' : '' }} left
          </p>
        </div>

        <!-- Questions on Current Page -->
        <div class="questions-page">
          <div 
            v-for="(question, idx) in currentPageQuestions" 
            :key="question.number"
            :ref="el => setQuestionRef(question.number, el)"
            class="question-item"
            :class="{ 'question-focused': focusedQuestion === question.number }"
          >
            <div class="question-header">
              <div class="question-text-large">
                {{ question.text }}
              </div>
            </div>
            
            <div class="dot-rating-group">
              <div 
                v-for="rating in [1, 2, 3, 4, 5]" 
                :key="rating"
                class="dot-option"
              >
                <input 
                  type="radio" 
                  :id="`q${question.number}-r${rating}`"
                  :name="`question-${question.number}`"
                  :value="rating"
                  v-model="answers[getQuestionIndex(question.number)]"
                  @change="handleAnswerChange(question.number)"
                />
                <label 
                  :for="`q${question.number}-r${rating}`"
                  :class="'dot-label dot-size-' + rating"
                >
                  <span class="dot-circle"></span>
                  <span class="dot-number">{{ rating }}</span>
                </label>
              </div>
            </div>
            
            <div class="rating-labels">
              <span class="label-left">Not at all</span>
              <span class="label-right">Highly characteristic</span>
            </div>
          </div>
        </div>

        <!-- Page Number Display -->
        <div class="page-indicator">
          Page {{ currentPage }} of {{ totalPages }}
        </div>

        <!-- Navigation Buttons -->
        <div class="card">
          <div style="display: flex; gap: 1rem; justify-content: space-between; align-items: center;">
            <button 
              class="btn btn-secondary" 
              @click="previousPage"
              :disabled="currentPage === 1"
            >
              ← Previous Page
            </button>
            
            <button 
              v-if="currentPage < totalPages"
              class="btn btn-primary" 
              @click="nextPage"
              :disabled="!isCurrentPageComplete"
            >
              Next Page →
            </button>
            
            <button 
              v-else
              class="btn btn-primary" 
              @click="submitSurvey"
              :disabled="!allQuestionsAnswered || submitting"
            >
              {{ submitting ? 'Submitting...' : 'Submit Survey' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { surveyAPI } from '../api'

export default {
  name: 'SurveyView',
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const error = ref(null)
    const questions = ref([])
    const answers = ref({})
    const currentPage = ref(1)
    const surveyStarted = ref(false)
    const userName = ref('')
    const userEmail = ref('')
    const submitting = ref(false)
    const focusedQuestion = ref(null)
    const questionRefs = ref({})
    const surveyId = ref(null)
    const QUESTIONS_PER_PAGE = 10

    const setQuestionRef = (questionNumber, el) => {
      if (el) {
        questionRefs.value[questionNumber] = el
      }
    }

    const handleAnswerChange = async (questionNumber) => {
      // Set focus and animate
      focusedQuestion.value = questionNumber
      
      // Save answer to backend if survey is created
      if (surveyId.value) {
        await saveCurrentAnswers()
      }
      
      // Find next unanswered question
      setTimeout(() => {
        const nextUnanswered = findNextUnansweredQuestion(questionNumber)
        if (nextUnanswered) {
          scrollToQuestion(nextUnanswered)
          focusedQuestion.value = nextUnanswered
        } else {
          // Clear focus after a moment if all answered
          setTimeout(() => {
            focusedQuestion.value = null
          }, 800)
        }
      }, 300)
    }

    const findNextUnansweredQuestion = (currentQuestionNumber) => {
      const currentPageQs = currentPageQuestions.value
      const currentIdx = currentPageQs.findIndex(q => q.number === currentQuestionNumber)
      
      // Look for next unanswered in current page
      for (let i = currentIdx + 1; i < currentPageQs.length; i++) {
        const q = currentPageQs[i]
        const qIdx = getQuestionIndex(q.number)
        if (!answers.value[qIdx]) {
          return q.number
        }
      }
      return null
    }

    const scrollToQuestion = (questionNumber) => {
      const el = questionRefs.value[questionNumber]
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }

    const saveCurrentAnswers = async () => {
      if (!surveyId.value || Object.keys(answers.value).length === 0) return
      
      try {
        const answersToSave = Object.keys(answers.value).map(index => ({
          question: questions.value[index].id,
          rating: parseInt(answers.value[index])
        }))
        
        await surveyAPI.updateAnswers(surveyId.value, answersToSave)
      } catch (err) {
        console.error('Failed to save answers:', err)
      }
    }

    const totalPages = computed(() => {
      return Math.ceil(questions.value.length / QUESTIONS_PER_PAGE)
    })

    const pagesRemaining = computed(() => {
      return totalPages.value - currentPage.value
    })

    const currentPageQuestions = computed(() => {
      const start = (currentPage.value - 1) * QUESTIONS_PER_PAGE
      const end = start + QUESTIONS_PER_PAGE
      return questions.value.slice(start, end)
    })

    const progressPercentage = computed(() => {
      const answeredCount = Object.keys(answers.value).length
      return (answeredCount / questions.value.length) * 100
    })

    const isCurrentPageComplete = computed(() => {
      const pageQuestions = currentPageQuestions.value
      return pageQuestions.every(q => {
        const idx = getQuestionIndex(q.number)
        return answers.value[idx] !== undefined
      })
    })

    const allQuestionsAnswered = computed(() => {
      return Object.keys(answers.value).length === questions.value.length
    })

    const getQuestionIndex = (questionNumber) => {
      return questions.value.findIndex(q => q.number === questionNumber)
    }

    onMounted(async () => {
      try {
        const response = await surveyAPI.getQuestions()
        questions.value = response.data.results || response.data
        
        // Check for existing survey in localStorage
        const existingSurveyId = localStorage.getItem('currentSurveyId')
        if (existingSurveyId) {
          try {
            const surveyResponse = await surveyAPI.getSurveyResponse(existingSurveyId)
            if (!surveyResponse.data.is_complete) {
              surveyId.value = existingSurveyId
              userName.value = localStorage.getItem('surveyUserName') || ''
              surveyStarted.value = true
              
              // Load existing answers
              if (surveyResponse.data.answers) {
                surveyResponse.data.answers.forEach(answer => {
                  const qIndex = questions.value.findIndex(q => q.id === answer.question)
                  if (qIndex !== -1) {
                    answers.value[qIndex] = answer.rating
                  }
                })
              }
            } else {
              // Survey is complete, clear localStorage
              localStorage.removeItem('currentSurveyId')
              localStorage.removeItem('surveyUserName')
            }
          } catch (err) {
            // Survey not found or error, clear localStorage
            localStorage.removeItem('currentSurveyId')
            localStorage.removeItem('surveyUserName')
          }
        }
        
        loading.value = false
      } catch (err) {
        error.value = 'Failed to load survey questions. Please try again later.'
        loading.value = false
        console.error(err)
      }
    })

    const startSurvey = async () => {
      if (!userName.value || userName.value.trim() === '') {
        alert('Please enter your name to begin the survey.')
        return
      }
      
      try {
        // Create survey response
        const response = await surveyAPI.createSurveyResponse({
          name: userName.value.trim(),
          email: userEmail.value || null
        })
        
        surveyId.value = response.data.id
        
        // Store in localStorage for page reload recovery
        localStorage.setItem('currentSurveyId', surveyId.value)
        localStorage.setItem('surveyUserName', userName.value)
        
        surveyStarted.value = true
      } catch (err) {
        error.value = 'Failed to start survey. Please try again.'
        console.error(err)
      }
    }

    const nextPage = async () => {
      if (currentPage.value < totalPages.value) {
        await saveCurrentAnswers()
        currentPage.value++
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }

    const previousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }

    const submitSurvey = async () => {
      if (!allQuestionsAnswered.value) {
        alert('Please answer all questions before submitting.')
        return
      }

      if (!userName.value || userName.value.trim() === '') {
        alert('Name is required to submit the survey.')
        return
      }

      submitting.value = true
      
      try {
        // Save final answers
        await saveCurrentAnswers()
        
        // Mark survey as complete
        await surveyAPI.completeSurvey(surveyId.value)
        
        // Clear localStorage
        localStorage.removeItem('currentSurveyId')
        localStorage.removeItem('surveyUserName')

        // Navigate to results page
        router.push(`/results/${surveyId.value}`)
      } catch (err) {
        error.value = 'Failed to submit survey. Please try again.'
        submitting.value = false
        console.error(err)
      }
    }

    return {
      loading,
      error,
      questions,
      answers,
      currentPage,
      totalPages,
      pagesRemaining,
      currentPageQuestions,
      surveyStarted,
      userName,
      userEmail,
      submitting,
      progressPercentage,
      isCurrentPageComplete,
      allQuestionsAnswered,
      focusedQuestion,
      getQuestionIndex,
      setQuestionRef,
      handleAnswerChange,
      startSurvey,
      nextPage,
      previousPage,
      submitSurvey
    }
  }
}
</script>
