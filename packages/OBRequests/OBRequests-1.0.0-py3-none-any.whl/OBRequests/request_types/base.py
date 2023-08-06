from ..method import MethodModel


class RequestsBase:
    def __init__(self, obj) -> None:
        """
        Base for requests.

        Attributes
        ----------
        obj:
            Initialized method.
        """

        self.obj = obj

    def _format_route(self, kwargs: dict, method: MethodModel) -> dict:
        """
        Formats routes.

        Attributes
        ----------
        kwargs: dict
            Kwargs to format.
        method: MethodModel
            Method data.
        """

        additional_params = {}
        path_params = {}
        for name, value in kwargs.items():
            if name.startswith("_"):
                path_params[name[1:]] = value if value else ""
            else:
                additional_params[name] = value

        if path_params:
            route = self.obj.prefix.format(**path_params)
        elif method.path_params:
            route = self.obj.prefix.format(**method.path_params)
        else:
            route = self.obj.prefix

        return additional_params, route
