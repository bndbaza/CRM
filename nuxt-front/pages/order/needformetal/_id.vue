<<template>
  <v-container>
    <v-row>
      <v-col cols="10">
        <v-card color="deep-purple">
          <v-card-title>Спецификация</v-card-title>
          <v-card-text v-if="run.length != 0">
            <v-data-table
              dense
              :headers="headers"
              :items="run"
              :items-per-page="100"
              hide-default-footer
            >
              <template v-slot:[`item.delete`]="{ item }">
                <v-btn v-if="item.buy" color="green" icon><v-icon>mdi-check</v-icon></v-btn>
                <v-btn v-else @click="remove(item)" color="red" icon><v-icon>mdi-close</v-icon></v-btn>
              </template>
            </v-data-table>
          </v-card-text>
          <v-card-actions v-if="run.length !=0">
            <v-spacer></v-spacer>
            <v-btn light :disabled="no_change" color="teal" @click="Add()">Применить</v-btn>
            <v-btn light color="red" @click="run=[]">Отмена</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col>
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
                v-if="steel.full_name"
                :items="Test('full_name')"
                item-text='size'
                item-value='size'
                label='Размер'
              ></v-select>
              <v-select
                v-model='steel.mark'
                v-if="steel.size"
                :items="Test('full_name','size')"
                item-text='mark'
                item-value='mark'
                label='Марка стали'
              ></v-select>
              <v-select
                v-model='steel.metal'
                v-if="steel.mark"
                :items="Test('full_name','size','mark')"
                item-text='gost'
                item-value='id'
                label='ГОСТ'
                @change="Lenght()"
              ></v-select>
              <v-text-field
                label="Наименование стали"
                v-model="steel.name_steel"
                v-if="steel.metal"
              ></v-text-field>
              <v-text-field
                v-model='steel.weight'
                v-if="steel.metal"
                label="Вес"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn v-if="steel.weight" light color="teal" @click="Run()">Добавить</v-btn>
              <v-btn light color="red" @click="Cancel()">Отмена</v-btn>
            </v-card-actions>
          </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {text: 'Наименование',value:'full_name'},
        {text: 'Размер',value:'size'},
        {text: 'Марка стали',value:'mark'},
        {text: 'Наименование стали',value:'name_steel'},
        {text: 'Вес',value:'weight'},
        {text: 'Действие',value:'delete'},
      ],
      catalog: [],
      run: [],
      steel: {},
      metal: {},
      no_change: true
    }
  }, 
  mounted(){
    this.Start()
    this.Get_nfm()
  },
  methods: {
    async Start() {
      let store
      store = await this.$axios.$get(this.$store.state.db.host+'store')
      this.catalog = store.catalog
    },
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
    Lenght() {
      for (const i of this.catalog) {
        if (i.metal == this.steel.metal) {
          this.metal = i
          break
        }
      }
    },
    Run() {
      this.steel.gost = this.metal.gost
      this.steel.buy = false
      this.steel.id = 0
      this.run.push(this.steel)
      this.steel = {}
      this.metal = {}
      this.no_change = false
    },
    Cancel() {
      this.steel = {}
      this.metal = {}
    },
    async Add() {
      this.run = await this.$axios.$post(this.$store.state.db.host+'need_for_metal',{run:this.run,case:this.$route.params.id}) 
      this.no_change = true
    },
    async Get_nfm() {
      this.run = await this.$axios.$get(this.$store.state.db.host+'need_for_metal/'+this.$route.params.id) 
    },
    remove(item) {
      this.run.splice(this.run.indexOf(item),1) 
      this.no_change = false
    },
  },
}
</script>
