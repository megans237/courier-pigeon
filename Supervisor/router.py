import dotenv
import os
import Common.common_datatypes


class Routing:
    def __init__(self):
        """Initializes the routing class with Token
        and DBG flag from .env file
        """
        dotenv.load_dotenv()
        self.TKN = os.getenv("MAPBOX_TOKEN")
        self.DBG = int(os.getenv("DEBUG"))
        self.OPT = ["source=first", "destination=last", "roundtrip=true"]

    def assemble_req(
        self,
        coordinates: [Common.Location],
        options: [str] = self.OPT,
        token: str = self.TKN,
    ) -> str:
        print("to be implemented")
