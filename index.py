from bs4 import BeautifulSoup
import pandas as pd

import src.requests as requests
import src.scrapper as scrapper


baseUrl = "https://www.adb.org"
projectListPath = "/projects/status/closed-1361?page="


def main():
    pageNum = 101
    url = baseUrl + projectListPath + str(pageNum)
    continueLoop = True
    fileInst = open('projectList.txt', "a")

    while(continueLoop):
        page = requests.getPage(url)
        soup = BeautifulSoup(page, 'html.parser')
        projectIdList = scrapper.getProjectList(soup)
        for projectId in projectIdList:
            fileInst.write(projectId)
            fileInst.write('\n')
                
        pageNum += 1
        url = baseUrl + projectListPath + str(pageNum)
        continueLoop = len(projectIdList) != 0

def projectMeta():
    with open("projectList.txt") as projectList:
        projectsMeta = []
        for project in projectList:
            url = baseUrl + project
            page = requests.getPage(url.strip())
            soup = BeautifulSoup(page, 'html.parser')
            checkProjectFile = open('check-project.txt', "a")
            metaInfo = scrapper.getProjectInfo(soup, checkProjectFile, url)
            projectsMeta.append(metaInfo)
            
            # Writing out after loop in case it terminates of an error
            df = pd.DataFrame.from_dict(projectsMeta, orient='columns')
            df.to_csv('output.csv', index=False)
            print('project done: ', project)

#Start Main Function
if __name__ == "__main__":
    projectMeta()