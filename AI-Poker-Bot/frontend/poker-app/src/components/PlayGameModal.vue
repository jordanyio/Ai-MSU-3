<template>
    <div class="modal-overlay" v-if="isVisible">
      <div class="modal-content">
        <span @click="submitStartGame" class="close">&times;</span>
        <h2>Start New Game</h2>
        <form @submit.prevent="submitStartGame">
          <div>
            <label for="buyIn">Buy-in Amount:</label>
            <input type="number" id="buyIn" v-model.number="buyIn" min="1" required>
          </div>
          <div>
            <label for="blinds">Select Blinds:</label>
            <select id="blinds" v-model="blinds">
              <option value="1/2">1/2</option>
              <option value="2/5">2/5</option>
            </select>
          </div>
          <button type="submit">Start Game</button>
        </form>
      </div>
    </div>
  </template>
  


  
  <script>
  import { mapActions } from 'vuex';
  
  export default {
    name: 'PlayGameModal',
    props: ['isVisible'],
    data() {
      return {
        buyIn: null,
        blinds: '1/2'
      };
    },
    methods: {
      ...mapActions({
        dispatchStartGame: 'startGame' // Mapping Vuex action with a clear method name
      }),
      submitStartGame() {
        // Make sure the data is correct before dispatching
        if (this.buyIn && this.blinds) {
          this.dispatchStartGame({ buyIn: this.buyIn, blinds: this.blinds }); // Dispatch the Vuex action with the current data
        } else {
          alert("Please enter all required fields."); // Basic validation feedback
        }
      }
    }
  }
  </script>
  

  

  
  <style scoped>
  .modal-overlay {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    z-index: 1000; /* High z-index to ensure it's on top */
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8); /* Dimmed background to block out other UI elements */
  }
  
  .modal-content {
    background-color: #fefefe;
    margin: auto;
    padding: 20px;
    border: 1px solid #888;
    width: 50%; /* Adjust width as necessary */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  </style>
  