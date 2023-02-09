<template>
  <div>
    <v-container fluid>
      <h1 v-if="$route.params.id.split(',')[1] != '0'" class="text-center">Заказ {{($route.params.id).split(',')[0]}} Фаза {{($route.params.id).split(',')[1]}}</h1>
      <h1 v-else class="text-center">Заказ {{($route.params.id).split(',')[0]}}</h1>
      <v-row>
        <v-col v-for="header in headers" :key="header">
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    <h4 class="text-center">{{header.text}}</h4>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="stage in stages"
                  :key="stage.id"
                >
                  <td v-if="Variant(header.text,stage) & (stage.detail == $store.state.db.search | $store.state.db.search == '')"><nuxt-link :to="'../../../detail/'+stage.detail" large><h2 class="text-center orange--text">{{ stage.detail }}</h2></nuxt-link></td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
      </v-row>
    </v-container>

  </div>
</template>

<script>
export default {
  data(){
    return{
      search: '',
      stages:[],
      aaa:{},
      headers:[
        {text:'Заготовка',value: 10},
        {text:'Готов к комплектации',value: 9},
        {text:'В комплектации',value: 1},
        {text:'Готов к сборке',value: 2},
        {text:'В сборке',value: 3},
        {text:'Готов к сварке',value: 4},
        {text:'В сварке',value: 5},
        {text:'Ожидает ОТК после сварки',value: 12},
        {text:'Готов к покраске',value: 6},
        {text:'В покраске',value: 7},
        {text:'Ожидает ОТК после покраски',value: 11},
        {text:'Готов к упаковке',value: 8},
        {text:'Упакован',value: 13},
        {text:'Отгружен',value: 14},
      ],
      trans:{
        assembly:'Сборка',
        set:'Комплектовка',
        weld:'Сварка',
        paint:'Покраска'
      }
    }
  },
  async mounted(){
    this.stages = await this.$axios.$get(this.$store.state.db.host+'stage/'+this.$route.params.id)
    this.$store.commit('db/mark','')
  },
  methods: {
    Variant(x,stage){
      if (x == 'Заготовка') {
        if (stage.set == 0){
          return true
        }else{
          return false
        }
      }
      if (x == 'Готов к комплектации') {
        if (stage.set == 1){
          return true
        }else{
          return false
        }
      }
      if (x == 'В комплектации') {
        if (stage.set == 2){
          return true
        }else{
          return false
        }
      }
      if (x == 'Готов к сборке') {
        if (stage.assembly == 1){
          return true
        }else{
          return false
        }
      }
      if (x == 'В сборке') {
        if (stage.assembly == 2){
          return true
        }else{
          return false
        }
      }if (x == 'Готов к сварке') {
        if (stage.weld == 1){
          return true
        }else{
          return false
        }
      }
      if (x == 'В сварке') {
        if (stage.weld == 2){
          return true
        }else{
          return false
        }
      }
      if (x == 'Ожидает ОТК после сварки') {
        if (stage.weld == 3 && stage.paint == 0){
          return true
        }else{
          return false
        }
      }
      if (x == 'Готов к покраске') {
        if (stage.paint == 1){
          return true
        }else{
          return false
        }
      }
      if (x == 'В покраске') {
        if (stage.paint == 2){
          return true
        }else{
          return false
        }
      }
      if (x == 'Ожидает ОТК после покраски') {
        if (stage.paint == 3 && stage.packed == 0){
          return true
        }else{
          return false
        }
      }
      if (x == 'Готов к упаковке') {
        if (stage.packed == 1){
          return true
        }else{
          return false
        }
      }
      if (x == 'Упакован') {
        if (stage.packed == 3 && stage.shipment != 3){
          return true
        }else{
          return false
        }
      }
      if (x == 'Отгружен') {
        if (stage.shipment == 3){
          return true
        }else{
          return false
        }
      }
    }
  },
}
</script>
