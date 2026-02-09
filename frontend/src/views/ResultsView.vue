<template>
  <div class="results-container">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Calculating your spiritual gifts...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-else>
      <!-- Action Icons -->
      <div class="action-icons">
        <button @click="printResults" class="icon-btn" title="Print Results">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 6 2 18 2 18 9"></polyline>
            <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
            <rect x="6" y="14" width="12" height="8"></rect>
          </svg>
        </button>
        <button @click="shareResults" class="icon-btn" title="Share Results">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="18" cy="5" r="3"></circle>
            <circle cx="6" cy="12" r="3"></circle>
            <circle cx="18" cy="19" r="3"></circle>
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
          </svg>
        </button>
      </div>

      <!-- Header -->
      <div class="card">
        <h2>Your Spiritual Gifts Assessment Results</h2>
        <p v-if="surveyResponse.name" style="margin-top: 0.5rem; color: var(--text-secondary);">
          For: <strong>{{ surveyResponse.name }}</strong>
        </p>
        <p style="margin-top: 0.5rem; color: var(--text-secondary);">
          Completed: {{ formatDate(surveyResponse.completed_at) }}
        </p>
      </div>

      <!-- Top 3 Gifts - No Scores -->
      <div class="card top-gifts-showcase">
        <h3 style="margin-bottom: 2rem; text-align: center;">Your Top 3 Spiritual Gifts</h3>
        <div class="top-gifts-grid">
          <div 
            v-for="(result, index) in results.slice(0, 3)" 
            :key="index"
            class="top-gift-card"
            :class="'rank-' + (index + 1)"
          >
            <div class="rank-badge">{{ index + 1 }}</div>
            <div class="gift-name-large">{{ result.gift_name }}</div>
          </div>
        </div>
        <p style="text-align: center; margin-top: 2rem; color: var(--text-secondary); font-style: italic;">
          Scroll down to see detailed scores and descriptions
        </p>
      </div>

      <!-- Gift Descriptions for Top 3 -->
      <div class="card">
        <h3 style="margin-bottom: 1.5rem;">Understanding Your Top Gifts</h3>
        <div v-for="(result, index) in results.slice(0, 3)" :key="index" style="margin-bottom: 2rem;">
          <h4 style="color: var(--secondary-color); margin-bottom: 0.75rem; font-size: 1.3rem;">
            {{ result.gift_name }}
          </h4>
          <div class="gift-description">
            <p style="line-height: 1.8; margin-bottom: 1rem;">
              {{ getGiftDescription(result.gift_name) }}
            </p>
            <div v-if="getGiftDetails(result.gift_name)" class="gift-details">
              <div v-if="getGiftDetails(result.gift_name).examples" style="margin-bottom: 0.75rem;">
                <strong>Biblical Examples:</strong> {{ getGiftDetails(result.gift_name).examples }}
              </div>
              <div v-if="getGiftDetails(result.gift_name).ministries" style="margin-bottom: 0.75rem;">
                <strong>Ministry Opportunities:</strong> {{ getGiftDetails(result.gift_name).ministries }}
              </div>
              <div v-if="getGiftDetails(result.gift_name).verse" style="font-style: italic; color: var(--text-secondary);">
                <strong>Scripture:</strong> "{{ getGiftDetails(result.gift_name).verse }}"
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Complete Results with Scores -->
      <div class="card">
        <h3 style="margin-bottom: 1.5rem;">Complete Results with Scores</h3>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <div 
            v-for="(result, index) in results" 
            :key="index"
            style="padding: 1rem; background: var(--background); border-radius: 6px; border-left: 4px solid var(--secondary-color);"
          >
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-size: 1.2rem; font-weight: 700;">
                {{ index + 1 }}. {{ result.gift_name }}
              </span>
              <span style="font-size: 1.5rem; font-weight: 700; color: var(--secondary-color);">
                {{ result.score }}
              </span>
            </div>
            <div>
              <div class="progress-bar" style="height: 10px;">
                <div 
                  class="progress-bar-fill" 
                  :style="{ width: result.percentage + '%' }"
                ></div>
              </div>
              <span style="font-size: 0.85rem; color: var(--text-secondary);">
                {{ result.percentage.toFixed(1) }}% of total score
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Community Results -->
      <div class="card">
        <h3 style="margin-bottom: 1.5rem;">Community Top Gifts</h3>
        <p style="margin-bottom: 1.5rem; color: var(--text-secondary);">
          See the top 3 spiritual gifts from others who completed the survey.
        </p>
        <div v-if="communityLoading" class="loading">
          <p>Loading community results...</p>
        </div>
        <div v-else-if="communityError" class="error">
          <p>{{ communityError }}</p>
        </div>
        <div v-else class="community-grid">
          <div v-for="summary in communitySummaries" :key="summary.response_id" class="community-card">
            <div class="community-name">{{ summary.name }}</div>
            <div class="community-gifts">
              <span v-for="(gift, index) in summary.top_gifts" :key="index" class="community-gift">
                {{ gift }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="card" style="text-align: center;">
        <button class="btn btn-primary" @click="startNewSurvey">
          Take Survey Again
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { surveyAPI } from '../api'

export default {
  name: 'ResultsView',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const loading = ref(true)
    const error = ref(null)
    const results = ref([])
    const surveyResponse = ref({})
    const communitySummaries = ref([])
    const communityLoading = ref(true)
    const communityError = ref(null)

    const giftDescriptions = {
      'Leadership': 'You have the ability to set goals in accordance with God\'s purposes and communicate them to others in such a way that they work together to accomplish those goals.',
      'Administration': 'You have the ability to organize ideas, resources, time, and people effectively to accomplish God\'s purposes in ministry.',
      'Teaching': 'You have the ability to communicate information relevant to the health and ministry of the body and its members in a way that helps others learn.',
      'Knowledge': 'You have the ability to discover, accumulate, analyze, and clarify information and ideas that are pertinent to the growth and well-being of the body.',
      'Wisdom': 'You have the ability to apply knowledge to specific situations in ways that bring insight and direction to God\'s people.',
      'Prophecy': 'You have the ability to proclaim God\'s truth in a way that calls people to righteousness and strengthens, encourages, or comforts them.',
      'Discernment': 'You have the ability to distinguish between truth and error, to discern the spirits, and to recognize whether something is of God.',
      'Exhortation': 'You have the ability to come alongside people to encourage, comfort, or urge them toward action that strengthens their walk with God.',
      'Shepherding': 'You have the ability to nurture, care for, and guide people toward ongoing spiritual maturity and becoming like Christ.',
      'Faith': 'You have the ability to act on God\'s promises with confidence and unwavering belief in God\'s ability to fulfill His purposes.',
      'Evangelism': 'You have the ability to communicate the gospel to unbelievers in a clear and meaningful way that brings them to respond in faith.',
      'Apostleship': 'You have the ability to start and oversee the development of new churches or ministry structures to expand God\'s kingdom.',
      'Service/Helps': 'You have the ability to identify unmet needs in the body and make use of available resources to meet them and help others increase their effectiveness.',
      'Mercy': 'You have the ability to feel genuine empathy and compassion for individuals suffering and translate that compassion into cheerfully done acts of service.',
      'Giving': 'You have the ability to contribute material resources to the work of the Lord with liberality and cheerfulness.',
      'Hospitality': 'You have the ability to provide an open house and a warm welcome to those in need of food, lodging, or fellowship.'
    }

    const giftDetails = {
      'Leadership': {
        examples: 'Moses, Nehemiah, Paul, Ellen G. White',
        ministries: 'Church leadership, department heads, ministry coordinators, board members, Pathfinder directors',
        verse: 'Romans 12:8 - If it is to lead, do it diligently'
      },
      'Administration': {
        examples: 'Joseph, Daniel, Jethro (advisor to Moses)',
        ministries: 'Church treasurer, secretary, event planning, facility management, database management',
        verse: '1 Corinthians 12:28 - God has placed in the church...those with gifts of administration'
      },
      'Teaching': {
        examples: 'Ezra, Jesus Christ, Apollos, Timothy',
        ministries: 'Sabbath School teaching, Bible studies, children\'s ministries, seminary instruction, health education',
        verse: 'Ephesians 4:11 - And he gave...the teachers'
      },
      'Knowledge': {
        examples: 'Solomon, Daniel, Luke the physician',
        ministries: 'Research, curriculum development, library services, health education, seminary teaching',
        verse: '1 Corinthians 12:8 - To one there is given through the Spirit a message of knowledge'
      },
      'Wisdom': {
        examples: 'Solomon, Joseph, Stephen, James',
        ministries: 'Counseling, conflict resolution, elder board, advisory roles, mentoring',
        verse: '1 Corinthians 12:8 - To one there is given...a message of wisdom'
      },
      'Prophecy': {
        examples: 'Elijah, John the Baptist, Ellen G. White, the apostles',
        ministries: 'Preaching, revival speaking, writing, prophetic ministry, Biblical interpretation',
        verse: 'Romans 12:6 - If your gift is prophesying, then prophesy in accordance with your faith'
      },
      'Discernment': {
        examples: 'Daniel, Peter, John',
        ministries: 'Church board, theological review, counseling, security ministry, doctrinal committees',
        verse: '1 Corinthians 12:10 - To another distinguishing between spirits'
      },
      'Exhortation': {
        examples: 'Barnabas, Paul, Silas',
        ministries: 'Small group leadership, visitation ministry, encouragement cards, prayer ministry, recovery groups',
        verse: 'Romans 12:8 - If it is to encourage, then give encouragement'
      },
      'Shepherding': {
        examples: 'David, Jesus the Good Shepherd, Peter',
        ministries: 'Pastoral care, small group facilitation, mentoring, youth ministry, elder responsibilities',
        verse: 'Ephesians 4:11 - And he gave...the pastors'
      },
      'Faith': {
        examples: 'Abraham, Elijah, George Mueller, pioneers of missions',
        ministries: 'Prayer ministry, mission advancement, building projects, faith-based initiatives, church planting',
        verse: '1 Corinthians 12:9 - To another faith by the same Spirit'
      },
      'Evangelism': {
        examples: 'Philip, Peter at Pentecost, Paul, William Miller',
        ministries: 'Public evangelism, Bible work, literature evangelism, media evangelism, personal witnessing',
        verse: 'Ephesians 4:11 - And he gave...the evangelists'
      },
      'Apostleship': {
        examples: 'Paul, Peter, modern mission pioneers',
        ministries: 'Church planting, mission work, establishing new ministries, international missions, pioneering work',
        verse: '1 Corinthians 12:28 - God has placed in the church first of all apostles'
      },
      'Service/Helps': {
        examples: 'Dorcas (Tabitha), Epaphroditus, Martha',
        ministries: 'Deacon/deaconess, hospitality team, maintenance, setup/cleanup, Community Services, food ministry',
        verse: 'Romans 12:7 - If it is serving, then serve'
      },
      'Mercy': {
        examples: 'Good Samaritan, Jesus healing the sick, Mother Teresa',
        ministries: 'Hospital visitation, Community Services, grief support, nursing home ministry, addiction recovery',
        verse: 'Romans 12:8 - If it is to show mercy, do it cheerfully'
      },
      'Giving': {
        examples: 'Barnabas, the Macedonian churches, Joseph of Arimathea',
        ministries: 'Stewardship committee, funding special projects, scholarship programs, building campaigns, mission support',
        verse: 'Romans 12:8 - If it is to give, then give generously'
      },
      'Hospitality': {
        examples: 'Abraham, Lydia, Priscilla and Aquila',
        ministries: 'Welcoming ministry, hosting small groups, fellowship dinners, guest accommodation, missionary hosting',
        verse: '1 Peter 4:9 - Offer hospitality to one another without grumbling'
      }
    }

    const giftColors = [
      '#667eea', '#f56565', '#48bb78', '#ed8936', 
      '#9f7aea', '#38b2ac', '#ecc94b', '#ed64a6',
      '#4299e1', '#f6ad55', '#fc8181', '#68d391',
      '#b794f4', '#4fd1c5', '#f6e05e'
    ]

    onMounted(async () => {
      try {
        const surveyId = route.params.id
        
        // Get survey response
        const responseData = await surveyAPI.getSurveyResponse(surveyId)
        surveyResponse.value = responseData.data
        
        // Get results
        const resultsData = await surveyAPI.getSurveyResults(surveyId)
        results.value = resultsData.data
        
        loading.value = false
      } catch (err) {
        error.value = 'Failed to load results. Please try again.'
        loading.value = false
        console.error(err)
      }

      // Load community summaries
      try {
        const summariesResponse = await surveyAPI.getPublicSummaries()
        communitySummaries.value = summariesResponse.data
        communityLoading.value = false
      } catch (err) {
        communityError.value = 'Failed to load community results.'
        communityLoading.value = false
        console.error(err)
      }
    })

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getGiftDescription = (giftName) => {
      return giftDescriptions[giftName] || 'This is a wonderful spiritual gift that God has given you to serve His church.'
    }

    const getGiftDetails = (giftName) => {
      return giftDetails[giftName] || null
    }

    const getGiftColor = (index) => {
      return giftColors[index % giftColors.length]
    }

    const startNewSurvey = () => {
      router.push('/')
    }

    const printResults = () => {
      window.print()
    }

    const shareResults = async () => {
      const shareData = {
        title: 'My Spiritual Gifts Results',
        text: `I discovered my top spiritual gifts: ${results.value.slice(0, 3).map(r => r.gift_name).join(', ')}`,
        url: window.location.href
      }
      
      if (navigator.share) {
        try {
          await navigator.share(shareData)
        } catch (err) {
          if (err.name !== 'AbortError') {
            copyToClipboard()
          }
        }
      } else {
        copyToClipboard()
      }
    }

    const copyToClipboard = () => {
      const url = window.location.href
      navigator.clipboard.writeText(url).then(() => {
        alert('Link copied to clipboard!')
      }).catch(() => {
        alert('Unable to copy link. Please copy manually: ' + url)
      })
    }

    return {
      loading,
      error,
      results,
      surveyResponse,
      communitySummaries,
      communityLoading,
      communityError,
      formatDate,
      getGiftDescription,
      getGiftDetails,
      getGiftColor,
      startNewSurvey,
      printResults,
      shareResults
    }
  }
}
</script>

<style scoped>
.community-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.community-card {
  background: var(--background);
  padding: 1rem;
  border-radius: 6px;
  border-left: 3px solid var(--secondary-color);
}

.community-name {
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.community-gifts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.community-gift {
  font-size: 0.9rem;
  color: var(--text-secondary);
  padding: 0.25rem 0.5rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 4px;
  display: inline-block;
}

@media print {
  button {
    display: none;
  }
}
</style>
