# in this branch i'll chane grabber.py to wind folders
#

import variables
import mapper
import saveFiles
import crawler
#import urllib.request
import sql_connector
import os
import time


def grab(siteUrl):
    """downloads the website"""

    # give values to the resource & crawlFrontier lists => crawl
    siteName = mapper.extractName(siteUrl)[0]

    #scan the site for the links from the home page
    crawler.crawlSite(siteUrl, siteName)

    # sort all the links & resources in decreasing order
    variables.allPaths = variables.crawlFrontier + variables.resources
    variables.allPaths.sort(reverse=True)

    ##################!
    '''
    To download a specific urls uncomment the row below and add the list of urls to parse there 
    '''
    #variables.allPaths = []
    ###################

    # make a directory
    try:
        os.chdir(variables.homeDirectory)
        os.makedirs(siteName)
    except Exception as e: print(e)
    finally:
        os.chdir(siteName)

    # first download all the pages
    for indx, row in enumerate(variables.allPaths):
        print("Done: "+str(round( (indx / len(variables.allPaths)*100), 2))+"%")
        saveFiles.save1(row, siteName)


"""-----------DRIVER CODE-----------"""


if __name__ == "__main__":
        
    try:


        ###################
        #Change here:
        variables.homeDirectory = r'C:\Users\15764\Site'
        ###################


        #for windows only
        if variables.homeDirectory[-1] != "\\":
            variables.homeDirectory += '\\'


        os.chdir(variables.homeDirectory)


        '''get list fo the urls to parse:'''
        # get a list of the sites form sql
        # the path to table can be specified in get_work_list function
        sites_to_process = sql_connector.get_work_list('list_of_sites2')

        # the local .csv can be used either
        # sites_to_process = pd.read_csv('file_to_read.csv')

        # print the list of the sites:
        list_of_sites = sites_to_process.website.tolist()

        print("Next sites will be parsed:\n"+"\n".join(str(x) for x in list_of_sites)+"\n-------")
        time.sleep(3)



        # every site downloading to local, processing and added to database
        for index, row in sites_to_process.iterrows():
            variables.seed = row.iloc[0]
            variables.div = row.iloc[1]
            variables.ent = row.iloc[2]
            variables.bu = row.iloc[3]
            print("Starting work with: ", str(variables.seed))


            # check the entirety of the url
            if 'http://' not in variables.seed and 'https://' not in variables.seed:
                variables.seed = 'http://' + variables.seed
            if variables.seed[-1] != '/':
                variables.seed += '/'

            #run the driving function
            grab(variables.seed)

            #--------end with the site
            print('Resources= ', variables.resources)
            print('Links= ', variables.crawlFrontier)
            print("DONE WITH "+str(variables.seed)+"\n------------------------")
            time.sleep(5)
            sql_connector.add_to_log(row)
            os.chdir(variables.homeDirectory)

    except Exception as e:
        print(e)
