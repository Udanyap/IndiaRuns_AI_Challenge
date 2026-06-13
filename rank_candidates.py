import json

def calculate_score(candidate):
    score = 0
    reasons = []

    # Experience Score
    years = candidate["profile"]["years_of_experience"]

    if 5 <= years <= 9:
        score += 25
        reasons.append("Experience matches JD")

    # Current Title Score
    good_titles = [
        "Data Engineer",
        "Backend Engineer",
        "ML Engineer",
        "AI Engineer",
        "Machine Learning Engineer",
        "Software Engineer",
        "Data Scientist",
        "Research Engineer",
        "Search Engineer",
        "Recommendation Engineer",
        "Recommendation Systems Engineer",
        "NLP Engineer",
        "Applied ML Engineer"
    ]

    if candidate["profile"]["current_title"] in good_titles:
        score += 20
        reasons.append("Relevant engineering role")

    # Skills Score
    candidate_skills = [skill["name"] for skill in candidate.get("skills", [])]

    important_skills = [
        "NLP",
        "Fine-tuning LLMs",
        "Milvus",
        "LoRA",
        "BentoML"
    ]

    for skill in important_skills:
        if skill in candidate_skills:
            score += 5

    # Open To Work
    if candidate["redrob_signals"]["open_to_work_flag"]:
        score += 10
        reasons.append("Open to work")

    # Career History Score
    career_text = ""

    for job in candidate.get("career_history", []):
        career_text += job.get("description", "").lower() + " "

    keywords = [
        "ml",
        "machine learning",
        "recommendation",
        "search",
        "ranking",
        "retrieval",
        "embedding",
        "vector",
        "vector database",
        "llm",
        "large language model",
        "fine-tuning",
        "fine tuning",
        "reranking",
        "semantic search",
        "python",
        "spark",
        "airflow"
    ]

    matches = 0

    for word in keywords:
        if word in career_text:
            matches += 1

    career_score = min(matches * 3, 20)

    score += career_score

    if career_score > 0:
        reasons.append("Relevant ML/Data engineering background")

    # Consulting-only Penalty
    consulting_companies = [
        "TCS",
        "Infosys",
        "Wipro",
        "Accenture",
        "Cognizant",
        "Capgemini"
    ]

    if candidate.get("career_history"):
        all_consulting = True

        for job in candidate["career_history"]:
            if job["company"] not in consulting_companies:
                all_consulting = False
                break

        if all_consulting:
            score -= 10
            reasons.append("Consulting-only background")

    # Recruiter Response Rate
    if candidate["redrob_signals"].get("recruiter_response_rate", 0) > 0.3:
        score += 5
        reasons.append("Good recruiter response rate")

    # Profile Completeness
    if candidate["redrob_signals"].get("profile_completeness_score", 0) > 70:
        score += 5
        reasons.append("Complete profile")

    # Notice Period Bonus
    notice = candidate["redrob_signals"].get("notice_period_days", 999)

    if notice <= 30:
        score += 10
        reasons.append("Short notice period")
    elif notice <= 60:
        score += 5

    # Relocation Bonus
    if candidate["redrob_signals"].get("willing_to_relocate", False):
        score += 5
        reasons.append("Willing to relocate")

    # Location Bonus
    preferred_locations = [
        "Pune",
        "Noida",
        "Delhi",
        "Mumbai",
        "Hyderabad",
        "Bengaluru",
        "Bangalore",
        "Chennai"
    ]

    location = candidate["profile"].get("location", "")

    for city in preferred_locations:
        if city.lower() in location.lower():
            score += 10
            reasons.append("Preferred location")
            break

    # Service Company Penalty
    service_companies = [
        "TCS",
        "Infosys",
        "Wipro",
        "Accenture",
        "Cognizant",
        "Capgemini",
        "Mindtree"
    ]

    current_company = candidate["profile"].get("current_company", "")

    if current_company in service_companies:
        score -= 5
        reasons.append("Service company background")

    return score, ", ".join(reasons)


# ===========================
# MAIN PROGRAM
# ===========================

results = []

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:

    for i, line in enumerate(f):

        candidate = json.loads(line)

        score, reason = calculate_score(candidate)

        results.append({
            "candidate_id": candidate["candidate_id"],
            "score": score,
            "reason": reason
        })

        

print("Candidates Processed:", len(results))

results = sorted(
    results,
    key=lambda x: x["score"],
    reverse=True
)

print("\nTop 5 Candidates:\n")
print("\nTop Candidate IDs:\n")

for candidate in results[:5]:
    print(candidate["candidate_id"])

for candidate in results[:5]:
    print(candidate)

    print("\nTop Candidate Details:\n")

top_id = "CAND_0050454"

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)

        if candidate["candidate_id"] == top_id:
            print(candidate["profile"])
            print("\nCareer History:\n")
            print(candidate["career_history"])
            break

        import pandas as pd

df = pd.DataFrame(results)

# Add rank column
df["rank"] = range(1, len(df) + 1)

# Rename reason -> reasoning
df = df.rename(columns={
    "reason": "reasoning"
})

# Match sample submission format
df = df[["candidate_id", "rank", "score", "reasoning"]]

# Save file
df.to_csv("final_submission.csv", index=False)

print("Final submission file created successfully!")