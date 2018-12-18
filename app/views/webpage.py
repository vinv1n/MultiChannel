from app.views.new_message import new_message
from app.views.sign_up import sign_up


def webpage(app):
    """
    This function adds to a flask app the logic
    for the webpage.
    """

    app.add_url_rule(
        rule="/webui/new_message",
        endpoint="new_message",
        view_func=new_message,
        methods=['GET', 'POST'],
    )

    app.add_url_rule(
        rule="/webui/sign_up",
        endpoint="sign_up",
        view_func=sign_up,
        methods=['GET', 'POST'],
    )
