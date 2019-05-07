<template>
  <v-layout row wrap>
    <v-flex md8 offset-md2>
      <h1 class="display-1">Lists of available devices</h1>
      <v-data-table
        :headers="headers"
        :items="devices"
        hide-actions
        class="elevation-1">
        <template slot="items" slot-scope="props">
          <!-- Type column -->
          <td v-if="props.item.family" class="text-xs-left">{{ props.item.family }}</td>
          <td v-else class="text-xs-left"> Unknown </td>
          <!-- Icon column -->
          <td v-if="props.item.family === 'Routers'" class="text-xs-left"><img src="/static/img/router.jpg" alt=""></td>
          <td v-else-if="props.item.family === 'Switches and Hubs'" class="text-xs-left"><img src="/static/img/content_switch.jpg" alt=""></td>
          <td v-else class="text-xs-left"><img src="" alt="">no image</td>
          <!-- Name column -->
          <td v-if="props.item.type" class="text-xs-left">{{ props.item.type }}</td>
          <td v-else class="text-xs-left"> -- </td>
          <!-- Hostname column -->
          <td v-if="props.item.hostname" class="text-xs-left">{{ props.item.hostname }}</td>
          <td v-else class="text-xs-left"> -- </td>
          <!-- IP address column -->
          <td class="text-xs-left">{{ props.item.ip }}</td>
          <!-- Status colump -->
          <td v-if="props.item.status" class="text-xs-center" style="color: green">on</td>
          <td v-else class="text-xs-center" style="color: red">off</td>
        </template>
      </v-data-table>
    </v-flex>
  </v-layout>
</template>

<script>
  import axios from 'axios'

  module.exports = {
    name: 'monitoring',

    data: function () {
      return {
        devices: [],

        headers: [
          { align: 'left', text: 'Type', value: 'family' },  // value -> this property using for sorting (must)
          { align: 'left', text: 'Icon', value: null },
          { align: 'left', text: 'Name', value: 'type' },
          { align: 'left', text: 'Hostname', value: 'hostname' },
          { align: 'left', text: 'IP addr', value: 'ip' },
          { align: 'center', text: 'Status', value: 'status' }
        ]
      }
    },

    created: function () {
      let self = this

      axios({
        method: 'get',
        url: '/api/get_devices_info/'
      })
        .then(function (response) {
          console.log('Data', response.data)
          self.devices = (response.data.status) ? response.data.data : {}
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
</script>

<style scoped>

</style>
