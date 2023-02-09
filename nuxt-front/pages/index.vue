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
            Выполнение
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
          <td><nuxt-link :to="'/order/'+order.cas"><h2 light class="orange--text">{{ order.cas }}</h2></nuxt-link></td>
          <td>{{ order.name }}</td>
          <!-- <td><v-chip :color="order.color"></v-chip></td> -->
          <td>
            <v-progress-circular
              v-model="order.finish"
              v-if="order.status != 'Готов'"
              :width="5.5"
              :color="order.color"
              size="35"
            >{{order.finish}}</v-progress-circular>
          </td>
          <td>{{ order.status }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
  <v-btn
    light
    color="orange"
    absolute
    top
    fab
    right
    small
    v-if="access()"
    class="mr-1 mt-10"
    @click="dialog=true"
  >
    <v-icon>mdi-plus</v-icon>
  </v-btn>
  <v-dialog
    v-model="dialog"
    scrollable
    dark
    persistent :overlay="false"
    max-width="800px"
    transition="dialog-transition"
  >
    <v-card>
      <v-card-title>Заказ</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col>
              <v-text-field
                v-model="order.cas"
                label="Номер заказа"
              ></v-text-field>
              <v-text-field
                v-model="order.name"
                label="Наименование"
              ></v-text-field>
              <v-text-field
                v-model="order.weight"
                label="Вес по договору"
                :disabled="order.inside"
              ></v-text-field>
              <v-checkbox
                color="teal"
                label="Внутренний заказ"
                v-model="order.inside"
                @click="inside()"
              ></v-checkbox>
            </v-col>
            <v-col>
              <v-text-field
                v-model="order.customer"
                label="Заказчик"
                :disabled="order.inside"
              ></v-text-field>
              <v-text-field
                v-model="order.contract"
                label="Договор"
                :disabled="order.inside"
              ></v-text-field>
              <v-text-field
                v-model="order.consignee"
                label="Грузополучатель"
                :disabled="order.inside"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn light color="teal" :disabled="test()" @click="add()">Создать</v-btn>
        <v-btn light color="red" @click="dialog=false">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog
    v-model="loading"
    scrollable
    persistent :overlay="false"
    max-width="150px"
    transition="dialog-transition"
  >
    <v-progress-linear
      indeterminate
      color="orange"
    ></v-progress-linear>
  </v-dialog>
  </v-container>
</template>

<script>
export default {
  data(){
    return{
      orders: [],
      dialog: false,
      order: {},
      loading: false,
    }
  },
  async mounted(){
    this.orders = await this.$axios.$get(this.$store.state.db.host+'index')
  },
  methods: {
    inside() {
      if (this.order.inside) {
        this.order.customer = 'ООО Байкалстальстрой'
        this.order.contract = 'ООО Байкалстальстрой'
        this.order.consignee = 'ООО Байкалстальстрой'
        this.order.weight = '1'
      }else{
        this.order.customer = ''
        this.order.contract = ''
        this.order.consignee = ''
        this.order.weight = ''
      }
    },
    test() {
      if (
        this.order.customer &&
        this.order.contract &&
        this.order.consignee &&
        this.order.cas &&
        this.order.name &&
        this.order.weight
      ) {
        return false
      }else{
        return true
      } 
    },
    async add() {
      this.loading = true
      this.dialog = false
      this.orders = await this.$axios.$post(this.$store.state.db.host+'add_order',this.order)
      this.order = {}
      this.loading = false
    },
    access() {
      let users = [57]
      try {
        return users.includes(this.$store.state.db.user.id)
      }
      catch {
        return false
      }
    }
  }
}
</script>
