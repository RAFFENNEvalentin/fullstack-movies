import { createRouter, createWebHistory } from 'vue-router'

const MoviesListPage = () => import('@/views/MoviesListPage.vue')
const MovieDetailPage = () => import('@/views/MovieDetailPage.vue')

const routes = [
  { path: '/', redirect: '/movies' },
  { path: '/movies', name: 'movies-list', component: MoviesListPage },
  { path: '/movies/:id', name: 'movie-detail', component: MovieDetailPage, props: true },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: { template: '<div class="pa-6">Not found</div>' } }
]

export default createRouter({
  history: createWebHistory(),
  routes
})