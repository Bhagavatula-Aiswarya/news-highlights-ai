import pandas as pd

def generate_highlights(df, cross_source_freq, duplicate_groups, preferred_source='ABC News', top_n=5):
    scored = []
    for idx, row in df.iterrows():
        text = f"{row['title']} {row['content']}".lower()
        keyword_score = sum(kw in text for kw in ['breaking news', 'urgent', 'exclusive', 'alert', 'just in'])
        cross_source_score = cross_source_freq.get(idx, 0)
        score = keyword_score * 2 + cross_source_score * 3
        scored.append({**row, "idx": idx, "score": score})

    scored_df = pd.DataFrame(scored)
    used = set()
    highlights = []

    for group in duplicate_groups:
        candidates = scored_df[scored_df['idx'].isin(group)]
        if preferred_source in candidates['source'].values:
            best = candidates[candidates['source'] == preferred_source].iloc[0]
        else:
            best = candidates.sort_values("score", ascending=False).iloc[0]
        highlights.append(best)
        used.update(group)

    unique = scored_df[~scored_df['idx'].isin(used)]
    final = pd.concat([pd.DataFrame(highlights), unique])
    return (
        final.groupby("category", group_keys=False)
        .apply(lambda x: x.sort_values(by="score", ascending=False).head(top_n))
        .reset_index(drop=True)
    )
