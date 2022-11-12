<template>
  <v-container fluid>
    <h1>Наряд {{$route.params.id}}</h1>
    <v-row>
      <v-col cols="5">
        <v-row>
          <v-col cols="3">
            <p v-if="detail.pointparts">Заказ</p>
            <p v-if="detail.pointparts">Марка</p>
            <p v-if="detail.pointparts">Количество</p>
            <p v-if="detail.pointparts">Вес</p>
            <p v-if="detail.pointparts">Фаза</p>
            <p v-if="detail.pointparts">Чертёж</p>
            <p v-for="detail in detail.details" :key="detail">{{manipulation[detail.oper]}}</p>
            <p v-if="detail.pack">Пачка</p>
            <p v-if="detail.pack && detail.pack.shipment">Машина</p>
            <p>-</p>
            <template v-for="detail in detail.details"  >
              <p :key="detail" v-if="detail.oper != 'set' && detail.oper != 'paint'">{{manipulation[detail.oper]}}</p>
            </template>
          </v-col>
          <v-col cols="4">
            <p v-if="detail.pointparts">{{detail.pointparts[0].point.assembly.cas.cas}}</p>
            <p v-if="detail.pointparts">{{detail.pointparts[0].point.assembly.assembly}}</p>
            <p v-if="detail.pointparts">{{detail.count}}</p>
            <p v-if="detail.pointparts">{{detail.pointparts[0].point.assembly.weight}} кг.</p>
            <p v-if="detail.pointparts">{{detail.pointparts[0].point.faza}}</p>
            <p v-if="detail.pointparts">{{detail.pointparts[0].point.draw}}</p>
            <p v-for="detail in detail.details" :key="detail">{{Status(detail,detail.start,detail.end)}}</p>
            <p v-if="detail.pack">{{ detail.pack.number }}</p>
            <p v-if="detail.pack && detail.pack.shipment">{{detail.pack.shipment.number}}</p>
            <p>Нормы</p>
            <template v-for="detail in detail.details">
              <p :key="detail" v-if="detail.oper != 'set' && detail.oper != 'paint'">{{detail.norm | norm}}</p>
            </template>
          </v-col>
          <v-col>
            <p v-if="detail.pointparts">-</p>
            <p v-if="detail.pointparts">-</p>
            <p v-if="detail.pointparts">-</p>
            <p v-if="detail.pointparts">-</p>
            <p v-if="detail.pointparts">-</p>
            <p v-if="detail.pointparts">-</p>
            <template v-for="detail in detail.details">
              <p :key="detail" v-if="detail.end">{{detail.start | date('datetime')}} - {{detail.end | date('datetime')}}</p>
              <p :key="detail" v-else-if="detail.start">{{detail.start | date('datetime')}}</p>
              <p :key="detail" v-else>-</p>
            </template>
            <p v-if="detail.pack">{{ detail.pack.date | date('datetime') }}</p>
            <p v-if="detail.pack && detail.pack.shipment">{{detail.pack.shipment.date | date('datetime')}}</p>
            <p>-</p>
          </v-col>
        </v-row>
      </v-col>
      <v-col>
        <v-data-table
          :headers="headers"
          :items="detail.tasks"
          hide-default-footer
          :items-per-page="100"
          class="elevation-1"
          :search="search"
          dense
        > 
          <template v-slot:[`item.status`]="{ item }">
            <template v-if="item.task.end">
              <v-chip color="white">Готов</v-chip>
            </template>
            <template v-else-if="item.task.start">
              <v-chip color="yellow">В работе</v-chip>
            </template>
            <template v-else>
              <v-chip color="red">Не в работе</v-chip>
            </template>
          </template>
          <template v-slot:[`item.date`]="{ item }">
            <template v-if="item.task.end">
              {{ item.task.end | date('datetime')}}
            </template>
            <template v-else-if="item.task.start">
              {{ item.task.start | date('datetime')}}
            </template>
            <template v-else>
              
            </template>
          </template>
          <template v-slot:[`item.task.oper`]="{ item }">
            {{ manipulation[item.task.oper] }}
          </template>
        </v-data-table>
      </v-col>
    </v-row> 
  </v-container>
</template>

<script>
export default {
  data(){
    return{
      detail:[],
      headers:[
        {text:'Задание',value:'task.task'},
        {text:'Позиция',value:'part.number'},
        {text:'Количество',value:'part.count'},
        {text:'Операция',value:'task.oper'},
        {text:'Статус',value:'status'},
        {text:'Дата',value:'date'},
        {text:'Работник',value:'task.worker_1.user.surname'},
      ],
      manipulation:{
        saw_b:'Пила Б',
        saw_s:'Пила М',
        cgm:'Фасонка',
        hole:'Сверловка',
        assembly:'Сборка',
        weld:'Сварка',
        set:'Комплектовка',
        paint:'Покраска',
        bevel:'Скос',
        notch:'Вырез',
        chamfer:'Фаска',
        milling:'Фрезеровка',
        joint:'Стыковка',
        bend:'Гибка'
      }
    }
  },
  async mounted(){
    this.detail = await this.$axios.$get(this.$store.state.db.host+'detail/'+this.$route.params.id)
  },
  methods:{
    Status(detail,start,end){
      let stat = 'Не в работе'
      if (end){
        if (detail.worker_2){
          stat = 'Готов ('+detail.worker_1.user.surname+','+detail.worker_2.user.surname+') '
        }else{
          stat = 'Готов ('+detail.worker_1.user.surname+') '
        }
      }else if (start) {
        if (detail.worker_2){
          stat = 'В работе ('+detail.worker_1.user.surname+','+detail.worker_2.user.surname+')'
        }else{
          stat = 'В работе ('+detail.worker_1.user.surname+')'
        }
      }
      return stat
    },
    StatusTask(start,end) {
      let stat = 'Не в работе'
      if (end){
          stat = 'Готов ('+end+')'
      }else if (start) {
          stat = 'В работе ('+start+')'
      }
      return stat
    },
    dateFilter(value, format= 'date') {
      const options ={day: 'numeric',month:'numeric',year:'numeric',hour:'numeric',minute:'numeric'}
      return new Intl.DateTimeFormat('ru-RU', options).format(new Date(value))
    }
  }
}
</script>