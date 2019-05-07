<template>

  <div
    id="e3"
    style="max-width: 1000px; margin: auto;"
    class="grey lighten-3"
  >
    <v-flex xs10 offset-xs1>
      <h1 class="display-1">About DNA-C Network Health Check automatically report</h1>
    </v-flex>
    <v-card>
      <v-container
        fluid
        style="min-height: 0;"
        grid-list-lg>
        <v-layout row wrap >
          <v-flex xs12>
            <v-card color="blue accent-2" class="white--text">
              <v-card-title primary-title>
                <v-flex xs7>
                  <div>
                    <div class="headline">Cool tools for Service Providers</div>
                    <div class="text-lg-right">Different level of reports (For CIO, IT director and DevOps)</div>
                    <div class="text-lg-right">Customer Satisfaction</div>
                    <div class="text-lg-right">Average mean time to recover from incidents</div>
                  </div>
                </v-flex>
                <v-flex xs5>
                  <v-card-media
                    src="/static/img/!mttr.png"
                    height="125px"
                    contain>
                  </v-card-media>
                </v-flex>
              </v-card-title>
              <v-card-actions>
                <v-btn flat dark>Try it now</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
          <v-flex xs12>
            <v-card color="indigo darken-1" class="white--text">
              <v-container fluid grid-list-lg>
                <v-layout row>
                  <v-flex xs7>
                    <div>
                      <div class="headline">Monitoring</div>
                      <div class="text-lg-right">Device status</div>
                      <div class="text-lg-right">Flow analytics</div>
                      <div class="text-lg-right">Automatic ticket creation</div>
                      <div class="text-lg-right">Mean time to repair</div>
                    </div>
                  </v-flex>
                  <v-flex xs5>
                    <v-card-media
                      src="/static/img/support.png"
                      height="125px"
                      contain>
                    </v-card-media>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card>
          </v-flex>
          <v-flex xs12>
            <v-card color="deep-purple darken-24" class="white--text">
              <v-container fluid grid-list-lg>
                <v-layout row>
                  <v-flex xs7>
                    <div>
                      <div class="headline">Quick information module</div>
                      <div class="text-lg-right">E-mail report</div>
                      <div class="text-lg-right">Integration with Webex (Bot)</div>
                    </div>
                  </v-flex>
                  <v-flex xs5>
                    <v-card-media
                      src="/static/img/!bot.png"
                      height="125px"
                      contain>
                    </v-card-media>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </div>

</template>

<script>
  module.exports = {
    name: 'home'
  }
</script>

<style scoped>
  div .headline {
    font-size: 35px !important;
  }
  div .text-lg-right {
    font-size: 18px !important;
  }
</style>
