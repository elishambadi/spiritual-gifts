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
    })

    return {
      loading,
      error,
      leaderboard
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

@media (max-width: 768px) {
  .table-header,
  .table-row {
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
}
</style>
