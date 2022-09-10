<template>
  <div>
    <!-- <v-text-field
      v-model="text"
      name="name"
      label="label"
      id="id"
    ></v-text-field>
    <v-btn color="success" @click="getUser(text),getDetail(text),text=''">text</v-btn> -->
    <v-alert v-if="user && user.error == 'Список Пуст'" type="info" :value="true">
      <h4>{{user.error}}</h4>
    </v-alert>
    <v-alert v-if="user && user.error != None && user.error != 'Список Пуст'" type="error" :value="true">
      <h4>{{user.error}}</h4>
    </v-alert>
    <v-container v-if="user != ''">
      <v-row justify="space-around">
        <v-col cols="9">
          <v-col cols="12" v-for="detail in user.detail" :key="detail.id">
            <v-card v-if="detail.detail" color="blue">
              <v-card-text>
                <h1>Наряд №{{detail.detail}} Время начала {{detail.start | date}}</h1>
              </v-card-text>
            </v-card>
            <v-card v-if="detail.task" color="green">
              <v-card-text>
                <h1>Задание №{{detail.task}} Время начала {{detail.start | date}}</h1>
              </v-card-text>
            </v-card>
          </v-col>
        </v-col>
        <v-col cols="3">
          <v-col cols="12" v-if="calc != 0">
            <v-card color="yellow">
              <v-card-text>
                <h1>Количество операций: {{calc}}</h1>  
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" v-for="worker in user.worker" :key="worker.id">
            <v-card color="green">
              <v-card-text>
                <h1>{{worker.user.surname}} {{worker.user.name}} {{worker.user.patronymic}}</h1>
                <h1><br></h1>
                <h1>{{worker.oper_rus}}</h1>
              </v-card-text>
            </v-card>
          </v-col>
        </v-col>
      </v-row>
    </v-container>
    <v-container fluid v-if="user == ''">
      <v-row justify="space-around">
        <v-col>
          <v-simple-table dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Заготовка
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in gowork.saw"
                  :key="item.id"
                >
                  
                  <td>
                    {{ item.detail}}
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
        <v-col cols="2" v-for="oper in opers" :key="oper.rus">
          <v-simple-table dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    {{oper.rus}}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in gowork.assembly"
                  :key="item.worker_1"
                >
                  <td 
                    v-if="item.oper == oper.eng && item.worker_1" 
                  >
                    {{ item.detail}} ({{ item.worker_1.user.surname }} {{ item.worker_1.user.name }} {{ item.start | date }})
                  </td>
                  <td v-if="item.oper == oper.eng && !item.worker_1"
                  >
                    {{ item.detail}}
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
        <v-col></v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  layout: 'empty',
  data() {
    return {
      barcode: '',
      timeout: null,
      user: '',
      details: [],
      col: "blue",
      timerId: null,
      text: '',
      gowork: [],
      calc: 0,
      opers: [
        {rus:'Комплектовка',eng:'set'},
        {rus:'Сборка',eng:'assembly'},
        {rus:'Сварка',eng:'weld'},
        {rus:'Покраска',eng:'paint'},
      ]
    }
  },
  mounted() {
    window.addEventListener('keydown', this.onGlobalKeyDown);
    this.goWork()
  },
  destroyed() {
    window.removeEventListener('keydown', this.onGlobalKeyDown);
  },
  methods: {
    onGlobalKeyDown(event) {
      clearTimeout(this.timeout);
      const THRESHOLD = 30;
      this.timeout = setTimeout(() => { this.resetBarcode(); }, THRESHOLD);
      const key = String.fromCharCode(event.which);
      if (key) this.barcode += key;
      const isEnter = event.key === 'Enter';
      // const isBarcode = this.barcode.length > 1;
      // if (!isEnter || !isBarcode) return;
      if (!isEnter) return;
      if (this.barcode[1] == 'U') {
        this.getUser(this.barcode,this.user);
      }else if ((this.barcode[1] == 'A' | this.barcode[1] == 'T') & this.user != '') {
        this.getDetail(this.barcode,this.barcodes);
      }else{
        this.details = {'error':'Работник не выбран'}
        this.timerId = setTimeout(() => this.timerRest(), 10000);
      }
      this.resetBarcode();
    },
    resetBarcode() {
      this.barcode = '';
    },
    async getUser(id) {
      let us = '';
      let ee = 0;
      if (this.user != '') ee = this.user.worker.length;
      if (this.user != '' & ee < 2) us = this.user.worker[0].id;
      this.user = await this.$axios.$post(this.$store.state.db.host+'worker',{id:id,user:us});
      await clearTimeout(this.timerId);
      this.timerId = await setTimeout(() => this.timerRest(), 10000);
    },
    async getDetail(detail) {
      this.user = await this.$axios.$post(this.$store.state.db.host+'details',{detail:detail,user: this.user.worker});
      await clearTimeout(this.timerId);
      this.calc += 1
      this.timerId = await setTimeout(() => this.timerRest(), 10000);
    },
    timerRest() {
      this.details = [];
      this.user = '';
      this.barcode = '';
      this.calc = 0;
      this.goWork()
    },
    async goWork(){
      this.gowork = await this.$axios.$get(this.$store.state.db.host+'task')
    },
  },
}
</script>