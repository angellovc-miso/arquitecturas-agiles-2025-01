require('dotenv').config()
const axios = require('axios');


const { getSeller, getClient, authUser, getAdmin } = require('./users');
const { createOrder, closeOrder, updateOrder } = require('./ordenes');
const { generateRandomText } = require('./stringUtils');
const { getUserLogs } = require('./logs');
const { generateHtmlReport } = require('./report');

const test1 = async () => {

    const testDetails = {
        filename: 'resistencia-test',
        name: 'Resistencia - Autenticación/Autorización',
        description: 'Este test busca entender la capacidad del sistema, usando las tácticas de autenticaicón y autorización para resistir el tampering en el servicio de ordenes',
        result: '',
        logs: []
    }

    // GET SELLER
    const seller = await getSeller(
        generateRandomText(),
        generateRandomText()
    );
    // console.log(seller)
    const client = await getClient(
        generateRandomText(),
        generateRandomText()
    );
    const authTokenSeller = await authUser(seller.user, seller.pass);
    const { order } = await createOrder({
        "tipoDePago": "EFECTIVO",
        "estado": "ABIERTO",
        "productos": [ "Pencil", "Beacon" ],
        "vendedor_id": seller.id,
        "cliente_id": client.id
    },
    authTokenSeller
    );
    await closeOrder(order, authTokenSeller);
    order.productos.push('Apple Juice');
    try {
        const {status} = await updateOrder(order, authTokenSeller);        
        if (status === 200) {
            testDetails.result = 'Failed'
        }
    } catch(error) {
        if (error.status === 403) {
            testDetails.result = 'Passed'
        } else {
            testDetails.result = 'Failed'
        }
    }

    const logs = await getUserLogs(seller.user)
    testDetails.logs = logs;
    console.dir(testDetails, {depth: 3});
    generateHtmlReport(testDetails)
    console.log('Finished test')
}

const test2 = async () => {
    const testDetails = {
        filename: 'deteccion-intrusos-test',
        name: 'Detección - detección de intrusos',
        description: 'Busca entender la capacidad del sistema para detectar intrusos que han logrado suplantar otros usuarios y buscan hacer tampering sobre el servicio de ordenes. Estos resultados nos ayudan a entender el impacto del tampering una vez que se ha producido el ataque de manera exitosa',
        result: '',
        logs: []
    }
        // GET SELLER
        const seller = await getSeller(
            generateRandomText(),
            generateRandomText()
        );
        // console.log(seller)
        const client = await getClient(
            generateRandomText(),
            generateRandomText()
        );

        const authTokenSeller = await authUser(seller.user, seller.pass);
        // console.log(authTokenSeller);

        const { order } = await createOrder({
            "tipoDePago": "EFECTIVO",
            "estado": "ABIERTO",
            "productos": [ "Pencil", "Beacon" ],
            "vendedor_id": seller.id,
            "cliente_id": client.id
        },
        authTokenSeller
        );
        await closeOrder(order, authTokenSeller);

        // Impersonating admin
        const admin = await getAdmin(
            generateRandomText(),
            generateRandomText() 
        );

        const authTokenAdmin = await authUser(admin.user, admin.pass);

        try {
            order.productos.push('Apple Juice');
            await updateOrder(order, authTokenAdmin);        
            order.productos.push('Red Bull');
            await updateOrder(order, authTokenAdmin);        
            order.productos.push('Gloves');
            await updateOrder(order, authTokenAdmin);        
            order.productos.push('Shampoo');
            const { status } = await updateOrder(order, authTokenAdmin);        
        } catch(error) {
            if (error.response.data.msg.includes('"Error de autenticación"')) {
                testDetails.result = 'Passed'
            } else {
                testDetails.result = 'Failed'
            }
        }

        const logs = await getUserLogs(admin.user)
        testDetails.logs = logs;
        console.dir(testDetails, {depth: 3});
        generateHtmlReport(testDetails)
        console.log('Finished test')
}

(async () => {
    await test1();
    await test2();
})()