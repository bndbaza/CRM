<template>
  <div>
    <v-text-field
      v-model="text"
      name="name"
      label="label"
      id="id"
    ></v-text-field>
    <v-btn color="success" @click="getUser(text),getDetail(text),text=''">text</v-btn>
    <v-alert v-if="user.error == 'Список Пуст'" type="info" :value="true">
      <h4>{{user.error}}</h4>
    </v-alert>
    <v-alert v-if="user.error != None && user.error != 'Список Пуст'" type="error" :value="true">
      <h4>{{user.error}}</h4>
    </v-alert>
    <v-container v-if="user != ''">
      <v-row justify="space-around">
        <v-col cols="9">
          <v-col cols="12" v-for="detail in user.detail" :key="detail">
            <v-card v-if="detail.detail" color="blue">
              <v-card-text>
                <h1>Наряд №{{detail.detail}} Время начала {{detail.start | date}}</h1>
              </v-card-text>
            </v-card>
            <v-card v-if="detail.task" color="red">
              <v-card-text>
                <h1>Задание №{{detail.task}} Время начала {{detail.start | date}}</h1>
              </v-card-text>
            </v-card>
          </v-col>
        </v-col>
        <v-col cols="3">
          <v-col cols="12" v-for="worker in user.worker" :key="worker">
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
        <v-col cols="2" v-for="oper in opers" :key="oper">
          <v-simple-table dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    {{oper[0]}}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in gowork"
                  :key="item.worker_1"
                >
                  <td v-if="item.oper == oper[1] && item.worker_1" >{{ item. detail}} ({{ item.worker_1.user.surname }} {{ item.worker_1.user.name }} {{ item.start | date }})</td>
                  <td v-if="item.oper == oper[1] && !item.worker_1">{{ item. detail}}</td>
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
import axios from 'axios'
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
      opers: [['Комплектовка','set'],['Сборка','assembly'],['Сварка','weld'],['Покраска','paint']]
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
      const isBarcode = this.barcode.length > 3;
      if (!isEnter || !isBarcode) return;
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
      this.user = await this.$axios.$post('http://192.168.0.75:8000/worker',{id:id,user:us})
      clearTimeout(this.timerId);
      this.timerId = setTimeout(() => this.timerRest(), 10000);
    },
    async getDetail(detail) {
      this.user = await this.$axios.$post('http://192.168.0.75:8000/details',{detail:detail,user: this.user.worker})
      // .then(response => this.user = response.data);
      clearTimeout(this.timerId);
      this.timerId = setTimeout(() => this.timerRest(), 10000);
    },
    timerRest() {
      this.details = [];
      this.user = '';
      this.barcode = '';
      this.goWork()
    },
    async goWork(){
      this.gowork = await this.$axios.$get('http://192.168.0.75:8000/task')
      // .then(response => this.gowork = response.data)
      // let response = await fetch('http://192.168.0.75:8000/task');
      // this.gowork = await response.json()
    },
  },
}
</script>