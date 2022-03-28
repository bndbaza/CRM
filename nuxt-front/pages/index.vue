<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="detail"
      hide-default-footer
      :items-per-page="1000"
      class="elevation-1"
    >
      <template v-slot:[`item.start`]="{ item }">
        <template v-if="item.start">
          {{ item.start | date }} {{item.worker_1.user.surname}} {{item.worker_1.user.name}} {{item.worker_1.user.patronymic}}
        </template>
      </template>
      <template v-slot:[`item.oper`]="{ item }">
        <template>
          {{ trans[item.oper] }}
        </template>
      </template>
      <template v-slot:[`item.detail`]="{ item }">
        <template>
          <nuxt-link :to="'/detail/'+item.detail">
            {{ item.detail }}
          </nuxt-link>
        </template>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  data(){
    return{
      detail:[],
      headers:[
        {text:'Наряд',value:'detail'},
        {text:'Стадия',value:'oper'},
        {text:'Начало',value:'start'}
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
    this.detail = await this.$axios.$get('http://192.168.0.75:8000/index')
  }
}
</script>