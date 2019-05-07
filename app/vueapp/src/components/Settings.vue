<template>
  <v-layout row wrap>
    <v-flex md4 offset-md4>
      <h1 class="display-1">Enter - APIC-EM/DNA-C credentials</h1>
      <v-form v-model="valid" ref="form" lazy-validation>

        <v-text-field
          class="browser-default"
          label="Controller IP"
          v-model="ip"
          :rules="ipRules"
          required>
        </v-text-field>
        <!--rules for ip only - v => /^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$/.test(v) || 'IP address must be valid'-->

        <v-text-field
          label="Enter username"
          v-model="username"
          :rules="[v => !!v || 'Username is required']"
          required>
        </v-text-field>

        <v-text-field
          v-model="password"
          :append-icon="e3 ? 'visibility' : 'visibility_off'"
          :append-icon-cb="() => (e3 = !e3)"
          :type="e3 ? 'password' : 'text'"
          :rules="passRules"
          name="input-10-2"
          label="Enter your password"
          hint="At least 8 characters"
          min="8"
          required>
        </v-text-field>

        <v-select
          :items="net_types"
          :rules="[v => !!v || 'Type is required']"
          v-model="type"
          label="Enter network type"
          single-line
          required>
        </v-select>

        <v-text-field
          v-model="token"
          :append-icon="e1 ? 'visibility' : 'visibility_off'"
          :append-icon-cb="() => (e1 = !e1)"
          :type="e1 ? 'password' : 'text'"
          name="input-10-2"
          label="Enter Webex Bot Token">
        </v-text-field>
          <!--hint="At least 8 characters"-->
        <!--min="8"-->
        <!--:rules="[v => !!v || 'Bot Token is required']"-->


        <v-btn
          @click="submitForm"
          :disabled="!fieldIsEmpty || !valid"
          v-if="!progress">
          submit
        </v-btn>

        <v-btn
          @click="clearForm"
          v-if="!progress">
          clear
        </v-btn>

        <v-progress-circular
          indeterminate
          color="green"
          v-if="progress"/>

      </v-form>
      <p :style="{color:post_status_color}"></p>
    </v-flex>

    <v-chip
      outline
      v-model="chipTrue"
      close
      @input="resp_message = null"
      color="green">{{ resp_message }}
    </v-chip>

    <v-chip
      outline
      v-model="chipFalse"
      close
      @input="resp_message = null"
      color="red">{{ resp_message }}
    </v-chip>

  </v-layout>
</template>

<script>
  import axios from 'axios'
  let FormData = require('form-data')

  module.exports = {
    name: 'settings',

    data: function () {
      return {
        e3: true,
        e1: true,
        credentials: [],
        valid: false,
        ip: '',
        username: '',
        password: '',
        type: null,
        token: '',
        net_types: ['APIC', 'DNA'],
        resp_message: null,
        post_status_color: null,
        ipRules: [
          v => !!v || 'Controller IP is required',
          v => (v && v.length >= 4) || 'At least 4 symbols'
        ],

        passRules: [
          v => !!v || 'Password is required',
          v => (v && v.length >= 8) || 'At least 8 symbols'
        ],
        progress: false,
        chipFalse: false,
        chipTrue: false
      }
    },

    computed: {
      fieldIsEmpty: function () {
        return !!(this.ip && this.username && this.password && this.type)
        // return !!(this.ip && this.username && this.password && this.type && this.token)
      }
    },

    methods: {

      submitForm: function () {
        let send = new FormData()
        let self = this
        send.append('net_ip', this.ip)
        send.append('net_user', this.username)
        send.append('net_pass', this.password)
        send.append('net_type', this.type)
        send.append('bot_token', this.token)

        this.progress = true
        this.chipFalse = false
        this.chipTrue = false

        axios.post('/api/setup_network/', send)
          .then(function (response) {
            console.log('Status', response.data.status)
            if (response.data.status) {
              console.log('OK')
              self.chipTrue = true
            } else {
              console.log('False')
              self.chipFalse = true
            }
            console.log(response.data)
            // self.post_status_color = response.data.status ? 'green' : 'red'
            self.resp_message = response.data.msg
            self.progress = false
          })
          .catch(function (error) {
            console.log(error)
          })
      },

      clearForm: function () {
        this.$refs.form.reset()
      }
    }
  }

</script>

<style scoped>

</style>
