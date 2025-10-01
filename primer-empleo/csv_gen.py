import pandas as pd
import random
import faker

fake = faker.Faker()

def generate_data(n=6000, seed=42):
    random.seed(seed)

    education_levels = ["High School", "Vocational Training", "Bachelor", "Master"]
    studies = [
        "Computer Science", "Business Administration", "Marketing", 
        "Mechanical Engineering", "Nursing", "Tourism", "Graphic Design",
        "Electrical Engineering", "Education", "Law"
    ]
    job_titles = [
        "Junior Developer", "Data Analyst", "Sales Assistant", "Marketing Intern", 
        "HR Assistant", "Nurse Assistant", "Receptionist", "Graphic Designer",
        "Electrician Assistant", "Teacher Assistant"
    ]
    cities = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Logroño", "Zaragoza"]
    companies = ["TechSolutions", "InnovaCorp", "GlobalBiz", "MediCare", "TravelX", "DesignHub"]

    job_requirements = {
        "Junior Developer": {"education": ["Bachelor", "Vocational Training"], "english": True, "studies": ["Computer Science", "Electrical Engineering"]},
        "Data Analyst": {"education": ["Bachelor", "Master"], "english": True, "studies": ["Computer Science", "Business Administration"]},
        "Sales Assistant": {"education": ["High School", "Vocational Training"], "english": False, "studies": ["Business Administration", "Marketing"]},
        "Marketing Intern": {"education": ["Bachelor"], "english": True, "studies": ["Marketing", "Business Administration"]},
        "HR Assistant": {"education": ["Bachelor"], "english": True, "studies": ["Business Administration", "Law"]},
        "Nurse Assistant": {"education": ["Vocational Training", "Bachelor"], "english": False, "studies": ["Nursing"]},
        "Receptionist": {"education": ["High School", "Vocational Training"], "english": True, "studies": ["Tourism", "Business Administration"]},
        "Graphic Designer": {"education": ["Vocational Training", "Bachelor"], "english": False, "studies": ["Graphic Design"]},
        "Electrician Assistant": {"education": ["Vocational Training"], "english": False, "studies": ["Electrical Engineering"]},
        "Teacher Assistant": {"education": ["Bachelor", "Master"], "english": True, "studies": ["Education"]}
    }

    contract_types = ["Internship", "Part-time", "Full-time"]

    data = []
    for _ in range(n):
        # Generate user profile
        name = fake.name()
        age = random.randint(18, 25)
        edu = random.choice(education_levels)
        eng = random.choice([True, False])
        study = random.choice(studies)
        user_city = random.choice(cities)
        has_car = random.choice([True, False])

        # Pick a matching job
        possible_jobs = [job for job, req in job_requirements.items() 
                         if edu in req["education"] and 
                            (not req["english"] or eng) and 
                            study in req["studies"]]
        
        if possible_jobs:
            job = random.choice(possible_jobs)
        else:
            job = random.choice(job_titles)

        # Job details
        company = random.choice(companies)
        job_city = random.choice(cities)
        salary = random.choice(["€900-1100", "€1100-1300", "€1300-1500"])
        contract = random.choice(contract_types)

        data.append([
            name, age, user_city, has_car, edu, eng, study,
            job, company, job_city, salary, contract
        ])

    df = pd.DataFrame(data, columns=[
        "name", "age", "user_city", "has_car", "education_level", "english", "studies",
        "job", "company", "job_city", "salary_range", "contract_type"
    ])
    return df

if __name__ == "__main__":
    df = generate_data()
    df.to_csv("historic.csv", index=False)
    print("Synthetic dataset saved to historic.csv")
    print(df.head())
