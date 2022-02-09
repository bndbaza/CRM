<template>
  <div>
    <v-container>
    <v-row justify="space-around">
      <v-col cols="9">
        <v-col cols="12" v-for="detail in details" :key="detail">
          <v-card color="blue">
            <v-card-text>
              <h1>{{detail}}</h1>
            </v-card-text>
          </v-card>
        </v-col>
      </v-col>
      <v-col cols="3">
        <v-col cols="12">
          <v-card color="green" v-if="user != ''">
            <v-card-text>
              <h1>{{user.surname}} {{user.name}} {{user.patronymic}}</h1>
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
        this.processBarcode(this.barcode)
      }else{
        this.getDetail(this.barcode,this.barcodes)
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
      .then(response => this.details = [...this.details, response.data])
    }
  },
}
</script>