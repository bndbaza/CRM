<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="10">

          <v-card
            class="mx-auto"
            v-if="run.length != 0"
            color="indigo"
          >
            <v-card-title>
              Приход
            </v-card-title>
            <v-card-text>
              <v-data-table
                dense
                :headers="headers"
                :items="run"
                :items-per-page="100"
                hide-default-footer
              ></v-data-table>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn light color="teal" @click.stop="dialog=true">OK</v-btn>
              <v-btn light color="red" @click="run = []">Отмена</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col v-if="access()">
          <v-card
            elevation="2"
            class="mx-auto"
          >
            <v-card-title>
              Добавить
            </v-card-title>
            <v-card-text>
              <v-select
                v-model='steel.full_name'
                :items='catalog'
                item-text='full_name'
                item-value='full_name'
                label='Наименование'
              ></v-select>
              <v-select
                v-model='steel.size'
                v-if="steel.full_name != ''"
                :items="Test('full_name')"
                item-text='size'
                item-value='size'
                label='Размер'
              ></v-select>
              <v-select
                v-model='steel.mark'
                v-if="steel.size != ''"
                :items="Test('full_name','size')"
                item-text='mark'
                item-value='mark'
                label='Марка стали'
              ></v-select>
              <v-select
                v-model='steel.id'
                v-if="steel.mark != ''"
                :items="Test('full_name','size','mark')"
                item-text='gost'
                item-value='id'
                label='ГОСТ'
                @change="Lenght()"
              ></v-select>
              <v-text-field
                label="Ширина"
                v-model="steel.width"
                v-if="id.width"
              ></v-text-field>
              <v-text-field
                label="Длина"
                v-model="steel.lenght"
                v-if="steel.width != ''"
              ></v-text-field>
              <v-text-field
                label="Наименование стали"
                v-model="steel.name_steel"
                v-if="steel.lenght != ''"
              ></v-text-field>
              <v-text-field
                label="Количество"
                v-model="steel.count"
                v-if="steel.name_steel != ''"
              ></v-text-field>
              <v-text-field
                label="Вес одной штуки"
                v-model="steel.weight"
                v-if="steel.count != ''"
              ></v-text-field>
              <v-text-field
                label="Цена"
                v-model="steel.price"
                v-if="steel.weight"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn v-if="steel.price" light color="teal" @click="Run()">Добавить</v-btn>
              <v-btn light color="red" @click="Cancel()">Отмена</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-dialog
      v-model="dialog"
      scrollable
      persistent :overlay="false"
      max-width="500px"
      transition="dialog-transition"
    >
      <v-card>
        <v-container>
        <v-card-title>
          Общая по приходу
        </v-card-title>
        <v-card-text>
          <v-menu
          ref="menu1"
          v-model="menu1"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="receipt_date"
              label="Дата поставки"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="date"
            no-title
            @input="menu1 = false,Replace(date)"
          ></v-date-picker>
        </v-menu>
          <!-- <v-date-picker -->
            <!-- v-model="date" -->
            <!-- :first-day-of-week="1" -->
            <!-- locale="ru-ru" -->
            <!-- no-title -->
          <!-- ></v-date-picker> -->
        <v-row v-if="!plus">
        <v-col cols="10">
          <v-select
            dense
            v-model="vendor"
            label="Поставщик"
            :items="items"
          ></v-select>
        </v-col>
        <v-col>
          <v-btn color="green" @click="plus=true" icon><v-icon>mdi-plus</v-icon></v-btn>
        </v-col>
        </v-row>
        <v-row v-else>
        <v-col>
          <v-text-field
            dense
            label="Поставщик"
            v-model="vendor"
          ></v-text-field>
        </v-col>
        </v-row>
        </v-card-text>
        <v-card-actions>
          <v-btn :disabled="vendor == '' || date == ''" color="blue" @click="StoreAdd()">ОК</v-btn>
          <v-btn color="red" @click="plus=false,provider=''">Назад</v-btn>
        </v-card-actions>
        </v-container>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {text: 'Наименование',value:'full_name'},
        {text: 'Размер',value:'size'},
        {text: 'Ширина',value:'width'},
        {text: 'Длина',value:'lenght'},
        {text: 'Наименование стали',value:'name_steel'},
        {text: 'Количество',value:'count'},
        {text: 'Марка стали',value:'mark'},
      ],
      run: [],
      steel: {full_name:'',size:'',id:'',width:'',lenght:'',name_steel:'',count:'',mark:''},
      id: {},
      catalog: [],
      start: [],
      all: [],
      dialog: false,
      receipt_date: '',
      date: '',
      vendor: '',
      items: '',
      plus: false,
      menu1: false,
    }
  },
  mounted(){
    this.Start()
  },
  methods: {
    Test(full_name,size='',mark='') {
      let catalog = []
      if (mark != '') {
        catalog = this.catalog.filter(cat => cat[mark] == this.steel[mark] && cat[size] == this.steel[size] && cat[full_name] == this.steel[full_name])
      }else if (size != '') {
        catalog = this.catalog.filter(cat => cat[size] == this.steel[size] && cat[full_name] == this.steel[full_name])
      }else{
        catalog = this.catalog.filter(cat => cat[full_name] == this.steel[full_name]);
      }
      return catalog
    },
    async Start() {
      let store
      store = await this.$axios.$get(this.$store.state.db.host+'store')
      this.catalog = store.catalog
      this.items = store.vendors
    },
    Lenght() {
      for (const i of this.catalog) {
        if (i.id == this.steel.id) {
          this.id = i
          if (i.width) {
            this.steel.width = ''
          } else {
            this.steel.width = '-'
          }
          this.steel.lenght = ''
          this.steel.count = ''
          this.steel.name_steel = ''
          this.steel.gost = ''
          break
        }
      }
    },
    Run() {
      this.steel.gost = this.id.gost
      this.run.push(this.steel)
      this.steel = {full_name:'',size:'',id:'',width:'',lenght:'',name_steel:'',count:'',gost:'',mark:''}
      this.id = {}
    },
    Cancel() {
      this.steel = {full_name:'',size:'',id:'',width:'',lenght:'',name_steel:'',count:'',gost:'',mark:''}
      this.id = {}
    },
    Replace(text) {
      text = new Date(text.split('-'))
      var options = {
      year: 'numeric',
      month: 'numeric',
      day: 'numeric',
      };
      text = text.toLocaleString("ru",options)
      this.receipt_date = text
      return
    },
    async StoreAdd() {
      let store
      store = await this.$axios.$post(this.$store.state.db.host+'store_add',{run: this.run, date: this.date, vendor: this.vendor})
      this.dialog = false
      this.run = []
      this.date = ''
      this.vendor = ''
      this.receipt_date = ''
      this.plus = false
      this.Start()
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
