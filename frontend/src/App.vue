<template>
  <div id="app">
    <header>
      <h1>Spiritual Gifts Survey</h1>
      <p>Discover your spiritual gifts through this comprehensive assessment</p>
      
      <nav class="header-nav">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">About Spiritual Gifts</router-link>
        <router-link to="/survey" class="nav-link" :class="{ active: $route.path === '/survey' }">Take Survey</router-link>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
