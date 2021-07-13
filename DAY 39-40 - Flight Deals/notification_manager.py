from twilio.rest import Client
from flight_data import FlightData
import smtplib

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
                Low price alert! Only €{item.price} to fly from {item.d_city}-{item.d_code} to {item.a_city}-{item.a_code}, from {item.outbound} to {item.inbound}."""

                if item.stopovers == 1:
                    text_body += f"\n\nFlight has 1 stop over, via {item.via_city} City."

                client = Client(self.sid, self.token)
                message = client.messages \
                    .create(
                        body=text_body,
                        from_="+17013532120",
                        to="+639262652721"
                    )
            
                print(message.status)
    
    def send_emails(self, userdata, email, password):
        for item in self.flights:
            if item != None:
                for row in userdata:
                    text_body = f"""
                        Low price alert! Only \u20ac{item.price} to fly from {item.d_city}-{item.d_code} to {item.a_city}-{item.a_code}, from {item.outbound} to {item.inbound}."""

                    if item.stopovers == 1:
                        text_body += f"\n\nFlight has 1 stop over, via {item.via_city} City."
                    
                    gflight = f"https://www.google.co.uk/flights?hl=en#flt={item.d_code}.{item.a_code}.{item.outbound}*{item.a_code}.{item.d_code}.{item.inbound}"

                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(email, password)
                        connection.sendmail(
                            from_addr=email,
                            to_addr=row["email"],
                            msg=f"Subject: Flight Deal!\n\n{text_body}\n{gflight}"
                        )

        pass