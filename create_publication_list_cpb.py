# -*- coding: utf-8 -*-
from Bio import Entrez
import pandas as pd

Entrez.email = 'geena.ildefonso@vanderbilt.edu' #can update email here 


def search(query):
    """ search a name across pubmed and return pubmed ids of publications

    :param query: string of format "first_name last_name"
    :return: string of ids of papers
    """

    query_string = '%s[AU] AND vanderbilt university[AD]' % query
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='20',
                            retmode='xml',
                            term=query_string)
    try:
        results = Entrez.read(handle, validate=True)
    except AttributeError:
        print("did not find any for %s" % query)
        return
    if 'Count' in results:
        if results['Count'] == '0':
            return
    else:
        return
    id_list = results['IdList']
    ids = ",".join(id_num for id_num in id_list)

    return ids


# loads in data, formatted file has FirstName, LastName, and papers as column headers
df = pd.read_csv('student_names_list.csv', index_col=False)

# empty list to stores papers column
new_papers = []
for i, row in df.iterrows():
    first_name = str(row['FirstName'])
    last_name = str(row['LastName'])
    full_name = '%s %s' % (first_name, last_name)
    tmp_papers = search(full_name)

    # if they don't have any publications, None will be returned
    # Nothing to do, so return empty string to new_papers column
    if tmp_papers is None:
        new_papers.append('')
        continue

    # if it isn't None, lets make it a list
    tmp_papers = tmp_papers.split(',')

    # get the current papers
    current_papers = row['papers']

    # if it isn't a string, the person hasn't published anything yet
    if type(current_papers) != str:
        current_papers = []
        papers_to_add = ''
    # if it is, split the row to a list
    # will keep the papers that already exist, add on to that string
    else:
        current_papers = current_papers.split(',')
        papers_to_add = row['papers']

    # iterate through new papers, check to see if it is already accounted for
    # if not, print it to screen, add it to the string
    for j in tmp_papers:
        if j in current_papers:
            continue
        else:
            print(last_name, j)
            papers_to_add += j + ','
    new_papers.append(papers_to_add)

# resetting column with new paper lsit
df['papers'] = new_papers
# saving to file
df.to_csv('student_names_list.csv', index=False)
