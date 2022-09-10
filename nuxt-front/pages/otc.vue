<template>
  <div class="">
    <v-container>
      <v-row>
        <v-col>
          <h2 v-if="str_date != ''" class="text-center mb-5">{{str_date | date('date')}}</h2>
          <v-btn color="success" block class="pa-5" v-if="report.weld != ''" @click="Download(report.weld)">Скачать Акт на Сварку</v-btn>
          <v-btn color="success" block class="mt-5 pa-5" v-if="report.paint != ''" @click="Download(report.paint)">Скачать Акт на Малярку</v-btn>
        </v-col>
        <v-col cols="2">
          <v-date-picker
            v-model="date"
            :first-day-of-week="1"
            locale="ru-ru"
            no-title
          ></v-date-picker>
          <v-btn color="info" @click="getReport()" v-if="date != ''" block>Запросить</v-btn>
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
import axios from 'axios'
export default {
  data () {
    return {
      date: '',
      str_date: '',
      report: { "weld": "", "paint": "" },
      loader: false
    }
  },
  methods: {
    async getReport(){
      this.loader = true
      this.report = { "weld": "", "paint": "" };
      this.str_date = ''
      this.report = await this.$axios.$get(this.$store.state.db.host+'act_everyday/'+this.date);
      this.str_date = this.date
      this.loader = false
    },
    Download(oper) {
      axios({
        url: this.$store.state.db.host+'act/file/' + oper,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', '1' +'.'+ (oper).split('.').pop());
        document.body.appendChild(link);
        link.click();
      });
    },
  },

}
</script>