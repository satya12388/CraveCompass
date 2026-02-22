
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal


# -------- Input Validation Model --------
class ValidateInputFoodImg(BaseModel):
    is_food_menu: bool = Field(description="Whether image is a food menu")

    @field_validator("is_food_menu", mode="before")
    @classmethod
    def normalize_bool(cls, v):
        if isinstance(v, str):
            return v.strip().lower() == "true"
        return bool(v)

class ValidateInputQuery(BaseModel):
    is_valid_query: bool = Field(description="Whether query is food related")

    @field_validator("is_valid_query", mode="before")
    @classmethod
    def normalize_bool(cls, v):
        if isinstance(v, str):
            return v.strip().lower() == "true"
        return bool(v)


# -------- Menu Item Model --------
ALLOWED_CATEGORIES = {"Veg", "Non-Veg", "Beverages", "Desserts", "Others"}

class MenuItem(BaseModel):
    name: str
    price: float
    category: str

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, value):
        if value not in ALLOWED_CATEGORIES:
            return "Others"
        return value

# -------- Item Details Models --------
class NutritionInfo(BaseModel):
    calories: str = Field(description="e.g. 250 kcal")
    protein: str = Field(description="e.g. 10g")
    carbs: str = Field(description="e.g. 30g")
    fat: str = Field(description="e.g. 5g")

class ItemDetailsResponse(BaseModel):
    nutritioninfo: NutritionInfo
    ingredients: List[str]
    preparation: List[str]
    image_url: str


# -------- Final Extraction Model --------
class MenuExtractionResponse(BaseModel):
    items: List[MenuItem]


# -------- API Response --------
class SuccessResponse(BaseModel):
    success: bool
    data: List[MenuItem]