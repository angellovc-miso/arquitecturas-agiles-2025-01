const axios = require('axios');

const LOGS_API = process.env.LOGS_API || 'http://localhost:3003'

const getUserLogs = async (username) => {
    const {data} = await axios.get(`${LOGS_API}/log?usuario=${username}`);
    return data.logs
}

module.exports = {
    getUserLogs
}