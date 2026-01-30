<template>
  <div class="gifts-container">
    <div v-if="loading" class="loading">
      <p>Loading spiritual gifts...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-else>
      <!-- Hero Image -->
      <div class="hero-image">
        <img src="https://example.com/spiritual-gifts-hero.jpg" alt="Spiritual Gifts" />
      </div>

      <!-- Intro Section -->
      <div class="card">
        <h2>Understanding Spiritual Gifts</h2>
        <p style="margin-top: 1rem; color: var(--text-secondary); line-height: 1.8;">
          Spiritual gifts are special abilities given by the Holy Spirit to believers for the purpose of building up the body of Christ. 
          These gifts enable us to serve God and others effectively. Discover the various spiritual gifts mentioned in Scripture 
          and find where you might best contribute to God's kingdom work.
        </p>
      </div>

      <!-- Gifts Grid -->
      <div class="gifts-grid">
        <div 
          v-for="gift in gifts" 
          :key="gift.id"
          class="gift-card"
        >
          <div class="gift-icon">
            <img :src="gift.icon_url || 'https://example.com/gift-icon.jpg'" :alt="gift.name" />
          </div>
          <h3 class="gift-title">{{ gift.name }}</h3>
          <p class="gift-description">{{ gift.description }}</p>
          
          <div class="gift-details-section">
            <div v-if="giftDetails[gift.name]" class="gift-extra-info">
              <div v-if="giftDetails[gift.name].examples" class="info-item">
                <strong>Biblical Examples:</strong>
                <p>{{ giftDetails[gift.name].examples }}</p>
              </div>
              <div v-if="giftDetails[gift.name].ministries" class="info-item">
                <strong>Ministry Opportunities:</strong>
                <p>{{ giftDetails[gift.name].ministries }}</p>
              </div>
              <div v-if="giftDetails[gift.name].verse" class="info-item scripture">
                <strong>Scripture:</strong>
                <p>"{{ giftDetails[gift.name].verse }}"</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="card cta-section">
        <h3 style="text-align: center; margin-bottom: 1rem;">Ready to Discover Your Gifts?</h3>
        <p style="text-align: center; color: var(--text-secondary); margin-bottom: 1.5rem;">
          Take our comprehensive 80-question survey to identify your unique spiritual gifts and find your place in ministry.
        </p>
        <div style="text-align: center;">
          <button class="btn btn-primary" @click="goToSurvey">
            Take the Survey Now
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { surveyAPI } from '../api'

export default {
  name: 'GiftsView',
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const error = ref(null)
    const gifts = ref([])

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

    onMounted(async () => {
      try {
        const response = await surveyAPI.getGifts()
        gifts.value = response.data.results || response.data
        loading.value = false
      } catch (err) {
        error.value = 'Failed to load spiritual gifts. Please try again later.'
        loading.value = false
        console.error(err)
      }
    })

    const goToSurvey = () => {
      router.push('/survey')
    }

    return {
      loading,
      error,
      gifts,
      giftDetails,
      goToSurvey
    }
  }
}
</script>

<style scoped>
.hero-image {
  width: 100%;
  max-height: 400px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gifts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.gift-card {
  background: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.gift-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.gift-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  overflow: hidden;
  background: var(--background);
}

.gift-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gift-title {
  text-align: center;
  color: var(--secondary-color);
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.gift-description {
  color: var(--text-primary);
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.gift-details-section {
  border-top: 2px solid var(--border-color);
  padding-top: 1rem;
}

.gift-extra-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  font-size: 0.9rem;
}

.info-item strong {
  color: var(--secondary-color);
  display: block;
  margin-bottom: 0.25rem;
}

.info-item p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.info-item.scripture {
  font-style: italic;
}

.cta-section {
  text-align: center;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  margin-top: 3rem;
}

@media (max-width: 768px) {
  .gifts-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .hero-image {
    max-height: 250px;
  }
}
</style>
