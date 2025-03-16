const axios = require('axios');

const USER_ADMIN_API = process.env.USER_ADMIN_API || 'http://localhost:3000';
const AUTH_ENTITY_API = process.env.AUTH_ENTITY_API || 'http://localhost:3001';



const createUser = async (user, pass, role) => {
    const { data } = await axios.post(`${USER_ADMIN_API}/usuario/crear`, {nombre: user, contrasena: pass, rol: role}); 
    const userData = { 
        id: data.id,
        user,
        pass,
        role: data.rol
    }
    return userData;
}

const authUser = async (user, pass) => {
    const { data } = await axios.post(`${AUTH_ENTITY_API}/ccpauth`, {nombre: user, contrasena: pass});
    return data.token;
}

const getClient = async (user, pass) => {
    return createUser(user, pass, 'CLIENTE');
}

const getSeller = async (user, pass) => {
    return createUser(user, pass, 'VENDEDOR');
}

const getAdmin = async (user, pass) => {
    return createUser(user, pass, 'ADMINISTRADOR');
}


module.exports = {
    getClient,
    getSeller,
    getAdmin,
    authUser
}
