from fastapi import APIRouter, status, Depends
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = Session(bind=engine)

# Route to signup the user
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):

    """
        ## Register the user
        This register the new user 
        This requires the following
        - user : SignUpModel

        ```
            username:str
            email:str
            password:str
            is_staff:bool
            is_active:bool

        ```

    """

    # Fetching the first record of user with requested user email
    db_email = session.query(User).filter(User.email == user.email).first()

    # checking if user with that useremail is found or not. If yes then raise 400 error    
    if (db_email is not None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the email already exists")

    # Fetching the first record of user with requested user username
    db_username = session.query(User).filter(User.username == user.username).first()

    # checking if user with that username is found or not. If yes then raise 400 error    
    if (db_username is not None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the username already exists")

    # raise the error if username's length is greater than 25
    if (len(user.username) > 25):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="length of username exceeds the limit 25")
    # raise the error if username's email is greater than 80
    if (len(user.email) > 80):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="length of email exceeds the limit 80")

    # Creating the user with requested credentials
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    # adding the user to database
    session.add(new_user)
    
    # commiting the changes
    session.commit()
    
    # Returning the new user details
    return new_user


# Route to login the user
@auth_router.post("/login")
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):

    """
        ## Login the user
        This register the new user 
        This requires the following
        - user : LoginModel

        ```
            username:str
            password:str

        ```
        This  end point return access token and refresh token

    """    

    # fetching the record of user having username matched with existing user in ddtabase
    db_user = session.query(User).filter(User.username == user.username).first()

    # checking if user with such username exists pand password matches with existing one in database. If so return access and refresh token else raise 401 error
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        response = {
            "access": access_token,
            "refresh": refresh_token
        }
        return jsonable_encoder(response)
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Invalid username or password"
                             )


# Route to manage refresh token
@auth_router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):

    """
        ## Get new access token
        This return new access token.
        This requires the following
        - refresh token
        
        This  end point return new access token 

    """

    # verifying the refresh token. Raise 401 error if its expired or not valid
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a valid refresh token")

    # get the subject details
    current_user = Authorize.get_jwt_subject()
    
    # creating new access token for user
    access_token = Authorize.create_access_token(subject=current_user)

    # return access token in json format 
    return jsonable_encoder({"access": access_token})
