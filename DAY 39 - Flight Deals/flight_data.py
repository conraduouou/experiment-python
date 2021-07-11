class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, **kw) -> None:
        """Initializes flight data structure with **price, **d_city, **d_code,
        **a_city, **a_code, **outbound, and **inbound."""

        self.price = kw.pop('price', None)
        self.d_city = kw.pop('d_city', None)
        self.d_code = kw.pop('d_code', None)
        self.a_city = kw.pop('a_city', None)
        self.a_code = kw.pop('a_code', None)
        self.outbound = kw.pop('outbound', None)
        self.inbound = kw.pop('inbound', None)