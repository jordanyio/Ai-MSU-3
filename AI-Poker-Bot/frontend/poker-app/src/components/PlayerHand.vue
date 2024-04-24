<template>
    <div class="player-hand">
      <!-- Status images displayed above the card row -->
      <div v-if="showBetAmount" class="bet-display">Bet: {{ betAmount }}</div>
      <div class="status-images">
        <img :src="dealerImage" alt="Status image">
      </div>
      <!-- Card images in a row, with conditional class for glow -->
      <div class="card-row">
          <img v-for="card in cards" :src="`/cards/${card}.png`" :key="card" alt="Card image"
              :class="cardClasses">
        </div>
      <control-panel :chips="playerChips" />
    </div>
  </template>
  
  
    
    <script>
    import { mapState } from 'vuex';
  
    import ControlPanel from './ControlPanel.vue';
    
    export default {
      data(){
        return {
          showBetAmount: false // Toggle to control visibility of the bet amount display
        };
      },
      props: ['cards'],
      components: {
        ControlPanel
      },
      methods: {
        toggleBetAmount() {
          this.showBetAmount = !this.showBetAmount; // Toggle the visibility
        }
      },
      computed: {
        ...mapState({
          dealer: state => state.dealer,
          bigBlind: state => state.bigBlind,
          actionOn: state => state.actionOn,
          playerChips: state => state.player_chips,
          handComplete: state => state.handComplete,
          winner: state => state.handWinner,
          betAmount: state =>state.currentBet
        }),
        dealerImage() {
          if (this.dealer === 'player') {
            return '/cards/dealer.png';
          } else if (this.bigBlind === 'player') {
            return '/cards/bigblind.png';
          } else {
            return '/cards/smallblind.png';
          }
        },
        cardClasses() {
          let classes = [];
          if (this.actionOn === 'player') {
            classes.push('action-glow'); 
          }
          if (this.handComplete) {
            classes.push(this.winner === 'player' ? 'bot-winner' : 'player-winner'); 
              if (this.winner == 'Chop'){
              classes.push('player-winner')
            }
          }
          return classes;
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
    
    .status-images {
      margin-bottom: 10px;
      display: flex;
      justify-content: center;
    }
    
    .status-images img {
      width: 40px;
      height: 40px;
      border-radius: 50px;
    }
    
    .card-row {
      display: flex;
      align-items: center;
    }
    
    .card-row img {
      width: 100px;
      height: 140px;
      border-radius: 6px;
      margin: 4px;
      transition: box-shadow 0.3s;  
    }
    .bet-display {
      font-size: 32px; /* Large font size */
      color: red; /* Red color text */
      font-weight: bold; /* Make the digits bold */
      margin-bottom: 10px; /* Space below the display */
      text-align: center; /* Center-align the text */
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
    
    
    