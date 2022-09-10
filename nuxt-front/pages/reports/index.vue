<template>
  <div>
    <v-container>
      <v-row>
        <v-col>
          <v-list>
            <v-list-item v-for="item in items" :key="item">
              <v-list-item-content>
                <nuxt-link :to="item.link"><v-btn block>{{ item.text }}</v-btn></nuxt-link>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data(){
    return{
      report:[],
      items: [
        { text: 'Отчет по Сборщикам', link: 'reports/assembly_user' },
        { text: 'Отчет по Сварщикам', link: 'reports/weld_user' },
        { text: 'Отчет по Малярам', link: 'reports/paint_user' },
        { text: 'Отчет по Работнику', link: 'reports/users' },
      ],
    }
  },
}
</script>