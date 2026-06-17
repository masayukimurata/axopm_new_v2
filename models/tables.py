from models.base import BaseModel, register_model

@register_model(label="レシピマスター", icon="restaurant_menu", table_name="t_recipes")
class Recipe(BaseModel):
    r_id: int
    r_name: str
    target_margin_rate: float
    selling_price: float
    remarks: str
    course: str
    category: str
    source_url: str
    serving_size: float
    total_cost: float
    instructions: str
    is_intermediate: bool

@register_model(label="レシピ材料紐付け", icon="list_alt", table_name="t_recipe_ingredients")
class RecipeIngredient(BaseModel):
    ing_id: int
    m_id: str
    usage_amount: float
    r_id: int

@register_model(label="商材マスター", icon="inventory", table_name="t_merchandise_pro")
class MerchandisePro(BaseModel):
    m_id: str
    scan_code: str
    m_name: str
    partner_id: int
    store_name: str
    purchase_unit: str
    pack_volume: float
    base_unit: str
    density: float
    cost_per_case: float
    tax_rate: float
    is_active: bool
    updated_at: str
    remarks: str
    storage_location: str
    unit_cost: float
    is_internal_product: bool

@register_model(label="商品マスタ", icon="inventory_2", table_name="t_product_master")
class ProductMaster(BaseModel):
    product_id: int
    vendor_brand_code: str
    product_name: str
    product_name_kana: str
    category_id: int
    partner_id: int
    new_jan_code: str
    new_price: float
    new_cost_price: float
    sales_type: str
    is_carton: bool
    tax_rate: float
    updated_at: str
    creation_date: str
