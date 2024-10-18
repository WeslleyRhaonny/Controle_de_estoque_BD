class ViewsInfo:
    VIEWS_DEFINITIONS = {
        "relatorio_mensal": """
                            SELECT 
                                v.vendedor_id,
                                v.nome AS nome_vendedor,
                                DATE_TRUNC('month', c.data) AS mes,
                                SUM(p.quantidade) AS total_produtos_vendidos,
                                SUM(c.preco_total) AS total_vendas
                            FROM 
                                compra c
                            JOIN 
                                vendedor v ON c.vendedor_id = v.vendedor_id
                            JOIN 
                                posse p ON c.compra_id = p.compra_id
                            JOIN 
                                produto prod ON p.prod_id = prod.prod_id
                            GROUP BY 
                                v.vendedor_id, v.nome, mes
                            ORDER BY 
                                v.vendedor_id, mes;
                            """
    }
