<template>
  <v-app id="inspire">
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
  </v-app>
</template>

<script>
import Navbar from '@/components/Navbar'
  export default {
    components:{
      Navbar
    },
    data: () => ({

    }),
  }
</script>
