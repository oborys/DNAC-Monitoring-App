// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import Vuetify from 'vuetify'

Vue.use(Vuetify)

import 'vuetify/dist/vuetify.min.css'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',

  data: {
    user_role: window.role,
    username: window.username
  },

  methods: {
    statusColor: function (status) {
      switch (status) {
        case 'New':
          return '#D32F2F'
        case 'In progress':
          return '#f0900f'
        case 'Close':
          return '#0e47a1'
        case 'Rejected':
          return '#a19315'
        default:
          return 'black'
      }
    },
    statusText: function (status) {
      switch (status) {
        case 'new':
          return 'New'
        case 'in_progress':
          return 'In progress'
        case 'close':
          return 'Solved'
        case 'rejected':
          return 'Rejected'
        default:
          return 'Unknown'
      }
    },
    prettyStatus: function (status) {
      return (status.slice(0, 1).toUpperCase() + status.slice(1)).replace('_', ' ')
    }
  },
  components: { App }
})
