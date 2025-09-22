<template>
  <v-app>
    <v-app-bar flat>
      <v-app-bar-title>🎬 Movies</v-app-bar-title>
      <v-spacer />
      <v-btn to="/movies" variant="text">Liste</v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>