import logging
import azure.functions as func
import xml.etree.ElementTree as ET
import glob as g
#Added this file in Git
def main(req: func.HttpRequest ,inputblob: func.InputStream, outputblob: func.Out[func.InputStream]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    root = ET.Element('catalog') # root tag name
    root.text = '\n'    # newline before the book element

    
    test = inputblob.readlines()
    #for filename in g.glob(path):
    #    with open(filename) as f:
            #firstline = f.readlines(1)    
    firstline = test[0].decode()
    tags = [word for line in firstline for word in line.split(',')]       
    
    for line in test:   
        line =line.decode()            
        if '\n' in line:
            

            book = ET.SubElement(root, 'book')
            book.text = '\n'
            book.tail = '\n\n'

        # Split the line into a List.
            F1 = line.split(',')
                        
        count = 0
        for data in F1:                            
            tags1 = tags[count].strip()     
            e = ET.SubElement(book, tags1.lower())
            e.text = data.strip()
            e.tail = '\n'
            count += 1                 

        # Display for debugging            
        #ET.dump(root)
            

        # Include the root element to the tree and write the tree
        # to the file.
        tree = ET.ElementTree(root)
        #tree.write('C:/Users/xs54tso/VSCode/csvtoxml/InsertRecords.xml', encoding='utf-8', xml_declaration=True)
        #f.close()
        outputblob.set(ET.tostring(root))

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
