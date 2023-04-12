# Entry point for the application.
from .. import hello_app    # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.
