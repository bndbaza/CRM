import Vue from 'vue'

Vue.filter('date', (value, format= 'datetimesec') => {
  const options ={}
  if (format.includes('date')) {
    options.day = 'numeric'
    options.month ='numeric'
    options.year ='numeric'
  }
  if (format.includes('time')) {
    options.hour ='numeric'
    options.minute ='numeric'
  }
  if (format.includes('sec')) {
    options.second ='numeric'
  }
  return new Intl.DateTimeFormat('ru-RU', options).format(new Date(value))
})


Vue.filter('number', (value, format= 'number') => {
  const options ={maximumFractionDigits: 2}
  return new Intl.NumberFormat('ru-RU',options).format(value)
})

Vue.filter('money', (value, format= 'money') => {
  const options ={style: 'currency', currency: 'RUB'}
  return new Intl.NumberFormat('ru-RU',options).format(value)
})

Vue.filter('norm', (value, format= 'norm') => {
  const options ={maximumFractionDigits: 2}
  let sec = Math.round(60 / 100 * (value - Math.floor(value)) * 100)
  let min = Math.floor(value) - (Math.floor(Math.floor(value) / 60) * 60)
  let hour = Math.floor(Math.floor(value) / 60)
  if (sec < 10) {
    sec = `0${sec.toString()}`
  }
  if (min < 10) {
    min = `0${min.toString()}`
  }
  return `${hour}:${min}:${sec}`
})
