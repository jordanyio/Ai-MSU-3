<template>
    <div class="player-hand">
      <!-- Render actual community cards -->
      <img v-for="card in communityCards" :src="`/cards/${card}.png`" :key="card" alt="Card image">
      <!-- Render placeholder cards for remaining slots -->
      <img v-for="(src, index) in placeholderCards" :src="src" :key="`placeholder-${index}`" alt="Placeholder card">
    </div>
  </template>
  
  
  <script>
  import { mapState } from 'vuex';
  
  export default {
    computed: {
      ...mapState(['communityCards']),
      remainingSlots() {
        const maxCards = 5; // Maximum number of community cards
        return maxCards - this.communityCards.length;
      },
      placeholderCards() {
        return Array.from({ length: this.remainingSlots }, () => '/cards/CardBack.png');
      }
    }
  }
  </script>
  
  
  <style scoped>
  .player-hand img {
    width: 100px;  
    height: 140px;  
    border-radius: 6px;
    margin: 4px;  
  }
  </style>
  