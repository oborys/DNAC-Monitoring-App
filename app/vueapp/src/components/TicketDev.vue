<template>
  <v-card class="no-margin">

    <v-card-title>

      <v-flex md7>
        <p class="headline text-md-left"> Ticket #{{ data.id }}</p>
      </v-flex>

      <template  v-if="data.status__value === 'rejected'">
        <v-flex md2>
          <p class="green--text caption text-md-left">Opened:</p>

          <p class="red--text caption text-md-left">Rejected:</p>
        </v-flex>
        <v-flex md3>
          <p class="green--text caption text-md-left">{{ data.date_start | moment('DD/MM/YY h:mm:ss a') || '==' }}</p>

          <p class="red--text caption text-md-left">{{ data.date_end | moment('DD/MM/YY h:mm:ss a') || '==' }}</p>
        </v-flex>
      </template>

      <template  v-else>
        <v-flex md2>
          <p class="green--text caption text-md-left">Opened:</p>

          <p class="grey--text caption text-md-left">Close:</p>
        </v-flex>
        <v-flex md3>
          <p class="green--text caption text-md-left">{{ data.date_start | moment('DD/MM/YY h:mm:ss a') || '==' }}</p>

          <p class="grey--text caption text-md-left">{{ data.date_end | moment('DD/MM/YY h:mm:ss a') || '==' }}</p>
        </v-flex>
      </template>

    </v-card-title>

    <v-divider/>

    <v-card-text>
      <v-layout row wrap>
        <v-flex md2>
          <p class="text-md-right title-padding-right">Type:</p>
        </v-flex>
        <v-flex md10>
          <p class="text-md-left">{{ data.issue_type__value }}</p>
        </v-flex>
      </v-layout>

      <v-layout row wrap>
        <v-flex md2>
          <p class="text-md-right title-padding-right">Status:</p>
        </v-flex>
        <v-flex md10>
          <p class="text-md-left" :style="{color: $root.statusColor(data.status__value)}">{{ data.status__value }}</p>
        </v-flex>
      </v-layout>

      <v-layout row wrap>
        <v-flex md2>
          <p class="text-md-right title-padding-right">Message:</p>
        </v-flex>
        <v-flex md10>
          <p class="text-md-left">{{ data.text }}</p>
        </v-flex>
      </v-layout>

      <v-layout row wrap>
        <v-flex md2>
          <p class="text-md-right title-padding-right">Solver:</p>
        </v-flex>
        <v-flex md10>
          <p class="text-md-left">{{ data.decision_unit__full_name }}</p>
        </v-flex>
      </v-layout>

      <v-layout row wrap v-if="data.status__value === 'rejected'">
        <v-flex md2>
          <p class="text-md-right title-padding-right">Reject message:</p>
        </v-flex>
        <v-flex md10>
          <p class="text-md-left">{{ data.reject_msg }}</p>
        </v-flex>
      </v-layout>

    </v-card-text>

    <v-divider/>

    <v-card-actions>
      <template v-if="!['close', 'rejected'].includes(data.status__value)">
        <v-dialog
          v-model="rejectDialog"
          hide-overlay
          max-width="600">
          <v-btn flat color="orange" slot="activator">Reject ticket</v-btn>
          <v-card class="no-margin">
            <v-card-title class="headline">Please provide reason of rejecting</v-card-title>

            <v-container fluid>
              <v-layout row>
                <v-flex xs12>
                  <v-text-field
                    v-model="rejecting_reason"
                    label="Reason"
                    multi-line
                    rows="9"
                    autofocus
                    full-width
                    counter="120">
                  </v-text-field>
                </v-flex>
              </v-layout>
            </v-container>

            <v-card-actions>
              <v-spacer/>
              <v-btn color="orange" flat @click.native="rejectTicket">Reject</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-btn flat color="orange" @click.native="issueSolved">Issue solved</v-btn>
      </template>
      <v-btn flat color="orange" @click.native="closeDialog">Close</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  import axios from 'axios'
  let FormData = require('form-data')

  export default {
    name: 'ticket-dev',

    props: ['data', 'parent', 'dialog'],

    data: function () {
      return {
        select: null,
        role: this.$root.user_role,
        rejectDialog: false,
        rejecting_reason: ''
      }
    },

    methods: {
      closeDialog: function () {
        this.$emit('close-dialog')
        this.rejectDialog = false
      },

      setSolver: function () {
        let self = this
        let send = new FormData()

        send.append('solver', this.getLogin(this.select))
        send.append('issue_id', this.data.id)

        axios.post('/api/set_solver/', send)
          .then(function (response) {
            console.log('Status', response.data.status)
            if (response.data.status) {
              self.parent.updateData()
            }
            self.closeDialog()
          })
          .catch(function (error) {
            console.log(error)
          })
      },

      rejectTicket: function () {
        let self = this
        let send = new FormData()

        send.append('issue_id', this.data.id)
        send.append('reject_msg', this.rejecting_reason)
        send.append('user', 'dkhlopov')

        axios.post('/api/reject_ticket/', send)
          .then(function (response) {
            console.log('Status', response.data.status)
            if (response.data.status) {
              self.parent.updateData()
            }
            self.closeDialog()
          })
          .catch(function (error) {
            console.log(error)
          })
      },

      issueSolved: function () {
        let self = this
        let send = new FormData()

        send.append('issue_id', this.data.id)

        axios.post('/api/set_issue_as_solved/', send)
          .then(function (response) {
            console.log('Status', response.data.status)
            if (response.data.status) {
              self.parent.updateData()
            }
            self.closeDialog()
          })
          .catch(function (error) {
            console.log(error)
          })
      },

      getLogin: function (input) {
        let arr = input.split(' ')
        return arr[arr.length - 1].slice(1, -1)
      }
    }
  }
</script>

<style scoped>
  p {
    margin: 0;
  }

  .title-padding-right {
    padding-right: 10px;
    text-decoration: underline;
  }
</style>
