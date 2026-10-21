import pandas as pd
from src.recommender import recommend_careers

# Load the career dataset
careers_df = pd.read_csv("data/careers.csv")

# Sample student profile
student_profile = {
    "stream": "Science",
    "interest": "Technology",
    "skill": "Programming",
    "work_style": "Problem Solving",
}

# Generate recommendations
results = recommend_careers(
    student_profile,
    careers_df,
    top_n=5,
)

# Display recommendations
print("\n===== STUDENT CAREER RECOMMENDATIONS =====\n")

for index, career in results.iterrows():
    print(f"{index + 1}. {career['career']}")
    print(f"   Match Score: {career['score']}")
    print(f"   Description: {career['description']}")
    print() 