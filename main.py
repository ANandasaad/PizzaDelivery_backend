from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from Models import models
from Database.db import engine
from Routers.user import user_router
from Routers.menu import menu_router
from Routers.pizza import pizza_router
from Routers.customization import customization_router
from Routers.order import order_router
from Routers.payment import payment_router
from Routers.deliveryPersonal import deliveryPersonal_router
from Routers.auth import auth_router
import asyncio

from Routers.restaurant import restaurant_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Order Tracking</title>
    </head>
    <body>
        <h1>Order Tracking</h1>
        <form action="" onsubmit="subscribeToTracking(event)">
            <input type="number" id="orderId" placeholder="Enter Order ID" required autocomplete="off"/>
            <button type="submit">Track Order</button>
        </form>
        <ul id="messages"></ul>
        <script>
            var ws;

            function subscribeToTracking(event) {
                event.preventDefault(); // Prevent form from reloading the page
                
                var orderId = document.getElementById("orderId").value;

                // Close existing WebSocket connection if any
                if (ws) {
                    ws.close();
                }

                // Create a new WebSocket connection for tracking
                ws = new WebSocket(`ws://localhost:8000/ws/tracking/${orderId}`);

                ws.onopen = function() {
                    console.log("WebSocket connection established");
                    ws.send("Client has connected!");
                };

                ws.onmessage = function(event) {
                    console.log("Received message:", event.data);
                    var messages = document.getElementById("messages");
                    var message = document.createElement("li");
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };

                ws.onerror = function(error) {
                    console.error("WebSocket error:", error);
                    alert("WebSocket error occurred. Please check your connection.");
                };

                ws.onclose = function() {
                    console.log("WebSocket connection closed");
                    alert("WebSocket connection closed");
                };
            }
        </script>
    </body>
</html>

"""


@app.get("/")
async def get():
    return HTMLResponse(html)
@app.websocket("/ws/tracking/{orderId}")
async def websocket_endpoint(websocket: WebSocket, orderId: int):
    await websocket.accept()
    try:
        for i in range(1, 6):  # Example loop to send updates
            await asyncio.sleep(2)  # Simulate delay
            await websocket.send_text(f"Update {i} for Order ID {orderId}")
    except Exception as e:
        print(f"Connection closed: {e}")
app.include_router(user_router)
app.include_router(menu_router)
app.include_router(pizza_router)
app.include_router(customization_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(deliveryPersonal_router)
app.include_router(auth_router)
app.include_router(restaurant_router)