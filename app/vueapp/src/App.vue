<template>
  <div id="app">
    <v-app>
      <v-content>
        <v-container
          class="main-container"
          fluid>

          <v-tabs ref="navTabs"
                  color="blue darken-4"
                  slider-color="cyan"
                  fixed-tabs>
            <v-tab>
              <router-link to="/" class="link"><span class="link-content">Home</span></router-link>
            </v-tab>
            <v-tab>
              <router-link to="/monitoring" class="link"><span class="link-content">Monitoring</span></router-link>
            </v-tab>
            <v-tab>
              <router-link to="/tickets" class="link"><span class="link-content">Ticket log</span></router-link>
            </v-tab>
            <v-tab v-if="$root.user_role === 'Admin'">
              <router-link to="/settings" class="link">
                <v-btn flat icon color="cyan">
                  <v-icon><span class="link-content"></span>settings</v-icon>
                </v-btn>
              </router-link>
            </v-tab>
          </v-tabs>
          <router-view @add-credential="saveCredential"/>
        </v-container>
        <!--<v-btn color="success" @click="sendMail">Send mail</v-btn>-->
      </v-content>
    </v-app>
  </div>
</template>

<script>
  import Vue from 'vue'
  import VueRouter from 'vue-router'
  import axios from 'axios'
  import VueAxios from 'vue-axios'
  import Settings from './components/Settings'
  import Monitoring from './components/Monitoring'
  import Home from './components/Home'
  import Tickets from './components/TicketsPage'
  import TicketAdmin from './components/TicketAdmin'
  import TicketDev from './components/TicketDev'
  import CIOView from './components/TicketsCIO-view'
  import ITDirectorView from './components/TicketsItDirector-view'
  import DevOpsView from './components/TicketsDevOps-view'
  import momenttt from 'vue-moment'

  let FormData = require('form-data')
  Vue.use(momenttt)
  Vue.use(VueRouter)
  Vue.use(VueAxios, axios)
  Vue.component('ticket-admin', TicketAdmin)
  Vue.component('ticket-dev', TicketDev)
  Vue.component('t-cio-view', CIOView)
  Vue.component('t-dev-view', DevOpsView)
  Vue.component('t-dir-view', ITDirectorView)

  let router = new VueRouter({
    // mode: 'history',
    routes: [
      { path: '/', component: Home },
      { path: '/monitoring', component: Monitoring },
      { path: '/settings', component: Settings },
      { path: '/tickets', component: Tickets }
    ]
  })

  module.exports = {
    name: 'app',

    data: function () {
      return {

      }
    },

    methods: {
      saveCredential: function (credential) {
        let credentials = []
        let local = JSON.parse(window.localStorage.getItem('credentials'))

        if (local) {
          credentials = local
        }

        credentials.push(credential)

        window.localStorage.setItem('credentials', JSON.stringify(credentials))
      },

      sendMail: function () {
        console.log('Mail is send')

        let form = new FormData()
        let credentials = window.localStorage.getItem('credentials')

        form.append('data', credentials)

        axios({
          method: 'post',
          url: '/api/sending_mail/',
          data: form
        })
          .then(function (response) {
            console.log('Mail delivered', response.data, response.status)
          })
          .catch(function (error) {
            console.log('Mail send error', error)
          })
      }
    },

    mounted: function () {
      // This piece of....code here for fixing position of slider according to current route
      this.$refs.navTabs.inputValue = this.$router.options.routes.indexOf(this.$router.options.routes.find(x => x.path === this.$router.currentRoute.path))
    },

    router: router,

    components: {
      Settings,
      Monitoring,
      Home
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    width: 100%;
    height: 100%;
  }
  #django {
    max-width:30%;
    height:auto;
  }

  .main-container {
    padding: 0;
  }

  .link {
    color: white;
    text-decoration: none;
  }

  .tabs__bar {
    width: 100%;
  }
</style>
