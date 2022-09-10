<template>
  <div>
    <v-card color='grey' v-for="user in users.no_job" :key="user">
      <v-card-text>
        <h1>Наряд {{user.detail}} Не готов к покраске</h1>
      </v-card-text>
    </v-card>
    <v-card color='blue' v-for="user in users.in_job" :key="user">
      <v-card-text>
        <h1>Наряд {{user.detail}} Не в работе</h1>
      </v-card-text>
    </v-card>
    <v-btn block x-large v-if="users.in_job.length" color="success" @click="inJob()">В работу</v-btn>
    <v-card color='yellow' v-for="user in users.from_job" :key="user">
      <v-card-text>
        <h1>Наряд {{user.detail}} В работе</h1>
      </v-card-text>
    </v-card>
    <v-btn block x-large v-if="users.from_job.length" color="success" @click="outJob()">Завершить</v-btn>
    <v-dialog
      v-model="dialog"
      hide-overlay
      persistent
      width="300"
    >
      <v-card
        color="primary"
        dark
      >
        <v-card-text>
          Идет загрузка
          <v-progress-linear 
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="dialog1"
      hide-overlay
      persistent
      width="300"
    >
      <v-card
        color="yellow"
      >
        <v-card-title primary-title>
          ЗАГРУЗИТЕ ДАННЫЕ
        </v-card-title>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  layout: 'empty',
  data(){
    return {
      barcode:'',
      dialog: false,
      dialog1: true,
      timeout: null,
      codes:[],
      users:{in_job:[],from_job:[],no_job:[]},
      timeId: null,
      res:''
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
      const THRESHOLD = 50;
      this.timeout = setTimeout(() => { this.resetBarcode(); }, THRESHOLD);
      const key = String.fromCharCode(event.which);
      if (key && key != '\r' && key != '\u0010') this.barcode += key;
      const isEnter = event.key === 'Enter';
      if (!isEnter) return;
      this.dialog1 = false;
      this.dialog = true;
      this.paintPost();
      this.resetBarcode();
    },
    async paintPost() {
      this.codes.push(this.barcode);
      await clearTimeout(this.timerId);
      this.timerId = await setTimeout(() => this.timerRest(), 1000);
    },
    async timerRest(){
      this.users = await this.$axios.$get(this.$store.state.db.host+'paint/'+this.codes);
      this.dialog = false;
    },
    resetBarcode() {
      this.barcode = '';
    },
    async inJob() {
      this.res = await this.$axios.$post(this.$store.state.db.host+'inpaint',{in_job: this.users.in_job});
      this.users['in_job'] = [];
      if (!this.users.in_job.length && !this.users.from_job.length) this.dialog1 = true
    },
    async outJob() {
      this.res = await this.$axios.$post(this.$store.state.db.host+'outpaint',{in_job: this.users.from_job});
      this.users['from_job'] = [];
      if (!this.users.in_job.length && !this.users.from_job.length) this.dialog1 = true
    },
  },
}
</script>