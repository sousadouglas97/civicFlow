from datetime import date, time
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.config.connect import engine


async def buscar_novas_movimentacoes(ultima_data: date, ultimo_horario: str):
      async with AsyncSession(engine) as conn:
        async with conn.begin():
          result = await conn.execute(text("""
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
                      (t."data" > :ultima_data OR 
                      (t."data" = :ultima_data AND m.horario > :ultimo_horario))
                  ORDER BY p.data_ultima_movimentacao DESC, m.horario DESC;
              """), {'ultima_data': ultima_data, 'ultimo_horario': ultimo_horario})
          
        novas_movimentacoes = result.fetchall()
        return novas_movimentacoes

