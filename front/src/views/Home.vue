<template>
  <div>
    <v-alert v-if="details.error == 'Список Пуст'" type="info" :value="true">
      <h4>{{details.error}}</h4>
    </v-alert>
    <v-alert v-if="details.error != None && details.error != 'Список Пуст'" type="error" :value="true">
      <h4>{{details.error}}</h4>
    </v-alert>
    <v-container>
      <v-row justify="space-around">
        <v-col cols="9">
          <v-col cols="12" v-for="detail in details.worker" :key="detail">
            <v-card :color=col>
              <v-card-text>
                <h1>Наряд №{{detail.detail}} Время начала {{detail.start | date}}</h1>
              </v-card-text>
            </v-card>
          </v-col>
        </v-col>
        <v-col cols="3">
          <v-col cols="12">
            <v-card color="green" v-if="user != ''">
              <v-card-text>
                <h1>{{user.user.surname}} {{user.user.name}} {{user.user.patronymic}}</h1>
                <h1><br></h1>
                <h1>{{user.oper_rus}}</h1>
              </v-card-text>
            </v-card>
          </v-col>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      barcode: '',
      timeout: null,
      barcodes: '',
      user: '',
      details: [],
      col: "blue",
      timerId: null,
    }
  },
  mounted() {
    window.addEventListener('keydown', this.onGlobalKeyDown);
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
        this.getUser(this.barcode);
        this.processBarcode(this.barcode);
        this.getDetail(this.barcode,this.barcodes);
      }else if (this.barcode[1] == 'A' & this.user != '') {
        this.getDetail(this.barcode,this.barcodes);
      }else{
        this.details = {'error':'Работник не выбран'}
        this.timerId = setTimeout(() => this.timerRest(), 10000);
      }
      this.resetBarcode();
    },
    processBarcode(barcode) {
      this.barcodes = barcode;
    },
    resetBarcode() {
      this.barcode = '';
    },
    getUser(id) {
      axios.get('http://192.168.0.75:8000/worker/'+id)
      .then(response => this.user = response.data)
    },
    getDetail(detail,user) {
      axios.post('http://192.168.0.75:8000/detail',{detail:detail,user: user})
      .then(response => this.details = response.data)
      clearTimeout(this.timerId)
      this.timerId = setTimeout(() => this.timerRest(), 10000);
    },
    timerRest() {
      this.details = [];
      this.user = '';
      this.barcodes = '';
      this.barcode = '';
    }
  },
}
</script>