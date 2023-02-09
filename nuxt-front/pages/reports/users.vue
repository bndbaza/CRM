<template>
  <v-container>
    <div v-if="!show_user">
      <v-btn v-if="user[0] && start && end" color="orange" light block @click="ReportUser()">Открыть</v-btn>
      <v-row>
        <v-col>
          <v-data-table
            v-model="user"
            :headers="headers"
            hide-default-footer
            :items-per-page="1000"
            :items="users"
            single-select="true"
            item-key="id"
            show-select
            class="elevation-1"
          >
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
        </v-col>
      </v-row>
    </div>

    <div v-if="show_user">
      <h2 class="text-center">{{user[0].surname}} {{user[0].name}} {{user[0].patronymic}}</h2>
      <h2 class="text-center">с {{start | date('date')}} по {{end | date('date')}}</h2>
      <v-row>
        <v-col v-for="keys,value in report" :key="value">
          <h3 class="text-center ma-3">
            {{value}}
          </h3>
          <v-data-table
            v-if="value == 'Сварка' || value == 'Сборка'"
            :headers="headers2"
            hide-default-footer
            :items-per-page="1000"
            :items="keys"
            single-select="true"
            item-key="id"
            class="elevation-1"
          >
            <template v-slot:[`item.norm`]="{ item }">
              {{ item.norm | norm }}
            </template>
            <template v-slot:[`item.end`]="{ item }">
              <template v-if="item.task != 'Итог'">
                {{ Replace(item.end)}}
              </template>
            </template>
          </v-data-table>

          <v-data-table
            v-if="value == 'Покраска'"
            :headers="headers2"
            hide-default-footer
            :items-per-page="5000"
            :items="keys"
            single-select="true"
            item-key="id"
            class="elevation-1"
          >
            <template v-slot:[`item.norm`]="{ item }">
              <template v-if="item.worker_2">
                {{ item.norm / 2 | money }}
              </template>
              <template v-else>
                {{ item.norm | money}}
              </template>
              
            </template>
            <template v-slot:[`item.end`]="{ item }">
              <template v-if="item.task != 'Итог'">
                {{ Replace(item.end)}}
              </template>
            </template>
          </v-data-table>

          <v-data-table
            v-if="value == 'Комплектовка'"
            :headers="headers4"
            hide-default-footer
            :items-per-page="1000"
            :items="keys"
            single-select="true"
            item-key="id"
            class="elevation-1"
          >
            <template v-slot:[`item.end`]="{ item }">
              <template v-if="item.task != 'Итог'">
                {{ Replace(item.end)}}
              </template>
            </template>
          </v-data-table>


          <v-data-table
            v-if="value != 'Сварка' && value != 'Сборка' && value != 'Комплектовка' && value != 'Покраска'  && value != 'Сверловка' && value != 'Пилы' && value != 'Скос'"
            :headers="headers3"
            hide-default-footer
            :items-per-page="1000"
            :items="keys"
            single-select="true"
            item-key="id"
            class="elevation-1"
          >
            <template v-slot:[`item.end`]="{ item }">
              <template v-if="item.task != 'Итог'">
                {{ Replace(item.end)}}
              </template>
            </template>
          </v-data-table>

          <v-data-table
            v-if="value == 'Сверловка'"
            :headers="headers5"
            hide-default-footer
            :items-per-page="1000"
            :items="keys"
            single-select="true"
            item-key="id"
            class="elevation-1"
          >
            <template v-slot:[`item.norm`]="{ item }">
              {{ item.norm | norm }}
            </template>
            <template v-slot:[`item.end`]="{ item }">
              <template v-if="item.task != 'Итог'">
                {{ Replace(item.end)}}
              </template>
            </template>
          </v-data-table>

          <v-data-table
            v-if="value == 'Пилы' || value == 'Скос'"
            :headers="headers6"
            hide-default-footer
            :items-per-page="1000"
            :items="keys"
            single-select="true"
            item-key="id"
            class="elevation-1"
          >
            <template v-slot:[`item.norm`]="{ item }">
              {{ item.norm | norm }}
            </template>
            <template v-slot:[`item.end`]="{ item }">
              <template v-if="item.task != 'Итог'">
                {{ Replace(item.end)}}
              </template>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      user: [],
      show_user: false,
      start: '',
      report: {},
      end: '',
      users: [],
      headers: [
        { text: 'Фамилия', value: 'surname' },
        { text: 'Имя', value: 'name' },
      ],
      headers2: [
        { text: 'Наряд', value: 'detail' },
        { text: 'Дата', value: 'end' },
        { text: 'Марка', value: 'mark' },
        { text: 'Чертеж', value: 'draw' },
        { text: 'Наименование', value: 'name' },
        { text: 'Вес', value: 'weight' },
        { text: 'Норма', value: 'norm' },
      ],
      headers4: [
        { text: 'Наряд', value: 'detail' },
        { text: 'Дата', value: 'end' },
        { text: 'Марка', value: 'mark' },
        { text: 'Чертеж', value: 'draw' },
        { text: 'Наименование', value: 'name' },
        { text: 'Вес', value: 'weight' },
      ],
      headers3: [
        { text: 'Задание', value: 'task' },
        { text: 'Дата', value: 'end' },
        { text: 'Профиль', value: 'profile' },
        { text: 'Размер', value: 'size' },
        { text: 'Количество', value: 'count_all' },
      ],
      headers5: [
        { text: 'Задание', value: 'task' },
        { text: 'Дата', value: 'end' },
        { text: 'Профиль', value: 'profile' },
        { text: 'Размер', value: 'size' },
        { text: 'Количество', value: 'count' },
        { text: 'Норма', value: 'norm' },
      ],
      headers6: [
        { text: 'Задание', value: 'task' },
        { text: 'Дата', value: 'end' },
        { text: 'Профиль', value: 'profile' },
        { text: 'Размер', value: 'size' },
        { text: 'Количество', value: 'count_all' },
        { text: 'Норма', value: 'norm' },
      ],
    }
  },
  async mounted() {
    await this.Report()
  },
  methods: {
    async Report() {
      this.users = await this.$axios.$get(this.$store.state.db.host+'users')
    },
    async ReportUser() {
      this.show_user = true
      this.report = await this.$axios.$get(this.$store.state.db.host+'report/user/'+this.user[0].id+'/'+this.start+'/'+this.end)
    },
    Replace(text) {
      text = text.split('T')[0]
      text = new Date(text.split('-'))
      var options = {
      year: 'numeric',
      month: 'numeric',
      day: 'numeric',
      };
      text = text.toLocaleString("ru",options)
      return text
    },
  }
}
</script>
