"""
Database Schemas for AWS Student Community Day 2025

Each Pydantic model corresponds to a MongoDB collection. Collection name is the lowercase of the class name.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Event(BaseModel):
    title: str = Field(..., description="Event title")
    tagline: Optional[str] = Field(None, description="Short one-line description")
    description: Optional[str] = Field(None, description="Detailed event description")
    date: str = Field(..., description="Event date, human readable e.g. 'Feb 15, 2025'")
    start_time: Optional[str] = Field(None, description="Start time e.g. '09:00 AM'")
    end_time: Optional[str] = Field(None, description="End time e.g. '05:30 PM'")
    venue: str = Field(..., description="Venue name and address")
    city: Optional[str] = Field(None, description="City name")
    registration_open: bool = Field(True, description="Whether registration is open")

class Speaker(BaseModel):
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    tags: Optional[List[str]] = None

class Session(BaseModel):
    title: str
    speaker: Optional[str] = None
    track: Optional[str] = None
    start: str = Field(..., description="Start time, e.g., '10:00 AM'")
    end: str = Field(..., description="End time, e.g., '10:45 AM'")
    level: Optional[str] = Field(None, description="Beginner/Intermediate/Advanced")
    description: Optional[str] = None

class Sponsor(BaseModel):
    name: str
    tier: str = Field(..., description="Platinum/Gold/Silver/Community")
    logo_url: Optional[str] = None
    website: Optional[str] = None

class Registration(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    institute: Optional[str] = Field(None, description="College/University/Organization")
    year: Optional[str] = None
    interests: Optional[List[str]] = None
    referral: Optional[str] = Field(None, description="How did you hear about us?")
    consent: bool = Field(True, description="Agreed to terms and updates")
