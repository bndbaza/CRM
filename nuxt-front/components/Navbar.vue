<template>
  <v-app-bar
      app
      flat
      dark
    >
      <v-container class="py-0 fill-height" fluid>
        <v-img
          src='/logo.png'
          max-height="50"
          max-width="50"
          class="mx-5"
        ></v-img>
        <!-- <h1 class="orange--text mx-5">БСС</h1> -->
        <!-- <v-spacer></v-spacer> -->
        <nuxt-link
          v-for="link in Filter()"
          :key="link.title"
          :to="link.link"
        >
          <v-btn text @click='State()'><h3 class="px-2">{{ link.title }}</h3></v-btn>
        </nuxt-link>
        <v-spacer></v-spacer>
        <h3 v-if="!$store.state.db.user">Ограниченный доступ</h3>
        <!-- <h3>{{$store.state.db.user.surname}} {{$store.state.db.user.name}}</h3> -->
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
        <v-btn rounded :to="Cheng()" text @click="$store.commit('db/mark',search)">Поиск</v-btn>
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
          link:'/',
          users: [0]
        },
        {
          title:'Обработка',
          link:'/stage',
          users: [0]
        },
        // {
          // title:'Терминал',
          // link:'/terminal'
        // },
        // {
        //   title:'Покраска',
        //   link:'/paint'
        // },
        {
          title:'Отчеты',
          link:'/reports',
          users: [0]
        },
        {
          title:'ОТК',
          link:'/otc',
          users: [0]
        },
        {
          title:'Склад',
          link:'/store',
          users: [0]
        },
        {
          title:'Связь',
          link:'/communication',
          users: [57]
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
      },
      Filter() {
        let user = 0
        if (this.$store.state.db.user) {
          user = this.$store.state.db.user.id
        }
        let items = this.links.filter(item => item['users'].includes(user) || item['users'].includes(0));
        return items
      },
    }
  }
</script>
