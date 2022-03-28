<template>
  <v-container>
    <h1>Наряд {{$route.params.id}}</h1>
    <v-row>
      <v-col cols="3">
        <v-row>
          <v-col>
            <p v-if="detail.pointparts">Марка</p>
            <p v-if="detail.pointparts">Вес</p>
            <p v-if="detail.pointparts">Фаза</p>
            <p v-for="detail in detail.details" :key="detail">{{manipulation[detail.oper]}}</p>
          </v-col>
          <v-col>
            <p v-if="detail.pointparts">{{detail.pointparts[0].point.assembly.assembly}}</p>
            <p v-if="detail.pointparts">{{detail.pointparts[0].point.assembly.weight}} кг.</p>
            <p v-if="detail.pointparts">{{detail.pointparts[0].point.faza}}</p>
            <p v-for="detail in detail.details" :key="detail">{{Status(detail,detail.start,detail.end)}}</p>
          </v-col>
        </v-row>
      </v-col>
      <v-col>
          <v-simple-table dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th>
                    Позиция
                  </th>
                  <th class="text-left">
                    Количество
                  </th>
                  <th class="text-left">
                    Операция
                  </th>
                  <th class="text-left">
                    Статус
                  </th>
                  <th class="text-left">
                    Работник
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="task in detail.tasks"
                  :key="task"
                >
                  <td>{{ task.part.number }}</td>
                  <td>{{ task.part.count }}</td>
                  <td>{{ manipulation[task.task.oper] }}</td>
                  <td>{{ Status(task.task.start,task.task.end) }}</td>
                  <td v-if="task.task.worker_1 && !task.task.worker_2">{{ task.task.worker_1.user.surname }} 
                    {{ task.task.worker_1.user.name }} 
                    {{ task.task.worker_1.user.patronymic }}</td>
                  <td v-if="task.task.worker_1 && task.task.worker_2">{{ task.task.worker_1.user.surname }} 
                    {{ task.task.worker_1.user.name }} 
                    {{ task.task.worker_1.user.patronymic }},
                    {{ task.task.worker_2.user.surname }} 
                    {{ task.task.worker_2.user.name }} 
                    {{ task.task.worker_2.user.patronymic }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
      </v-col>
    </v-row> 
  </v-container>
</template>

<script>
export default {
  data(){
    return{
      detail:[],
      manipulation:{
        saw_b:'Пила Б',
        saw_s:'Пила М',
        cgm:'Фасонка',
        hole:'Сверловка',
        assembly:'Сборка',
        weld:'Сварка',
        set:'Комплектовка',
        paint:'Покраска'
      }
    }
  },
  async mounted(){
    this.detail = await this.$axios.$get('http://192.168.0.75:8000/detail/'+this.$route.params.id)
  },
  methods:{
    Status(detail,start,end){
      let stat = 'Не в работе'
      if (end){
        if (detail.worker_2){
          stat = 'Готов ('+detail.worker_1.user.surname+','+detail.worker_2.user.surname+')'
        }else{
          stat = 'Готов ('+detail.worker_1.user.surname+')'
        }
      }else if (start) {
        if (detail.worker_2){
          stat = 'В работе ('+detail.worker_1.user.surname+','+detail.worker_2.user.surname+')'
        }else{
          stat = 'В работе ('+detail.worker_1.user.surname+')'
        }
      }
      return stat
    }
  }
}
</script>