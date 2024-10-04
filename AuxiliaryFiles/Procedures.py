class Procedures:
    PROCEDURES = [
        """
            CREATE OR REPLACE FUNCTION verificar_compra(cliente_id INTEGER, cart JSONB)
            RETURNS TABLE(desconto BOOLEAN, produto_invalido INTEGER, preco_total NUMERIC) AS $$
            DECLARE
                cliente RECORD;
                produto_carrinho RECORD;
                quantidade_produto INTEGER;
                estoque INTEGER;
                preco NUMERIC;
                total NUMERIC := 0;  -- Inicializa o total com 0
            BEGIN
                -- Busca informações do cliente
                SELECT * INTO cliente FROM cliente c WHERE c.cliente_id = $1;

                -- Verifica se o cliente tem direito a desconto
                desconto := cliente.torce_flamengo OR cliente.mora_em_sousa OR cliente.assiste_one_piece;

                -- Inicializa produto_invalido e o preco_total como 0
                produto_invalido := 0;
                preco_total := 0;

                -- Itera sobre os produtos no carrinho
                FOR produto_carrinho IN SELECT * FROM jsonb_each(cart) LOOP
                    quantidade_produto := produto_carrinho.value::INTEGER;

                    -- Verifica a quantidade disponível no estoque
                    SELECT p.quantidade, p.preco INTO estoque, preco FROM produto p WHERE p.prod_id = produto_carrinho.key::INTEGER;

                    -- Se a quantidade no estoque for menor que a do carrinho, define produto_invalido
                    IF estoque < quantidade_produto THEN
                        produto_invalido := produto_carrinho.key::INTEGER;
                        EXIT;  -- Sai do loop se encontrar um produto inválido
                    ELSE
                        total := total + (preco * quantidade_produto);  -- Adiciona ao total
                    END IF;
                END LOOP;

                preco_total := total;

                RETURN NEXT;
            END;
            $$ LANGUAGE plpgsql;
        """,
        """
            CREATE OR REPLACE FUNCTION salvar_compra(
                cliente_id INTEGER,
                vendedor_id INTEGER,
                tipo_pagamento VARCHAR,
                cart JSONB,
                preco_total NUMERIC
            )
            RETURNS VOID AS $$
            DECLARE
                nova_compra_id INTEGER;  -- Variável para armazenar o ID da nova compra
                produto_carrinho RECORD;  -- Variável para armazenar o produto do carrinho
            BEGIN
                -- Insere a nova compra
                INSERT INTO compra (cliente_id, vendedor_id, tipo_pagamento, data, preco_total)
                VALUES ($1, $2, $3, CURRENT_TIMESTAMP, $5)
                RETURNING compra_id INTO nova_compra_id;

                -- Itera sobre os produtos no carrinho
                FOR produto_carrinho IN SELECT * FROM jsonb_each(cart) LOOP
                    -- Insere os produtos na tabela posse
                    INSERT INTO posse (compra_id, prod_id, quantidade)
                    VALUES (nova_compra_id, produto_carrinho.key::INTEGER, produto_carrinho.value::INTEGER);

                    -- Atualiza a quantidade de produtos no estoque
                    UPDATE produto
                    SET quantidade = quantidade - produto_carrinho.value::INTEGER
                    WHERE prod_id = produto_carrinho.key::INTEGER;
                END LOOP;
            END;
            $$ LANGUAGE plpgsql;
        """
    ]
