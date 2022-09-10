export const state = () => ({
  host: 'http://192.168.0.75:8000/',
  search: '',
  user: '1',
})


export const mutations = {
  mark(state,text){
    state.search = text
  }
}

export const getters = {
  getHost: state => state.host
}