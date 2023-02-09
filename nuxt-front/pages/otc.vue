<template>
  <div class="">
    <v-container>
      <v-row>
        <v-col>
          <h2 v-if="str_date != ''" class="text-center mb-5">{{str_date | date('date')}}</h2>
          <v-btn color="orange" light block class="pa-5" v-if="report.weld != ''" @click="Download(report.weld)">Скачать Акт на Сварку</v-btn>
          <v-btn color="orange" light block class="mt-5 pa-5" v-if="report.paint != ''" @click="Download(report.paint)">Скачать Акт на Малярку</v-btn>
        </v-col>
        <v-col cols="2">
          <v-row>
          <v-col>
          <v-date-picker
            v-model="date"
            :first-day-of-week="1"
            locale="ru-ru"
            color="teal"
            no-title
          ></v-date-picker>
          </v-col>
          </v-row>
          <v-row>
          <v-col>
          <v-btn color="teal" class="mx-2" light @click="getReport()" v-if="date != ''" block>Запросить</v-btn>
          </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
    <v-dialog
      v-model="loader"
      scrollable
      persistent :overlay="false"
      max-width="150px"
      transition="dialog-transition"
    >
      <v-progress-linear
        indeterminate
        color="orange"
      ></v-progress-linear>
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
        link.setAttribute('download', (oper).replace('z',' ')+'.pdf');
        document.body.appendChild(link);
        link.click();
      });
    },
  },

}
</script>
