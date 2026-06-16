from models.base import BaseModel, register_model

@register_model(label="レシピマスター", icon="restaurant_menu")
class Recipe(BaseModel):
    r_id: int
    r_name: str
    total_weight_gram: float
    total_cost: float
    category: str

@register_model(label="レシピ材料紐付け", icon="list_alt")
class RecipeIngredient(BaseModel):
    i_id: int
    r_id: int
    m_id: str
    usage_amount: float

@register_model(label="商材マスター", icon="inventory")
class MerchandisePro(BaseModel):
    m_id: str
    m_name: str
    unit_cost: float
    is_internal_product: bool
    is_active: bool
