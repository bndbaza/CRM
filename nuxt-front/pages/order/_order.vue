<template>
  <div>
    <v-container v-if="!loading">
      <v-row>
        <h1>Заказ {{$route.params.order}}</h1>
      </v-row>
      <v-row>
        <v-col cols="3">
          <v-list>
            <v-list-item v-for="item in Filter()" :key="item">
              <v-list-item-content v-if="report && item.text!='Загрузка'">
                <nuxt-link :to="item.link" class="text-decoration=none"><v-btn light block color="orange">{{ item.text }}</v-btn></nuxt-link>
              </v-list-item-content>
              <v-list-item-content v-if="item.text=='Загрузка' && report.status!='Готов'">
                <nuxt-link :to="item.link" class="text-decoration=none"><v-btn light block color="orange">{{ item.text }}</v-btn></nuxt-link>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>
        <v-col>
          <v-row>
            <h1>Динамика обработки заказа</h1>
          </v-row>
          <v-row>
            <v-col>
              <p>Разработано КМД</p>
              <p>Передано на производство</p>
              <p>Изготовлено</p>
              <p>Окрашено</p>
              <p>Упаковано</p>
              <p>Отгружено</p>
              <!-- <p>Смонтировано</p> -->
            </v-col>
            <v-col v-if="report">
              <p>{{ report.weight_kmd /1000 | number }} тн</p>
              <p>{{ report.weight_in_work /1000 | number }} тн</p>
              <p>{{ report.weight_weld /1000 | number }} тн</p>
              <p>{{ report.weight_paint /1000 | number }} тн</p>
              <p>{{ report.weight_packed /1000 | number }} тн</p>
              <p>{{ report.weight_shipment /1000 | number }} тн</p>
              <!-- <p>{{ report.weight_mount /1000 | number }} тн</p> -->
            </v-col>
            <v-col v-if="report">
              <p>{{ Math.floor(100 / weight * report.weight_kmd) }}%</p>
              <p>{{ Math.floor(100 / weight * report.weight_in_work) }}%</p>
              <p>{{ Math.floor(100 / weight * report.weight_weld) }}%</p>
              <p>{{ Math.floor(100 / weight * report.weight_paint) }}%</p>
              <p>{{ Math.floor(100 / weight * report.weight_packed) }}%</p>
              <p>{{ Math.floor(100 / weight * report.weight_shipment) }}%</p>
              <!-- <p>{{ Math.floor(100 / weight * report.weight_mount) }}%</p> -->
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  <v-dialog
    v-model="loading"
    scrollable
    persistent :overlay="false"
    max-width="150px"
    transition="dialog-transition"
  >
    <v-progress-linear
      indeterminate
      color="orange"
    ></v-progress-linear>
  </v-dialog>
  </div>
</template>


<script>
export default {
  data(){
    return{
      report:[],
      loading: true,
      weight: 0,
      items: [
        { text: 'Отчет по фазам', link: 'reports/'+this.$route.params.order, users: [0] },
        { text: 'Отгрузка', link: 'shipments/'+this.$route.params.order, users:[57] },
        { text: 'Комплектовочная ведомось', link: 'register/'+this.$route.params.order, users: [0] },
        { text: 'Загрузка', link: 'upload/'+this.$route.params.order, users: [57] },
        { text: 'Материал', link: 'metall/'+this.$route.params.order, users: [0] },
        { text: 'Спецификация на металл', link: 'needformetal/'+this.$route.params.order, users: [57] },
      ],
    }
  },
  mounted(){
    this.getReport()
  },
  methods:{
    async getReport(){
      try {
        this.report = await this.$axios.$get(this.$store.state.db.host+'report/all/'+this.$route.params.order);
        this.weight = this.report.weight_order
      } catch {
        this.report = false
        this.weight = false
      }
      this.loading = false
    },
    Filter() {
      let user = 0
      if (this.$store.state.db.user) {
        user = this.$store.state.db.user.id
      }
      let items = this.items.filter(item => item['users'].includes(user) || item['users'].includes(0));
      return items
    },
  }
}
</script>

