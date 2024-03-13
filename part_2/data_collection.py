# %%
import pandas as pd
import sqlite3
import os

def write_to_sqlite(dataframe, file_path, table_name='data_table', index=False, if_exists='replace'):
    # Connect to the SQLite database
    conn = sqlite3.connect(file_path)

    # Write the DataFrame to SQLite
    dataframe.to_sql(table_name, conn, index=index, if_exists=if_exists)

    # Close the database connection
    conn.close()

def encode_columns(dataframe, column_names):
    # Create a copy of the original DataFrame to avoid modifying the original data
    encoded_df = dataframe.copy()

    # Create reference DataFrames for each column
    reference_dfs = []
    for col in column_names:
        # Encode the column and add it to the DataFrame
        encoded_column = encoded_df[col].astype('category').cat.codes
        encoded_df[col + '_id'] = encoded_column

        # Create a reference DataFrame
        reference_df = pd.DataFrame({
            'Original_' + col: encoded_df[col],
            'Encoded_' + col: encoded_column
        })

        reference_dfs.append(reference_df.drop_duplicates())

    # Remove the original columns from the encoded DataFrame
    encoded_df = encoded_df.drop(columns=column_names)

    # Return the list of DataFrames [encoded_df, reference_df1, reference_df2, ...]
    return [encoded_df] + reference_dfs

def get_reddit_comments(r_script_path = 'Reddit_scrape.R'):
    # This function will run the R script developed to retrieve the reddit comments
    from rpy2.robjects import r
    
    reddit_comments_path = 'reddit_scrape.txt'
    if os.path.exists(reddit_comments_path):
        pass
    else:
        try:
            with open(r_script_path, 'r') as r_file:
                r_script_content = r_file.read()

            # Run the R script
            r(r_script_content)
        
        except Exception as e:
            print(f"Error: {e}")
            
            return None
    

    df = []

    for chunk in pd.read_csv(
        reddit_comments_path,
        chunksize = 10_000,
        encoding = 'windows-1252',
        sep = "\t",
        on_bad_lines = 'skip'
    ):
        df.append(chunk)
    
    df = pd.concat(df)

    return df

def get_linkedin_skills(python_script_path = 'SkillsScrape.py'):
    import subprocess

    linkedin_skills_path = 'linkedin_skills.csv'
    
    if os.path.exists(linkedin_skills_path):
        pass
    else:
        try:
            subprocess.run(
                [
                    'python'
                    , python_script_path
                ]
            )
        except Exception as e:
            print(f"Error: {e}")

            return None

    df = pd.read_csv(
        linkedin_skills_path,
        encoding='utf-8',
        sep='\t'
    )

    return df

def main():    
    # Get our linkedin data
    linkedin_skills = get_linkedin_skills()
    linkedin_skills.head()

    # Get our reddit comments data
    reddit_comments = get_reddit_comments()
    reddit_comments = reddit_comments[reddit_comments['date'].notna()]
    reddit_comments.head()

    # Encode the reddit data
    r_comments, r_authors, r_posts = encode_columns(
        reddit_comments,
        [
            'author',
            'url'
        ]
    )

    # Write the comments data to a sqlite file
    write_to_sqlite(
        r_comments
        , "reddit.db"
        , table_name='reddit_comments'
        , index = False
        , if_exists = 'replace'
    )

    write_to_sqlite(
        r_authors
        , "reddit.db"
        , table_name='reddit_authors'
        , index = False
        , if_exists = 'replace'
    )

    write_to_sqlite(
        r_posts
        , "reddit.db"
        , table_name='reddit_posts'
        , index = False
        , if_exists = 'replace'
    )

    write_to_sqlite(
        linkedin_skills
        , 'reddit.db'
        , table_name = 'linkedin_skills'
        , index = False
        , if_exists = 'replace'
    )
    
# %%
if __name__ == '__main__':
    main()
# %%
