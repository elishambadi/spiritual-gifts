<template>
  <div class="admin-container">
    <!-- Header -->
    <div class="card admin-header">
      <div class="header-main">
        <div>
          <h2>Admin Reports</h2>
          <p class="subtitle">
            Gift leaderboards and archetype rosters built from completed surveys.
          </p>
        </div>
        <div class="header-actions">
          <span v-if="lastUpdated" class="updated">Updated {{ lastUpdated }}</span>
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
      <div class="tabs" role="tablist">
        <button
          class="tab"
          role="tab"
          :class="{ active: activeTab === 'leaderboard' }"
          :aria-selected="activeTab === 'leaderboard'"
          @click="activeTab = 'leaderboard'"
        >
          Gift Leaderboard
        </button>
        <button
          class="tab"
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
        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-value">{{ leaderboardStats.giftsWithData }}<span class="stat-total">/{{ leaderboardStats.totalGifts }}</span></span>
            <span class="stat-label">Gifts with data</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ leaderboardStats.uniqueParticipants }}</span>
            <span class="stat-label">Participants ranked</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ leaderboardStats.totalEntries }}</span>
            <span class="stat-label">Leaderboard entries</span>
          </div>
          <div class="stat-card">
            <span class="stat-value stat-value--text">{{ leaderboardStats.leadingGift }}</span>
            <span class="stat-label">Most represented gift</span>
          </div>
        </div>

        <div class="card info-note">
          <strong>How to read this:</strong>
          Share is the percentage of a participant's <em>own</em> total score that this gift represents.
          It highlights relative gifting strength, not absolute performance, so it is not comparable across participants.
        </div>

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
              <button class="pill" :class="{ active: activeGift === 'all' }" @click="activeGift = 'all'">All</button>
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

        <div v-if="!visibleGifts.length" class="card no-results">
          <p>No gifts match your filters.</p>
          <button class="btn btn-secondary" style="margin-top: 1rem;" @click="resetFilters">Clear filters</button>
        </div>

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
        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-value">{{ archetypeStats.totalPlaced }}</span>
            <span class="stat-label">People placed</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ archetypeStats.active }}<span class="stat-total">/{{ archetypeStats.total }}</span></span>
            <span class="stat-label">Archetypes filled</span>
          </div>
          <div class="stat-card">
            <span class="stat-value stat-value--text">{{ archetypeStats.largest.name }}</span>
            <span class="stat-label">Largest group ({{ archetypeStats.largest.member_count }})</span>
          </div>
          <div class="stat-card">
            <span class="stat-value stat-value--text">{{ archetypeStats.leadingFamily }}</span>
            <span class="stat-label">Strongest family</span>
          </div>
        </div>

        <div class="card info-note">
          <strong>How to read this:</strong>
          Every completed survey is placed in the archetype whose signature gifts best match their top gifts.
          Members are listed strongest match first, and each person's top three gifts are shown by name.
        </div>

        <div class="card controls">
          <div class="control">
            <label for="arch-search">Search</label>
            <input
              id="arch-search"
              type="text"
              v-model="archetypeSearch"
              placeholder="Filter by archetype, member, or gift"
            />
          </div>

          <div class="control">
            <label for="arch-family">Family</label>
            <select id="arch-family" v-model="familyFilter">
              <option value="all">All families</option>
              <option v-for="family in families" :key="family" :value="family">{{ family }}</option>
            </select>
          </div>

          <div class="control control--toggle">
            <label class="toggle">
              <input type="checkbox" v-model="hideEmptyArchetypes" />
              <span>Hide archetypes with no members</span>
            </label>
          </div>
        </div>

        <div v-if="!filteredArchetypes.length" class="card no-results">
          <p>No archetypes match your filters.</p>
          <button class="btn btn-secondary" style="margin-top: 1rem;" @click="resetArchetypeFilters">Clear filters</button>
        </div>

        <template v-else>
          <template v-for="family in visibleFamilies" :key="family">
            <div class="family-header">
              <h3>{{ family }}</h3>
              <p>{{ familyMeta[family] }}</p>
            </div>

            <div class="gift-grid">
              <div
                v-for="archetype in archetypesInFamily(family)"
                :key="archetype.name"
                class="card gift-card"
              >
                <div class="archetype-head">
                  <div>
                    <span class="archetype-badge" :class="'family-' + archetype.family.toLowerCase()">
                      {{ archetype.family }}
                    </span>
                    <h3 class="gift-title">{{ archetype.name }}</h3>
                    <p class="archetype-tagline">{{ archetype.tagline }}</p>
                  </div>
                  <div class="member-count">
                    <span class="member-count-num">{{ archetype.member_count }}</span>
                    <span class="member-count-label">people</span>
                  </div>
                </div>

                <div class="signature-chips">
                  <span v-for="gift in archetype.signature" :key="gift" class="signature-chip">
                    {{ gift }}
                  </span>
                </div>

                <div v-if="archetype.members.length === 0" class="no-data">
                  <p>No completed surveys matched this archetype yet.</p>
                </div>

                <ol v-else class="performer-list">
                  <li
                    v-for="(member, index) in archetype.members"
                    :key="member.response_id"
                    class="performer-row"
                    :class="'rank-' + (index + 1)"
                  >
                    <span class="rank-badge">{{ index + 1 }}</span>
                    <div class="performer-main">
                      <div class="performer-top">
                        <span class="performer-name">{{ member.name }}</span>
                        <span class="performer-share">{{ member.match_percentage }}%</span>
                      </div>
                      <div
                        class="share-bar"
                        role="progressbar"
                        :aria-valuenow="member.match_percentage"
                        aria-valuemin="0"
                        aria-valuemax="100"
                        :aria-label="member.name + ' match for ' + archetype.name"
                      >
                        <div class="share-fill" :style="{ width: member.match_percentage + '%' }"></div>
                      </div>
                      <div class="member-gifts">
                        <span v-for="gift in member.top_gifts" :key="gift" class="gift-tag">
                          {{ gift }}
                        </span>
                      </div>
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

/* Tabs */
.tabs {
  display: flex;
  gap: 0.5rem;
  margin-top: 1.5rem;
  border-bottom: 2px solid var(--border-color);
}

.tab {
  border: none;
  background: transparent;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s ease;
}

.tab:hover {
  color: var(--secondary-color);
}

.tab.active {
  color: var(--secondary-color);
  border-bottom-color: var(--secondary-color);
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

/* Performer / member list */
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

.member-gifts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.5rem;
}

.gift-tag {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
  padding: 0.15rem 0.55rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 999px;
  white-space: nowrap;
}

/* Archetypes */
.family-header {
  margin: 2.5rem 0 1.25rem;
  text-align: center;
}

.family-header h3 {
  font-size: 1.75rem;
  color: var(--secondary-color);
  margin-bottom: 0.25rem;
}

.family-header p {
  color: var(--text-secondary);
  font-style: italic;
  margin: 0;
}

.archetype-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--border-color);
}

.archetype-badge {
  display: inline-block;
  padding: 0.2rem 0.75rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
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

.archetype-tagline {
  font-style: italic;
  color: var(--text-secondary);
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
}

.member-count {
  text-align: right;
  flex-shrink: 0;
}

.member-count-num {
  display: block;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--secondary-color);
  line-height: 1.1;
}

.member-count-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.signature-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
}

.signature-chip {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-primary);
  padding: 0.2rem 0.6rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 999px;
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

  .tabs {
    width: 100%;
  }

  .tab {
    flex: 1;
    padding: 0.75rem 0.5rem;
    font-size: 0.9rem;
  }
}

/* Print */
@media print {
  .header-actions,
  .tabs,
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
