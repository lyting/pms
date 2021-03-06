# -*- coding: utf-8 -*-
'''测试结果管理操作

@author: Wang Qianxiang
'''

from .db import Demand, ActivityMember, TestCase, TestSet, Case_Set, TestResult, User


def create_test_result(test_result):
    '''新建测试结果'''
    dev_id = list(TestCase.select(
        ActivityMember.memberId.alias('devId')
    ).join(
        Demand,
        on=(TestCase.demandId == Demand.id)
    ).join(
        ActivityMember,
        on=(Demand.activityId == ActivityMember.activityId)
    ).where(
        (TestCase.id == test_result['caseId']) & (ActivityMember.role == "dev")
    ).dicts())[0]['devId']

    return TestResult.get_or_create(
        name=test_result['name'],
        detail=test_result['detail'],
        testSetId=test_result['setId'],
        caseId=test_result['caseId'],
        output=test_result['output'],
        status=test_result['status'],
        devId=dev_id,
        level=test_result['level'],
        priority=test_result['priority'],
        releaseId=test_result['releaseId'],
        ownerId=test_result['ownerId'])


def update_test_results(test_result):
    '''更新测试结果'''
    TestResult.update(
        name=test_result['name'],
        detail=test_result['detail'],
        testSetId=test_result['setId'],
        caseId=test_result['caseId'],
        output=test_result['output'],
        status=test_result['status'],
        level=test_result['level'],
        priority=test_result['priority']).where(
            TestResult.id == test_result['id']).execute()
    return test_result_detail(test_result['id'])


def test_result_detail(r_id):
    '''获取测试结果详情'''
    return TestResult.sfind(
        TestResult,
        TestResult.testSetId.alias('setId'),
        TestCase.name.alias('caseName'),
        TestSet.name.alias('setName'),
        User.username.alias('devName')
    ).join(
        TestCase,
        on=(TestResult.caseId == TestCase.id)
    ).join(
        TestSet,
        on=(TestResult.testSetId == TestSet.id)
    ).join(
        User,
        on=(TestResult.devId == User.id)
    ).where(TestResult.id == r_id).get()


def find_test_result_by_id(test_result_id):
    '''按test_result_id查询测试结果'''
    return TestResult.getOne(TestResult.id == test_result_id)


def find_test_result_by_name(name):
    '''按case_id和set_id查询测试结果'''
    return TestResult.getOne(TestResult.name == name)


def search_set_list(r_id):
    '''查询测试集'''
    return TestSet.sfind().where(TestSet.releaseId == r_id).dicts()

def search_case_list(s_id, r_id):
    '''查询测试集相关测试案例'''
    return TestCase.sfind().join(
        Case_Set,
        on=(TestCase.id == Case_Set.caseId)
    ).where(
        (TestCase.releaseId == r_id) & (Case_Set.setId == s_id)
    ).dicts()
