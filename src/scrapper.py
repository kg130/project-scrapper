from bs4 import NavigableString, Comment


def getProjectList(soup):
    projectList = soup.find('div', class_='list')
    projectIdList = []
    if (projectList):
        projectItems = projectList.find_all('div', class_='item')
        for project in projectItems:
            projectTitle = project.find('div', class_='item-title')
            projectId = projectTitle.find('a')
            projectIdList.append(projectId['href'])

    return projectIdList


def getValue(cell):
    a = ''
    for child in cell.children:
        if isinstance(child, NavigableString) and not isinstance(child, Comment):
            a+=(child.strip().replace('\n', '\t'))
        else:
            a+=(child.get_text().strip().replace('\n', '\t'))
        a+=('\t')
    return a

def getProjectInfo(soup, fileInst, link):
    metaList = {}
    appendLink = False

    tableList = soup.find_all('table', class_='pds')
    if (tableList):
        for table in tableList:
            rows = table.find_all('tr')
            headRow = rows[0].find('th')
            for row in rows:
                cells = row.find_all('td')
                if (cells):
                    if (headRow):
                        metaList[headRow.get_text() + ' - ' + cells[0].string] = getValue(cells[1])
                    else:
                        metaList[cells[0].string] = getValue(cells[1])

    # Milestone Table
    milestoneTable = soup.find_all('table', class_='milestones')
    if (milestoneTable):
        if (len(milestoneTable) != 1):
            appendLink = True

        rows = milestoneTable[0].find_all('tr')
        columnNum = int(rows[0].find('th')['colspan'])

        if (len(rows) != 4 and columnNum != 6):
            appendLink = True
        else:
            header = rows[0].find('th').get_text()
            columnSubHead = rows[1].find_all('th')
            columnSubSubHead = rows[2].find_all('th')
            values = rows[3].find_all('td')
            ind = 0

            while(ind < columnNum):
                if (ind < 3):
                    metaList[header + ' - ' + columnSubHead[ind].get_text()] = getValue(values[ind])
                else:
                    metaList[header + ' - ' + columnSubHead[3].get_text() + ' - ' + columnSubSubHead[ind - 3].get_text()] = getValue(values[ind])

                ind += 1

    # Finance Table
    financeTable = soup.find_all('table', class_='financing')
    if (financeTable):
        if (len(financeTable) != 1):
            appendLink = True

        rows = financeTable[0].find_all('tr')

        if (len(rows) == 6):
            rowFiveValues = rows[5].find_all('td')
            if (len(rowFiveValues) != 6):
                appendLink = True
            else:
                headers = ['Financing Plan', 'Loan Utilization']
                columnSubHead = rows[1].find_all('td')
                rowCells = {}
                for i in [1, 2, 3, 4]:
                    rowCells[i] = rows[i + 1].find_all('td')
                    metaList[headers[0] + ' - ' + rowCells[i][0].get_text()] = getValue(rowCells[i][1])
                    if (i % 2 == 0):
                        for j in [1, 2, 3, 4]:
                            key = headers[1] + ' - ' + columnSubHead[j + 1].get_text() + ' - ' + rowCells[i - 1][2].get_text()
                            metaList[key] = getValue(rowCells[i][j + 1])

        elif (len(rows) == 4):
            rowFourValues = rows[3].find_all('td')
            if (len(rowFourValues) != 9):
                appendLink = True
            else:
                headers = ['Financing Plan', 'Cumulative Disbursements']
                columnSubHead = rows[1].find_all('td')
                rowThreeHead = rows[2].find_all('td')
                for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                    if (i <= 1):
                        metaList[headers[0] + ' - ' + columnSubHead[i].get_text()] = getValue(rowFourValues[i])
                    elif (i > 1 and i < 6):
                        key = headers[0] + ' - ' + columnSubHead[2].get_text() + ' - ' + rowThreeHead[i - 2].get_text()
                        metaList[key] = getValue(rowFourValues[i])
                    elif (i == 6):
                        metaList[headers[0] + ' - ' + columnSubHead[i - 3].get_text()] = getValue(rowFourValues[i])
                    else:
                        metaList[headers[1] + ' - ' + columnSubHead[i - 3].get_text()] = getValue(rowFourValues[i])

        else:
            appendLink = True

    if (appendLink):
        fileInst.write(link)
    return metaList
