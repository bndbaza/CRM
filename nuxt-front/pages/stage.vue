<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col v-for="stage in stages" :key="stage">
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    <h4 class="text-center">{{stage.name}}</h4>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="faza in stage.faza"
                  :key="faza"
                >
                  <!-- <td><p>{{faza.detail}}</p></td> -->
                  <td v-if="(faza.detail == $store.state.db.search | $store.state.db.search == '')"><nuxt-link :to="'detail/'+faza.detail" large><h2 class="text-center"><font :color="faza.color">{{ faza.detail }}</font></h2></nuxt-link></td>
                  <!-- <td v-if="Variant(header.text,stage) & (stage.detail == $store.state.db.search | $store.state.db.search == '')"><nuxt-link :to="'detail/'+stage.detail" large><h2 class="text-center"><font :color="stage.case.color">{{ stage.detail }}</font></h2></nuxt-link></td> -->
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
      color: 'green',
      trans:{
        assembly:'Сборка',
        set:'Комплектовка',
        weld:'Сварка',
        paint:'Покраска'
      }
    }
  },
  async mounted(){
    // this.$store.commit('db/mark','')
    this.stages = await this.$axios.$get(this.$store.state.db.host+'stage/0')
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
        if (stage.packed == 3 && stage.shipment == 0){
          return true
        }else{
          return false
        }
      }
      if (x == 'Отгружен') {
        if (stage.packed == 3 && stage.shipment == 3){
          return true
        }else{
          return false
        }
      }
    }
  },
}
</script>