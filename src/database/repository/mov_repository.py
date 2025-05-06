# app/database/repositories/movimentacao_repository.py
from datetime import date, time
from database.config.connect import get_db


async def buscar_novas_movimentacoes(ultima_data: date, ultimo_horario: time):
    conn = await get_db()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                SELECT 
                    p.id AS id_processo, 
                    p.numero AS numero_processo, 
                    p.sigla_grau AS grau,   
                    p.data_ultima_movimentacao,
                    t."data" AS data_movimentacao,
                    m.horario AS horario_movimentacao,
                    m.id_movimento,
                    mo.nome AS nome_movimento, 
                    m.id_situacao,
                    s.nome AS nome_situacao,
                    m.id_situacao_iniciar, 
                    s1.nome AS nome_situacao_iniciar, 
                    m.id_situacao_finalizar,
                    s2.nome AS nome_situacao_finalizar,
                    t1."data" AS dt_iniciar_situacao,
                    t2."data" AS dt_finalizar_situacao, 
                    m.id_classe, 
                    c.nome AS nome_classe,
                    m.id_fase_processual, 
                    fp.nome AS nome_fase_processual,
                    oj.nome AS orgao_julgador, 
                    oj.sigla_tribunal AS sigla_tribunal_julgador, 
                    oj.nome_municipio AS municipio_julgador,
                    p.nome_sistema AS sistema
                FROM movimentacao m
                    INNER JOIN processo p ON (p.id = m.id_processo)
                    INNER JOIN tempo t ON (m.data = t.id)
                    INNER JOIN movimento mo ON (m.id_movimento = mo.id)
                    INNER JOIN orgao_julgador oj ON (m.id_orgao_julgador = oj.id)
                    INNER JOIN classe c ON (m.id_classe = c.id)
                    INNER JOIN situacao s ON (m.id_situacao = s.id)
                    INNER JOIN situacao s1 ON (m.id_situacao_iniciar = s1.id)
                    INNER JOIN situacao s2 ON (m.id_situacao_finalizar = s2.id)
                    INNER JOIN tempo t1 ON (m.dt_inicio_situacao = t1.id)
                    INNER JOIN tempo t2 ON (m.dt_fim_situacao = t2.id)
                    INNER JOIN fase_processual fp ON (m.id_fase_processual = fp.id)
                WHERE 
                    -- Filtra por data e hora da movimentação
                    (p.data_ultima_movimentacao > %s OR (p.data_ultima_movimentacao = %s AND horario_movimentacao > %s))
                ORDER BY p.data_ultima_movimentacao DESC, horario_movimentacao DESC;
            """, (ultima_data, ultimo_horario))
            
            novas_movimentacoes = await cursor.fetchall()
            return novas_movimentacoes
    finally:
        await conn.close()