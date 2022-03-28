import Vue from 'vue'

Vue.filter('date', (value, format= 'date') => {
  const options ={day: 'numeric',month:'numeric',year:'numeric',hour:'numeric',minute:'numeric',second:'numeric'}
  return new Intl.DateTimeFormat('ru-RU', options).format(new Date(value))
})

// export default function dateFilter(value, format= 'date') {
//   const options ={day: 'numeric',month:'numeric',year:'numeric',hour:'numeric',minute:'numeric',second:'numeric'}
//   return new Intl.DateTimeFormat('ru-RU', options).format(new Date(value))
// }