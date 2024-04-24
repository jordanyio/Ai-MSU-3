<template>
  <div class="poker-table">
    <opponent-hand :cards="opponentCards" />
    <community-cards :cards="communityCards" />
    <pot-display />  
    <player-hand :cards="playerCards" />
  </div>
</template>

<script>
import { mapState } from 'vuex';
import PlayerHand from './PlayerHand.vue';
import OpponentHand from './OpponentHand.vue';
import CommunityCards from './CommunityCards.vue';
import PotDisplay from './PotDisplay.vue';  

export default {
  components: {
    PlayerHand,
    OpponentHand,
    CommunityCards,
    PotDisplay  
  },
  computed: {
    ...mapState({
      playerCards: state => state.playerCards,
      opponentCards: state => state.opponentCards,
      communityCards: state => state.communityCards,
      blinds: state => state.blinds
    })
  }
}
</script>

<style scoped>
.poker-table {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  height: 100vh;
}
</style>

  

  