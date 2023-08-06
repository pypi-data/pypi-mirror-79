from datetime import datetime
import logging 


log = logging.getLogger(__name__)

class StateVector:
    """A state vector is a row from the OpenSky historic database.
    """

    def __init__(
        self,
        time=None,
        icao24=None,
        lat=None,
        lon=None,
        velocity=None,
        heading=None,
        vertrate=None,
        callsign=None,
        onground=None,
        alert=None,
        spi=None,
        squawk=None,
        baroaltitude=None,
        geoaltitude=None,
        lastposupdate=None,
        lastcontact=None,
        serials=None,
        hour=None,
    ):

        if not (time and lat and lon and icao24):
            raise ValueError(
                "State vector must contain at least timestamp, icao24, latitude and longitude"
            )

        self.time = time
        self.icao24 = icao24
        self.lat = lat
        self.lon = lon
        self.velocity = velocity
        self.heading = heading
        self.vertrate = vertrate
        self.callsign = callsign
        self.onground = onground
        self.alert = alert
        self.spi = spi
        self.squawk = squawk
        self.baroaltitude = baroaltitude
        self.geoaltitude = geoaltitude
        self.lastposupdate = lastposupdate
        self.lastcontact = lastcontact
        self.serials = serials
        self.hour = hour

    def __repr__(self):

        repstr = "time: {}\nicao24: {}\nlat: {}\nlon: {}".format(
            self.time, self.icao24, self.lat, self.lon
        )

        # TODO ADD OTHER DETAILS
        return repstr


class Ping:
    """A ping is the discrete unit of information in a flight track.
    It contains a subset of the information of a state vector. 
    The reason for using a ping and not a state vector is that a list of state vectors will contain redundant information
    for a given flight track.
    """

    def __init__(
        self,
        time=None,
        lat=None,
        lon=None,
        velocity=None,
        heading=None,
        vertrate=None,
        baroaltitude=None,
        geoaltitude=None,
        sv=None,
        **kwargs
    ):
        """A ping can either be generated (1) by specifying all the individual pieces of information, or (2) by supplying a state vector.
        If the state vector is supplied, it must be the only argument.

        Args:
            time (int, optional): Unix timestamp. Defaults to None.
            lat (float, optional): WGS84 latitude in degrees. Defaults to None.
            lon (float, optional): WGS84 longitude in degrees. Defaults to None.
            velocity (float, optional): [description]. Defaults to None.
            heading (float, optional): [description]. Defaults to None.
            vertrate (float, optional): [description]. Defaults to None.
            baroaltitude (float, optional): [description]. Defaults to None.
            geoaltitude (float, optional): [description]. Defaults to None.
            sv (encounter.StateVector, optional): [description]. Defaults to None.
        """

        if sv and (
            time
            or lat
            or lon
            or velocity
            or heading
            or vertrate
            or baroaltitude
            or geoaltitude
        ):
            raise ValueError(
                "Ping must be constructed either from an equivalent state vector or its particular values, not both"
            )

        if not sv and not (time and lat and lon):
            raise ValueError(
                "If state vector is not supplied, ping must contain at least timestamp, latitude and longitude"
            )

        if sv:
            self.time = sv.time
            self.lat = sv.lat
            self.lon = sv.lon
            self.velocity = sv.velocity
            self.heading = sv.heading
            self.vertrate = sv.vertrate
            self.baroaltitude = sv.baroaltitude
            self.geoaltitude = sv.geoaltitude
        else:
            self.time = time
            self.lat = lat
            self.lon = lon
            self.velocity = velocity
            self.heading = heading
            self.vertrate = vertrate
            self.baroaltitude = baroaltitude
            self.geoaltitude = geoaltitude

    def __repr__(self):
        return "{}: lat, lon = {},{}".format(
            datetime.utcfromtimestamp(self.time).strftime("%Y-%m-%d %H:%M:%S"),
            self.lat,
            self.lon,
        )


class FlightTrack:
    def __init__(self, svs=None):
        """[summary]

        Args:
            svs (List of encounter.StateVector, optional): [description]. Defaults to None.

        Raises:
            ValueError: [description]
            ValueError: [description]
        """

        if not svs:
            self.pings = []
            self.icao24 = ""
        else:

            pings = []
            self.icao24 = svs[0].icao24

            for sv in svs:
                if type(sv) is not StateVector:
                    raise ValueError("svs must be list of encounter.StateVector")
                if sv.icao24 != self.icao24:
                    raise ValueError("List of state vectors must have same icao24")
                pings.append(Ping(sv=sv))
            
            self.pings = pings
            log.debug("Created FlighTrack with {} pings".format(len(self.pings)))

    def __repr__(self):

        return "Flight {} track with {} pings".format(self.icao24, len(self.pings))
