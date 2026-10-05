<template>
  <div class="rp-container">
    <!-- Header -->
    <div class="card rp-header">
      <div class="rp-header-main">
        <div>
          <h2>Admin Reports</h2>
          <p class="rp-subtitle">
            Gift leaderboards and archetype rosters built from completed surveys.
          </p>
        </div>
        <div class="rp-header-actions">
          <span v-if="lastUpdated" class="rp-updated">Updated {{ lastUpdated }}</span>
          <button class="btn btn-secondary" @click="loadAll" :disabled="refreshing">
            {{ refreshing ? 'Refreshing...' : 'Refresh' }}
          </button>
          <button class="btn btn-primary" @click="exportCsv" :disabled="!canExport">
            Export CSV
          </button>
          <button class="btn btn-primary" @click="printReport" :disabled="!canExport">
            Print
          </button>
        </div>
      </div>

      <!-- Tabs -->
      <div class="rp-tabs" role="tablist">
        <button
          class="rp-tab"
          role="tab"
          :class="{ active: activeTab === 'leaderboard' }"
          :aria-selected="activeTab === 'leaderboard'"
          @click="activeTab = 'leaderboard'"
        >
          Gift Leaderboard
        </button>
        <button
          class="rp-tab"
          role="tab"
          :class="{ active: activeTab === 'archetypes' }"
          :aria-selected="activeTab === 'archetypes'"
          @click="activeTab = 'archetypes'"
        >
          Archetype Roster
        </button>
      </div>
    </div>

    <!-- ===================== LEADERBOARD TAB ===================== -->
    <template v-if="activeTab === 'leaderboard'">
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>Loading leaderboard data...</p>
      </div>

      <div v-else-if="error" class="error card">
        <p>{{ error }}</p>
        <button class="btn btn-secondary" style="margin-top: 1rem;" @click="retryLeaderboard">Try again</button>
      </div>

      <template v-else>
        <div class="rp-stats">
          <div class="rp-stat">
            <span class="rp-stat-value">{{ leaderboardStats.giftsWithData }}<span class="rp-stat-total">/{{ leaderboardStats.totalGifts }}</span></span>
            <span class="rp-stat-label">Gifts with data</span>
          </div>
          <div class="rp-stat">
            <span class="rp-stat-value">{{ leaderboardStats.uniqueParticipants }}</span>
            <span class="rp-stat-label">Participants ranked</span>
          </div>
          <div class="rp-stat">
            <span class="rp-stat-value">{{ leaderboardStats.totalEntries }}</span>
            <span class="rp-stat-label">Leaderboard entries</span>
          </div>
          <div class="rp-stat">
            <span class="rp-stat-value rp-stat-value--text">{{ leaderboardStats.leadingGift }}</span>
            <span class="rp-stat-label">Most represented gift</span>
          </div>
        </div>

        <div class="card rp-info">
          <strong>How to read this:</strong>
          Share is the percentage of a participant's <em>own</em> total score that this gift represents.
          It highlights relative gifting strength, not absolute performance, so it is not comparable across participants.
        </div>

        <div class="card rp-controls">
          <div class="rp-control">
            <label for="admin-search">Search</label>
            <input
              id="admin-search"
              type="text"
              v-model="searchQuery"
              placeholder="Filter by participant or gift name"
            />
          </div>

          <div class="rp-control">
            <label for="admin-sort">Sort gifts by</label>
            <select id="admin-sort" v-model="sortBy">
              <option value="name">Gift name (A-Z)</option>
              <option value="participants">Most participants</option>
              <option value="topShare">Highest top share</option>
            </select>
          </div>

          <div class="rp-control rp-control--toggle">
            <label class="rp-toggle">
              <input type="checkbox" v-model="hideEmpty" />
              <span>Hide gifts with no data</span>
            </label>
          </div>

          <div class="rp-control rp-control--full">
            <label>Jump to gift</label>
            <div class="rp-pills">
              <button class="rp-pill" :class="{ active: activeGift === 'all' }" @click="activeGift = 'all'">All</button>
              <button
                v-for="name in giftNames"
                :key="name"
                class="rp-pill"
                :class="{ active: activeGift === name }"
                @click="activeGift = name"
              >
                {{ name }}
              </button>
            </div>
          </div>
        </div>

        <div v-if="!visibleGifts.length" class="card rp-no-results">
          <p>No gifts match your filters.</p>
          <button class="btn btn-secondary" style="margin-top: 1rem;" @click="resetFilters">Clear filters</button>
        </div>

        <div v-else class="rp-grid">
          <div
            v-for="gift in visibleGifts"
            :key="gift.gift_name"
            class="card rp-card"
            :id="'gift-' + slugify(gift.gift_name)"
          >
            <div class="rp-card-head">
              <h3 class="rp-card-title">{{ gift.gift_name }}</h3>
              <span class="rp-card-count">
                {{ gift.top_performers.length }}
                {{ gift.top_performers.length === 1 ? 'entry' : 'entries' }}
              </span>
            </div>

            <div v-if="gift.top_performers.length === 0" class="rp-empty">
              <p>No completed surveys for this gift yet.</p>
            </div>

            <ol v-else class="rp-list">
              <li
                v-for="(performer, index) in gift.top_performers"
                :key="performer.response_id + '-' + index"
                class="rp-item"
                :class="'rp-rank-' + (index + 1)"
              >
                <span class="rp-rank">{{ index + 1 }}</span>
                <div class="rp-body">
                  <span class="rp-name">{{ performer.name }}</span>
                  <div
                    class="rp-track"
                    role="progressbar"
                    :aria-valuenow="performer.percentage"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    :aria-label="performer.name + ' share for ' + gift.gift_name"
                  >
                    <div class="rp-fill" :style="{ width: performer.percentage + '%' }"></div>
                  </div>
                </div>
                <div class="rp-metric">
                  <span class="rp-pct">{{ performer.percentage }}%</span>
                  <span class="rp-score">{{ performer.score }} pts</span>
                </div>
              </li>
            </ol>
          </div>
        </div>
      </template>
    </template>

    <!-- ===================== ARCHETYPES TAB ===================== -->
    <template v-else>
      <div v-if="archetypesLoading" class="loading">
        <div class="loading-spinner"></div>
        <p>Loading archetype roster...</p>
      </div>

      <div v-else-if="archetypesError" class="error card">
        <p>{{ archetypesError }}</p>
        <button class="btn btn-secondary" style="margin-top: 1rem;" @click="retryArchetypes">Try again</button>
      </div>

      <template v-else>
        <div class="rp-stats">
          <div class="rp-stat">
            <span class="rp-stat-value">{{ archetypeStats.totalPlaced }}</span>
            <span class="rp-stat-label">People placed</span>
          </div>
          <div class="rp-stat">
            <span class="rp-stat-value">{{ archetypeStats.active }}<span class="rp-stat-total">/{{ archetypeStats.total }}</span></span>
            <span class="rp-stat-label">Archetypes filled</span>
          </div>
          <div class="rp-stat">
            <span class="rp-stat-value rp-stat-value--text">{{ archetypeStats.largest.name }}</span>
            <span class="rp-stat-label">Largest group ({{ archetypeStats.largest.member_count }})</span>
          </div>
          <div class="rp-stat">
            <span class="rp-stat-value rp-stat-value--text">{{ archetypeStats.leadingFamily }}</span>
            <span class="rp-stat-label">Strongest family</span>
          </div>
        </div>

        <div class="card rp-info">
          <strong>How to read this:</strong>
          Every completed survey is placed in the archetype whose signature gifts best match their top gifts.
          Members are listed strongest match first, and each person's top three gifts are shown by name.
        </div>

        <div class="card rp-controls">
          <div class="rp-control">
            <label for="arch-search">Search</label>
            <input
              id="arch-search"
              type="text"
              v-model="archetypeSearch"
              placeholder="Filter by archetype, member, or gift"
            />
          </div>

          <div class="rp-control">
            <label for="arch-family">Family</label>
            <select id="arch-family" v-model="familyFilter">
              <option value="all">All families</option>
              <option v-for="family in families" :key="family" :value="family">{{ family }}</option>
            </select>
          </div>

          <div class="rp-control rp-control--toggle">
            <label class="rp-toggle">
              <input type="checkbox" v-model="hideEmptyArchetypes" />
              <span>Hide archetypes with no members</span>
            </label>
          </div>
        </div>

        <div v-if="!filteredArchetypes.length" class="card rp-no-results">
          <p>No archetypes match your filters.</p>
          <button class="btn btn-secondary" style="margin-top: 1rem;" @click="resetArchetypeFilters">Clear filters</button>
        </div>

        <template v-else>
          <template v-for="family in visibleFamilies" :key="family">
            <div class="rp-family">
              <h3>{{ family }}</h3>
              <p>{{ familyMeta[family] }}</p>
            </div>

            <div class="rp-grid">
              <div
                v-for="archetype in archetypesInFamily(family)"
                :key="archetype.name"
                class="card rp-card"
              >
                <div class="rp-card-head rp-card-head--top">
                  <div>
                    <span class="rp-badge" :class="'rp-badge--' + archetype.family.toLowerCase()">
                      {{ archetype.family }}
                    </span>
                    <h3 class="rp-card-title">{{ archetype.name }}</h3>
                    <p class="rp-tagline">{{ archetype.tagline }}</p>
                  </div>
                  <div class="rp-member-count">
                    <span class="rp-member-num">{{ archetype.member_count }}</span>
                    <span class="rp-member-label">people</span>
                  </div>
                </div>

                <div class="rp-signature">
                  <span v-for="gift in archetype.signature" :key="gift" class="rp-signature-chip">
                    {{ gift }}
                  </span>
                </div>

                <div v-if="archetype.members.length === 0" class="rp-empty">
                  <p>No completed surveys matched this archetype yet.</p>
                </div>

                <ol v-else class="rp-list">
                  <li
                    v-for="(member, index) in archetype.members"
                    :key="member.response_id"
                    class="rp-item"
                    :class="'rp-rank-' + (index + 1)"
                  >
                    <span class="rp-rank">{{ index + 1 }}</span>
                    <div class="rp-body">
                      <span class="rp-name">{{ member.name }}</span>
                      <div
                        class="rp-track"
                        role="progressbar"
                        :aria-valuenow="member.match_percentage"
                        aria-valuemin="0"
                        aria-valuemax="100"
                        :aria-label="member.name + ' match for ' + archetype.name"
                      >
                        <div class="rp-fill" :style="{ width: member.match_percentage + '%' }"></div>
                      </div>
                      <div class="rp-chips">
                        <span v-for="gift in member.top_gifts" :key="gift" class="rp-chip">
                          {{ gift }}
                        </span>
                      </div>
                    </div>
                    <div class="rp-metric">
                      <span class="rp-pct">{{ member.match_percentage }}%</span>
                      <span class="rp-score">match</span>
                    </div>
                  </li>
                </ol>
              </div>
            </div>
          </template>
        </template>
      </template>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { surveyAPI } from '../api'

export default {
  name: 'AdminView',
  setup() {
    const activeTab = ref('leaderboard')
    const refreshing = ref(false)
    const lastUpdated = ref('')

    // Leaderboard state
    const loading = ref(true)
    const error = ref(null)
    const leaderboard = ref([])
    const searchQuery = ref('')
    const sortBy = ref('name')
    const hideEmpty = ref(true)
    const activeGift = ref('all')

    // Archetype state
    const archetypesLoading = ref(true)
    const archetypesError = ref(null)
    const archetypeRoster = ref([])
    const archetypeSearch = ref('')
    const familyFilter = ref('all')
    const hideEmptyArchetypes = ref(true)

    const families = ['Reach', 'Keep', 'Build']
    const familyMeta = {
      Reach: 'Outward voice: grow & win',
      Keep: 'Inward care: retain & deepen',
      Build: 'Operations: make it run'
    }

    /* ---------------- Data loading ---------------- */

    const fetchLeaderboard = async () => {
      error.value = null
      try {
        const response = await surveyAPI.getAdminLeaderboard()
        leaderboard.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 403) {
          error.value = 'Access denied. Admin privileges required.'
        } else {
          error.value = 'Failed to load leaderboard data. Please try again.'
        }
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const fetchArchetypes = async () => {
      archetypesError.value = null
      try {
        const response = await surveyAPI.getAdminArchetypes()
        archetypeRoster.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 403) {
          archetypesError.value = 'Access denied. Admin privileges required.'
        } else {
          archetypesError.value = 'Failed to load archetype roster. Please try again.'
        }
        console.error(err)
      } finally {
        archetypesLoading.value = false
      }
    }

    const loadAll = async () => {
      refreshing.value = true
      await Promise.all([fetchLeaderboard(), fetchArchetypes()])
      lastUpdated.value = new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      })
      refreshing.value = false
    }

    const retryLeaderboard = () => {
      loading.value = true
      fetchLeaderboard()
    }

    const retryArchetypes = () => {
      archetypesLoading.value = true
      fetchArchetypes()
    }

    /* ---------------- Helpers ---------------- */

    const slugify = (value) => value.toLowerCase().replace(/[^a-z0-9]+/g, '-')

    const resetFilters = () => {
      searchQuery.value = ''
      sortBy.value = 'name'
      hideEmpty.value = true
      activeGift.value = 'all'
    }

    const resetArchetypeFilters = () => {
      archetypeSearch.value = ''
      familyFilter.value = 'all'
      hideEmptyArchetypes.value = true
    }

    /* ---------------- Leaderboard computed ---------------- */

    const giftNames = computed(() => leaderboard.value.map((gift) => gift.gift_name))

    const leaderboardStats = computed(() => {
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

    /* ---------------- Archetype computed ---------------- */

    const archetypeStats = computed(() => {
      const roster = archetypeRoster.value
      const totalPlaced = roster.reduce((sum, a) => sum + a.member_count, 0)
      const active = roster.filter((a) => a.member_count > 0).length

      let largest = { name: '—', member_count: 0 }
      const familyTotals = {}

      roster.forEach((a) => {
        if (a.member_count > largest.member_count) {
          largest = { name: a.name, member_count: a.member_count }
        }
        familyTotals[a.family] = (familyTotals[a.family] || 0) + a.member_count
      })

      let leadingFamily = '—'
      let leadingCount = 0
      Object.entries(familyTotals).forEach(([family, count]) => {
        if (count > leadingCount) {
          leadingCount = count
          leadingFamily = family
        }
      })

      return { totalPlaced, active, total: roster.length, largest, leadingFamily }
    })

    const filteredArchetypes = computed(() => {
      const query = archetypeSearch.value.trim().toLowerCase()

      let list = archetypeRoster.value.map((archetype) => {
        if (!query) return archetype

        const archetypeMatch =
          archetype.name.toLowerCase().includes(query) ||
          (archetype.tagline || '').toLowerCase().includes(query) ||
          archetype.signature.some((gift) => gift.toLowerCase().includes(query))

        if (archetypeMatch) return archetype

        const members = archetype.members.filter((member) =>
          (member.name || '').toLowerCase().includes(query)
        )
        return { ...archetype, members, member_count: members.length }
      })

      if (familyFilter.value !== 'all') {
        list = list.filter((archetype) => archetype.family === familyFilter.value)
      }

      if (hideEmptyArchetypes.value) {
        list = list.filter((archetype) => archetype.member_count > 0)
      }

      return list
    })

    const archetypesInFamily = (family) =>
      filteredArchetypes.value.filter((archetype) => archetype.family === family)

    const visibleFamilies = computed(() => {
      if (familyFilter.value !== 'all') {
        return archetypesInFamily(familyFilter.value).length ? [familyFilter.value] : []
      }
      return families.filter((family) => archetypesInFamily(family).length > 0)
    })

    /* ---------------- Export / print ---------------- */

    const canExport = computed(() => {
      if (activeTab.value === 'archetypes') {
        return archetypeRoster.value.some((archetype) => archetype.member_count > 0)
      }
      return leaderboard.value.some((gift) => gift.top_performers.length > 0)
    })

    const toCsv = (rows) =>
      rows
        .map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(','))
        .join('\n')

    const download = (csv, filename) => {
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }

    const exportCsv = () => {
      const stamp = new Date().toISOString().slice(0, 10)

      if (activeTab.value === 'archetypes') {
        const rows = [['Archetype', 'Family', 'Rank', 'Name', 'Match (%)', 'Top Gifts']]
        filteredArchetypes.value.forEach((archetype) => {
          archetype.members.forEach((member, index) => {
            rows.push([
              archetype.name,
              archetype.family,
              index + 1,
              member.name,
              member.match_percentage,
              member.top_gifts.join(' / ')
            ])
          })
        })
        download(toCsv(rows), `spiritual-gifts-archetypes-${stamp}.csv`)
        return
      }

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
      download(toCsv(rows), `spiritual-gifts-leaderboard-${stamp}.csv`)
    }

    const printReport = () => {
      window.print()
    }

    onMounted(loadAll)

    return {
      activeTab,
      refreshing,
      lastUpdated,
      loading,
      error,
      searchQuery,
      sortBy,
      hideEmpty,
      activeGift,
      archetypesLoading,
      archetypesError,
      archetypeSearch,
      familyFilter,
      hideEmptyArchetypes,
      families,
      familyMeta,
      loadAll,
      retryLeaderboard,
      retryArchetypes,
      slugify,
      resetFilters,
      resetArchetypeFilters,
      giftNames,
      leaderboardStats,
      visibleGifts,
      archetypeStats,
      filteredArchetypes,
      archetypesInFamily,
      visibleFamilies,
      canExport,
      exportCsv,
      printReport
    }
  }
}
</script>

<style scoped>
/* ============================================================
   Admin reports — scoped, namespaced with `rp-` so nothing
   collides with global styles (e.g. the global .rank-badge).
   ============================================================ */

.rp-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* ---------------- Header ---------------- */
.rp-header {
  padding: 1.5rem 2rem;
}

.rp-header-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.rp-header h2 {
  margin-bottom: 0.35rem;
}

.rp-subtitle {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.rp-header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.rp-updated {
  font-size: 0.85rem;
  color: var(--text-secondary);
  white-space: nowrap;
}

/* ---------------- Tabs ---------------- */
.rp-tabs {
  display: flex;
  gap: 0.25rem;
  margin-top: 1.5rem;
  border-bottom: 2px solid var(--border-color);
}

.rp-tab {
  border: none;
  background: transparent;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: color 0.2s ease, border-color 0.2s ease;
}

.rp-tab:hover {
  color: var(--secondary-color);
}

.rp-tab.active {
  color: var(--secondary-color);
  border-bottom-color: var(--secondary-color);
}

/* ---------------- Stats ---------------- */
.rp-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.rp-stat {
  background: var(--card-background);
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  border-left: 4px solid var(--secondary-color);
}

.rp-stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--secondary-color);
  line-height: 1.1;
}

.rp-stat-value--text {
  font-size: 1.25rem;
  line-height: 1.5;
}

.rp-stat-total {
  font-size: 1.1rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.rp-stat-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* ---------------- Info note ---------------- */
.rp-info {
  padding: 1rem 1.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.7;
  border-left: 4px solid var(--secondary-color);
}

.rp-info strong {
  color: var(--text-primary);
}

/* ---------------- Controls ---------------- */
.rp-controls {
  display: grid;
  grid-template-columns: 1fr 220px auto;
  gap: 1.25rem;
  align-items: end;
  padding: 1.5rem 2rem;
}

.rp-control {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.rp-control--full {
  grid-column: 1 / -1;
}

.rp-control label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.rp-control select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 1rem;
  background: var(--card-background);
  color: var(--text-primary);
  cursor: pointer;
}

.rp-control select:focus {
  outline: none;
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.rp-control--toggle {
  align-self: center;
  padding-bottom: 0.35rem;
}

.rp-toggle {
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

.rp-toggle input {
  width: 18px;
  height: 18px;
  accent-color: var(--secondary-color);
  cursor: pointer;
}

.rp-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.rp-pill {
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

.rp-pill:hover {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
}

.rp-pill.active {
  background: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}

/* ---------------- Card grid ---------------- */
.rp-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: 1.5rem;
  align-items: start;
}

.rp-card {
  margin-bottom: 0;
  padding: 1.5rem;
}

.rp-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.85rem;
  border-bottom: 2px solid var(--border-color);
}

.rp-card-head--top {
  align-items: flex-start;
}

.rp-card-title {
  color: var(--secondary-color);
  font-size: 1.25rem;
  margin: 0;
}

.rp-card-count {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--secondary-color);
  background: rgba(102, 126, 234, 0.1);
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  white-space: nowrap;
  flex-shrink: 0;
}

.rp-empty {
  text-align: center;
  padding: 1.5rem;
  color: var(--text-secondary);
  font-style: italic;
  font-size: 0.9rem;
}

/* ---------------- Ranked list ---------------- */
.rp-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.rp-item {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 0.7rem 0.85rem;
  border-radius: 8px;
  background: var(--background);
  border-left: 3px solid transparent;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.rp-item:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.rp-item.rp-rank-1 {
  border-left-color: #f6ad55;
}

.rp-item.rp-rank-2 {
  border-left-color: #a0aec0;
}

.rp-item.rp-rank-3 {
  border-left-color: #ed8936;
}

.rp-rank {
  flex: 0 0 auto;
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--secondary-color);
  color: #fff;
  font-weight: 700;
  font-size: 0.85rem;
}

.rp-item.rp-rank-1 .rp-rank {
  background: #f6ad55;
}

.rp-item.rp-rank-2 .rp-rank {
  background: #a0aec0;
}

.rp-item.rp-rank-3 .rp-rank {
  background: #ed8936;
}

/* The name gets all remaining width; metric is fixed. */
.rp-body {
  flex: 1 1 auto;
  min-width: 0;
}

.rp-name {
  display: block;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  overflow-wrap: break-word;
}

.rp-track {
  margin-top: 0.45rem;
  height: 6px;
  background: var(--border-color);
  border-radius: 3px;
  overflow: hidden;
}

.rp-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--secondary-color), var(--success-color));
  transition: width 0.3s ease;
}

.rp-metric {
  flex: 0 0 auto;
  min-width: 62px;
  text-align: right;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.rp-pct {
  font-weight: 700;
  color: var(--secondary-color);
  font-size: 0.95rem;
}

.rp-score {
  font-size: 0.7rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

/* ---------------- Archetype specifics ---------------- */
.rp-badge {
  display: inline-block;
  padding: 0.2rem 0.7rem;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.rp-badge--reach {
  background: rgba(245, 101, 101, 0.15);
  color: #c53030;
}

.rp-badge--keep {
  background: rgba(72, 187, 120, 0.15);
  color: #276749;
}

.rp-badge--build {
  background: rgba(102, 126, 234, 0.15);
  color: #4c51bf;
}

.rp-tagline {
  font-style: italic;
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0.3rem 0 0;
}

.rp-member-count {
  text-align: right;
  flex-shrink: 0;
}

.rp-member-num {
  display: block;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--secondary-color);
  line-height: 1.1;
}

.rp-member-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.rp-signature {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
}

.rp-signature-chip {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-primary);
  padding: 0.2rem 0.6rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 999px;
}

.rp-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.5rem;
}

.rp-chip {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-primary);
  padding: 0.15rem 0.55rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 999px;
  white-space: nowrap;
}

/* ---------------- Family headers ---------------- */
.rp-family {
  margin: 2.5rem 0 1.25rem;
  text-align: center;
}

.rp-family h3 {
  font-size: 1.75rem;
  color: var(--secondary-color);
  margin-bottom: 0.25rem;
}

.rp-family p {
  color: var(--text-secondary);
  font-style: italic;
  margin: 0;
}

/* ---------------- Empty state ---------------- */
.rp-no-results {
  text-align: center;
  color: var(--text-secondary);
  padding: 2.5rem;
}

/* ---------------- Responsive ---------------- */
@media (max-width: 900px) {
  .rp-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .rp-header {
    padding: 1.25rem;
  }

  .rp-controls {
    grid-template-columns: 1fr;
    padding: 1.25rem;
  }

  .rp-control--toggle {
    align-self: flex-start;
  }

  .rp-header-actions {
    width: 100%;
  }

  .rp-header-actions .btn {
    flex: 1;
  }

  .rp-tabs {
    width: 100%;
  }

  .rp-tab {
    flex: 1;
    padding: 0.75rem 0.5rem;
    font-size: 0.9rem;
  }
}

/* ---------------- Print ---------------- */
@media print {
  .rp-header-actions,
  .rp-tabs,
  .rp-controls {
    display: none;
  }

  .rp-container {
    max-width: none;
  }

  .rp-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .card,
  .rp-stat {
    box-shadow: none;
    border: 1px solid var(--border-color);
    break-inside: avoid;
  }
}
</style>
