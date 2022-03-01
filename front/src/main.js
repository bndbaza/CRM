import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import dateFilter from '@/filters/date'

Vue.config.productionTip = false

Vue.filter('date', dateFilter)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
