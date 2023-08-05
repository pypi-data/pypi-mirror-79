__author__ = "houyan"


from controller.CommitToPlan import CommitToPlan
from controller.DB import DB
import time

from controller.GetMethod import GetMethod


class BuildPlanDetail:

    @staticmethod
    def genaratePlan(partnerId,branch,datetext,client,platform,planId,icase_userName,icase_pasWord,project,token):
        plan=CommitToPlan()
        #endDateText = "2020-05-22 23:00:00"
        endDateText=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        codeType = plan.codeCommitWay(partnerId, client, platform)
        #print(codeType)
        partner_result = "业务线未入库"
        client_result = "业务线的这个客户端未入库"
        platform_result = "业务线的客户端的这个平台未入库"
        if codeType == "":
            partner = DB.getPartnerName(partnerId)
            platformdb = DB.getPlatform(partnerId, client)
           #print(platformdb)
            if partner == "":
                return partner_result
            elif platformdb == "":
                return platform_result
            return client_result
        file_method=''
        if codeType=="git":
            gitInfo = DB.getGitInfo(partnerId, client, platform)
            gitId = gitInfo[0]
            tableName = gitInfo[1]
            gitLink =gitInfo[2]
            gitIdList = gitId.split(",")
            gitIdList = list(set(gitIdList))
            if platform=='server':
                gitIdList=[project]
            cmtList=plan.updateGitCommitId(token, gitIdList, branch, datetext, endDateText)
            #print(cmtList)
            git_result = GetMethod.getParallelRun(client, cmtList, token, gitLink,partnerId,platform)
            file_method = GetMethod.methodDeal(git_result)
            #print(file_method)
        elif codeType=="gerrit":
            sinceTime = datetext + '.000000000'
            untilTime = endDateText + '.000000000'
            gerritInfo = DB.getGerritInfo(partnerId, client, platform)
            user = gerritInfo[0]
            password = gerritInfo[1]
            gerritProject = gerritInfo[2]
            gerritUrl = gerritInfo[3]
            tableName = gerritInfo[4]
            rest=plan.updateGerritRest(gerritUrl, user, password)
            gerritIdList = plan.updateGerritId(rest,gerritProject, branch, sinceTime, untilTime)
            #print(gerritIdList)
            gerritFile = GetMethod.getGerritParallelRun(gerritIdList,client,gerritUrl,user,password,gerritProject)
            file_method = GetMethod.methodDeal(gerritFile)
            #print(file_method)

        return file_method




