from app.views.login import login
from app.views.new_message import new_message
from app.views.sign_up import sign_up
from app.views.message_status import message_status


def webpage(app):
    """
    This function adds to a flask app the logic
    for the webpage.
    """

    app.add_url_rule(
        rule="/webui/login",
        endpoint="login",
        view_func=login,
        methods=['GET', 'POST'],
    )

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

    app.add_url_rule(
        rule="/webui/message_status/<string:message_id>",
        endpoint="message_status",
        view_func=message_status,
        methods=['GET', 'DELETE'],
    )
