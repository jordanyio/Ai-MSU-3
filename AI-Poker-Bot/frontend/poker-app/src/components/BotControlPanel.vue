<!-- <template>
    <div class="control-panel">
      <!-- <button 
        @click="handleAction('fold')"
        :disabled="handOver">
        Fold
      </button>
      <button 
        @click="handleAction('check')" 
        :disabled="currentBet > 0 || playerAllIn || handOver"
        :class="{'button-disabled': currentBet > 0 || playerAllIn || handOver}">
        Check
      </button>
      <button 
        @click="handleAction('bet')" 
        :disabled="currentBet > 0 || playerAllIn || handOver"
        :class="{'button-disabled': currentBet > 0 || playerAllIn || handOver}">
        Bet
      </button>
      <button 
        @click="handleAction('call')" 
        :disabled="currentBet == 0 || handOver"
        :class="{'button-disabled': currentBet == 0 || handOver}">
        Call
      </button>
      <button 
        @click="handleAction('raise')" 
        :disabled="currentBet == 0 || playerAllIn || handOver"
        :class="{'button-disabled': currentBet == 0 || playerAllIn || handOver}">
        Raise
      </button>
      
      <div>Chips: {{ chips }}</div>
      <input type="range" v-model="betAmount" :min="0" :max="chips" :disabled="playerAllIn || handOver">
      <div>Bet Amount: {{ betAmount }}</div> -->
    </div>
  </template>
  
  
  
  
    
  <script>
  import { mapState } from 'vuex';
  export default {
    props: ['chips'],
    computed: {
        ...mapState({
          dealer: state => state.dealer,
          bigBlind: state => state.bigBlind,
          actionOn: state => state.actionOn,
          playerChips: state => state.player_chips,
          currentBet: state => state.currentBet,
          playerAllIn: state => state.playerAllIn,
          handOver: state => state.handComplete,
          botResponseReturned: state => state.botResponseReturned,
          botResponse: state => state.botResponse
        }),
      },
    data() {
      return {
        betAmount: 0,
        isBet: false
      };
    },
    methods: {
      handleAction(action) {
        if (action == 'Bet'){
          this.isBet = true;
          
          this.$store.dispatch('playerBet', this.betAmount)
          console.log(action, this.betAmount)
          this.betAmount = 0
        }
        if (action == 'Raise'){
          this.isBet = true;
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
          this.$store.dispatch('fetchNewHand')
        }
  
      }
    },
    watch: {
      actionOn(newVal){
        if (newVal == 'bot'){
          console.log('Action on bot!')
          let action = this.$store.dispatch('getBotAction')
          console.log('Bot Move: ', action)
        }
      },
      botResponseReturned(newVal){
        if (newVal){
          this.betAmount = this.botResponse['Amount']
          this.handleAction(this.botResponse['Action'])
        }
      }

    }
  }
  </script>
  
    
  <style scoped>
  .control-panel button {
    margin: 5px;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .control-panel button:hover {
    background-color: #0056b3;
  }
  
  .control-panel button:disabled, .control-panel .button-disabled {
    background-color: #ccc;
    color: #666;
    cursor: not-allowed;
  }
  
  .control-panel input[type="range"] {
    width: 100%; /* Full-width slider */
    margin: 10px 0; /* Space around the slider */
  }
  
  .control-panel div {
    margin: 5px;
  }
  </style>
  
  
    
     -->