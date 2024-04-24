<template>
  <div id="app">
    <play-game-modal :isVisible="!isPlaying"/>
    <poker-table v-if="isPlaying"/>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import PlayGameModal from './components/PlayGameModal.vue';
import PokerTable from './components/PokerTable.vue';

export default {
  components: {
    PlayGameModal,
    PokerTable
  },
  computed: {
    ...mapState({
      isPlaying: state => state.isPlaying,
      dealer: state => state.dealer,
      bettingRoundComplete: state => state.bettingRoundComplete,
      bettingRound: state => state.currentBettingRound,
      callCount: state => state.bettingRoundCallCount,
      checkCount: state => state.bettingRoundCheckCount,
      noMoreAction: state => state.noMoreAction
    })
  },
  methods: {
    startGameProcess() {
      console.log("Game has started. Setting up...");
      this.loopGameProcess();
    },
    loopGameProcess() {
      if (this.isPlaying) {
        this.fetchInitialGameData();
        this.playHand();
      }
    },
    fetchInitialGameData() {
      this.$store.dispatch('fetchNewHand');
    },
    playHand() {
      console.log('Playing hand')

    }
  },
  watch: {
    isPlaying(newValue) {
      if (newValue) {
        this.startGameProcess();
      }
    },
    bettingRoundComplete(newValue){
      if (newValue){
        console.log("Betting round hit")
        console.log("Betting round", this.bettingRound, 'callcount', this.callCount, 'checkcout', this.checkCount)

        if (this.noMoreAction){
          console.log('No More Action, all in and call. Dealing the board out and assigning winner.')
            if (this.bettingRound === 0) {
              setTimeout(() => {
                this.$store.dispatch('fetchFlop');
            }, 1000); 
            setTimeout(() => {
              this.$store.dispatch('fetchTurn');
            }, 2000); 
            setTimeout(() => {
              this.$store.dispatch('fetchRiver');
            }, 4000); 
            console.log("ENDROUND");
            setTimeout(() => {
              this.$store.dispatch('endHand')
            }, 5000);
            
            setTimeout(() => {
              this.$store.dispatch('fetchNewHand');
            }, 10000); 
            
          } else if (this.bettingRound === 1) {
            setTimeout(() => {
              this.$store.dispatch('fetchTurn');
            }, 1000); 
            setTimeout(() => {
              this.$store.dispatch('fetchRiver');
            }, 2000); 
            console.log("ENDROUND");
            setTimeout(() => {
              this.$store.dispatch('endHand')
            }, 4000);
            
            setTimeout(() => {
              this.$store.dispatch('fetchNewHand');
            }, 8000); 
          } else if (this.bettingRound === 2) {
            setTimeout(() => {
              this.$store.dispatch('fetchRiver');
            }, 1000); 
            console.log("ENDROUND");
            setTimeout(() => {
              this.$store.dispatch('endHand')
            }, 3000);
            
            setTimeout(() => {
              this.$store.dispatch('fetchNewHand');
            }, 8000); 
          } 
        }
        else {
            if ((this.bettingRound === 0 && (this.callCount == 1 || this.checkCount == 2))) {
            console.log('bettingRoundComplete0');
            this.$store.dispatch('fetchFlop');
            this.$store.dispatch('updateRoundState');
          } else if ((this.bettingRound === 1 && (this.callCount == 1 || this.checkCount == 2))) {
            console.log('bettingRoundComplete1');
            this.$store.dispatch('fetchTurn');
            this.$store.dispatch('updateRoundState');
          } else if ((this.bettingRound === 2 && (this.callCount == 1 || this.checkCount == 2))) {
            console.log('bettingRoundComplete2');
            this.$store.dispatch('fetchRiver');
            this.$store.dispatch('updateRoundState');
          } 
          else {
            console.log("ENDROUND");
            this.$store.dispatch('endHand')
            setTimeout(() => {
              this.$store.dispatch('fetchNewHand');
            }, 5000); 
          }
        }

        
      }
    }
  }
}
</script>

