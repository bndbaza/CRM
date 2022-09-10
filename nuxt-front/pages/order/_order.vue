<template>
  <div>
    <v-container>
      <v-row>
        <h1>Заказ {{$route.params.order}}</h1>
      </v-row>
      <v-row>
        <v-col cols="3">
          <v-list>
            <v-list-item v-for="item in items" :key="item">
              <v-list-item-content>
                <nuxt-link :to="item.link"><v-btn block>{{ item.text }}</v-btn></nuxt-link>
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
              <p>Смонтировано</p>
            </v-col>
            <v-col>
              <p>{{ report.weight_kmd /1000 | number }} тн</p>
              <p>{{ report.weight_in_work /1000 | number }} тн</p>
              <p>{{ report.weight_weld /1000 | number }} тн</p>
              <p>{{ report.weight_paint /1000 | number }} тн</p>
              <p>{{ report.weight_packed /1000 | number }} тн</p>
              <p>{{ report.weight_shipment /1000 | number }} тн</p>
              <p>{{ report.weight_mount /1000 | number }} тн</p>
            </v-col>
            <v-col>
              <p>{{ Math.round(100 / weight * report.weight_kmd) }}%</p>
              <p>{{ Math.round(100 / weight * report.weight_in_work) }}%</p>
              <p>{{ Math.round(100 / weight * report.weight_weld) }}%</p>
              <p>{{ Math.round(100 / weight * report.weight_paint) }}%</p>
              <p>{{ Math.round(100 / weight * report.weight_packed) }}%</p>
              <p>{{ Math.round(100 / weight * report.weight_shipment) }}%</p>
              <p>{{ Math.round(100 / weight * report.weight_mount) }}%</p>
            </v-col>
          </v-row>
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
      weight: 0,
      items: [
        { text: 'Отчет по фазам', link: 'reports/'+this.$route.params.order },
        { text: 'Отгрузка', link: 'shipments/'+this.$route.params.order },
        { text: 'Комплектовочная ведомось', link: 'register/'+this.$route.params.order },
        { text: 'Загрузка', link: 'upload/'+this.$route.params.order },
        { text: 'Материал', link: 'metall/'+this.$route.params.order },
      ],
    }
  },
  mounted(){
    this.getReport()
  },
  methods:{
    async getReport(){
      this.report = await this.$axios.$get(this.$store.state.db.host+'report/all/'+this.$route.params.order);
      this.weight = this.report.weight_order
    }
  }
}
</script>