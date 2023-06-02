from sqlalchemy import create_engine
from sqlalchemy import text, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session
# входная функция create_and_push, основная функция преобразования create_new_db_table, проверил на тестовой таблице - все работает 

test_table = [
    (1, None, "Напитки"),
    (2, 1, "Соки"),
    (3, 2, "Апельсиновые соки"),
    (4,	3, "Rich апельсиновый"),
    (5,	3, "J7 апельсиновый"),
    (6,	3, "Добрый апельсиновый"),
    (7, 2, "Берёзовый сок"),
    (8,	1, "Минеральная вода"),
    (9,	8, "Минеральная вода газ."),
    (10, 9, "Монастырская газ."),
    (11, 9, "Сосновская газ."),
    (12, 8, "Минеральная вода негаз."),
    (13, 12, "Монастырская негаз."),
    (14, 12, "Сосновская негаз."),
    (15, None, "Крупы"),
    (16, 15, "Рис"),
    (17, 15, "Гречка"), 
]

# получение списка родителей для элемента
def get_hierarchy(parent_id, parent_table: list):
    if not parent_id:
        return []
    return get_hierarchy(parent_table[parent_id - 1][1], parent_table) + [(parent_table[parent_id - 1][2])]


def create_new_db_table(parent_table: list = test_table):
    new_table = list(); id = list(); parent_id = list() 
    
    # разделение исходной таблицы на столбцы id и parent_id
    for table_str in parent_table:
        id.append(table_str[0])
        parent_id.append(table_str[1])
    
    # получение новой таблицы
    for i in range(len(parent_table)):
        if id[i] not in parent_id:
            new_table.append([parent_table[i][0], parent_table[i][2]] + get_hierarchy(parent_table[i][1], parent_table))
    
    new_table_fin = list()
    for data in new_table:
        if len(data) < len(max(new_table, key=len)):
            new_table_fin.append(data + [None] * (len(max(new_table, key=len)) - len(data)))
        else:
            new_table_fin.append(data)
    return new_table_fin    


def connect_to_db(path_to_db):
    engine = create_engine(path_to_db)
    return engine


def create_and_push(table_name, path_to_db):   #table_name = "EMPLOYEE", path_to_db = "postgresql://postgres:rootroot@localhost/intership"
    try:
        engine = connect_to_db(path_to_db)
        session = Session(engine)
        with session as conn:
            # получение исходной таблицы
            response = conn.execute(text(f'SELECT * FROM "{table_name}"'))
            source_table = response.all()
            
            # создание, заполнение и отправка таблицы на сервер бд
            new_table = create_new_db_table(source_table); table_columns = list()
            for i in range(len(max(new_table, key=len))):
                if i == 0:
                    table_columns.append(Column('Id', Integer, primary_key=True))
                elif i == 1:
                    table_columns.append(Column('Name', String))
                else:
                    table_columns.append(Column(f'Parent_Name_{i - 1}', String))
                
            metadata = MetaData()
            new_db_table = Table('Table2', metadata, *table_columns)
            metadata.create_all(engine)
            for data in new_table:
                conn.execute(new_db_table.insert().values(data))
            conn.commit()
        return 0
    except:
        return 1
        

        
        
        
        


           
                
       
            
    
    
        
        



