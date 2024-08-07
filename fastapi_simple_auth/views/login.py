from typing import Annotated

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, Form
from pydantic import BaseModel

from sqlalchemy.orm import Session

from ..db import get_db
from ..router import auth_router
from ..templates import template_env
from ..settings import settings
from ..captcha import verify_captcha
from ..exceptions import SimpleAuthCaptchaFailed
from .. import crud

class Captcha(BaseModel):    
    captcha_token: str


@auth_router.get('/login')
def get_login(request: Request, response_class=HTMLResponse):
    tpl = template_env.get_template('login.html')

    ctx = {
        'rq': request,
        'settings': settings,
        'motd2': 'motd motd motd motd motd motd',
        'error2': 'some problem'
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)

@auth_router.post('/login')
def post_login(
            rq: Request, 
            form: Annotated[OAuth2PasswordRequestForm, Depends()],
            captcha_token: Annotated[str, Form()],
            db: Session = Depends(get_db)):

    try:
        verify_captcha(rq, token=captcha_token)
    except SimpleAuthCaptchaFailed as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    # here is POST
    user = crud.get_auth_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # what if unverified?
    if settings.username_is_email and not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # authenticate ZZZZZZZZZ !!!!
    # if settings.auth_transport == "session":
    rq.session['user'] = user.uuid        

    return {
        'status': 'OK',
        'url': settings.afterlogin_url
    }

@auth_router.post('/logout')
def logout(rq: Request):
    del rq.session['user']
    return RedirectResponse(settings.afterlogout_url)

