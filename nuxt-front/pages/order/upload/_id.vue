<template>
  <v-container grid-list-xs>
    <v-row>
      <v-col>
        <v-file-input
          label="Загрузите файл"
          v-model="file"
        ></v-file-input>
        <v-btn color="info" @click="Upload(), load = true" :loading="load" :disabled='load' v-if="file != ''">Загрузить</v-btn>
        <v-checkbox label="Исправление ошибок" v-model="correct" v-if="result != ''"></v-checkbox>
      </v-col>
      <v-col>
        <p>Количество ошибок: {{result['error']}}</p>
        <p v-for="res in result['ASSEMBLY']" :key="res">{{res}}</p>
        <p v-for="res in result['PART']" :key="res">{{res}}</p>
        <p v-for="res in result['others']" :key="res">{{res}}</p>
        <p v-for="res in result['area']" :key="res">{{res}}</p>
        <p v-for="res in result['weight']" :key="res">{{res}}</p>
        <p v-for="res in result['weld']" :key="res">{{res}}</p>
        <p v-for="res in result['bolt']" :key="res">{{res}}</p>
        <p v-for="res in result['nut']" :key="res">{{res}}</p>
        <p v-for="res in result['washer']" :key="res">{{res}}</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      file:'',
      result:'',
      load: false,
      correct: false
    }
  },
  methods: {
    // async Upload() {
    //   let formData = new FormData();
    //   formData.append('file', this.file)
    //   formData.append('order', this.$route.params.id)
    //   this.result = await this.$axios.post(this.$store.state.db.host+'opder',formData,{headers: {'Content-Type': 'multipart/form-data'}})
    // }
    async Upload() {
      let formData = new FormData();
      formData.append('file',this.file)
      formData.append('order', this.$route.params.id)
      formData.append('correct', this.correct)
      await axios.post(this.$store.state.db.host+'order',formData,{headers: {'Content-Type': 'multipart/form-data'}})
      .then(response => {
        this.result = response.data
        this.file=''
        this.load = false
      })
    }
  }
}
</script>