<template>
  <v-app id="inspire">
    <!-- <template v-if="$store.state.db.user"> -->
    <template>
      <Navbar />
      <v-main class="black lighten-3">
        <v-container fluid>
          <v-row>
            <v-col>
              <v-sheet
                min-height="90vh"
                rounded="lg"
                dark
              >
                <nuxt />
              </v-sheet>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </template>
    <!-- <template v-else> -->
      <!-- <h1>Вы не зарегистрированы</h1> -->
      <!-- <p>{{host}}</p> -->
    <!-- </template> -->
  </v-app>
</template>

<script>
import Navbar from '@/components/Navbar'
  export default {
    components:{
      Navbar
    },
    data () {
      return {
        host: null,
      }
    },
    async mounted() {
      this.host = await this.$axios.$get(this.$store.state.db.host+'ip')
      this.$store.commit('db/user_get',this.host)
    }
  }
</script>

<style>
  a {
    text-decoration: none
  } 
</style>
