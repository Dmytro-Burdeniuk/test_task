import pandas as pd

data = [
    {"period": "2025-11-01", "category_name": "Видача", "sum": 25000},
    {"period": "2025-11-01", "category_name": "Збір", "sum": 13000},
    {"period": "2025-12-01", "category_name": "Видача", "sum": 20000},
    {"period": "2025-12-01", "category_name": "Збір", "sum": 12000},
]

df = pd.DataFrame(data)
df.to_excel("plans_test.xlsx", index=False)

print("Файл plans_test.xlsx успішно створено")
