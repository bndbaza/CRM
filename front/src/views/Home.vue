<template>
  <div>
    <v-container>
    <v-row justify="space-around">
      <v-col cols="9">
        <v-col cols="12" v-for="code in barcodes" :key="code">
          <v-card color="blue">
            <v-card-text>
              <h1>{{code}}</h1>
            </v-card-text>
          </v-card>
        </v-col>
      </v-col>
      <v-col cols="3">
        <v-col cols="12" v-for="user in users" :key="user">
          <v-card color="green">
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
      barcodes: [],
      users: [],
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
        this.getDetail(this.barcode);
      }else{
        this.processBarcode(this.barcode)
      }
      this.resetBarcode();
    },
    processBarcode(barcode) {
      this.barcodes = [...this.barcodes, barcode];
    },
    resetBarcode() {
      this.barcode = '';
    },
    getDetail(id) {
      axios.get('http://192.168.0.75:8000/worker/'+id)
      .then(response => this.users = [...this.users,response.data])
    }
  },
}
</script>