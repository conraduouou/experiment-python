class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, **kw) -> None:
        """Initializes flight data structure with **price, **d_city, **d_code,
        **a_city, **a_code, **outbound, and **inbound."""

        self.price = kw.pop('price')
        self.d_city = kw.pop('d_city')
        self.d_code = kw.pop('d_code')
        self.a_city = kw.pop('a_city')
        self.a_code = kw.pop('a_code')
        self.outbound = kw.pop('outbound')
        self.inbound = kw.pop('inbound')
        self.stopovers = kw.pop('stopovers', 0)
        self.via_city = kw.pop('via_city', "")