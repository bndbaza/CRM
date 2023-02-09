<template>
  <div>
    <v-container>
      <v-row>
        <v-col>
          <v-data-table
            dense
            :headers="headers"
            :items="items"
            :items-per-page="100"
            hide-default-footer
          >
            <template v-slot:[`item.date_in`]="{ item }">
              {{ item.date_in | date }}
            </template>
            <template v-slot:[`item.date_out`]="{ item }">
              <template v-if="item.date_out != null">
                {{ item.date_out | date }}
              </template>
            </template>
            <template v-slot:[`item.record`]="{ item }">
              <audio controls v-if="item.record != null" preload="metadata">
                <source :src="Audio(item.record)" type="audio/wav">
              </audio>
            </template>
          </v-data-table>
        </v-col>
        <v-col cols="2">
          <p>{{list_call}}</p>
        </v-col>
        <v-col cols="3">
          <!-- <v-btn block v-for="phone in phone_book" :key="phone.id" color="orange" light text @click="Call(phone.phone),Ringing()">{{phone.company}} {{phone.surname}} {{phone.name}} {{phone.patronymic}}</v-btn> -->
          <v-btn block v-for="phone in phone_book" :key="phone.id" color="orange" light text @click="Ringing()">{{phone.company}} {{phone.surname}} {{phone.name}} {{phone.patronymic}}</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<<script>
export default {
  data() {
    return {
      items: [],
      phone_book: [],
      sound: '',
      list_call: [],
      headers: [
        {text:'Исходящие',value:'inbound'},
        {text:'Начало звонка',value:'date_in'},
        {text:'Входящие',value:'outgoing'},
        {text:'Окончание звонка',value:'date_out'},
        {text:'Запись',value:'record'},
      ],
    }
  },
  async mounted() {
    this.items = await this.$axios.$get(this.$store.state.db.host+'call_list')
    this.phone_book = await this.$axios.$get(this.$store.state.db.host+'phone_book')
    await this.Ringing()
  },
  methods: {
    Audio(record) {
      let sound
      sound = 'http://192.168.0.69:8088/ari/recordings/stored/'+record+'/file?api_key=viktor:35739517'
      return sound
    },
    async Call(number) {
      await this.$axios.$get(this.$store.state.db.host+'ring/'+this.$store.state.db.user.phone+'/'+number)
    },
    async Ringing() {
      // while (true) {
      // await this.$axios.$get(this.$store.state.db.host+'ringing')
        this.list_call = await this.$axios.$get(this.$store.state.db.host+'ringing')
        // await new Promise(r => setTimeout(r,1000))
      // }
    }
  } 
}
</script>
