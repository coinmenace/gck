import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_connect(message):
    #pass
    Group('users').add(message.reply_channel)
    Group('users').send({
        'text': json.dumps({
           'status':'ok'
        })
    })


@channel_session_user
def ws_disconnect(message):
    Group('users').send({
        'text': json.dumps({
           'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('users').discard(message.reply_channel)


@channel_session_user
def ws_message(message):
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
           'is_logged_in': False
        })
    })
    Group('users').discard(message.reply_channel)