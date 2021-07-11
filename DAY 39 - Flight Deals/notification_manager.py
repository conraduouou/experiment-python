from twilio.rest import Client
from flight_data import FlightData

class NotificationManager:
    def __init__(self, flight_list, sid, token) -> None:
        """Initializes twilio messenger with specified list of flights."""
        self.flights = flight_list
        self.sid = sid
        self.token = token
        
    def send_message(self):
        for item in self.flights:
            if item != None:
                text_body = f"""
                Low price alert! Only €{item.price} to fly from
                {item.d_city}-{item.d_code} to {item.a_city}-{item.a_code},
                from {item.outbound} to {item.inbound}."""

                client = Client(self.sid, self.token)
                message = client.messages \
                    .create(
                        body=text_body,
                        from_="+17013532120",
                        to="+639262652721"
                    )
            
                print(message.status)