from typing import Type, Dict, Any, List

# モデルを登録するためのグローバルレジストリ
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {}

def register_model(label: str, icon: str, table_name: str, schema: str = "public"):
    """
    モデルに運用情報（テーブル名・スキーマ）を付与して登録するデコレータ
    """
    def decorator(cls: Type):
        MODEL_REGISTRY[cls.__name__] = {
            "model": cls,
            "label": label,
            "icon": icon,
            "table_name": table_name,
            "schema": schema
        }
        # クラス自体にもメタデータを付与してアクセスを容易にする
        setattr(cls, "_label", label)
        setattr(cls, "_icon", icon)
        setattr(cls, "_table_name", table_name)
        setattr(cls, "_schema", schema)
        return cls
    return decorator

def get_registered_models() -> List[Type]:
    """登録されたモデルクラスのリストを返す"""
    return [item["model"] for item in MODEL_REGISTRY.values()]

class BaseModel:
    """
    すべてのデータモデルの基底クラス
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
