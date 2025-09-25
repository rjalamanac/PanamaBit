# generate_csv.py
import csv
import random
from datetime import datetime, timedelta
import faker

fake = faker.Faker('es_ES')

titles = [
    "Técnico en mantenimiento", "Analista de datos", "Ingeniero de software",
    "Gestor administrativo", "Abogado laboral", "Inspector de trabajo",
    "Técnico de sistemas", "Responsable de RRHH", "Economista", "Técnico de calidad"
]

contracts = ["Contrato indefinido", "Contrato temporal", "Prácticas", "Contrato por obra"]

def random_date(start, end):
    delta = end - start
    days = random.randrange(delta.days)
    return (start + timedelta(days=days)).strftime("%Y-%m-%d")

def make_description(title):
    base = f"Búsqueda de {title} para tareas relacionadas con el área laboral. "
    tasks = [
        "Gestión de documentación sindical y contratos colectivos.",
        "Análisis de datos y elaboración de informes estadísticos.",
        "Soporte técnico a plataformas digitales internas.",
        "Atención y asesoramiento a empresas y trabajadores.",
        "Supervisión de procesos y control de calidad de datos."
    ]
    reqs = [
        "Se requiere experiencia mínima de 2 años.",
        "Valorable titulación universitaria.",
        "Se valorará experiencia con Python y bases de datos.",
        "Conocimientos de normativa laboral.",
        "Capacidad de trabajo en equipo y comunicación."
    ]
    return base + " ".join(random.sample(tasks, 2)) + " " + " ".join(random.sample(reqs, 2))

def generate_csv(path="data/jobs.csv", N=200):
    start = datetime(2018,1,1)
    end = datetime(2025,12,31)
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["id","title","employer","location","contract_number","start_date","end_date","description","requirements"]
        writer.writerow(header)
        for i in range(1, N+1):
            title = random.choice(titles)
            employer = fake.company()
            location = fake.city()
            contract_number = f"CINT-{random.randint(1000,9999)}-{random.choice(['MX','PA'])}"
            sd = random_date(start, end)
            ed = random_date(datetime.strptime(sd, "%Y-%m-%d"), end)
            description = make_description(title)
            requirements = "; ".join(random.sample(["python", "sql", "analisis estadistico", "excel avanzado", "nlp", "gestion documental"], 3))
            writer.writerow([i, title, employer, location, contract_number, sd, ed, description, requirements])
    print(f"CSV generado en {path} con {N} filas.")

if __name__ == "__main__":
    generate_csv()
