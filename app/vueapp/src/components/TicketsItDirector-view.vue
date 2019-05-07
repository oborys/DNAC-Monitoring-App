<template>
  <v-layout row wrap>
    <v-flex md8 offset-md2>

      <h1 class="display-1">Ticket log</h1>

      <v-container grid-list-md text-xs-center wrap style="margin-bottom: 15px">
        <v-layout row wrap>

          <v-flex lg12>
            <v-card color="cyan lighten-1" dark height="100%" class="adjust-flex">
              <v-card-text class="px-5 pt-5">
                <v-container>
                  <v-layout row wrap>
                    <v-flex lg12>
                      <p class="display-1">Average Mean time</p>
                    </v-flex>
                  </v-layout>
                  <v-layout row wrap>
                    <v-flex lg6 md12>
                      <p class="title">to repair (MTTR)</p>
                      <p v-if="mttr === 'None'" class="display-2">-</p>
                      <p v-else class="display-2">{{ mttr }}</p>
                    </v-flex>
                    <v-flex lg6 md12>
                      <p class="title">to recover incedent</p>
                      <p v-if="mttr === 'None'" class="display-2">-</p>
                      <p v-else class="display-2">{{ mttri }}</p>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>
            </v-card>
          </v-flex>

        </v-layout>
      </v-container>

      <v-card>
        <v-card-title>

          <!--<v-icon class="ml-1" style="cursor: pointer" color="cyan lighten-1">filter</v-icon>-->

          <v-spacer/>
          <v-text-field
            v-model="search"
            append-icon="search"
            row-height="3"
            label="Filter"
            class="ml-4">
          </v-text-field>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="issues"
          :search="search"
          :rows-per-page-items="[10,25,50,{text:'All',value:-1}]"
          must-sort
          sort-icon="expand_more"
          class="elevation-2">

          <template slot="items" slot-scope="props" >
            <tr class="pointer" @click.stop="openDialog(props.item)">
              <!-- Ticket id column -->
              <td class="text-xs-left">#{{ props.item.id }}</td>
              <!-- Date column -->
              <td class="text-xs-left">{{ props.item.date | moment("dddd, MMMM Do YYYY, h:mm:ss")}}</td>
              <!-- Type column -->
              <td class="text-xs-left">{{ props.item.issue_type__value }}</td>
              <!-- Device column -->
              <td class="text-xs-left">{{ props.item.device__ip }}</td>
              <!-- Status column -->
              <td class="text-xs-center"
                  :style="{color: $root.statusColor(props.item.status__value)}">
                {{ props.item.status__value }}
              </td>
              <!-- Solver column -->
              <td v-if="props.item.decision_unit__full_name" class="text-xs-right">{{ fullName(props.item) }}</td>
              <td v-else class="text-xs-right">--</td>
            </tr>
          </template>

        </v-data-table>

      </v-card>

      <v-dialog
        v-model="dialog"
        max-width="600">
        <ticket-admin :data="dialogData"
                      :parent="this"
                      :solvers="solvers"
                      @close-dialog="dialog = false">
        </ticket-admin>
      </v-dialog>
    </v-flex>
  </v-layout>
</template>

<script>
  import axios from 'axios'

  module.exports = {
    data: function () {
      return {
        issues: [],

        headers: [
          {align: 'left', text: 'Ticket id', value: 'id'},  // value -> this property using for sorting
          {align: 'left', text: 'Date happened', value: 'date'},
          {align: 'left', text: 'Type', value: 'issue_type__value'},
          {align: 'left', text: 'Device ip', value: 'device__ip'},
          {align: 'center', text: 'Status', value: 'status__value'},
          {align: 'right', text: 'Solver', value: 'decision_unit__full_name'}
        ],
        dialog: false,
        dialogData: [],
        solvers: [],
        user_role: this.$root.user_role,
        mttr: null,
        mttri: null,
        customer_satisfaction: null,
        service_availability: null,
        search: '',
        filterStatus: null
      }
    },

    methods: {
      fullName: function (data) {
        return data.decision_unit__full_name + ' (' + data.decision_unit__user__username + ')'
      },

      openDialog: function (data) {
        this.dialog = true
        this.dialogData = data
      },

      updateData: function () {
        axios({
          method: 'get',
          url: '/api/get_issue_list/'
        })
          .then(response => {
            this.issues = response.data.data
            this.solvers = response.data.solvers
            this.mttr = response.data.mttr.split('.')[0]
            this.mttri = response.data.mttri.split('.')[0]
            this.service_availability = response.data.service_availability
            this.customer_satisfaction = response.data.customer_satisfaction

            for (let issue of this.issues) {
              issue.status__value = this.$root.prettyStatus(issue.status__value)
              issue.issue_type__value = this.$root.prettyStatus(issue.issue_type__value)
              issue.date = this.$moment(issue.date).format('dddd, MMMM Do YYYY, h:mm:ss')
            }
          })
          .catch(error => {
            console.log(error)
          })
      }
    },

    created: function () {
      this.updateData()
    }
  }

</script>

<style scoped>
  .pointer {
    cursor: pointer;
  }

  .adjust-flex {
    display: flex;
    align-items: center;
  }
</style>
