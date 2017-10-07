import requests
from xml.etree import ElementTree
import os
import json


# Retrive 
def get_arxiv(start,length=100,query='all:machine%20learning'):
    try:
        resp = requests.get('http://export.arxiv.org/api/query?search_query='+query+'&start='+str(start)+'&max_results='+str(length))
        return resp.content
    except:
        print 'error'
        return None

# Create Xml document from raw string
def xml(content):
    root = ElementTree.fromstring(content)
    return root

# Returns an array of => [id, title, summary]
# where http://arxiv.org/pdf/[id] is the pdf download link
def get_entries(xml_root):
    entries = []
    for r in xml_root.findall('{http://www.w3.org/2005/Atom}entry'):
        id = r.find('{http://www.w3.org/2005/Atom}id').text.replace('http://arxiv.org/abs/','')
        title = r.find('{http://www.w3.org/2005/Atom}title').text
        summary = r.find('{http://www.w3.org/2005/Atom}summary').text
        entries.append({'id':id,'title':title,'summary':summary})
    return entries

# Writes the entries to the json index file + Removes the doubles from the new entries
def write_entries_to_index(entries,index_file='index.json'):
    json_entries = []
    if os.path.isfile(index_file):
        with open(index_file,'r') as json_file:
            json_entries = json.loads(json_file.read())

    # Add to json entries + Prevent doubles from the entry list
    existing_ids = [entry['id'] for entry in json_entries]
    new_entries = []
    for e in entries:
        if e['id'] in existing_ids:
            continue
        json_entries.append(e)
        new_entries.append(e)

    with open(index_file,'w') as json_file:
        json_file.write(json.dumps(json_entries))
    return new_entries

# Downloads the pdfs from the entry ids to a folder
def download_pdfs(entries,folder='pdfs'):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    for e in entries:
        try:
            print '[Downloading... ' + e['id'] + ']'
            resp = requests.get('https://arxiv.org/pdf/'+e['id']+'.pdf')

            # If no pdf exists, continue
            if resp.headers['Content-Type'] != 'application/pdf':
                print 'Not PDF'
                continue
            
            with open(folder+'/'+e['id']+'.pdf', 'wb') as file:
                file.write(resp.content)
        except:
            print '[PDF-Download-Error: id='+e['id']+' could not be downloaded!]'
            continue

for i in range(0,1000,100):
    print 'Retriving entries [',i,'/',i+100,']'
    raw = get_arxiv(i,length=100)
    print 'Extracting xml entries...'
    xml_root = xml(raw)
    entries = get_entries(xml_root)
    print 'Writing to json index...'
    entries = write_entries_to_index(entries,index_file='index.json')
    print 'Downloading PDFs...'
    download_pdfs(entries,folder='pdfs')






