<template>
  <div>
    <v-container>
      <v-row>
        <v-col>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Работник
                  </th>
                  <th class="text-left">
                    Сумма
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="report in reports"
                  :key="report"
                >
                  <td>{{ report.user.__data__.surname }} {{ report.user.__data__.name }} {{ report.user.__data__.patronymic }}</td>
                  <td>{{ report.norm | money }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
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
          <v-btn block color="info" @click="getReport()">Запросить</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      reports: [],
      start:'',
      end:'',
      title:'',
    }
  },
  methods: {
    async getReport(){
      if (this.start != '' & this.end != '') {
        this.reports = await this.$axios.$get(this.$store.state.db.host+'report/workers/paint/'+this.start+'/'+this.end);
        this.title = this.start
      }
    }
  },
}
</script>