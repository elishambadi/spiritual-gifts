<template>
  <div class="admin-container">
    <div class="card">
      <h2>Admin Dashboard - Spiritual Gifts Leaderboard</h2>
      <p style="margin-top: 0.5rem; color: var(--text-secondary);">
        Top 5 performers by percentage for each spiritual gift.
      </p>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Loading leaderboard data...</p>
    </div>

    <div v-else-if="error" class="error card">
      <p>{{ error }}</p>
    </div>

<div v-else>
          <div v-for="giftData in leaderboard" :key="giftData.gift_name" class="card gift-leaderboard">
            <h3 class="gift-title">{{ giftData.gift_name }}</h3>
            
            <div v-if="giftData.top_performers.length === 0" class="no-data">
              <p>No completed surveys for this gift yet.</p>
            </div>
            
            <div v-else class="performers-table">
              <div class="table-header">
                <div class="col-rank">Rank</div>
                <div class="col-name">Name</div>
                <div class="col-percentage">Percentage</div>
                <div class="col-score">Score</div>
              </div>
              <div 
                v-for="(performer, index) in giftData.top_performers" 
                :key="index"
                class="table-row"
                :class="'rank-' + (index + 1)"
              >
                <div class="col-rank">
                  <span class="rank-badge">{{ index + 1 }}</span>
                </div>
                <div class="col-name">{{ performer.name }}</div>
                <div class="col-percentage">
                  <div class="percentage-bar">
                    <div class="percentage-fill" :style="{ width: performer.percentage + '%' }"></div>
                  </div>
                  <span class="percentage-text">{{ performer.percentage }}%</span>
                </div>
                <div class="col-score">{{ performer.score }}</div>
              </div>
</div>
        </div>
      </div>

    <!-- Archetype Roster -->
    <div class="card">
      <h2>Archetype Roster</h2>
      <p style="margin-top: 0.5rem; color: var(--text-secondary);">
        Every completed submission grouped by its primary archetype.
      </p>
    </div>

    <div v-if="archetypesLoading" class="loading">
      <div class="loading-spinner"></div>
      <p>Loading archetype roster...</p>
    </div>

    <div v-else-if="archetypesError" class="error card">
      <p>{{ archetypesError }}</p>
    </div>

    <div v-else>
      <template v-for="family in archetypeFamilies" :key="family">
        <div class="family-header">
          <h3>{{ family }}</h3>
        </div>

        <div
          v-for="archetype in archetypesInFamily(family)"
          :key="archetype.name"
          class="card archetype-roster"
        >
          <div class="archetype-head">
            <div>
              <span class="archetype-badge" :class="'family-' + archetype.family.toLowerCase()">
                {{ archetype.family }}
              </span>
              <h3 class="archetype-title">{{ archetype.name }}</h3>
              <p class="archetype-tagline">{{ archetype.tagline }}</p>
            </div>
            <div class="member-count">
              <span class="member-count-num">{{ archetype.member_count }}</span>
              <span class="member-count-label">people</span>
            </div>
          </div>

          <div v-if="archetype.members.length === 0" class="no-data">
            <p>No completed surveys matched this archetype yet.</p>
          </div>

          <div v-else class="performers-table">
            <div class="table-header">
              <div class="col-rank">Rank</div>
              <div class="col-name">Name</div>
              <div class="col-percentage">Match</div>
              <div class="col-gifts">Top Gifts</div>
            </div>
            <div
              v-for="(member, index) in archetype.members"
              :key="member.response_id"
              class="table-row"
              :class="'rank-' + (index + 1)"
            >
              <div class="col-rank">
                <span class="rank-badge">{{ index + 1 }}</span>
              </div>
              <div class="col-name">{{ member.name }}</div>
              <div class="col-percentage">
                <div class="percentage-bar">
                  <div class="percentage-fill" :style="{ width: member.match_percentage + '%' }"></div>
                </div>
                <span class="percentage-text">{{ member.match_percentage }}%</span>
              </div>
              <div class="col-gifts">
                <span v-for="gift in member.top_gifts" :key="gift" class="gift-tag">
                  {{ gift }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { surveyAPI } from '../api'

export default {
  name: 'AdminView',
  setup() {
    const loading = ref(true)
    const error = ref(null)
    const leaderboard = ref([])
    const archetypesLoading = ref(true)
    const archetypesError = ref(null)
    const archetypeRoster = ref([])

    const archetypeFamilies = ['Reach', 'Keep', 'Build']

    const archetypesInFamily = (family) => {
      return archetypeRoster.value.filter(a => a.family === family)
    }

    onMounted(async () => {
      try {
        const response = await surveyAPI.getAdminLeaderboard()
        leaderboard.value = response.data
        loading.value = false
      } catch (err) {
        if (err.response && err.response.status === 403) {
          error.value = 'Access denied. Admin privileges required.'
        } else {
          error.value = 'Failed to load leaderboard data. Please try again.'
        }
        loading.value = false
        console.error(err)
      }

      try {
        const rosterResponse = await surveyAPI.getAdminArchetypes()
        archetypeRoster.value = rosterResponse.data
        archetypesLoading.value = false
      } catch (err) {
        if (err.response && err.response.status === 403) {
          archetypesError.value = 'Access denied. Admin privileges required.'
        } else {
          archetypesError.value = 'Failed to load archetype roster. Please try again.'
        }
        archetypesLoading.value = false
        console.error(err)
      }
    })

    return {
      loading,
      error,
      leaderboard,
      archetypesLoading,
      archetypesError,
      archetypeRoster,
      archetypeFamilies,
      archetypesInFamily
    }
  }
}
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
}

.gift-leaderboard {
  margin-bottom: 2rem;
}

.gift-title {
  color: var(--secondary-color);
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--border-color);
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  font-style: italic;
}

.performers-table {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.table-header {
  display: grid;
  grid-template-columns: 60px 1fr 200px 80px;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: var(--background);
  border-radius: 6px;
  font-weight: 700;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.table-row {
  display: grid;
  grid-template-columns: 60px 1fr 200px 80px;
  gap: 1rem;
  padding: 1rem;
  background: var(--background);
  border-radius: 6px;
  align-items: center;
  transition: all 0.2s ease;
}

.table-row:hover {
  background: rgba(102, 126, 234, 0.05);
  transform: translateX(4px);
}

.table-row.rank-1 {
  border-left: 4px solid #f6ad55;
}

.table-row.rank-2 {
  border-left: 4px solid #a0aec0;
}

.table-row.rank-3 {
  border-left: 4px solid #ed8936;
}

.col-rank {
  text-align: center;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--secondary-color);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.9rem;
}

.col-name {
  font-weight: 600;
  color: var(--text-primary);
}

.col-percentage {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.percentage-bar {
  flex: 1;
  height: 8px;
  background: var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.percentage-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--secondary-color), var(--success-color));
  transition: width 0.3s ease;
}

.percentage-text {
  font-weight: 700;
  color: var(--secondary-color);
  min-width: 50px;
  text-align: right;
}

.col-score {
  text-align: center;
  font-weight: 700;
  color: var(--text-primary);
}

.family-header {
  margin: 2.5rem 0 1.5rem;
  text-align: center;
}

.family-header h3 {
  font-size: 1.75rem;
  color: var(--secondary-color);
  margin: 0;
}

.archetype-roster {
  margin-bottom: 2rem;
}

.archetype-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.archetype-badge {
  display: inline-block;
  padding: 0.2rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
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
  font-size: 1.4rem;
  margin: 0.5rem 0 0.25rem;
}

.archetype-tagline {
  font-style: italic;
  color: var(--text-secondary);
  margin: 0;
}

.member-count {
  text-align: right;
  flex-shrink: 0;
}

.member-count-num {
  display: block;
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--secondary-color);
  line-height: 1.1;
}

.member-count-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.col-gifts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.gift-tag {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-primary);
  padding: 0.2rem 0.6rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 999px;
  white-space: nowrap;
}

.table-header .col-gifts {
  align-items: center;
}

.archetype-roster .table-header,
.archetype-roster .table-row {
  grid-template-columns: 60px 1fr 200px 1fr;
}

@media (max-width: 768px) {
  .table-header,
  .table-row,
  .archetype-roster .table-header,
  .archetype-roster .table-row {
    grid-template-columns: 50px 1fr 80px;
    gap: 0.5rem;
  }
  
  .col-percentage {
    grid-column: 1 / -1;
    margin-top: 0.5rem;
  }
  
  .col-score {
    display: none;
  }
  
  .col-gifts {
    grid-column: 1 / -1;
  }
}
</style>
