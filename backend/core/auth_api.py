from ninja import Router, Schema
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()

router = Router()

class CadastroSchema(Schema):
    email: str
    password: str


class LoginSchema(Schema):
    email: str
    password: str


@router.post("/login")
@csrf_exempt
def login_usuario(request, data: LoginSchema):
    user = authenticate(
        request,
        username=data.email,
        password=data.password
    )

    if user is None:
        return {"success": False, "message": "Usuário ou senha inválidos."}

    login(request, user)

    return {
        "success": True,
        "message": "Login realizado com sucesso.",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    }


@router.post("/logout")
def logout_usuario(request):
    logout(request)
    return {"success": True, "message": "Logout realizado com sucesso."}


@router.get("/me")
def usuario_logado(request):
    if not request.user.is_authenticated:
        return {"authenticated": False}

    return {
        "authenticated": True,
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        }
    }

@router.post("/cadastro")
def cadastrar_usuario(request, data: CadastroSchema):

    email = data.email.lower().strip()

    if User.objects.filter(email=email).exists():
        return {
            "success": False,
            "message": "Este e-mail já está cadastrado."
        }

    user = User.objects.create_user(
        username=email,
        email=email,
        password=data.password
    )

    login(request, user)

    return {
        "success": True,
        "message": "Conta criada com sucesso.",
        "user": {
            "id": user.id,
            "email": user.email,
        }
    }