import os
import urllib.request

import mapper
import crawler
import variables
import doc_transform
import sql_connector

def pathBuilder(path):
    """creates the path & saves url onto file with name = fileName"""

    # path is a list storing directory structure in the apt nest order

    try:
        if len(path) != 0 and path[0] != '':
            try:
                if path[0] == '.':
                    path[0] = 'dot'
                elif path[0] == '..':
                    path[0] = 'ddot'
                os.mkdir(path[0])


            except FileExistsError:
                pass

            finally:
                os.chdir(path[0])

            pathBuilder(path[1:])
    except:
        pass


def extractFileName(path):
    """returns file name from a path"""

    test = ''

    i = len(path) - 1

    if i >= 0:
        ch = path[i]

        # check if there is any file specified in path
        while ch != '/' and i >= 0:
            test += ch
            i -= 1
            ch = path[i]

    # if completePath has just the file name i would become -1
    if i == -1:
        i = 0

    return test[:: -1], i


def extractPath(completePath):
    """separates and returns the path and filename"""

    fileName, i = extractFileName(completePath)
    path = ''

    # assign a default file name if none specified. eg: 'www.silive.in/bytepad'. It should not be an existing directory
    if fileName == '':
        fileName = 'index.html'
        path = completePath

    elif '.' not in fileName and fileName in [x[1] for x in os.walk(os.getcwd())][0]:
        fileName = 'index.html'
        path = completePath

    elif '.' not in fileName:
        fileName += '.html'
        path = completePath[:i]

    else:
        path = completePath[: i]

    # path returned does not end with a '/'
    return path, fileName


def save1(url, siteName):
    title = ''
    html = ''
    meta = ''

    """saves a file locally onto it's path and push to server"""

    different = False

    # differentiate b/w: techtrishna.in & 2013.techtrishna.in
    thisSiteName = mapper.extractNewName(url)

    if thisSiteName != siteName and thisSiteName != 'www.' + siteName:
        # make a directory
        try:
            os.makedirs(thisSiteName)
        except Exception as e: print(e)
        finally:
            os.chdir(thisSiteName)
        different = True

    # generate local path
    completePath = mapper.extractPathFromUrl(url)

    # separate path & fileName
    path, fileName = extractPath(completePath)

    # generate a list of nested directories
    path = path.split('/')

    try:
        # build the path locally
        if path != ['']:
            pathBuilder(path)

        # save the file - first var
        urllib.request.urlretrieve(url, fileName)
        print('site ='+str(variables.seed)+'\nDownloaded page: ', completePath)

        # geting the path of new file
        cleanfilepath = os.getcwd() +'\\'+ fileName

        # open new file to cleaning
        with open(cleanfilepath, 'r', encoding="utf-8") as f:
            html = f.read()
        # cleaning and writing back clean data
        with open(cleanfilepath, 'w', encoding="utf-8") as f:
            # this will cancell after sucsesfull connectivity
            f.write(doc_transform.text_from_html(html))
            print('Cleaned: ', completePath)

        title = doc_transform.extract_title(html)
        meta = doc_transform.extract_meta(html)
        html = doc_transform.text_from_html(html)

        table_name = ''.join(e for e in thisSiteName if e.isalnum())
        '''push data to sql'''
        sql_connector.push_to_server(table_name, url, meta, title, html)






    except Exception as e:
        print(e)

    finally:
        # go back to home directory
        while os.getcwd() != variables.homeDirectory + siteName:
            os.chdir('..')
