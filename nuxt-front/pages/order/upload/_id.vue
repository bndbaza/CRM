<template>
  <div>
  <v-container>
    <v-row>
      <v-col>
        <v-btn color="orange" @click.stop="tekla=false,dlist=true,file=''">Диспетчерский лист</v-btn>
        <v-btn color="blue" @click="tekla=true,dlist=false">Tekla</v-btn>
      </v-col>
    </v-row>
    <v-row v-if="tekla">
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
    <v-row v-if="dlist">
      <v-col>
        <v-card color="grey" class="mb-2" v-for="m in marks" :key="m">
          <v-card-title>
            <v-spacer></v-spacer>
            <p>Марка: {{m.mark}}</p>
            <v-spacer></v-spacer>
            <p>Чертеж: {{m.draw}}</p>
            <v-spacer></v-spacer>
            <p>Наименование: {{m.name}}</p>
            <v-spacer></v-spacer>
            <p>Количество: {{m.count}}</p>
            <v-spacer></v-spacer>
            <p>Сварка: {{m.weld}}</p>
            <!-- <p>Марка: {{m.mark}} | Чертеж: {{m.draw}} | Наименование: {{m.name}} | Количество: {{m.count}} | Сварка: {{m.weld}}</p> -->
            <v-spacer></v-spacer>
            <v-btn color="green" @click="edit(m)" icon><v-icon>mdi-pencil</v-icon></v-btn>
            <v-btn color="red" @click="remove(m)" icon><v-icon>mdi-close</v-icon></v-btn>
          </v-card-title>
          <v-card-text>
            <v-simple-table dense>
              <template v-slot:default>
                <thead>
                  <tr>
                    <th class="text-center">
                      Номер детали
                    </th>
                    <th class="text-center">
                      Профиль
                    </th>
                    <th class="text-left">
                      Размер
                    </th>
                    <th class="text-left">
                      Длина
                    </th>
                    <th class="text-left">
                      Ширина
                    </th>
                    <th class="text-left">
                      Марка стали
                    </th>
                    <th class="text-left">
                      Количество
                    </th>
                    <th class="text-left">
                      Вес
                    </th>
                    <th class="text-left">
                      
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="item in m.details"
                    :key="item.number"
                  >
                    <td class="text-center">{{ item.number }}</td>
                    <td>{{ item.steel.full_name }}</td>
                    <td>{{ item.steel.size }}</td>
                    <td>{{ item.lenght }}</td>
                    <td>{{ item.width }}</td>
                    <td>{{ item.steel.mark }}</td>
                    <td>{{ item.count }}</td>
                    <td v-if="item.steel.width">{{ (item.lenght/1000) * (item.width/1000) * item.steel.weight | number }}</td>
                    <td v-if="!item.steel.width">{{ (item.lenght/1000) * item.steel.weight | number }}</td>
                    <td>
                      <v-btn color="green" icon @click="edit(m,item)"><v-icon>mdi-pencil</v-icon></v-btn>
                      <v-btn color="red" icon @click="remove(m,item)"><v-icon>mdi-close</v-icon></v-btn>
                    </td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-btn v-if="dlist" :disabled="marks.length == 0" color="green" @click="Manual()">Загрузить</v-btn>
    <v-btn v-if="dlist" color="orange" @click.stop="dialog=true">Создать марку</v-btn>
  </v-container>
  <v-dialog
    v-model="dialog"
    scrollable
    persistent :overlay="false"
    max-width="500px"
    transition="dialog-transition"
  >
    <v-card>
      <v-card-title>Марка</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col>
              <v-text-field
                v-model=mark.mark
                label="Наименование Марки"
              ></v-text-field>
              <v-text-field
                v-model=mark.draw
                label="Чертеж"
              ></v-text-field>
              <v-text-field
                v-model=mark.name
                label="Наименование конструкции"
              ></v-text-field>
              <v-text-field
                v-model=mark.weld
                label="Сварка"
                hint="Пример: 6=3520,8=2360"
              ></v-text-field>
              <v-text-field
                v-model=mark.count
                label="Количество"
              ></v-text-field>
              <v-checkbox
                v-model="mark.paint"
                label='Покраска'
              ></v-checkbox>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue" :disabled="!mark.mark || !mark.draw || !mark.name || !mark.count || mark.details.length == 0" @click="addMark()">OK</v-btn>
        <v-btn :disabled="!mark.mark || !mark.draw || !mark.name || !mark.count" color="green" @click="dialog2=true,dialog=false">Добавить детали</v-btn>
        <v-btn color="red" @click="dialog=false,mark={details:[]}">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog
    v-model="dialog2"
    scrollable
    persistent :overlay="false"
    max-width="800px"
    transition="dialog-transition"
  >
    <v-card>
      <v-card-title>
        Деталь
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col>
              <v-text-field
                v-model='detail.number'
                label="Номер детали в чертеже"
              ></v-text-field>
              <v-select
                v-model='steel.full_name'
                :items='catalog'
                item-text='full_name'
                item-value='full_name'
                label='Профиль'
                @click="steel={},detail.manipulation = []"
              ></v-select>
              <v-select
                v-model='steel.size'
                :disabled='!steel.full_name'
                :items="Test('full_name')"
                item-text='size'
                item-value='size'
                label='Размер'
                @click="steel={full_name:steel.full_name}"
              ></v-select>
              <v-select
                v-model='steel.mark'
                :disabled='!steel.size'
                :items="Test('full_name','size')"
                item-text='mark'
                item-value='mark'
                label='Марка металла'
                @click="steel={full_name:steel.full_name,size:steel.size}"
              ></v-select>
              <v-select
                v-model='detail.id'
                :disabled='!steel.mark'
                :items="Test('full_name','size','mark')"
                item-text='gost'
                item-value='id'
                label='ГОСТ'
                @change="Steel()"
              ></v-select>
              <v-text-field
                v-model='detail.count'
                label="Количество в марке"
              ></v-text-field>
              <v-text-field
                v-model='detail.width'
                v-if="steel.width"
                label="Ширина"
              ></v-text-field>
              <v-text-field
                v-model='detail.lenght'
                label="Длина"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model='detail.hole'
                label="Отверстия"
                hint="количество=диаметер в одной детали"
              ></v-text-field>
              <v-checkbox
                v-model="detail.manipulation"
                value='turning'
                label='Токарка'
                v-if="steel.id"
              ></v-checkbox>
              <v-checkbox
                v-model="detail.manipulation"
                value='bevel'
                label='Скос'
                v-if="steel.id && !steel.width"
              ></v-checkbox>
              <v-checkbox
                v-model="detail.manipulation"
                value='notch'
                label='Вырез'
                v-if="steel.id && !steel.width"
              ></v-checkbox>
              <v-checkbox
                v-model="detail.manipulation"
                value='chamfer'
                label='Фаска'
                v-if="steel.id"
              ></v-checkbox>
              <v-checkbox
                v-model="detail.manipulation"
                value='milling'
                label='Фрезеровка'
                v-if="steel.id"
              ></v-checkbox>
              <v-checkbox
                v-model="detail.manipulation"
                value='bend'
                label='Гибка'
                v-if="steel.id"
              ></v-checkbox>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="!detail.number || !steel.id || !detail.lenght || !detail.count" color="green" @click="addDetail()">Добавить</v-btn>
        <v-btn color="red" @click="dialog2=false,dialog=true,steel={},detail={manipulation:[]}">Назад</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog
    v-model="dialog3"
    scrollable
    persistent :overlay="false"
    max-width="800px"
    transition="dialog-transition"
  >
    <v-card>
      <v-card-title>
        Файл загружен
      </v-card-title>
      <v-card-text>
        Text
      </v-card-text>
      <v-card-actions>
        <v-btn disabled color="blue">OK</v-btn>
        <v-btn color="red" @click="dialog3=false">Назад</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      file:'',
      mark: {details:[]},
      marks: [],
      detail: {manipulation:[]},
      result:'',
      load: false,
      correct: false,
      tekla: false,
      dlist: false,
      dialog: false,
      dialog2: false,
      dialog3: false,
      catalog: [],
      steel: {},
      back:'',
      test: '',
      editIndex: [-1,-1],
      editItem: {}
    }
  },
  async mounted(){
    let marks = {}
    this.catalog = await this.$axios.$get(this.$store.state.db.host+'store')
    marks = await this.$axios.$get(this.$store.state.db.host+'manual_read/'+this.$route.params.id)
    this.marks = marks.marks
  },
  methods: {
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
        if (this.result.error == 0) {
          this.dialog3 = true
        }
      })
    },
    Test(full_name,size='',mark='') {
      let catalog = []
      if (mark != '') {
        catalog = this.catalog.filter(cat => cat['mark'] == this.steel['mark'] && cat['size'] == this.steel['size'] && cat['full_name'] == this.steel['full_name'])
      }else if (size != '') {
        catalog = this.catalog.filter(cat => cat['size'] == this.steel['size'] && cat['full_name'] == this.steel['full_name'])
      }else{
        catalog = this.catalog.filter(cat => cat['full_name'] == this.steel['full_name']);
      }
      return catalog
    },
    Steel() {
      this.steel = this.catalog.filter(cat => cat.id == this.detail.id)[0]
    },
    async Manual() {
      this.back = await this.$axios.$post(this.$store.state.db.host+'manual_write',{marks: this.marks,case: this.$route.params.id}) 
      this.marks = []
    },
    async ManualSave() {
      this.back = await this.$axios.$post(this.$store.state.db.host+'manual_save',{marks: this.marks,case: this.$route.params.id}) 
    },
    remove(mark,detail=false) {
      if (detail) {
        this.editIndex[0] = this.marks.indexOf(mark)
        this.editIndex[1] = this.marks[this.editIndex[0]].details.indexOf(detail)
        this.marks[this.editIndex[0]].details.splice(this.editIndex[1],1)
      }else{
        this.editIndex[0] = this.marks.indexOf(mark)
        this.marks.splice(this.editIndex[0],1)
      }
      this.ManualSave()
    },
    edit(mark,detail=false) {
      if (detail) {
        this.editIndex[0] = this.marks.indexOf(mark)
        this.editIndex[1] = this.marks[this.editIndex[0]].details.indexOf(detail)
        this.detail = {
          number: detail.number,
          count: detail.count,
          lenght: detail.lenght,
          width: detail.width,
          hole: detail.hole,
          manipulation: detail.manipulation,
        }
        this.steel = {
          full_name:detail.steel.full_name,
          size:detail.steel.size,
          mark:detail.steel.mark,
          full_name:detail.steel.full_name,
        }
        this.dialog2 = true
      }else{
        this.editIndex[0] = this.marks.indexOf(mark)
        this.mark = mark
        this.dialog = true
      }
    },
    addDetail() {
      this.detail.steel = this.steel
      if (this.editIndex[1] == -1) {
        this.mark.details.push(this.detail)
      }else{
        this.marks[this.editIndex[0]].details[this.editIndex[1]] = this.detail
        this.dialog2 = false
        this.editIndex = [-1,-1]
        this.ManualSave()
      }
      this.detail = {manipulation:[]}
      this.steel = {}
    },
    addMark() {
      if (this.editIndex[0] == -1) {
        this.marks.push(this.mark)
      }else{
        this.marks[this.editIndex[0]] = this.mark
      }
      this.mark = {details:[]}
      this.dialog = false
      this.editIndex = [-1,-1]
      this.ManualSave()

    },
  }
}
</script>
