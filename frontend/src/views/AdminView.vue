<template>
  <div class="admin-container">
    <!-- Header -->
    <div class="card admin-header">
      <div class="header-main">
        <div>
          <h2>Admin Reports</h2>
          <p class="subtitle">
            Top 5 participants per spiritual gift, ranked by share of their personal score.
          </p>
        </div>
        <div class="header-actions">
          <span v-if="lastUpdated" class="updated">Updated {{ lastUpdated }}</span>
          <button class="btn btn-secondary" @click="retry" :disabled="refreshing">
            {{ refreshing ? 'Refreshing...' : 'Refresh' }}
          </button>
          <button class="btn btn-primary" @click="exportCsv" :disabled="!hasResults">
            Export CSV
          </button>
          <button class="btn btn-primary" @click="printReport" :disabled="!hasResults">
            Print
          </button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Loading leaderboard data...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error card">
      <p>{{ error }}</p>
      <button class="btn btn-secondary" style="margin-top: 1rem;" @click="retry">Try again</button>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Overview stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-value">{{ stats.giftsWithData }}<span class="stat-total">/{{ stats.totalGifts }}</span></span>
          <span class="stat-label">Gifts with data</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ stats.uniqueParticipants }}</span>
          <span class="stat-label">Participants ranked</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ stats.totalEntries }}</span>
          <span class="stat-label">Leaderboard entries</span>
        </div>
        <div class="stat-card">
          <span class="stat-value stat-value--text">{{ stats.leadingGift }}</span>
          <span class="stat-label">Most represented gift</span>
        </div>
      </div>

      <!-- Metric explanation -->
      <div class="card info-note">
        <strong>How to read this:</strong>
        Share is the percentage of a participant's <em>own</em> total score that this gift represents.
        It highlights relative gifting strength, not absolute performance, so it is not comparable across participants.
      </div>

      <!-- Controls -->
      <div class="card controls">
        <div class="control">
          <label for="admin-search">Search</label>
          <input
            id="admin-search"
            type="text"
            v-model="searchQuery"
            placeholder="Filter by participant or gift name"
          />
        </div>

        <div class="control">
          <label for="admin-sort">Sort gifts by</label>
          <select id="admin-sort" v-model="sortBy">
            <option value="name">Gift name (A-Z)</option>
            <option value="participants">Most participants</option>
            <option value="topShare">Highest top share</option>
          </select>
        </div>

        <div class="control control--toggle">
          <label class="toggle">
            <input type="checkbox" v-model="hideEmpty" />
            <span>Hide gifts with no data</span>
          </label>
        </div>

        <div class="control control--full">
          <label>Jump to gift</label>
          <div class="pills">
            <button
              class="pill"
              :class="{ active: activeGift === 'all' }"
              @click="activeGift = 'all'"
            >
              All
            </button>
            <button
              v-for="name in giftNames"
              :key="name"
              class="pill"
              :class="{ active: activeGift === name }"
              @click="activeGift = name"
            >
              {{ name }}
            </button>
          </div>
        </div>
      </div>

      <!-- Empty results -->
      <div v-if="!visibleGifts.length" class="card no-results">
        <p>No gifts match your filters.</p>
        <button class="btn btn-secondary" style="margin-top: 1rem;" @click="resetFilters">Clear filters</button>
      </div>

      <!-- Gift grid -->
      <div v-else class="gift-grid">
        <div
          v-for="gift in visibleGifts"
          :key="gift.gift_name"
          class="card gift-card"
          :id="'gift-' + slugify(gift.gift_name)"
        >
          <div class="gift-card-header">
            <h3 class="gift-title">{{ gift.gift_name }}</h3>
            <span class="count-badge">
              {{ gift.top_performers.length }}
              {{ gift.top_performers.length === 1 ? 'entry' : 'entries' }}
            </span>
          </div>

          <div v-if="gift.top_performers.length === 0" class="no-data">
            <p>No completed surveys for this gift yet.</p>
          </div>

          <ol v-else class="performer-list">
            <li
              v-for="(performer, index) in gift.top_performers"
              :key="performer.response_id + '-' + index"
              class="performer-row"
              :class="'rank-' + (index + 1)"
            >
              <span class="rank-badge">{{ index + 1 }}</span>
              <div class="performer-main">
                <div class="performer-top">
                  <span class="performer-name">{{ performer.name }}</span>
                  <span class="performer-share">{{ performer.percentage }}%</span>
                </div>
                <div
                  class="share-bar"
                  role="progressbar"
                  :aria-valuenow="performer.percentage"
                  aria-valuemin="0"
                  aria-valuemax="100"
                  :aria-label="performer.name + ' share for ' + gift.gift_name"
                >
                  <div class="share-fill" :style="{ width: performer.percentage + '%' }"></div>
                </div>
              </div>
              <span class="performer-score" :title="'Raw score: ' + performer.score">
                {{ performer.score }}
              </span>
            </li>
          </ol>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { surveyAPI } from '../api'

export default {
  name: 'AdminView',
  setup() {
    const loading = ref(true)
    const refreshing = ref(false)
    const error = ref(null)
    const leaderboard = ref([])
    const lastUpdated = ref('')

    const searchQuery = ref('')
    const sortBy = ref('name')
    const hideEmpty = ref(true)
    const activeGift = ref('all')

    const fetchLeaderboard = async () => {
      refreshing.value = true
      error.value = null
      try {
        const response = await surveyAPI.getAdminLeaderboard()
        leaderboard.value = response.data
        lastUpdated.value = new Date().toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (err) {
        if (err.response && err.response.status === 403) {
          error.value = 'Access denied. Admin privileges required.'
        } else {
          error.value = 'Failed to load leaderboard data. Please try again.'
        }
        console.error(err)
      } finally {
        loading.value = false
        refreshing.value = false
      }
    }

    const retry = () => {
      loading.value = true
      fetchLeaderboard()
    }

    const resetFilters = () => {
      searchQuery.value = ''
      sortBy.value = 'name'
      hideEmpty.value = true
      activeGift.value = 'all'
    }

    const slugify = (value) => value.toLowerCase().replace(/[^a-z0-9]+/g, '-')

    const giftNames = computed(() => leaderboard.value.map((gift) => gift.gift_name))

    const hasResults = computed(() =>
      leaderboard.value.some((gift) => gift.top_performers.length > 0)
    )

    const stats = computed(() => {
      const totalGifts = leaderboard.value.length
      const giftsWithData = leaderboard.value.filter(
        (gift) => gift.top_performers.length > 0
      ).length
      const totalEntries = leaderboard.value.reduce(
        (sum, gift) => sum + gift.top_performers.length,
        0
      )

      const participantIds = new Set()
      let leadingGift = '—'
      let leadingCount = 0

      leaderboard.value.forEach((gift) => {
        gift.top_performers.forEach((performer) => participantIds.add(performer.response_id))
        if (gift.top_performers.length > leadingCount) {
          leadingCount = gift.top_performers.length
          leadingGift = gift.gift_name
        }
      })

      return {
        totalGifts,
        giftsWithData,
        totalEntries,
        uniqueParticipants: participantIds.size,
        leadingGift
      }
    })

    const visibleGifts = computed(() => {
      const query = searchQuery.value.trim().toLowerCase()

      let list = leaderboard.value.map((gift) => {
        if (!query || gift.gift_name.toLowerCase().includes(query)) {
          return gift
        }
        return {
          ...gift,
          top_performers: gift.top_performers.filter((performer) =>
            (performer.name || '').toLowerCase().includes(query)
          )
        }
      })

      if (activeGift.value !== 'all') {
        list = list.filter((gift) => gift.gift_name === activeGift.value)
      }

      if (hideEmpty.value) {
        list = list.filter((gift) => gift.top_performers.length > 0)
      }

      const topShare = (gift) =>
        gift.top_performers.length
          ? Math.max(...gift.top_performers.map((p) => p.percentage))
          : -1

      return [...list].sort((a, b) => {
        if (sortBy.value === 'participants') {
          return (
            b.top_performers.length - a.top_performers.length ||
            a.gift_name.localeCompare(b.gift_name)
          )
        }
        if (sortBy.value === 'topShare') {
          return topShare(b) - topShare(a) || a.gift_name.localeCompare(b.gift_name)
        }
        return a.gift_name.localeCompare(b.gift_name)
      })
    })

    const exportCsv = () => {
      const rows = [['Gift', 'Rank', 'Name', 'Share (%)', 'Score']]
      visibleGifts.value.forEach((gift) => {
        gift.top_performers.forEach((performer, index) => {
          rows.push([
            gift.gift_name,
            index + 1,
            performer.name,
            performer.percentage,
            performer.score
          ])
        })
      })

      const csv = rows
        .map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(','))
        .join('\n')

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `spiritual-gifts-leaderboard-${new Date().toISOString().slice(0, 10)}.csv`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }

    const printReport = () => {
      window.print()
    }

    onMounted(fetchLeaderboard)

    return {
      loading,
      refreshing,
      error,
      lastUpdated,
      searchQuery,
      sortBy,
      hideEmpty,
      activeGift,
      giftNames,
      hasResults,
      stats,
      visibleGifts,
      retry,
      resetFilters,
      slugify,
      exportCsv,
      printReport
    }
  }
}
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.admin-header {
  padding: 1.5rem 2rem;
}

.header-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.admin-header h2 {
  margin-bottom: 0.35rem;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.updated {
  font-size: 0.85rem;
  color: var(--text-secondary);
  white-space: nowrap;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: var(--card-background);
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  border-left: 4px solid var(--secondary-color);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--secondary-color);
  line-height: 1.1;
}

.stat-value--text {
  font-size: 1.25rem;
  line-height: 1.6;
}

.stat-total {
  font-size: 1.1rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

/* Info note */
.info-note {
  padding: 1rem 1.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.7;
  border-left: 4px solid var(--secondary-color);
}

.info-note strong {
  color: var(--text-primary);
}

/* Controls */
.controls {
  display: grid;
  grid-template-columns: 1fr 220px auto;
  gap: 1.25rem;
  align-items: end;
  padding: 1.5rem 2rem;
}

.control {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.control--full {
  grid-column: 1 / -1;
}

.control label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.control select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 1rem;
  background: var(--card-background);
  color: var(--text-primary);
  cursor: pointer;
}

.control select:focus {
  outline: none;
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.control--toggle {
  align-self: center;
  padding-bottom: 0.35rem;
}

.toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: none;
  letter-spacing: normal;
  cursor: pointer;
  white-space: nowrap;
}

.toggle input {
  width: 18px;
  height: 18px;
  accent-color: var(--secondary-color);
  cursor: pointer;
}

.pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.pill {
  padding: 0.4rem 0.9rem;
  border-radius: 999px;
  border: 1px solid var(--border-color);
  background: var(--background);
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pill:hover {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
}

.pill.active {
  background: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}

/* Gift grid */
.gift-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.5rem;
  align-items: start;
}

.gift-card {
  margin-bottom: 0;
  padding: 1.5rem;
}

.gift-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--border-color);
}

.gift-title {
  color: var(--secondary-color);
  font-size: 1.25rem;
}

.count-badge {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--secondary-color);
  background: rgba(102, 126, 234, 0.1);
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  white-space: nowrap;
}

.no-data {
  text-align: center;
  padding: 1.5rem;
  color: var(--text-secondary);
  font-style: italic;
  font-size: 0.9rem;
}

/* Performer list */
.performer-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.performer-row {
  display: grid;
  grid-template-columns: 32px 1fr auto;
  gap: 0.75rem;
  align-items: center;
  padding: 0.5rem 0.6rem;
  border-radius: 6px;
  border-left: 3px solid transparent;
  transition: background 0.2s ease;
}

.performer-row:hover {
  background: rgba(102, 126, 234, 0.05);
}

.performer-row.rank-1 {
  border-left-color: #f6ad55;
}

.performer-row.rank-2 {
  border-left-color: #a0aec0;
}

.performer-row.rank-3 {
  border-left-color: #ed8936;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: var(--secondary-color);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.8rem;
}

.performer-row.rank-1 .rank-badge {
  background: #f6ad55;
}

.performer-row.rank-2 .rank-badge {
  background: #a0aec0;
}

.performer-row.rank-3 .rank-badge {
  background: #ed8936;
}

.performer-main {
  min-width: 0;
}

.performer-top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.3rem;
}

.performer-name {
  font-weight: 600;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.performer-share {
  font-weight: 700;
  color: var(--secondary-color);
  font-size: 0.9rem;
  flex-shrink: 0;
}

.share-bar {
  height: 6px;
  background: var(--border-color);
  border-radius: 3px;
  overflow: hidden;
}

.share-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--secondary-color), var(--success-color));
  transition: width 0.3s ease;
}

.performer-score {
  font-weight: 700;
  color: var(--text-secondary);
  font-size: 0.9rem;
  min-width: 24px;
  text-align: right;
}

/* Empty state */
.no-results {
  text-align: center;
  color: var(--text-secondary);
  padding: 2.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .admin-header {
    padding: 1.25rem;
  }

  .controls {
    grid-template-columns: 1fr;
    padding: 1.25rem;
  }

  .control--toggle {
    align-self: flex-start;
  }

  .gift-grid {
    grid-template-columns: 1fr;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions .btn {
    flex: 1;
  }
}

/* Print */
@media print {
  .header-actions,
  .controls {
    display: none;
  }

  .admin-container {
    max-width: none;
  }

  .gift-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .card,
  .stat-card {
    box-shadow: none;
    border: 1px solid var(--border-color);
    break-inside: avoid;
  }
}
</style>
