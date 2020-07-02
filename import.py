from models import *
from bs4 import BeautifulSoup
from datetime import date

with open('CCCBR_methods.xml', 'r') as f:
    xml = f.read()

soup = BeautifulSoup(xml, 'lxml')

for mset in soup.find_all('methodset'):
    if not mset.name: continue # catches the extraneous '\n's
    # first, step through the <properties> tag and put values in a dictionary
    mset_dict = {prop.name: prop.string 
                 for prop in mset.properties.children 
                 if prop.name}
    # next, get a list of any boolean attributes on the classification tag
    mset_bools = [ attr for attr in mset.properties.classification.attrs ]

    for method in mset.find_all('method'):
        if not method.name: continue # catches the extraneous '\n's
        print('Working on: ' + method.name)
        method_db = Method(id=int(method['id'][1:]))
        for prop, val in mset_dict.items():
            print('... ' + str(prop) +','+ str(val))
            # We need to special-case notes, which is ambiguous — both msets and methods have notes
            if prop == 'notes':
                prop = 'methodset_notes'
            setattr(method_db, prop, val)
        for attr in mset_bools:
            print('... ' + str(attr))
            setattr(method_db, attr, True)
        for tag in method.children:
            if not tag.name: continue # catches the extraneous '\n's
            # skip these — we deal with them below
            if tag.name == 'references' or tag.name == 'performances': continue
            print('... ' + str(tag))
            setattr(method_db, tag.name, tag.string)

        # get all the references
        if not method.references:
            continue
        print('... references:')
        for tag in method.references.children:
            if not tag.name: continue # catches the extraneous '\n's
            print('... ' + str(tag))
            setattr(method_db, tag.name, tag.string)
        session.add(method_db)

        # Next, do the performances
        if not method.performances:
            continue
        print('... performances:')
        for performance in method.performances.children:
            if not performance.name: continue
            print('... ... ' + str(performance.name))
            performance_db = Performance()
            performance_db.kind = performance.name
            for tag in performance.children:
                if not tag.name: continue # catches the extraneous '\n's
                if tag.name == 'location': continue # we'll do this later
                print('... ... ' + str(tag))
                # special-case date tag, for formatting
                if tag.name == 'date':
                    setattr(performance_db, tag.name, date.fromisoformat(tag.string))
                    continue
                setattr(performance_db, tag.name, tag.string)
            if not performance.location: continue
            for tag in performance.location.children:
                if not tag.name: continue # catches the extraneous '\n's
                print('... ... ' + str(tag))
            performance_db.method = method_db
            session.add(performance_db)


session.commit()

            

    
