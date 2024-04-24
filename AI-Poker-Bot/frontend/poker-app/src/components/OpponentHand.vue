<template>
    <div class="player-hand">
      <!-- <control-panel :chips="botChips" /> -->
      <div class="button-container">
        <button @click="toggleShowHand">{{ showHand ? 'Hide Hand' : 'Show Hand' }}</button>
      </div>
      <div class="card-row">
        <img v-for="card in cards" :src="getImageUrl(card)" :key="card" alt="Card image"
            :class="cardClasses">
      </div>
      <div>Chips: {{ botChips }}</div>
      <div class="status-images">
        <img :src="dealerImage" alt="Status image">
      </div>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';
  //import ControlPanel from './ControlPanel.vue';
  
  export default {
    props: ['cards', 'chips'],
    components: {
      //ControlPanel
    },
    data() {
      return {
        showHand: false,
        betAmount: 0,
        isBet: false
      };
    },
    computed: {
      ...mapState({
        dealer: state => state.dealer,
        bigBlind: state => state.bigBlind,
        actionOn: state => state.actionOn,
        botChips: state => state.bot_chips,
        handComplete: state => state.handComplete,
        winner: state => state.handWinner,
        noMoreAction: state => state.noMoreAction,
        playerChips: state => state.player_chips,
        currentBet: state => state.currentBet,
        playerAllIn: state => state.playerAllIn,
        handOver: state => state.handComplete,
        botResponseReturned: state => state.botResponseReturned,
        botResponse: state => state.botResponse
      }),
      dealerImage() {
        if (this.dealer === 'bot') {
          return '/cards/dealer.png';
        } else if (this.bigBlind === 'bot') {
          return '/cards/bigblind.png';
        } else {
          return '/cards/smallblind.png';
        }
      },
      cardClasses() {
        let classes = [];
        if (this.actionOn === 'bot') {
          classes.push('action-glow'); // Always apply action glow if the action is on bot
        }
        if (this.handComplete) {
          classes.push(this.winner === 'bot' ? 'bot-winner' : 'player-winner');
          if (this.winner == 'Chop'){
            classes.push('bot-winner')
          }
        }
        return classes;
      }
    },
    methods: {
      toggleShowHand() {
        // Toggle showHand only if hand is not complete or already showing the hand
        if (!this.handComplete) {
          this.showHand = !this.showHand;
        }
      },
      getImageUrl(card) {
        if (this.showHand) {
          return `/cards/${card}.png`; // Show the actual card
        } else {
          return `/cards/CardBack.png`; // Show a generic card back image
        }
      },
      handleAction(action) {
        if (action == 'Bet'){
          this.isBet = true;
          
          this.$store.dispatch('playerBet', this.betAmount)
          console.log(action, this.betAmount)
          this.betAmount = 0
        }
        if (action == 'Raise'){
          this.isBet = true;
          if (this.currentBet == 0 || this.currentBet == this.betAmount){
            this.$store.dispatch('playerBet', this.betAmount)
            console.log(action, this.betAmount)
            return
          }
          this.$store.dispatch('playerRaise', this.betAmount)
          console.log(action, this.betAmount)
          this.betAmount = 0
        }
        if (action == 'Check'){
          if (this.currentBet > 0){
            console.log("Tried to check when the other player bet")
            return
          }
          this.$store.dispatch('playerCheck');
        }
        if (action == 'Call'){
          if (this.currentBet == 0){
            console.log("Player tried to call when there is no bet")
            return
          }
          this.$store.dispatch('playerCall')
        }
        if (action == 'Fold'){
          console.log("Bot Fold")
          this.$store.dispatch('fetchNewHand')
        }
  
      }
    },
    watch: {
      handComplete(newVal) {
        // Always show the hand when complete, hide when not complete
        if (newVal && this.noMoreAction){
            this.showHand = newVal;
            return
        }

        this.showHand = newVal
        
      },
      noMoreAction(newVal){
        if (newVal){
            this.showHand = newVal
        }
      
      },
      actionOn(newVal){
        if (newVal == 'bot'){
          let action;
          setTimeout(() => {
            action = this.$store.dispatch('getBotAction');
            }, 1000); 
          
          console.log('Bot Move: ', action)
        }
      },
      botResponseReturned(newVal){
        console.log('Watching bot response: ', newVal)
        if (newVal){
          console.log('Bot response readY?')
          this.betAmount = this.botResponse['Amount']
          this.handleAction(this.botResponse['Action'])
        }
      }
    }
  }
  </script>
  
  
  

  <style scoped>
 .player-hand {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
  }
  
  .button-container {
    display: flex;
    justify-content: center;  
    width: 100%; 
    margin-bottom: 20px; 
  }
  
  .player-hand button {
    padding: 10px 20px;
    font-size: 16px; 
    background-color: #007BFF;  
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    outline: none;
    transition: background-color 0.3s;
  }
  
  .player-hand button:hover {
    background-color: #0056b3;  
  }
  
  .player-hand img {
    width: 100px;
    height: 140px;
    border-radius: 6px;  
    margin: 4px;  
  }

  .status-images img {
    width: 40px;  
    height: 40px;
    border-radius: 50px;
  }

  .action-glow {
    box-shadow: 0 0 16px 10px rgb(89, 28, 255);  
  }

  .player-winner {
  box-shadow: 0 0 16px 10px rgba(255, 28, 89, 0.607);
}

.bot-winner {
    box-shadow: 0 0 16px 10px rgb(165, 254, 12); 
}
  </style>
  