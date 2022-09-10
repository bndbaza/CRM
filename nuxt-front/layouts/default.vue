<template>
  <v-app id="inspire">
    <template v-if="$store.state.db.user != ''">
      <Navbar />
      <v-main class="grey lighten-3">
        <v-container fluid>
          <v-row>
            <v-col>
              <v-sheet
                min-height="70vh"
                rounded="lg"
              >
                <nuxt />
              </v-sheet>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </template>
    <template v-else>
      <h1>Вы не зарегистрированы</h1>
      <p>{{host}}</p>
    </template>
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
        host: '',
      }
    },
    async mounted() {
      this.host = await this.$axios.$get(this.$store.state.db.host+'ip')

    }
  }
</script>
