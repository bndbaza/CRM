export const state = () => ({
  host: 'http://192.168.0.75:8000/',
  search: '',
  user: null,
})


export const mutations = {
  mark(state,text){
    state.search = text
  },
  user_get(state,text) {
    state.user = text
  }
}

export const getters = {
  getHost: state => state.host
}
