import pandas as pd
from lxml import objectify


def xml_to_df(xml):
    root = xml.getroot()

    document_ids = [document['id'].text for document in root.getchildren()]
    document_vols = [document['vol'].text for document in root.getchildren()]
    document_bodies = [document['body'].text for document in root.getchildren()]

    data = {'id': document_ids, 'vol': document_vols, 'body': document_bodies}
    return pd.DataFrame(data)


def split_pages(df):
    # Matches strings like "[p.12]", "[p.123]" ... which were used as page delimiters in the XML,
    split_re = r'\[p\.\d+\]'
    # Split body by page separator and explode each split item into new row
    df = pd.DataFrame(df.body.str.split(split_re).tolist(), index=df.vol).stack()
    # Use volume and page number as cols rather than indices.
    df = df.reset_index(level=[0, 1])
    # Rename newly-created columns.
    df.columns = ['vol', 'page', 'body']
    # Remove rows with empty strings
    df = df[df['body'] != '']

    return df

# Replace by appropriate path ...
path_to_xml = 'archives_berberes_v2.xml'
xml = objectify.parse(path_to_xml)
df = xml_to_df(xml)

# Split each volume into pages .. if you want to.
df = split_pages(df)

# Insert awesome text mining project below :-)
