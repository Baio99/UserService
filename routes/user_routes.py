from fastapi import APIRouter, HTTPException, status
from models.user import UserCreate, UserUpdate, UserResponse
from config.database import Database
from bson import ObjectId
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])

def hash_password(password: str) -> str:
    """Encriptar contraseña con bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_object_id(id: str) -> ObjectId:
    """Verificar si el ID es válido"""
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuario inválido"
        )
    return ObjectId(id)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Crear un nuevo usuario"""
    collection = Database.get_collection("users")
    
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    hashed_password = hash_password(user.password)
    
    user_dict = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    }
    
    result = await collection.insert_one(user_dict)
    
    created_user = await collection.find_one({"_id": result.inserted_id})
    
    return UserResponse(
        _id=str(created_user["_id"]),
        name=created_user["name"],
        email=created_user["email"]
    )

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: str):
    """Obtener usuario por ID"""
    object_id = verify_object_id(id)
    collection = Database.get_collection("users")
    
    user = await collection.find_one({"_id": object_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserResponse(
        _id=str(user["_id"]),
        name=user["name"],
        email=user["email"]
    )

@router.put("/{id}", response_model=UserResponse)
async def update_user(id: str, user_update: UserUpdate):
    """Actualizar usuario"""
    object_id = verify_object_id(id)
    collection = Database.get_collection("users")
    
    existing_user = await collection.find_one({"_id": object_id})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    update_data = {}
    
    if user_update.name is not None:
        update_data["name"] = user_update.name
    
    if user_update.email is not None:
        email_exists = await collection.find_one({
            "email": user_update.email,
            "_id": {"$ne": object_id}
        })
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        update_data["email"] = user_update.email
    
    if user_update.password is not None:
        update_data["password"] = hash_password(user_update.password)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay datos para actualizar"
        )
    
    await collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )
    
    updated_user = await collection.find_one({"_id": object_id})
    
    return UserResponse(
        _id=str(updated_user["_id"]),
        name=updated_user["name"],
        email=updated_user["email"]
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    """Eliminar usuario"""
    object_id = verify_object_id(id)
    collection = Database.get_collection("users")
    
    user = await collection.find_one({"_id": object_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    await collection.delete_one({"_id": object_id})
    
    return None