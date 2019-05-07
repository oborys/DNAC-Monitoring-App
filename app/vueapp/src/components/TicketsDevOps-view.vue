<template>
  <v-layout row wrap>
    <v-flex md8 offset-md2>
      <h1 class="display-1">Ticket log</h1>

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

          <template slot="items" slot-scope="props">
            <tr class="pointer" @click.stop="openDialog(props.item)">
              <!-- Ticket id column -->
              <td class="text-xs-left">#{{ props.item.id }}</td>
              <!-- Date column -->
              <td class="text-xs-left">{{ props.item.date }}</td>
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
        <ticket-dev :data="dialogData"
                    :parent="this"
                    @close-dialog="dialog = false">
        </ticket-dev>
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
          { align: 'left', text: 'Ticket id', value: 'id' },  // value -> this property using for sorting
          { align: 'left', text: 'Date happened', value: 'date' },
          { align: 'left', text: 'Type', value: 'issue_type__value' },
          { align: 'left', text: 'Device ip', value: 'device__ip' },
          { align: 'center', text: 'Status', value: 'status__value' },
          { align: 'right', text: 'Solver', value: 'decision_unit__full_name' }
        ],
        dialog: false,
        dialogData: [],
        user_role: this.$root.user_role,
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
          url: '/api/get_issue_list/' + this.user
        })
          .then(response => {
            this.issues = response.data.data

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

    computed: {
      user: function () {
        return this.user_role === 'DevOps' ? this.$root.username : ''
      }
    },

    created: function () {
      this.updateData()
    }
  }
</script>

<style scoped>

</style>
