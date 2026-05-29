import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def criar_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def obter_usuario_por_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return User.objects.get(id=payload["user_id"])
    except Exception:
        return None


def obter_usuario_request(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        prefix, token = auth_header.split(" ")

        if prefix.lower() != "bearer":
            return None

        return obter_usuario_por_token(token)
    except Exception:
        return None