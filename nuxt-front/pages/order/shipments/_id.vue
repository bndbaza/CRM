<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="10">
          <h1 class="text-center">Заказ {{$route.params.id}}</h1>
        </v-col>
        <v-col>
          <v-btn color="success" @click="dialog4 = true">Новая машина</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <h2 class="text-center">Машины</h2>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Машина
                  </th>
                  <th class="text-left">
                    Дата отправки
                  </th>
                  <th class="text-left">
                    Марка машины
                  </th>
                  <th class="text-left">
                    Гос. номер
                  </th>
                  <th class="text-left">
                    Водитель
                  </th>
                  <th class="text-left">
                    Готовность
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="car in cars"
                  :key="car.id"
                >
                  <td>{{car.number}}</td>
                  <td v-if="car.date">{{car.date | date}}</td>
                  <td v-if="!car.date"></td>
                  <td>{{car.car}}</td>
                  <td>{{car.number_car}}</td>
                  <td>{{car.driver}}</td>
                  <td v-if="!car.date"><v-btn color="success" @click="ship = car,dialog5 = true">Закончить</v-btn></td>
                  <td v-if="car.date"><v-btn color="info" @click="DownloadShip(car)">Отправлен</v-btn></td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <h2 class="text-center">Необработанные пачки</h2>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Пакет
                  </th>
                  <th class="text-left">
                    Дата упаковки
                  </th>
                  <th class="text-left">
                    Размер
                  </th>
                  <th class="text-left">
                    Упаковка
                  </th>
                  <th class="text-left">
                    Готовность
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="pack in packed"
                  :key="pack.id"
                >
                  <td v-if="!pack.ready"><v-btn color="black" icon text @click="structurePackage(pack.number)">{{ pack.number }}</v-btn></td>
                  <td v-if="!pack.ready">{{ pack.date | date }}</td>
                  <td v-if="!pack.ready">{{ pack.size }}</td>
                  <td v-if="!pack.ready">{{ pack.pack }}</td>
                  <td v-if="!pack.ready">
                    <v-btn color="success" icon @click="dialog = true, openDialog(pack)">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn color="red" @click="dialog2 = true, openDialog(pack)" icon><v-icon>mdi-close</v-icon></v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
        <v-col>
          <h2 class="text-center">Готовые пачки</h2>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Пакет
                  </th>
                  <th class="text-left">
                    Дата упаковки
                  </th>
                  <th class="text-left">
                    Размер
                  </th>
                  <th class="text-left">
                    Упаковка
                  </th>
                  <th class="text-left">
                    Готовность
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="pack in packed"
                  :key="pack.id"
                >
                  <!-- <td v-if="pack.ready">{{ pack.number }}</td> -->
                  <td v-if="pack.ready"><v-btn color="black" icon text @click="structurePackage(pack.number)">{{ pack.number }}</v-btn></td>
                  <td v-if="pack.ready">{{ pack.date | date }}</td>
                  <td v-if="pack.ready">{{ pack.size }}</td>
                  <td v-if="pack.ready">{{ pack.pack }}</td>
                  <td v-if="pack.ready">
                    <v-btn color="info" @click="Download(pack)" icon><v-icon>mdi-download</v-icon></v-btn>
                    <v-btn color="red" @click="dialog2 = true, openDialog(pack)" icon><v-icon>mdi-close</v-icon></v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
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
        <v-card-title primary-title>
          Изменение
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="Длина"
            v-model="dict.length"
          ></v-text-field>
          <v-text-field
            label="Ширина"
            v-model="dict.width"
          ></v-text-field>
          <v-text-field
            label="Высота"
            v-model="dict.height"
          ></v-text-field>
          <v-select
            :items="items"
            label="Упаковка"
            v-model="dict.package"
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="success" @click="editPack()">Сохранить</v-btn>
          <v-btn color="red" dark @click="cancelPack()">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="dialog2"
      scrollable
      persistent :overlay="false"
      max-width="500px"
      transition="dialog-transition"
    >
      <v-card>
        <v-card-title primary-title>
          Удаление пачки
        </v-card-title>
        <v-card-text>
          Вы уверены что хотите удалить пачку № {{pack.number}}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" dark @click="delete_pack()">Удалить</v-btn>
          <v-btn color="success" @click="dialog2 = false, pack = {}">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="dialog3"
      scrollable
      persistent :overlay="false"
      max-width="500px"
      transition="dialog-transition"
    >
      <v-card>
        <v-card-title primary-title>
          Состав пачки
        </v-card-title>
        <v-card-text>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Наряд
                  </th>
                  <th class="text-left">
                    Марка
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="structure in structures"
                  :key="structure.id"
                >
                  <td>{{ structure.detail }}</td>
                  <td>{{ structure.point.assembly.assembly }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="success" @click="dialog3 = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="dialog4"
      scrollable
      persistent :overlay="false"
      max-width="500px"
      transition="dialog-transition"
    >
      <v-card>
        <v-card-title primary-title>
          Машина
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="Марка и модель"
            v-model="car.car"
          ></v-text-field>
          <v-text-field
            label="Гос. Номер"
            v-model="car.number_car"
          ></v-text-field>
          <v-text-field
            label="Водитель"
            v-model="car.driver"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="success" @click="postCar()">OK</v-btn>
          <v-btn color="error" @click="dialog4 = false">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="dialog5"
      scrollable
      persistent :overlay="false"
      max-width="500px"
      transition="dialog-transition"
    >
      <v-card>
        <v-card-title primary-title>
          Состав машины
        </v-card-title>
        <v-card-text>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Пакет
                  </th>
                  <th class="text-left">
                    Размер
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="pak in ship.packeds"
                  :key="pak.id"
                >
                  <td>{{ pak.number }}</td>
                  <td>{{ pak.size }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="success" @click="closeShip()">OK</v-btn>
          <v-btn color="error" @click="dialog5 = false">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="loader"
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
  </div>
</template>


<script>
import axios from 'axios'
export default {
  data() {
    return {
      packed: [],
      pack: {},
      dialog: false,
      dialog2: false,
      dialog3: false,
      dialog4: false,
      dialog5: false,
      loader: false,
      structures: [],
      car: {},
      cars: [],
      ship: {},
      dict: {
        length:'',
        width:'',
        height:'',
        package:''
      },
      items:[
        'Пакет',
        'Ящик'
      ],
    }
  },
  mounted() {
    this.getPackage();
    this.getCars();
  },
  methods: {
    async getPackage() {
      this.packed = await this.$axios.$get(this.$store.state.db.host+'package_get/'+this.$route.params.id);
    },
    async structurePackage(id) {
      this.structures = await this.$axios.$get(this.$store.state.db.host+'package_structure/'+id);
      this.dialog3 = true;
    },
    openDialog(pack) {
      this.pack = pack
    },
    editPack() {
      this.pack.size = this.dict.length+'x'+this.dict.width+'x'+this.dict.height;
      this.pack.pack = this.dict.package;
      this.postPackage();
      this.dict = {length:'',width:'',height:'',package:''};
      this.pack = '';
      this.dialog = false;
      this.packed = []
    },
    cancelPack() {
      this.dict = {length:'',width:'',height:'',package:''};
      this.pack = {};
      this.dialog = false;
    },
    async delete_pack(){
      this.packed = await this.$axios.$get(this.$store.state.db.host+'package_delete/'+this.pack.id+'/'+this.$route.params.id);
      this.dialog2 = false
    },
    async postPackage() {
      this.packed = await this.$axios.$post(this.$store.state.db.host+'package_post',{pack: this.pack})
    },
    async postCar() {
      this.car.case = this.$route.params.id
      this.cars = await this.$axios.$post(this.$store.state.db.host+'post_car',{car: this.car});
      this.dialog4 = false
    },
    async getCars() {
      this.cars = await this.$axios.$get(this.$store.state.db.host+'get_cars/'+this.$route.params.id)
    },
    async getShip(car) {
      // this.ship = await this.$axios.$get(this.$store.state.db.host+'get_ship/'+car);
      this.dialog5 = true
    },
    async closeShip() {
      this.dialog5 = false
      this.loader = true
      this.cars = await this.$axios.$get(this.$store.state.db.host+'close_ship/'+this.ship.id+','+this.$route.params.id);
      this.loader = false
    },
    Download(pack) {
      axios({
        url: this.$store.state.db.host+'file/' + pack.id,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', pack.number +'.'+ (pack.ready).split('.').pop());
        document.body.appendChild(link);
        link.click();
      });
    },
    DownloadShip(car) {
      axios({
        url: this.$store.state.db.host+'file_ship/' + car.id,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', car.number +'.'+ (car.ready).split('.').pop());
        document.body.appendChild(link);
        link.click();
      });
    },
  },
}
</script>