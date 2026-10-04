<template>
  <div class="archetypes-container">
    <div v-if="loading" class="loading">
      <p>Loading talent archetypes...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-else>
      <!-- Hero Image -->
      <div class="hero-image">
        <img src="/hero.jpg" alt="Spiritual Gifts" />
      </div>

      <!-- Intro Section -->
      <div class="card">
        <h2>Understanding Talent Archetypes</h2>
        <p style="margin-top: 1rem; color: var(--text-secondary); line-height: 1.8;">
          Spiritual gifts rarely come alone — they blend into a signature. A talent archetype is that blend:
          a way of serving that shows <em>where</em> you fit in God's work, not just <em>what</em> you are.
          The twelve archetypes below organize into three ministry families that mirror how a healthy church functions:
          <strong>Reach</strong> (grow &amp; win), <strong>Keep</strong> (care &amp; deepen), and <strong>Build</strong> (make it run). <br>
          Take the spiritual gifts survey <a href="/survey" style="color: var(--secondary-color); font-weight: 600; text-decoration: underline;">here</a> to discover your primary archetype.
        </p>
      </div>

      <!-- Families -->
      <template v-for="family in families" :key="family.name">
        <div class="family-header">
          <h3>{{ family.name }}</h3>
          <p>{{ family.tagline }}</p>
        </div>

        <div class="archetypes-grid">
          <div
            v-for="archetype in familyArchetypes(family.name)"
            :key="archetype.name"
            class="archetype-card"
          >
            <div class="archetype-badge" :class="'family-' + archetype.family.toLowerCase()">
              {{ archetype.family }}
            </div>
            <h3 class="archetype-title">{{ archetype.name }}</h3>
            <p class="archetype-tagline">{{ archetype.tagline }}</p>
            <p class="archetype-description">{{ archetype.description }}</p>

            <div class="archetype-section">
              <strong>Signature Gifts</strong>
              <div class="signature-chips">
                <span v-for="gift in archetype.signature" :key="gift" class="signature-chip">
                  {{ gift }}
                </span>
              </div>
            </div>

            <div class="archetype-section">
              <strong>Fits These Roles</strong>
              <p class="archetype-roles">{{ archetype.roles.join(', ') }}</p>
            </div>

            <div class="engage-note" v-if="archetype.engage">
              <strong>For Leaders:</strong> {{ archetype.engage }}
            </div>
          </div>
        </div>
      </template>

      <!-- CTA Section -->
      <div class="card cta-section">
        <h3 style="text-align: center; margin-bottom: 1rem;">Ready to Discover Your Archetype?</h3>
        <p style="text-align: center; color: var(--text-secondary); margin-bottom: 1.5rem;">
          Take our comprehensive 80-question survey to identify your gift blend and find your place in ministry.
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
  name: 'ArchetypesView',
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const error = ref(null)
    const archetypes = ref([])

    const families = [
      { name: 'Reach', tagline: 'Outward voice: grow & win' },
      { name: 'Keep', tagline: 'Inward care: retain & deepen' },
      { name: 'Build', tagline: 'Operations: make it run' }
    ]

    const familyArchetypes = (familyName) => {
      return archetypes.value.filter(a => a.family === familyName)
    }

    onMounted(async () => {
      try {
        const response = await surveyAPI.getArchetypes()
        archetypes.value = response.data.results || response.data
        loading.value = false
      } catch (err) {
        error.value = 'Failed to load talent archetypes. Please try again later.'
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
      archetypes,
      families,
      familyArchetypes,
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

.family-header {
  margin: 3rem 0 1.5rem;
  text-align: center;
}

.family-header h3 {
  font-size: 2rem;
  color: var(--secondary-color);
  margin-bottom: 0.35rem;
}

.family-header p {
  color: var(--text-secondary);
  font-style: italic;
  margin: 0;
}

.archetypes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.archetype-card {
  background: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.archetype-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.archetype-badge {
  display: inline-block;
  padding: 0.2rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

.archetype-badge.family-reach {
  background: rgba(245, 101, 101, 0.15);
  color: #c53030;
}

.archetype-badge.family-keep {
  background: rgba(72, 187, 120, 0.15);
  color: #276749;
}

.archetype-badge.family-build {
  background: rgba(102, 126, 234, 0.15);
  color: #4c51bf;
}

.archetype-title {
  color: var(--secondary-color);
  font-size: 1.5rem;
  margin-bottom: 0.35rem;
  font-weight: 700;
}

.archetype-tagline {
  font-style: italic;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.archetype-description {
  color: var(--text-primary);
  line-height: 1.7;
  margin-bottom: 1.25rem;
}

.archetype-section {
  border-top: 2px solid var(--border-color);
  padding-top: 1rem;
  margin-top: 1rem;
}

.archetype-section strong {
  color: var(--secondary-color);
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.signature-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.signature-chip {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
  padding: 0.25rem 0.75rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 999px;
}

.archetype-roles {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.engage-note {
  padding: 0.75rem;
  background: var(--background);
  border-radius: 6px;
  border-left: 4px solid var(--secondary-color);
  margin-top: 1rem;
  font-size: 0.9rem;
}

.cta-section {
  text-align: center;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  margin-top: 3rem;
}

@media (max-width: 768px) {
  .archetypes-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .hero-image {
    max-height: 250px;
  }
}
</style>