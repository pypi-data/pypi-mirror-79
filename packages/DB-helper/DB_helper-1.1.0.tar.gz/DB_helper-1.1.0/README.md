# Example Package
> import
```python
from DB_helper import DataBase
db = DataBase(DB_helper.create_table())
```
> Create_table
```python
db.create_table()
```
>> table_name - name
>> columns - values ​​in the form "{VALUE} TYPE (sql), {VALUE} TYPE (sql)"
> Add data
```python
db.insert_data()
```
>> table_name - name
>> data - tuple dats
> Update data
```python
db.update_data()
```
>>table_name - name
>>set_name - sql
>>where_name - sql
>>set_value - sql
>>where_value - sql
>Delete data
```python
db.delete_data()
```
>>table_name - anme
>>where_name - which field to look at
>>value - value in field
>Get data
```python
db.get_data()
```
>>table_name - name
>>returned values in list