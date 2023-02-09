<template>
  <div>
    <v-container fluid>      
      <h1>Заказ {{$route.params.faza}}</h1>
      <v-data-table
        :headers="headers"
        :items="report"
        hide-default-footer
        :items-per-page="100"
        class="elevation-1"
        dense
      >
        <template v-slot:[`item.faza`]="{ item }">
          <nuxt-link class="orange--text" :to="'stage/'+$route.params.faza+','+item.faza" v-if="item.faza != 'Итог'">Фаза {{ item.faza }}</nuxt-link>
          <nuxt-link class="orange--text" :to="'stage/'+$route.params.faza+',0'" v-else >Итог</nuxt-link>
        </template>
        <template v-slot:[`item.weight_kmd`]="{ item }">
          {{ item.weight_kmd / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_in_work`]="{ item }">
          {{ item.weight_in_work / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_preparation`]="{ item }">
          {{ item.weight_preparation / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_set`]="{ item }">
          {{ item.weight_set / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_assembly`]="{ item }">
          {{ item.weight_assembly / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_weld`]="{ item }">
          {{ item.weight_weld / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_paint`]="{ item }">
          {{ item.weight_paint / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_packed`]="{ item }">
          {{ item.weight_packed / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_shipment`]="{ item }">
          {{ item.weight_shipment / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_in_object`]="{ item }">
          {{ item.weight_in_object / 1000 | number }}
        </template>
        <template v-slot:[`item.weight_mount`]="{ item }">
          {{ item.weight_mount / 1000 | number }}
        </template>
      </v-data-table>
    </v-container>
  </div>
</template>

<script>
export default {
  data(){
    return {
      report:[],
      cas:{},
      headers:[
        {text:'фаза',value:'faza'},
        {text:'Разработано КМД',value:'weight_kmd'},
        {text:'Передано в производство',value:'weight_in_work'},
        {text:'Заготовка завершена',value:'weight_preparation'},
        {text:'Скопмплектовано',value:'weight_set'},
        {text:'Собрано',value:'weight_assembly'},
        {text:'Сварено',value:'weight_weld'},
        {text:'Окрашено',value:'weight_paint'},
        {text:'Упаковано',value:'weight_packed'},
        {text:'Отгружено',value:'weight_shipment'},
        // {text:'Доставлено на объект',value:'weight_in_object'},
        // {text:'Смонтировано',value:'weight_mount'},
      ]
    }
  },
  mounted(){
    this.getReport()
  },
  methods: {
    async getReport(){
      this.report = await this.$axios.$get(this.$store.state.db.host+'report/faza/'+this.$route.params.faza);
      this.cas = this.report.case
      this.report = this.report.faza
    }
  },
}
</script>
