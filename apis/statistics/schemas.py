from pydantic import BaseModel

class TotalUsersResponse(BaseModel):
    total_users: int

class TotalUpdatesResponse(BaseModel):
    total_updates: int

class TimelineResponse(BaseModel):
    registered_last_24h: int
