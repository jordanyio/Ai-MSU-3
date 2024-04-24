import Vue from 'vue';
import Vuex from 'vuex';
import apiService from './apiService'; 

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isPlaying: false,
    playerCards: [],
    opponentCards: [],
    communityCards: ['CardBack','CardBack','CardBack','CardBack','CardBack'],
    commCards: [],
    pot: 0,
    player_chips: 0,
    bot_chips: 0,
    blinds: '',
    dealer: 'player', // player or bot
    actionOn: 'player',
    currentBet: 0,
    currentBettingRound: 0,
    bettingRoundCheckCount: 0,
    bettingRoundCallCount: 0,
    bettingRoundBetCount: 0,
    bettingRoundComplete: false,
    handComplete: false,
    handWinner: '',
    playerAllIn: false,
    noMoreAction: false,
    playerActionsThisHand: [],
    botResponse: {},
    botResponseReturned: false
  },
  mutations: {
    SET_GAME_DATA(state, { buyIn, blinds }) {
      state.player_chips = buyIn;
      state.bot_chips = buyIn;
      state.blinds = blinds;
    },
    SET_IS_PLAYING(state, payload) {
      state.isPlaying = payload;
    },
    UPDATE_PLAYER_CHIPS(state, chips){
      state.player_chips = chips; 
    },
    UPDATE_BOT_CHIPS(state, chips){
      state.bot_chips = chips;
    },
    PLAYER_CHECK(state){
      let context = `Action was on ${state.actionOn} who checked in betting round ${state.currentBettingRound}, while the dealer button is on ${state.dealer} and pot size ${state.potSize}`;

      state.playerActionsThisHand.push(context);
      console.log(context);
      state.bettingRoundCheckCount++;
      state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
      if (state.bettingRoundCheckCount == 2){
        state.bettingRoundComplete = true;
      }
      console.log(JSON.stringify(this.state, null, 2));
    },
    PLAYER_BET(state, data){
      let context = `Action was on ${state.actionOn} who bet in betting round ${state.currentBettingRound}, while the dealer button is on ${state.dealer}. The bet amount is ${state.currentBet} and the pot size is ${state.potSize}.`;

      state.playerActionsThisHand.push(context);
      console.log(context);
      const betAmount = +data; // Ensure data is treated as a number
      state.currentBet = betAmount;
      state.pot += betAmount; 
      state.bettingRoundBetCount++;
      if (state.actionOn === 'player') {
        if (betAmount == state.player_chips) {
          state.playerAllIn = true    
        }
        state.player_chips -= betAmount;
      } else {
        state.bot_chips -= betAmount;
        if (betAmount == state.bot_chips) {
          state.playerAllIn = true    
        }
      }
      state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
    },
    
    PLAYER_RAISE(state, data){
      state.bettingRoundBetCount++;
      const betAmount = +data;
      let context = `Action was on ${state.actionOn} who raised in betting round ${state.currentBettingRound}, while the dealer button is on ${state.dealer}. The raise amount is ${betAmount} and the pot size is ${state.potSize}. Is player all in: ${state.playerAllIn}`;

      state.playerActionsThisHand.push(context);
      if (state.actionOn == 'player') {
        if (betAmount == state.player_chips) {
          state.player_chips -= betAmount
          state.pot += betAmount
          state.currentBet = betAmount-state.currentBet
          state.playerAllIn = true
          state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
          return
        }
        
        if (state.bettingRoundBetCount == 2){
          if (betAmount/2 < state.currentBet ){
            console.log('the raise was not enough')
            return
          }
        } else {
          if (betAmount < state.currentBet){
            console.log('The raise was not enough')
            return
          }
        }
        state.player_chips -= betAmount
        state.pot += betAmount
        state.currentBet = betAmount-state.currentBet
        state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
      }
      else {
        if (betAmount == state.bot_chips) {
          state.bot_chips -= betAmount
          state.pot += betAmount
          state.currentBet = betAmount-state.currentBet
          state.playerAllIn = true
          state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
          return
        }
        if (state.bettingRoundBetCount == 2){
          if (betAmount/2 < state.currentBet ){
            console.log('the raise was not enough')
            return
          }
        } else {
          if (betAmount < state.currentBet){
            console.log('The raise was not enough')
            return
          }
        }
        state.bot_chips -= betAmount
        state.pot += betAmount
        state.currentBet = betAmount-state.currentBet
        state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
      }

      
      
    },
    PLAYER_CALL(state){
      
      let betAmount = state.currentBet;

      if (state.actionOn === 'player') {
        if (state.player_chips < state.currentBet){
          let returnToRaiserAmount = state.currentBet - state.player_chips
          state.bot_chips += returnToRaiserAmount
          betAmount = state.player_chips
        }
        state.player_chips -= betAmount;
        
      } else {
        if (state.bot_chips < state.currentBet){
          let returnToRaiserAmount = state.currentBet - state.bot_chips
          state.player_chips += returnToRaiserAmount
          betAmount = state.bot_chips
        }
        state.bot_chips -= betAmount
      }
      state.pot += betAmount

      state.currentBet = 0;
      state.bettingRoundCallCount = 1;
      state.bettingRoundComplete = true;
      if (state.playerAllIn){
        state.noMoreAction = true;
      }
      let context = `Action was on ${state.actionOn} who raised in betting round ${state.currentBettingRound}, while the dealer button is on ${state.dealer}. The raise amount is ${state.currentBet} and the pot size is ${state.potSize}. Is player all in: ${state.playerAllIn}`;

      state.playerActionsThisHand.push(context);
      state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
    },
    PLAYER_FOLD(state){
      let context = `Action was on ${state.actionOn} who folded in betting round ${state.currentBettingRound}, the pot size is ${state.potSize}.`;

      state.playerActionsThisHand.push(context);
      state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
      state.currentBet = 0;
      state.bettingRoundComplete = true;
      state.handComplete = true;
    },
    SET_NEW_HAND(state, data) {
      state.botResponseReturned = false;
      state.currentBettingRound = 0;
      state.handComplete = false;
      state.bettingRoundComplete = false;
      state.bettingRoundCallCount = 0;
      state.bettingRoundCheckCount = 0;
      state.currentBet = 0

      state.playerCards = data.player_hand;
      state.opponentCards = data.opponent_hand;
      state.handWinner = ''
      state.communityCards = ['CardBack','CardBack','CardBack','CardBack','CardBack'];  // Clear community cards on new hand
      state.pot = 0;  // Reset pot for a new game
      state.dealer = state.dealer === 'player' ? 'bot' : 'player';
      state.actionOn = state.dealer === 'player' ? 'bot' : 'player';
      console.log("Playing hand. Dealer is", state.dealer);
      
      state.dealer === 'player' ? state.player_chips-=2 : state.player_chips-=1;
      state.dealer === 'bot' ? state.bot_chips-=2 : state.bot_chips-=1;
      if (state.dealer == 'player'){
        state.actionOn = 'bot'
      }
      let antes = +3
      state.pot += antes
      state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';
      console.log(state.dealer, 'paid the big blind for $2', state.actionOn, 'paid the small blind $1')
      console.log('First state')
      console.log(JSON.stringify(this.state, null, 2));
      state.actionOn = state.actionOn === 'player' ? 'bot' : 'player';

    },
    SET_COMMUNITY_CARDS(state, cards) {
      state.communityCards = cards;
      state.commCards = cards;
      console.log('state', state.communityCards)
    },
    UPDATE_POT(state, amount) {
      state.pot += amount;
    },
    UPDATE_ROUND(state){
      state.botResponseReturned = false
      state.bettingRoundCallCount = 0
      state.bettingRoundCheckCount = 0
      state.bettingRoundBetCount = 0
      state.bettingRoundComplete = false
      state.currentBettingRound++
      state.currentBet = 0
      state.botResponse = {}
      state.actionOn = state.dealer === 'player' ? 'bot' : 'player';
      console.log('Update State')
      console.log(JSON.stringify(this.state, null, 2));
    },
    END_HAND(state, data){
      state.handComplete = true
      let playerScore = data.playerScore
      let botScore = data.botScore
      let winningHand;
      if (playerScore < botScore) {
        state.handWinner = 'player'
        winningHand = state.player_hand;
        state.player_chips += state.pot
      }
      else if (botScore < playerScore) {
        state.handWinner = 'bot'
        winningHand = state.opponent_hand;
        state.bot_chips += state.pot
      } else {
        state.handWinner = 'Chop'
        let halfPot = state.pot/2
        state.bot_chips += halfPot
        state.player_chips += halfPot
        winningHand = 'Chop'
      }

      let context = `The winner of the recent hand is: ${state.handWinner}, The winning cards: ${winningHand}.`;


      state.playerActionsThisHand.push(context);

      state.noMoreAction = false;
      state.playerAllIn = false;
      if (state.playerActionsThisHand.length > 24) {
        state.playerActionsThisHand.splice(0, 8);
      }
      state.botResponse = {}
      state.botResponseReturned = false
      state.actionOn = ""
      console.log('Final state')
      console.log(JSON.stringify(this.state, null, 2));
    },
    BOT_ACTION(state, data){
      state.botResponse = data
      state.botResponseReturned = true
      console.log('Mutating the state from bot response. Data: ', data)
    }
  },
  actions: {
    playerCheck({commit}){
      commit('PLAYER_CHECK')
    },
    playerBet({commit}, data){
      commit('PLAYER_BET', data)
    },
    playerRaise({commit}, data){
      commit('PLAYER_RAISE', data)
    },
    playerCall({commit}){
      commit('PLAYER_CALL')
    },
    startGame({ commit }, data) {
      commit('SET_GAME_DATA', data);
      commit('SET_IS_PLAYING', true);
    },
    endGame({ commit }) {
      commit('SET_IS_PLAYING', false); 
    },
    fetchNewHand({ commit }) {
      apiService.getNewHand().then(response => {
        console.log(response.data)
        commit('SET_NEW_HAND', response.data);
      });
    },
    fetchFlop({ commit }) {
      apiService.getFlop().then(response => {
        console.log('Fetching Flop')
        commit('SET_COMMUNITY_CARDS', response.data);
      });
    },
    fetchTurn({ commit }) {
      apiService.getTurn().then(response => {
        console.log('Fetching Turn')
        commit('SET_COMMUNITY_CARDS', response.data);
      });
    },
    fetchRiver({ commit }) {
      apiService.getRiver().then(response => {
        console.log('Fetching River')
        commit('SET_COMMUNITY_CARDS', response.data);
      });
    },
    updatePot({ commit }, amount) {
      commit('UPDATE_POT', amount);
    },
    updateRoundState({commit}){
      commit('UPDATE_ROUND');
    },
    endHand({ state, commit }) {
      const handData = {
        playerHand: state.playerCards,
        opponentHand: state.opponentCards,
        communityCards: state.communityCards
      };
      apiService.evaluateHands(handData)
        .then(response => {
          console.log('Evaluation Complete:', response.data);
          commit('END_HAND', response.data); 
        })
        .catch(error => console.error('Failed to evaluate hands:', error));
    },
    getBotAction({state, commit}) {

      let gameState = {
        botHand: state.opponentCards,
        communityCards: state.commCards,
        currentBettingRound: state.currentBettingRound,
        potSize: state.pot,
        playerActionsThisHand: state.playerActionsThisHand,
        dealer: state.dealer,
        currentBet: state.currentBet,
        botStackSize: state.bot_chips,
        opponentStackSize: state.player_chips

      };

      
      let botResponse;
      apiService.getBotAction(gameState)
        .then(response => {
          console.log('Bot Action: ', response.data);
          botResponse = response.data;
          commit('BOT_ACTION', response.data); 
        })
        .catch(error => console.error('Failed to get bot action:', error));

        return botResponse;
    }
  }
  
  
});
