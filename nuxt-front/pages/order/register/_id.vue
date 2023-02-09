<template>
  <v-container>
    <h1 class="text-center">Заказ {{$route.params.id}}</h1>
    <!-- <p>{{marks}}</p> -->

    <v-simple-table dense>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">
              Марка ({{all.drawing}})
            </th>
            <th class="text-left">
              Количество ({{all.count}})
            </th>
            <th class="text-left">
              Вес шт.
            </th>
            <th class="text-left">
              Вес общий
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="mark in marks.point"
            :key="mark"
          >
            <td v-if="mark.assembly == $store.state.db.search | $store.state.db.search == ''"><nuxt-link class="orange--text" :to="'stage/'+$route.params.id+','+mark.assembly">{{ mark.assembly }}</nuxt-link></td>
            <td v-if="mark.assembly == $store.state.db.search | $store.state.db.search == ''">{{ mark.count }}</td>
            <td v-if="mark.assembly == $store.state.db.search | $store.state.db.search == ''">{{ mark.weight }}</td>
            <td v-if="mark.assembly == $store.state.db.search | $store.state.db.search == ''">{{ mark.weight_all }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      marks:[],
      all:{}
    }
  },
  async mounted() {
    this.marks = await this.$axios.$get(this.$store.state.db.host+'register/'+this.$route.params.id);
    this.all = this.marks.all
  }
}
</script>
