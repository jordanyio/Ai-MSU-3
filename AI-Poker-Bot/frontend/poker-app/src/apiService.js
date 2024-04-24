import axios from 'axios';

const API_URL = 'http://localhost:5000'; 

export default {
  getNewHand() {
    return axios.get(`${API_URL}/GetNewHand`);
  },
  getFlop() {
    return axios.get(`${API_URL}/GetFlop`);
  },
  getTurn() {
    return axios.get(`${API_URL}/GetTurn`);
  },
  getRiver() {
    return axios.get(`${API_URL}/GetRiver`);
  },
  updateState(data) {
    return axios.post(`${API_URL}/UpdateState`, data);
  },
  evaluateHands(data) {  
    return axios.post(`${API_URL}/EvaluateHands`, data);
  },
  getBotAction(data) {
    return axios.post(`${API_URL}/GetBotAction`, data)
  }
};
