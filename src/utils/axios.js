import axios from 'axios'

const BASE_URL = "http://localhost:8000/";

// create a new axios instance
const instance = axios.create({
	baseURL: BASE_URL,
	headers: {
		"Content-Type": "application/json; charset=utf-8",
		"Accept": "application/json"
	}
})
export default instance