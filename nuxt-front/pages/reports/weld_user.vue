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
            <template v-slot:[`item.weld`]="{ item }">
              <p v-for="w in item.weld" :key="w">
                катет {{ w.cathet.cathet }}: {{ w.length / 1000 | number}} м
              </p>
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
    <v-dialog
      v-model="loader"
      hide-overlay
      persistent
      width="300"
    >
      <v-card
        color="primary"
        dark
      >
        <v-card-text>
          Идет загрузка
          <v-progress-linear 
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data(){
    return {
      report:[],
      loader: false,
      start:'',
      end:'',
      headers:[
        {text:'Сварщик',value:'worker'},
        {text:'Сварено',value:'weight_all'},
        {text:'Время',value:'norm_all'},
        {text:'Длина шва',value:'weld'}
      ],
    }
  },
  // mounted(){
  //   this.getReport()
  // },
  methods: {
    async getReport(){
      this.loader = true
      this.report = await this.$axios.$get(this.$store.state.db.host+'report/workers/weld/'+this.start+'/'+this.end);
      this.loader = false
    }
  },
}
</script>