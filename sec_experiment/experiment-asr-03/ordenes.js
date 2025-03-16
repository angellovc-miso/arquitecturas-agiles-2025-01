const axios = require('axios');

const ORDERS_API = process.env.ORDERS_API || 'http://localhost:3002'

const createOrder = async (orderInfo, sessionToken) => {
    const { data, status } = await axios.post(`${ORDERS_API}/pedidos`, orderInfo, {
        headers: {
            Authorization: `Bearer ${sessionToken}`
        }
    });
    return { order: data, status };
}

const closeOrder = async (order, sessionToken) => {
    order.estado = "CERRADO";
    const { data, status } = await axios.put(`${ORDERS_API}/pedido/${order.id}`, order, {
        headers: {
            Authorization: `Bearer ${sessionToken}`
        }
    });
    return { order: data, status };
}

const updateOrder = async (order, sessionToken) => {
    const { data, status } = await axios.put(`${ORDERS_API}/pedido/${order.id}`, order, {
        headers: {
            Authorization: `Bearer ${sessionToken}`
        }
    });
    return { order: data, status };    
} 

module.exports = {
    createOrder,
    closeOrder,
    updateOrder
}
