import pandas as pd


def recommend_careers(student_profile, careers_df, top_n=5):
    """
    Recommend careers based on a student's interests,
    skills, academic stream, and preferred work style.
    """

    scored_careers = careers_df.copy()
    scored_careers["score"] = 0

    # Match the student's academic stream.
    stream = student_profile.get("stream", "").strip().lower()

    if stream:
        scored_careers.loc[
            (scored_careers["stream"].str.lower() == stream)
            | (scored_careers["stream"].str.lower() == "any"),
            "score",
        ] += 2

    # Match the student's interest.
    interest = student_profile.get("interest", "").strip().lower()

    if interest:
        scored_careers.loc[
            scored_careers["interest"].str.lower() == interest,
            "score",
        ] += 3

    # Match the student's strongest skill.
    skill = student_profile.get("skill", "").strip().lower()

    if skill:
        scored_careers.loc[
            scored_careers["skill"].str.lower() == skill,
            "score",
        ] += 3

    # Match the student's preferred work style.
    work_style = student_profile.get("work_style", "").strip().lower()

    if work_style:
        scored_careers.loc[
            scored_careers["work_style"].str.lower() == work_style,
            "score",
        ] += 2

    # Sort careers by their matching scores.
    recommendations = scored_careers.sort_values(
        by=["score", "career"],
        ascending=[False, True],
    )

    # Return the highest-scoring careers.
    return recommendations.head(top_n).reset_index(drop=True) 