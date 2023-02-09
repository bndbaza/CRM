<template>
  <v-container>
    <v-row>
      <v-col cols="1">
        <v-btn block class="ma-1" small light color="orange" v-for="faza in fazas" :key="faza" @click="Metall(faza[0])">Фаза {{faza[0]}}</v-btn>
      </v-col>
      <v-col>
        <h2 v-if="fz != 0">Заказ {{$route.params.id}} Фаза {{fz}}</h2>
        <v-simple-table  v-if="fz != 0" dense>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">
                  Профиль
                </th>
                <th class="text-left">
                  Размер
                </th>
                <th class="text-left">
                  Марка
                </th>
                <th class="text-left">
                  Вес (кг)
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="metall in metalls"
                :key="metall"
              >
                <td>{{ metall.profile }}</td>
                <td>{{ metall.size }}</td>
                <td>{{ metall.mark }}</td>
                <td>{{ metall.weight }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      fz: 0,
      fazas: [],
      metalls: [],
    }
  },
  mounted(){
    this.Faza()
  },
  methods:{
    async Faza(){
      this.fazas = await this.$axios.$get(this.$store.state.db.host+'fazas/'+this.$route.params.id)
    },
    async Metall(faza) {
      this.fz = faza
      this.metalls = await this.$axios.$get(this.$store.state.db.host+'metall/'+this.$route.params.id+'/'+faza)
    }
  }
}
</script>
