from collections import Counter

def score_articles(df, similar_df, priority_keywords=None):
    if priority_keywords is None:
        priority_keywords = ['breaking news', 'urgent', 'exclusive', 'alert', 'just in']

    cross_source_freq = Counter()
    duplicate_groups = []

    for _, row in similar_df.iterrows():
        i1, i2 = int(row['index_1']), int(row['index_2'])
        if df.loc[i1, 'source'] != df.loc[i2, 'source']:
            cross_source_freq[i1] += 1
            cross_source_freq[i2] += 1
            duplicate_groups.append({i1, i2})

    merged_groups = []
    for pair in duplicate_groups:
        added = False
        for group in merged_groups:
            if not pair.isdisjoint(group):
                group.update(pair)
                added = True
                break
        if not added:
            merged_groups.append(set(pair))

    return cross_source_freq, merged_groups
