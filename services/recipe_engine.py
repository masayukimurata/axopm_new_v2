import os
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from typing import List, Dict, Any, Tuple, cast

class MurataRecipeEngine:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def _get_connection(self):
        return psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)

    def calculate_cost_recursive(self, r_id: int) -> Tuple[Decimal, List[Dict[str, Any]]]:
        """
        中間仕込み品を考慮した原価の再帰計算ロジック
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                query = """
                    SELECT i.m_id, i.usage_amount, m.unit_cost, m.is_internal_product, m.m_name,
                           r.total_weight_gram
                    FROM public.t_recipe_ingredients i
                    JOIN public.t_merchandise_pro m ON i.m_id = m.m_id
                    LEFT JOIN public.t_recipes r ON (m.is_internal_product = true AND r.r_id = CAST(REPLACE(m.m_id, 'M_', '') AS INTEGER))
                    WHERE i.r_id = %s AND m.is_active = true
                    ORDER BY i.m_id
                """
                cur.execute(query, (r_id,))
                ingredients = cast(List[Dict[str, Any]], cur.fetchall())

                if not ingredients:
                    return Decimal('0.00'), []

                total_cost = Decimal('0.00')
                details: List[Dict[str, Any]] = []

                for item in ingredients:
                    m_id = str(item.get('m_id', ''))
                    qty = Decimal(str(item.get('usage_amount') or '0'))
                    is_internal = bool(item.get('is_internal_product'))

                    if is_internal:
                        sub_r_id = int(m_id.replace('M_', ''))
                        sub_total_cost, _ = self.calculate_cost_recursive(sub_r_id)
                        total_weight = Decimal(str(item.get('total_weight_gram') or '1'))
                        unit_price = sub_total_cost / total_weight if total_weight > 0 else Decimal('0.00')
                    else:
                        unit_price = Decimal(str(item.get('unit_cost') or '0.00'))

                    line_cost = qty * unit_price
                    total_cost += line_cost

                    details.append({
                        "m_name": str(item.get('m_name')),
                        "quantity": float(qty),
                        "unit_price": float(unit_price),
                        "line_cost": float(line_cost)
                    })

                return total_cost, details
        finally:
            conn.close()
