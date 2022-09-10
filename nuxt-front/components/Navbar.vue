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
          <v-btn text @click='State()'>{{ link.title }}</v-btn>
        </nuxt-link>
        <v-spacer></v-spacer>

        <v-responsive max-width="260">
          <v-text-field
            dense
            flat
            hide-details
            rounded
            solo-inverted
            v-model="search"
          ></v-text-field>
        </v-responsive>
        <v-btn color="black" rounded :to="Cheng()" text @click="$store.commit('db/mark',search)">Поиск</v-btn>
        <!-- <v-btn color="black" rounded :to="Cheng()" text @click="search = ''">Поиск</v-btn> -->
      </v-container>
    </v-app-bar>
</template>

<script>
  export default {
    data: () => ({
      search: '',
      links: [
        {
          title:'Заказы',
          link:'/'
        },
        {
          title:'Обработка',
          link:'/stage'
        },
        {
          title:'Терминал',
          link:'/terminal'
        },
        // {
        //   title:'Покраска',
        //   link:'/paint'
        // },
        {
          title:'Отчеты',
          link:'/reports'
        },
        {
          title:'ОТК',
          link:'/otc'
        },
      ],
    }),
    methods: {
      Cheng() {
        if (/[а-яА-Яa-zA-Z]/.test(this.search)) {
          return '/order/register/stage/0,'+this.search
        }else{
          return '/stage'
        }
      },
      State() {
        this.search = ''
        this.$store.commit('db/mark','')
      }
    }
  }
</script>