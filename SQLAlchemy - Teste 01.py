import sqlalchemy as db
import pymysql.cursors
import pandas as pd

DB_USER = 'root'
DB_PASS = 'abc123**'
DB_HOST = 'localhost'
DB_PORT = '3306'
DATABASE = 'db_meuslivros'
string_con = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DB_USER,DB_PASS,DB_HOST,DB_PORT,DATABASE)

# Criar engine
engine = db.create_engine(string_con)

# Criar a conexão
con = engine.connect()
print('Conexão realizada com sucesso!')

# Carregar informações de uma tabela (metadados)
metadata = db.MetaData()
livros = db.Table('tbl_livros',metadata,autoload=True,autoload_with=engine)

# Imprimir os nomes das colunas da tabela
#print(livros.columns.keys())

# Imprimir os metadados completos da tabela
#print(repr(metadata.tables['tbl_livros']))

# CONSULTAS
consulta = db.select([livros])

ResultProxy = con.execute(consulta)
ResultSet =  ResultProxy.fetchall()
print(ResultSet[:3])

# Converter em DataFrame Pandas para visualização:
df = pd.DataFrame(ResultSet)
print(df)
# Ver somente os nomes das colunas:
df.columns = ResultSet[0].keys()
print(df.columns)

# Consulta retornado duas colunas:
consulta = db.select([livros.columns.NomeLivro,livros.columns.PrecoLivro])
res = con.execute(consulta).fetchall()
df = pd.DataFrame(res)
print(df)

# Consulta com filtro
# Usando método filter
#consulta = db.select([livros.columns.NomeLivro,livros.columns.PrecoLivro]).filter(livros.columns.PrecoLivro > '200.00')
# Usando método where
consulta = db.select([livros.columns.NomeLivro,livros.columns.PrecoLivro]).where(livros.columns.PrecoLivro > '200.00')
# Para testes: imprimir o SQL formado:
#print(consulta)
res = con.execute(consulta).fetchall()
df = pd.DataFrame(res)
print(df)

