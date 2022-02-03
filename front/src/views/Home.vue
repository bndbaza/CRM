<template>
  <div>
    <p v-for="code in barcodes" v-bind:key="code">{{code}}</p>
    <!-- <p v-for="user in users" :key="user">{{user.surname}} {{user.name}} {{user.patronymic}}</p> -->
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
      const isBarcode = this.barcode.length > 0;
      if (!isEnter || !isBarcode) return;
      this.processBarcode(this.barcode);
      this.getDetail(this.barcode)
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