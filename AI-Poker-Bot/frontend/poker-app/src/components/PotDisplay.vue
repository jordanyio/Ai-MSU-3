<template>
    <div class="pot-display">
      Current Pot: ${{ pot }}
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';
  
  export default {
    computed: {
      ...mapState({
        pot: state => state.pot  
      })
    }
  }
  </script>
  
  <style scoped>
  .pot-display {
    margin-top: 20px;
    font-size: 20px;  
    font-weight: bold;
  }
  </style>
  