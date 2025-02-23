import { serve } from '@hono/node-server'
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => {
  return c.text('Hello Hono!')
})

let requestCount = 0;
app.get('/optimizacion_envios', (c):any => {
  requestCount++;

  let coordinates:any = {
    altitude: 15.2,
    latitude: 37.7749,
    longitude: -122.4194,
    coordinate_system: "Node - Delivery optimization service",
  };

  if (requestCount % 10 === 0) {
    const keys = ["altitude", "latitude", "longitude"];
    const randomKey = keys[Math.floor(Math.random() * keys.length)];
    coordinates[randomKey] += (Math.random() - 0.5) * 0.5; // Slight random variation
  }

  return c.json(coordinates);
});

serve({
  fetch: app.fetch,
  port: 3000
}, (info) => {
  console.log(`Server is running on http://localhost:${info.port}`)
})
