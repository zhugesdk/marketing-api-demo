"""基于智能触达2.0API，命令行Demo
"""
import os
import json
import copy
import base64
from urllib.parse import urljoin
from typing import List, Dict
import click
import requests

ANALYZE_API_URL = os.environ["ANALYZE_API_URL"]  # 分析API base url
MARKETING_API_URL = os.environ["MARKETING_API_URL"]  # 触达API base url

API_USERNAME = os.environ["ZHUGE_API_USERNAME"]  # API用户名
API_PASSWORD = os.environ["ZHUGE_API_PASSWORD"]  # 密码

GET_GROUPS_API = urljoin(
    ANALYZE_API_URL,
    "/v2/api_user_groups/{app_id}/user/groups")

GET_CHANNEL_CONFIG_API = urljoin(
    MARKETING_API_URL,
    "/market/api/v2/postman/channel/{app_id}/{channel_type}")

CREATE_ACTIVITY_API = urljoin(
    MARKETING_API_URL,
    "/market/api/v2/activity/create"
)

VIEW_ACTIVITY_DETAILS_API = urljoin(
    MARKETING_API_URL,
    "/market/api/v2/activity/{id}"
)

PAUSE_ACTIVITY_API = urljoin(
    MARKETING_API_URL,
    "/market/api/v2/activity/pause"
)

CONTINUE_ACTIVITY_API = urljoin(
    MARKETING_API_URL,
    "/market/api/v2/activity/continue"
)

DELETE_ACTIVITY_API = urljoin(
    MARKETING_API_URL,
    "/market/api/v2/activity/delete"
)

GET_ALL_ACTIVITIES_API = urljoin(
    MARKETING_API_URL,
    "/market/api/v2/activity/{type}/all"
)

GET_ACTIVITY_USER_RECORDS_API = urljoin(
    MARKETING_API_URL,
    "/market/api/v2/statistics/users"
)


class APIException(Exception):
    """当调用API失败时抛出此异常
    """

    def __init__(self, msg: str):
        super().__init__(msg)


class UserGroup:
    """人群信息
    """

    @classmethod
    def from_data(cls, data):
        return cls(**data)

    def __init__(self,
                 group_id: int,
                 group_name: str,
                 user_count: int,
                 create_time: str):
        """
        :param group_id: 人群ID
        :param group_name: 人群名称
        :param user_count: 用户数目
        :param create_time: 创建时间
        """

        self.group_id = group_id
        self.group_name = group_name
        self.user_count = user_count
        self.create_time = create_time

    def __repr__(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    def __str__(self):
        return self.__repr__()


class WebhookChannelConfig:
    """webhook渠道配置信息
    """

    def __init__(self,
                 channel_id: int,
                 display_name: str,
                 enable: bool,
                 send_type: str,
                 url: str,
                 params: List[Dict]):
        """
        :param channel_id: 渠道ID
        :param display_name: 显示名称
        :param enable: 是否可用
        :param send_type: 发送类型 sms push weixin other
        :param url: 请求地址
        :param params: 渠道参数
        """
        self.channel_id = channel_id
        self.display_name = display_name
        self.enable = enable
        self.send_type = send_type
        self.url = url
        self.params = params

    def __repr__(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    def __str__(self):
        return self.__repr__()


class ActivityTypes:
    """活动类型
    """

    AUTO = "auto"  # 自动活动

    MANUAL = "manual"  # 手动活动


class ActivityStatus:
    """活动状态
    """
    RUNNING = 0  # 运行中

    WAITING = 7  # 定时等待中

    PAUSED = 2  # 已暂停

    FINISHED = 6  # 已完成


class GlobalStatistics:

    """全局统计指标
    """

    @classmethod
    def from_data(cls, data):
        return GlobalStatistics(
            data["trigger"]["s"],
            data["send"]["s"],
            data["send"]["f"],
            data["target"]["s"],
            data["target"]["f"]
        )

    def __init__(self,
                 trigger_success: int,
                 send_success: int,
                 send_failure: int,
                 target_success: int,
                 target_failure: int):
        """
        :param trigger_success: 触发成功
        :param send_success: 发送成功
        :param send_failure: 发送失败
        :param target_success: 转化成功
        :param target_failure: 转化失败
        """
        self.trigger_success = trigger_success
        self.send_success = send_success
        self.send_failure = send_failure
        self.target_success = target_success
        self.target_failure = target_failure


class ActivityCreator:

    """活动创建者信息
    """

    @classmethod
    def from_data(cls, data):
        return cls(
            user_id=data["id"],
            name=data["name"],
            account=data["account"]
        )

    def __init__(self, user_id: int, name: str, account: str):
        """
        :param user_id: 用户ID
        :param name: 用户名称
        :param account: 账号
        """
        self.user_id = user_id
        self.name = name
        self.account = account


class Activity:

    """活动信息
    """

    @classmethod
    def from_data(cls, data):
        return cls(
            activity_id=data["id"],
            app_id=data["appId"],
            name=data["name"],
            activity_type=data["type"],
            status=data["status"],
            units=data["units"],
            begin_time=data.get("beginTime", ""),
            end_time=data.get("endTime", ""),
            creator=ActivityCreator.from_data(data["creator"]),
            global_statistics=GlobalStatistics.from_data(data["globalStatistics"]),
            created_on=data["createdOn"]
        )

    def __init__(self,
                 activity_id: int,
                 app_id: int,
                 name: str,
                 activity_type: str,
                 status: int,
                 units: List[Dict],
                 begin_time: str,
                 end_time: str,
                 creator: ActivityCreator,
                 global_statistics: GlobalStatistics,
                 created_on: str):
        """
        :param activity_id: 活动ID
        :param app_id: 应用ID
        :param name: 活动展示名称
        :param activity_type: 活动类型 auto - 自动 manual - 手动
        :param status 活动状态
        :param units: 工作单元
        :param begin_time: 开始时间
        :param end_time: 结束时间
        :param creator 创建者信息
        :param global_statistics 全局统计信息
        :param created_on 创建时间
        """
        self.activity_id = activity_id
        self.app_id = app_id
        self.name = name
        self.activity_type = activity_type
        self.status = status
        self.units = units
        self.begin_time = begin_time
        self.end_time = end_time
        self.creator = creator
        self.global_statistics = global_statistics
        self.created_on = created_on

    def is_auto_activity(self):
        return ActivityTypes.AUTO == self.activity_type

    def is_manual_activity(self):
        return ActivityTypes.MANUAL == self.activity_type

    def is_running(self):
        return self.status == ActivityStatus.RUNNING

    def is_waiting(self):
        return self.status == ActivityStatus.WAITING

    def is_paused(self):
        return self.status == ActivityStatus.PAUSED

    def is_finished(self):
        return self.status == ActivityStatus.PAUSED

    def to_dict(self):
        data = copy.copy(self.__dict__)
        data["creator"] = copy.copy(self.creator.__dict__)
        data["global_statistics"] = copy.copy(self.global_statistics.__dict__)
        return data

    def __repr__(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    def __str__(self):
        return self.__repr__()


class ActivityUserRecord:
    """活动衡量用户记录
    """

    @classmethod
    def from_data(cls, data):
        return cls(
            data["zgId"],
            data["cusProperties"],
            data["fixedProperties"]
        )

    def __init__(self,
                 zg_id: int,
                 cus_properties: Dict,
                 fixed_properties: Dict):
        """
        :param zg_id: 用户的系统ID
        :param cus_properties: 自定义用户属性 属性名 -> 属性值
        :param fixed_properties: 分析平台内置用户属性 属性名 -> 属性值
        """
        self.zg_id = zg_id
        self.cus_properties = cus_properties
        self.fixed_properties = fixed_properties

    def __repr__(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    def __str__(self):
        return self.__repr__()


def _gen_authorization() -> str:
    """API验证信息生成
    """
    return base64.b64encode(("%s:%s" % (
        API_USERNAME,
        API_PASSWORD
    )).encode()).decode("UTF-8")


def _check_response(api_name: str, response) -> dict:
    """检查API响应结果
    :return API响应结果数据
    """
    if response.status_code != 200:
        raise APIException(
            "Invalid %s API status code: %d" % (api_name, response.status_code)
        )
    data = response.json()
    if data["code"] != 200:
        raise APIException(
            "Invalid %s API return code: %d, msg: %s" % (
                api_name, data["code"], data["msg"])
        )
    return data["data"]


@click.command(help="获取分析平台人群列表")
@click.option("--app_id", type=int, required=True, help="应用ID")
@click.option("--limit", type=int, default=100, help="展示个数")
def get_all_groups(app_id: int, limit: int):
    response = requests.get(
        GET_GROUPS_API.format(app_id=app_id),
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        },
        params={
            "limit": limit
        }
    )

    if response.status_code != 200:
        raise APIException(
            "Invalid group API status code: %d" %
            response.status_code
        )

    group_data_list = response.json()["results"]
    for group_data in group_data_list:
        print(UserGroup.from_data(group_data))


@click.command(help="获取所有webhook类型渠道配置")
@click.option("--app_id", type=int, required=True, help="应用ID")
def get_all_webhook_channels(app_id: int):
    response = requests.get(
        GET_CHANNEL_CONFIG_API.format(app_id=app_id, channel_type="webhook"),
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        }
    )

    response_data = _check_response("get all webhook channels", response)
    all_config_data = response_data["configs"]["user_properties_webhook"]
    for webhook_config_data in all_config_data.values():
        print(WebhookChannelConfig(
            webhook_config_data["id"],
            webhook_config_data["display_name"],
            webhook_config_data["enable"],
            webhook_config_data["config"]["send_type"],
            webhook_config_data["config"]["url"],
            webhook_config_data["config"]["params"]
        ))


def _create_activity(
        app_id: int,
        name: str,
        units: List[Dict],
        creator: str,
        begin_time: str = None,
        end_time: str = None) -> Activity:
    """
    :param app_id: 应用ID
    :param name: 活动展示名称
    :param units: 活动单元编排
    :param creator: 创建者账号
    :param begin_time: 开始时间
    :param end_time: 结束时间
    :return: 新创建的活动对象
    """
    # 组装请求数据
    post_data = {
        "appId": app_id,
        "name": name,
        "units": units,
        "creator": creator
    }

    if begin_time:
        post_data["beginTime"] = begin_time
    if end_time:
        post_data["endTime"] = end_time

    response = requests.post(
        CREATE_ACTIVITY_API,
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        },
        json=post_data
    )
    response_data = _check_response("create activity", response)
    return Activity.from_data(response_data)


@click.command(help="创建手动活动示例")
@click.option("--app_id", type=int, required=True, help="应用ID")
@click.option("--name", type=str, required=True, help="活动名称")
@click.option("--crowd_id", type=int, required=True, help="人群ID")
@click.option("--channel_id", type=int, required=True, help="渠道ID")
@click.option("--channel_params_json", required=True, type=str, help="渠道参数JSON描述")
@click.option("--target_event_name", type=str, required=True, help="目标事件名称")
@click.option("--timeout_expr", type=str, required=True, help="超时时间表达式")
@click.option("--creator", type=str, required=True, help="创建者账号")
@click.option("--begin_time", type=str, default="", help="开始时间")
def create_manual_activity(
        app_id: int,
        name: str,
        crowd_id: int,
        channel_id: int,
        channel_params_json: str,
        target_event_name: str,
        timeout_expr: str,
        creator: str,
        begin_time: str):
    activity = _create_activity(
        app_id=app_id,
        name=name,
        units=[
            {
                "name": "unit_0",
                "type": "crowdTrigger",
                "args": {
                    "crowd": crowd_id
                },
                "success": [
                    "unit_1"
                ]
            },
            {
                "name": "unit_1",
                "type": "webhook",
                "args": {
                    "channelId": channel_id,
                    "params": json.loads(channel_params_json)
                },
                "success": [
                    "unit_2"
                ]
            },
            {
                "name": "unit_2",
                "type": "target",
                "args": {
                    "timeout": timeout_expr,
                    "events": [
                        {
                            "eventName": target_event_name
                        }
                    ]
                }
            }
        ],
        creator=creator,
        begin_time=begin_time
    )
    print(activity)


@click.command(help="创建自动活动示例")
@click.option("--app_id", type=int, required=True, help="应用ID")
@click.option("--name", type=str, required=True, help="活动名称")
@click.option("--trigger_event_name", type=str, required=True, help="触发事件名称")
@click.option("--channel_id", type=int, required=True, help="渠道ID")
@click.option("--channel_params_json", type=str, required=True, help="渠道参数JSON描述")
@click.option("--sleep_time_expr", type=str, required=True, help="触发后的休眠时间")
@click.option("--target_event_name", type=str, required=True, help="目标事件名称")
@click.option("--timeout_expr", type=str, required=True, help="超时时间表达式")
@click.option("--creator", type=str, required=True, help="创建者账号")
@click.option("--begin_time", type=str, default="", help="活动开始时间")
@click.option("--end_time", type=str, default="", help="活动结束时间")
def create_auto_activity(
        app_id: int,
        name: str,
        trigger_event_name: str,
        channel_id: int,
        channel_params_json: str,
        sleep_time_expr: str,
        target_event_name: str,
        timeout_expr: str,
        creator: str,
        begin_time: str,
        end_time: str):
    activity = _create_activity(
        app_id=app_id,
        name=name,
        units=[
            {
                "name": "unit_0",
                "type": "onceEventTrigger",
                "args": {
                    "events": [
                        {
                            "eventName": trigger_event_name
                        }
                    ]
                },
                "success": [
                    "unit_1"
                ]
            },
            {
                "name": "unit_1",
                "type": "sleep",
                "args": {
                    "time": sleep_time_expr
                },
                "success": [
                    "unit_2"
                ]
            },
            {
                "name": "unit_2",
                "type": "webhook",
                "args": {
                    "channelId": channel_id,
                    "params": json.loads(channel_params_json)
                },
                "success": [
                    "unit_3"
                ]
            },
            {
                "name": "unit_3",
                "type": "target",
                "args": {
                    "timeout": timeout_expr,
                    "events": [
                        {
                            "eventName": target_event_name
                        }
                    ]
                }
            }
        ],
        creator=creator,
        begin_time=begin_time,
        end_time=end_time
    )
    print(activity)


@click.command(help="查看活动详情")
@click.option("--activity_id", type=int, required=True, help="活动ID")
def view_activity(activity_id: int):
    response = requests.get(
        VIEW_ACTIVITY_DETAILS_API.format(id=activity_id),
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        }
    )
    activity = Activity.from_data(
        _check_response("view activity details", response))
    print(activity)


@click.command(help="暂停活动执行")
@click.option("--activity_id", type=int, required=True, help="活动ID")
def pause_activity(activity_id: int):
    response = requests.post(
        PAUSE_ACTIVITY_API,
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        },
        json={
            "id": activity_id
        }
    )
    activity = Activity.from_data(
        _check_response("pause activity", response))
    print(activity)


@click.command(help="恢复已经暂停的活动")
@click.option("--activity_id", type=int, required=True, help="活动ID")
def continue_activity(activity_id: int):
    response = requests.post(
        CONTINUE_ACTIVITY_API,
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        },
        json={
            "id": activity_id
        }
    )
    activity = Activity.from_data(
        _check_response("continue activity", response))
    print(activity)


@click.command(help="删除指定活动")
@click.option("--activity_id", type=int, required=True, help="活动ID")
def delete_activity(activity_id: int):
    response = requests.post(
        DELETE_ACTIVITY_API,
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        },
        json={
            "id": activity_id
        }
    )
    _check_response("delete activity", response)
    print("Deleted! %d" % activity_id)


@click.command(help="根据类型查询活动列表")
@click.option("--app_id", type=int, required=True, help="应用ID")
@click.option("--activity_type", type=str, required=True,
              help="活动类型 auto - 自动活动 manual - 手动活动")
def get_activity_list(app_id: int, activity_type: str):
    response = requests.get(
        GET_ALL_ACTIVITIES_API.format(type=activity_type),
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        },
        params={
            "appId": app_id
        }
    )
    all_activity_data_list = _check_response("get activity list", response)["activities"]
    for activity_data in all_activity_data_list:
        activity = Activity.from_data(activity_data)
        print(activity)


@click.command(help="查询活动的用户洞察记录")
@click.option("--activity_id", type=int, required=True, help="活动ID")
@click.option("--type", type=str, default="", help="统计动作类型 trigger-触发 send-发送 target-转化")
@click.option("--status", type=str, default="", help="执行状态 s-成功 f-失败")
@click.option("--unit", type=str, default="", help="活动单元名称")
@click.option("--send_type", type=str, default="", help="发送类型 sms-短信 push-推送 weixin-微信 other-其它")
@click.option("--begin_date", type=str, default="", help="起始查询时间")
@click.option("--end_date", type=str, default="", help="结束查询时间")
@click.option("--page", type=int, default=1, help="分页")
@click.option("--rows", type=int, default=20, help="每页显示行数")
def query_user_records(
        activity_id: int,
        type: str,
        status: str,
        unit: str,
        send_type: str,
        begin_date: str,
        end_date: str,
        page: int,
        rows: int):
    # 拼接查询参数
    params = {
        "activityId": activity_id,
        "page": page,
        "rows": rows
    }
    for param_name, param_val in (
        ("type", type),
        ("status", status),
        ("unit", unit),
        ("sendType", send_type),
        ("beginDate", begin_date),
        ("endDate", end_date),
        ("page", page),
        ("rows", rows)
    ):
        if param_val:
            params[param_name] = param_val

    response = requests.get(
        GET_ACTIVITY_USER_RECORDS_API,
        headers={
            "Authorization": "Basic %s" % _gen_authorization()
        },
        params=params
    )
    user_data_list = _check_response("query user records", response)["users"]
    for user_data in user_data_list:
        user_record = ActivityUserRecord.from_data(user_data)
        print(user_record)


@click.group()
def cli():
    ...


if __name__ == "__main__":
    for func in (
        get_all_webhook_channels,
        get_all_groups,
        get_activity_list,
        view_activity,
        pause_activity,
        continue_activity,
        delete_activity,
        create_auto_activity,
        create_manual_activity,
        query_user_records
    ):
        cli.add_command(func)
    cli()
