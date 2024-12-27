from pydantic import BaseModel


class AddressBase(BaseModel):
    city: str | None = None
    state: str | None = None
    address: str | None = None
    locality: str | None = None
    additional_instructions: str | None = None
    is_primary: bool | None = None
    zipcode: int | None = None

class AddressCreate(AddressBase):
    pass


class AddressInResponse(AddressBase):
    id: int
    latitude: float
    longitude: float
    user_id: int

    class Config:
        orm_mode = True
class UpdateAddress(AddressBase):

    class Config:
        orm_mode = True
class AddressResponse(BaseModel):
    message: str
    data: AddressInResponse

class SetAddress(BaseModel):
    is_primary: bool | None = None
class SetAddressResponse(BaseModel):
    message: str
    data: AddressInResponse