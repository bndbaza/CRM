<template>
  <v-app-bar
      app
      color="white"
      flat
    >
      <v-container class="py-0 fill-height" fluid>
        <h1>БСС</h1>
        <nuxt-link
          v-for="link in links"
          :key="link.title"
          :to="link.link"
        >
          <v-btn text>{{ link.title }}</v-btn>
        </nuxt-link>

        <v-spacer></v-spacer>

        <v-responsive max-width="260">
          <v-text-field
            dense
            flat
            hide-details
            rounded
            solo-inverted
          ></v-text-field>
        </v-responsive>
      </v-container>
    </v-app-bar>
</template>

<script>
  export default {
    data: () => ({
      links: [
        {
          title:'Заказы',
          link:'/'
        },
        {
          title:'Терминал',
          link:'/terminal'
        }
      ],
    }),
  }
</script>