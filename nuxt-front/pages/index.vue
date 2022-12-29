<template>
  <v-container>
    <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">
            Номер заказа
          </th>
          <th class="text-left">
            Наименование
          </th>
          <th class="text-left">
            Цвет
          </th>
          <th class="text-left">
            Статус
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="order in orders"
          :key="order.id"
        >
          <td><nuxt-link :to="'/order/'+order.cas"><h2>{{ order.cas }}</h2></nuxt-link></td>
          <td>{{ order.name }}</td>
          <!-- <td><v-chip :color="order.color"></v-chip></td> -->
          <td>
            <v-progress-circular
              v-model="pr"
              :width="17.5"
              :color="order.color"
              size="35"
            ></v-progress-circular>
          </td>
          <td>{{ order.status }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
  </v-container>
</template>

<script>
export default {
  data(){
    return{
      orders: [],
      pr: 100,
    }
  },
  async mounted(){
    this.orders = await this.$axios.$get(this.$store.state.db.host+'index')
  }
}
</script>
