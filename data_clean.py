import pandas as pd
import ast

fec_data = pd.read_csv('HouseData.csv', encoding='unicode_escape')
# fec_data['normalize_name'] = fec_data['name'].str.split(',').str[1].str.strip() + " " + fec_data['name'].str.split(',').str[0]
fec_data['normalize_name'] = fec_data['name'].str.split(',')
vote_data = pd.read_csv('1976-2018-house3.csv', encoding='unicode_escape')
vote_data['year'] = vote_data['year'].tolist()
vote_data = vote_data[vote_data['year'] >= 2008]
vote_data = vote_data[~vote_data['candidate'].isna()]
print()

master_df = pd.DataFrame()
for group in fec_data.groupby(by='candidate_election_year'):
    year = group[0]
    group = group[1]
    for row in group.iterrows():
        row = row[1]
        try:
            val = vote_data[((vote_data['candidate'].str.contains(row['normalize_name'][0])) |
                            (vote_data['candidate'].str.contains(row['normalize_name'][1]))) &
                            (vote_data['state_po'] == row['state']) & (vote_data['year'] == year)]

            if len(val) > 0:
                append_df = pd.DataFrame(row).T
                append_df['candidatevotes'] = int(val['candidatevotes'].iloc[0])
                append_df['totalvotes'] = int(val['totalvotes'].iloc[0])
                master_df = master_df.append(append_df)
        except Exception as e:
            print(row['name'], e)
    print()
master_df['percent_vote'] = master_df['candidatevotes'] / master_df['totalvotes']
master_df.loc[master_df['percent_vote'] > .5, 'win'] = 1
master_df.loc[master_df['percent_vote'] <= .5, 'win'] = 0
master_df['election_years'] = master_df['election_years'].str.replace('{', '[').str.replace('}', ']').apply(ast.literal_eval)
master_df['num_terms'] = master_df['election_years'].str.len() - 1
to_csv = master_df[['candidate_id', 'name', 'party', 'state', 'incumbent_challenge_full', 'candidate_election_year',
                    'receipts', 'disbursements', 'cash_on_hand_end_period', 'debts_owed_by_committee', 'percent_vote',
                    'win', 'num_terms']]
master_df.to_csv('cleaned_election_data.csv', index=False)
to_csv.to_csv('subset_cleaned_election_data.csv', index=False)
print()
