<template>
  <div>
    <v-container grid-list-xs>
      <v-row>
        <v-col>
          <v-data-table
            :headers="headers"
            :items="report"
            hide-default-footer
            :items-per-page="100"
            class="elevation-1"
            dense
          >
            <template v-slot:[`item.worker`]="{ item }">
              {{ item.worker.user.surname }} {{ item.worker.user.name }} {{ item.worker.user.patronymic }}
            </template>
            <template v-slot:[`item.weight_all`]="{ item }">
              {{ item.weight_all / 1000 | number }} тн
            </template>
          </v-data-table>
        </v-col>
        <v-col cols="2">
          <v-date-picker
            v-model="start"
            :first-day-of-week="1"
            locale="ru-ru"
            no-title
          ></v-date-picker>
          <v-date-picker
            v-model="end"
            :first-day-of-week="1"
            locale="ru-ru"
            no-title
          ></v-date-picker>
          <v-btn block color="info" @click="getReport()" dark>Запросить</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data(){
    return {
      report:[],
      start:'',
      end:'',
      title:'',
      headers:[
        {text:'Сборщик',value:'worker'},
        {text:'Собрано',value:'weight_all'},
        {text:'Время',value:'norm_all'},
      ],
    }
  },
  // mounted(){
  //   this.getReport()
  // },
  methods: {
    async getReport(){
      if (this.start != '' & this.end != '') {
        this.report = await this.$axios.$get(this.$store.state.db.host+'report/workers/assembly/'+this.start+'/'+this.end);
        this.title = this.start
      }
    }
  },
}
</script>