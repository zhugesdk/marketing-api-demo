# 智能触达2.0开放API

[TOC]

## 概述

智能触达2.0为开发者提供了各功能模块的开放API，基于这些API，您可以：

* 与您内部的系统紧密结合。比如打通您的运营后台，当新的商品上架时，自动创建一个与之相关的推广活动。
* 通过API进行二次开发，满足自己的个性化需求。

按照功能模块，智能触达API分为以下部分：

* 活动管理
  * 活动创建
  * 活动修改
  * 活动暂停
  * 活动恢复
  * 活动删除
  * 查看活动详情
  * 查看活动列表
* 效果衡量
  * 按不同维度查询计数
  * 按不同维度查询用户

下面我们将依次介绍各个模块的API详情。

## 活动管理

### 活动创建

```
[POST] /market/api/v2/activity/create
```

**Request body**

```
Content-Type: application/json;charset=utf-8
```

```json
{
  "appId": 1,
  "name": "登录用户欢迎",
  "beginTime": "2020-07-14 09:00:00",
  "endTime": "2020-07-14 10:00:00",
  "units": [
      {
        "name": "unit_trigger",
        "type": "onceEventTrigger",
        "args": {
          "events": [
            {
                "eventName": "打开APP",
                "eventProperties": [
                    {
                        "propertyName": "平台",
                        "operator": "=",
                        "params": [
                            "Android"
                        ]
                    }
                ]
            }
          ]
        },
        "success": [
            "unit_sleep"
        ]
      },
      {
          "name": "unit_sleep",
          "type": "sleep",
          "args": {
              "time": "1 minutes"
          },
          "success": [
              "unit_push"
          ]
      },
      {
          "name": "unit_push",
          "type": "push",
          "args": {
              "title": [
                  "Hi",
                  {
                      "propertyName": "姓名"
                  }
              ],
              "message": [
                  "您好！",
                  {
                      "propertyName": "姓名"
                  }
              ]
          }
      }
   ]
}
```

请求字段解释：

* `appId` 应用ID，必须
* `name` 活动的展示名称，必须
* `beginTime` 活动开始时间，格式`yyyy-MM-dd HH:mm:ss`，非必须。
* `endTime` 活动结束时间，格式`yyyy-MM-dd HH:mm:ss`，非必须。只作用于自动活动
* `units`  使用JSON描述的活动定义，必须，具体详情参见活动定义部分。

**Response body**

```
Content-Type: application/json;charset=utf-8
```

```json
{
  "code": 200,
  "data": {
    "id": 10010,
    "appId": 1,
    "status": 0,
    "name": "登录用户欢迎",
    "beginTime": "2020-07-14 09:00:00",
    "endTime": "2020-07-14 10:00:00",
    "units": [
        
    ],
    "createdOn": "2020-07-14 09:00:00"
  }
}
```

如果创建成功，会返回新创建活动的ID，这个ID是后续对活动进行诸如暂停、删除等各种操作的依据。

### 活动修改

```
[POST] /market/api/v2/activity/modify
```

**Request Body**

```
Content-Type: application/json;charset=utf-8
```

```json
{
	"id": 10010,
  "version": "0",
	"displayName": "登录用户欢迎",
	"units": [
      
  ]
}
```

请求字段解释：

* `id`  要修改的活动ID，必须。
* `version`  活动定义版本，非必须。我们的活动修改操作涉及两种不同的方式：一种是修改不会涉及到活动流程的变更，比如只是修改一下短信或者推送的文案，这种不需要指定版本，修改会应用到触发活动的所有用户；还有一种方式会涉及到活动流程的变更，比如删除了一个活动单元或者添加了一个新的单元，这种修改会对已经触发的活动实例产生影响，比如会找不到旧的单元或者活动步骤出现了错乱，这种在修改的时候就需要去指定一个版本号用来与之前的定义进行区分，这样新触发的活动实例会执行新的定义，而旧有的活动实例依然会执行过去的版本，从而达成无缝更新的目标。
* `displayName` 活动展示名称，如不修改，非必须
* `units` UI层JSON活动定义，如不修改，非必须

**Response Body**

```
Content-Type: application/json;charset=utf-8
```

```json
{
  "code": 200,
  "data": {
    "id": 10010,
    "appId": 1,
    "status": 0,
    "name": "登录用户欢迎",
    "beginTime": "2020-07-14 09:00:00",
    "endTime": "2020-07-14 10:00:00",
    "units": [
        
    ],
    "createdOn": "2020-07-14 09:00:00"
  }
}
```

### 活动暂停

```
[POST] /market/api/v2/activity/pause
```

**Request Body**

```
Content-type: application/json;charset=utf-8
```

```json
{
  "id": 10010
}
```

请求字段解释：

* `id`  活动ID

**Response Body**

```
Content-type: application/json;charset=utf-8
```

```json
{
  "code": 200,
  "data": {
    "id": 10010,
    "appId": 1,
    "status": 2,
    "name": "登录用户欢迎",
    "beginTime": "2020-07-14 09:00:00",
    "endTime": "2020-07-14 10:00:00",
    "units": [
        
    ],
    "createdOn": "2020-07-14 09:00:00"
  }
}
```

### 活动恢复

用于恢复已经被暂停的活动。

```
[POST] /market/api/v2/activity/continue
```

**Request Body**

```
Content-type: application/json;charset=utf-8
```

```
{
  "id": 10010
}
```

请求字段解释：

* `id`  活动ID

**Response Body**

```
Content-type: application/json;charset=utf-8
```

```json
{
  "code": 200,
  "data": {
    "id": 10010,
    "appId": 1,
    "status": 2,
    "name": "登录用户欢迎",
    "beginTime": "2020-07-14 09:00:00",
    "endTime": "2020-07-14 10:00:00",
    "units": [
        
    ],
    "createdOn": "2020-07-14 09:00:00"
  }
}
```

### 活动删除

```
[POST] /market/api/v2/activity/delete
```

**Request Body**

```
Content-type: application/json;charset=utf-8
```

```json
{
  "id": 10010
}
```

请求字段解释：

* `id`  活动ID

**Response Body**

```
Content-type: application/json;charset=utf-8
```

```json
{
  "code": 200,
  "data": {
    
  }
}
```

### 查看活动详情

```
[GET] /market/api/v2/activity/<ID>
```

**Response Body**

```
Content-Type: application/json;charset=utf-8
```

```json
{
  "code": 200,
  "data": {
    "id": 10010,
    "appId": 1,
    "status": 2,
    "name": "登录用户欢迎",
    "beginTime": "2020-07-14 09:00:00",
    "endTime": "2020-07-14 10:00:00",
    "units": [
      {
        "name": "unit_trigger",
        "type": "onceEventTrigger",
        "args": {
          "events": [
            {
                "eventName": "打开APP",
                "eventProperties": [
                    {
                        "propertyName": "平台",
                        "operator": "=",
                        "params": [
                            "Android"
                        ]
                    }
                ]
            }
          ]
        },
        "success": [
            "unit_sleep"
        ],
        "statistics": {
          "s": 100,
          "f": 0
        }
      }
    ],
    "globalStatistics": {
        "trigger": {
          "s": 100
        },
        "send": {
          "s": 80,
          "f": 20
        },
        "target": {
          "s": 10,
          "f": 0
        }
    },
    "channelStatistics": {
        "other": {
          "s": 0,
          "f": 0
        },
        "weixin": {
          "s": 0,
          "f": 0
        },
        "sms": {
          "s": 0,
          "f": 0
        },
        "push": {
          "s": 0,
          "f": 0
        }
    },
    "sendErrorReasonCounts": [
        {
            "errorCode": "10000",
            "desc": "系统错误",
            "sendType": "other",
            "count": 0
        }
    ],
    "createdOn": "2020-07-14 09:00:00"
  }
}
```

响应数据说明：

* `id` 活动ID
* `appId` 应用ID
* `status` 活动状态
  * 0 - 运行中
  * 7 - 定时.等待中
  * 2 - 已暂停
  * 6 - 已完成
* `name` 活动展示名称
* `beginTime` 活动开始时间
* `endTime` 活动结束时间
* `units` 活动单元
  * `name` 单元名称，在整个活动定义里面唯一，供其它单元引用
  * `type` 单元类型
  * `args` 单元参数，不同类型的单元参数不同。参见活动定义章节
  * `success` 执行成功后的下一步去向
  * `fail` 执行失败后的下一步去向
  * `statistics` 单元执行汇总结果
    * `s` - 执行成功数目
    * `f` - 执行失败数目
* `globalStatistics` 活动全局统计数据
  * `trigger` 触发
    * `s` 总触发数目
  * `send`
    * `s` 总发送成功数目
    * `f` 总发送失败数目
  * `target`
    * `s` 总转化成功数目
    * `f` 总转化失败数目
* `channelStatistics` 各个渠道类型的发送数目统计
* `sendErrorReasonCounts` 各个发送错误原因的数目统计
* `createdOn` 活动创建时间

### 查看活动列表

```
[GET] /market/api/v2/activity/<activityType>/all
```

* `activityType`
  * `auto` 自动活动
  * `manual` 手动活动

**Response body**

```
Content-Type: application/json;charset=utf-8
```

```json
{
  "code": 200,
  "data": {
    "activities": [
      {
        "id": 10010,
    		"appId": 1,
    		"status": 2,
    		"name": "登录用户欢迎",
    		"beginTime": "2020-07-14 09:00:00",
    		"endTime": "2020-07-14 10:00:00",
        "globalStatistics": {
            "trigger": {
              "s": 0
            },
            "send": {
              "s": 0,
              "f": 0
            },
            "target": {
              "s": 0,
              "f": 0
            }
        }
      }
    ]
  }
}
```

## 效果衡量

通过效果衡量API，可以实现自定义的日报，以及对数据进行更充分的利用，比如对某个活动结果的人群进行深入分析后再进行二次营销。

### 按时间范围查询计数

```
[GET] /market/api/v2/statistics/common?id=<id>&beginDate=2020-07-14&endDate=2020-07-20
```

**Query Param**

查询参数解释：

* `id` 活动id 必须
* `beginDate` 开始日期 必须
* `endDate` 结束日期 必须

**Response body**

```
Content-Type: application/json;charset=utf-8
```

```json
{
    "code": 200,
    "msg": "成功",
    "data": {
        "series": [
            {
                "names": [
                    "触发人次"
                ],
                "values": [
                    0,
                    0,
                    0,
                    5186
                ]
            },
            {
                "names": [
                    "发送人次"
                ],
                "values": [
                    0,
                    0,
                    0,
                    5186
                ]
            },
            {
                "names": [
                    "发送成功人次"
                ],
                "values": [
                    0,
                    0,
                    0,
                    2440
                ]
            },
            {
                "names": [
                    "达成目标人次"
                ],
                "values": [
                    0,
                    0,
                    0,
                    0
                ]
            }
        ],
        "xAxis": [
            "2020-07-12",
            "2020-07-13",
            "2020-07-14",
            "2020-07-15"
        ]
    }
}
```

* `xAxis` 时间轴
* `series` 对应于时间轴上各个指标的数据
  * `name` 指标名称
  * `values` 针对`xAxis`上每个时间点的值

### 按不同维度洞察用户

```
[GET] /market/api/v2/statistics/users
```

**Query Param**

查询参数解释

* `id` 活动ID，必须
* `type` 统计类型，可选
  * trigger - 触发动作
  * send - 发送动作
  * target 转化动作
* `status` 状态，可选
  * s - 成功
  * f - 失败
* `unit` 活动单元名称，可选
* `sendType` 发送类型，可选
  * sms - 短信
  * push 推送
  * weixin - 微信
  * other - 其它
* `beginDate` 开始时间，可选
* `endDate` 结束时间，可选
* `page` 分页，必须
* `rows` 每页最大获取行数，必须

参数组合示例

以上参数可以进行灵活组合，以满足不同维度的查询需要。

查询指定活动的触发用户

```
[GET] /market/api/v2/statistics/users?id=1&type=trigger&page=1&rows=100
```

查询在07-10到07-15日触发的用户：

```
[GET] /market/api/v2/statistics/users?id=1&type=trigger&beginDate=2020-07-10&endDate=2020-07-15&page=1&rows=100
```

查询所有发送失败的用户

```
[GET] /market/api/v2/statistics/users?id=1&type=send&status=f&page=1&rows=100
```

查询所有短信发送失败的用户

```
[GET] /market/api/v2/statistics/users?id=1&sendType=sms&status=f&page=1&rows=100
```

查询某个单元执行成功的用户

```
[GET] /market/api/v2/statistics/users?id=1&unit=<unitName>&status=s&page=1&rows=100
```

**Response Body**

```
Content-Type: application/json;charset=utf-8
```

```json
{
  "code": 200,
  "data": {
    "users": [
      {
        "zgId": 107301,
        "cusProperties": [
          {
            "propertyName": "xxxx",
            "propertyValue": "xxxxx"
          }
        ],
        "fixedProperties": [
          {
            "propertyName": "xxxx",
            "propertyValue": "xxxxx"
          }
        ]
      }
    ]
  }
}
```

* users 洞察用户列表
  * zgId - 系统ID
  * cusProperties 自定义属性
    * propertyName 属性名称
    * propertyValue 属性值
  * fixedProperties 内置属性
    * propertyName 属性名称
    * propertyValue 属性值

## 活动定义

### 整体格式

#### 活动单元

每个活动单元的基本格式

```json
{
  "name": "unit_name",
  "type": "unitType",
  "args": {
    "arg1": "value1",
    "arg2": "value2",
    "arg3": "value3"
  },
  "success": [
    
  ],
  "fail": [
    
  ],
  "annotations": {
    "k1": "v1",
    "k2": "v2",
    "k3": "v3"
  }
}
```

属性说明：

* `name` 单元名称，必须，在一个活动定义中，单元名称必须要唯一。
* `type` 单元类型，必须
* `args` 单元接受的参数，必须
* `success` 当单元返回成功，或者单元无返回时，下一步的流程走向。
* `fail` 当单元返回失败，下一步的流程走向。
* `annotations` 注解，可选，注解是一个字典，但系统不会做任何处理，只是原样保存并且返回，可用于夹带开发者自己所需要的一些标记数据。

#### 整体活动定义

```json
"units": [
    {
      "name": "unit_0",
      "type": "onceEventTrigger",
      "args": {
        "events": [
          {
            "properties": [
              {
                
              }
            ]
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
        "time": "minutes(1)"
      },
      "success": [
        "unit_2",
        "unit_3"
      ]
    }
]
```

* 数组中的第一个单元必须是自动活动或手动活动的触发单元
* 其余的单元顺序没有要求，系统会按照执行结果以及success和fail中的编排进行查找。

### 自动活动触发单元

#### 某个事件

某个事件类型的触发条件基于单次事件触发判定，可以包含或者条件。单元定义：

```json
{
  "name": "unit_0",
  "type": "onceEventTrigger",
  "args": {
    "events": [
      {
        "eventName": "打开APP",
        "eventProperties": [
          {
            "propertyName": "平台",
            "operator": "=",
            "params": [
              "Android"
            ]
          },
          {
            "propertyName": "渠道",
            "operator": "=",
            "params": [
              "360",
              "baidu"
            ]
          }
        ]
      },
      {
        "eventName": "登录APP"
      }
    ],
    "target": {
        "timeout": "1 days",
        "events": [
            {
              "eventName": "提交订单"
            }
        ]
    }
  },
  "success": [
    "next_unit"
  ]
}
```

* `name` 单元名称，需要在活动定义中保持唯一
* `type` 单元类型，某个事件类型的触发为`onceEventTrigger`
* `args` 参数
  * `events` 事件条件列表，必须，允许指定多个事件，这些事件是并且的关系
  * `target` 未完成的转化事件条件，可选
    * `timeout` 转化等待时间，支持的时间单位：
      * `minutes` 分钟
      * `hours` 小时
      * `days` 天
    * `events` 事件条件列表，允许指定多个事件，这些事件是并且的关系
      * `eventName` 事件名称
      * `eventProperties` 事件属性比较条件
        * `propertyName` 事件属性名
        * `operator` 比较运算符，支持的比较运算符
          * `<`
          * `<=`
          * `>`
          * `>=`
          * `=`
          * `!=`
          * `contains` 字符串包含
          * `not contains` 字符串不包含
          * `begin with` 字符串前缀匹配
          * `not begin with` 字符串前缀匹配取反
          * `end with` 字符串后缀匹配
          * `not end with` 字符串后缀匹配取反
        * `params` 比较参数，通过数组指定多个目标值，只要一个值满足条件，就会通过判断

#### 多个事件

多个事件的触发，事件与事件之间会维系状态。用于满足多个事件之前并且条件的匹配。单元定义：

```json
{
  "name": "unit_0",
  "type": "multiEventTrigger",
  "args": {
    "timeout": "10 days",
    "events": [
      {
        "eventName": "打开APP",
        "eventProperties": [
          {
            "propertyName": "平台",
            "operator": "=",
            "params": [
              "Android"
            ]
          },
          {
            "propertyName": "渠道",
            "operator": "=",
            "params": [
              "360",
              "baidu"
            ]
          }
        ]
      },
      {
        	"eventName": "登录APP",
          "eventProperties": [
            {
            	"propertyName": "位置",
            	"operator": "=",
            	"params": [
              	"北京",
              	"上海"
            	]
          	}
          ]
      },
      {
        	"eventName": "访问首页"
      }
    ],
    "target": {
        "timeout": "1 days",
        "events": [
            
        ]
    }
  },
  "success": [
    "unit_1"
  ]
}
```

* `type` 固定为`multiEventTrigger`
* `args` 参数
  * `timeout` 等待超时时间，如果在指定时间内达不到并且条件，则触发失败
  * `events` 事件表达列表，事件之间是并且关系
  * `target` 转化目标

### 用户属性比较单元

用户属性比较单元的定义需要分两种情况进行讨论。第一种是独立的用户属性比较单元，单元之中的属性是并且关系。

<img src="独立用户属性比较.jpg"/>

```json
{
  "name": "unit_1",
  "type": "userProperty",
  "args": {
    "properties": [
      {
        "propertyName": "性别",
        "propertValue": {
        	"operator": "=",
        	"params": [
          	"男"
        	]
        }
      },
      {
        "propertyName": "is_anonymous",
        "propertyValue": {
        	"operator": "=",
        	"params": [
          	"实名"
        	]
        }
      }
    ]
  },
  "success": [
    "unit_a"
  ],
  "fail": [
    "unit_b"
  ]
}
```

* `type` 固定为`userProperty`
* `args` 参数
  * `properties` 用户属性条件，之间是并且关系
* `success` 满足比较条件后的流程走向
* `fail` 不满足比较条件的流程走向

并列的用户属性比较单元，单元与单元之间是或者关系，从左到右，最左边的单元匹配优先。

<img src="并列用户属性比较.jpg"/>

单元定义：

```json
[
	{
  	"name": "unit_1",
  	"type": "weixin",
  	"args": {
    
  	},
  	"success": [
      "unit_2",
      "unit_3"
    ]
	},
  {
    "name": "unit_2",
    "type": "userProperty",
    "args": {
      "properties": [
      	{
        	"propertyName": "性别",
          "propertyValue": {
        		"operator": "=",
        		"params": [
          		"男"
        		]
          }
      	},
      	{
        	"propertyName": "is_anonymous",
          "propertyValue": {
        		"operator": "=",
        		"params": [
          		"实名"
        		]
          }
      	}
    	]
    },
    "success": [
      "unit_a"
    ]
  },
  {
      "name": "unit_3",
      "type": "userProperty",
      "args": {
          "properties": [
              {
                  "propertyName": "地区",
                	"propertyValue": {
                  	"operator": "=",
                  	"params": [
                     	 "北京"
                  	]
                  }
              }
          ]
      },
      "success": [
        "unit_b"
      ],
    	"fail": [
        "unit_c"
      ]
  }
]
```

### 转化目标单元

独立的目标单元，在指定的时间内等待或者关系的多个事件

```json
{
  "name": "unit_4",
  "type": "target",
  "args": {
    "timeout": "1 days",
    "events": [
      {
        "eventName": "开户",
        "eventProperties": []
      },
      {
        "eventName": "转账",
        "eventProperties": []
      }
    ]
  },
  "success": [
    "unit_a"
  ],
  "fail": [
    "unit_b"
  ]
}
```

* `type` 类型固定为`target`

* `args`
  * `timeout` 超时时间
  * `events` 事件列表，彼此之间是或者关系

* `success` 转化成功的流程走向

* `fail` 转化失败的流程走向

### AB测试单元

AB测试单元可以按照指定的概率，将用户路由到指定的目标单元。

```json
[
    {
        "name": "unit_1",
        "type": "ab",
        "args": {},
        "success": [
            "unit_2",
            "unit_3",
            "unit_4"
        ]
    },
    {
        "name": "unit_2",
        "type": "abItem",
        "args": {
            "name": "A",
            "weight": 20
        },
        "success": [
            "unit_a"
        ]
    },
    {
        "name": "unit_3",
        "type": "abItem",
        "args": {
            "name": "B",
            "weight": 30
        },
        "success": [
            "unit_b"
        ]
    },
    {
        "name": "unit_4",
        "type": "abItem",
        "args": {
            "name": "C",
            "weight": 50
        },
        "success": [
            "unit_c"
        ]
    }
]
```

其定义被划分为两个层次，首先有一个`type`为`ab`的父单元，其`success` 参数指向了各个子分支。子分支的`type`为`abItem`，包含了每个分支的名称、概率，以及跳转单元。

### 等待单元

等待单元允许您指定等待固定的时长，再执行下一步的流程。定义如下：

```json
{
  "name": "unit_1",
  "type": "sleep",
  "args": {
    "time": "1 days"
  },
  "success": [
    "unit_2"
  ]
}
```

单元参数：

* `time` 等待时长

### 动作单元 - 内置短信

```json
{
  "name": "unit_1",
  "type": "sms",
  "args": {
    "channel": "diexin",
    "tplId": "tplId",
    "tplArgs": [
      "text1",
      {
        "propertyType": "official",
        "propertyName": "zg_id"
      },
      "text2"
    ]
  }
}
```

* `type` 固定为sms
* `args` 参数
  * `channel` 渠道代号，目前只支持diexin(碟信)和rly(容联云)
  * `tplId` 短信模板ID
  * `tplArgs` 短信模板参数，按第三方约定的模板参数位置填写

### 动作单元 - 内置推送

```json
{
      "name": "unit_push",
      "type": "push",
      "args": {
        "title": [
          "aaaaa",
          {
            "propertyName": "name"
          },
          {
            "propertyName": "is_anonymous"
          }
        ],
        "message": [
          "aaaaa",
          {
            "propertyName": "name"
          }
        ]
      },
      "success": [
        "next_unit"
      ]
    }
```

* `type` 类型为push
* `args`
  * `title` 推送标题
    * 数组中可以穿插字符串和用户属性，系统会自动将它们完整拼接起来。
  * `message` 推送消息内容
    * 数组中可以穿插字符串和用户属性，系统会自动将它们完整拼接起来。
* `success` 

### 动作单元 - webhook

```json
{
    "name": "unit_2",
    "type": "webhook",
    "args": {
        "channelId": 3,
        "params": {
          "name": [
            "Hello,",
            {
              "propertyName": "name"
            }
          ]
        }
    },
    "success": [
      "unit_3"
    ]
}
```

* `type`为webhook
* `args`
  * `channelId` 使用的渠道ID
  * `params` 渠道配置的自定义参数，其中每个参数都是一个数组形式，可以穿插字符串和用户属性，系统会自动将它们完整拼接起来。

### 手动活动触发单元 - 基于诸葛分析平台的人群

手动互动触发单元从一个指定的数据源获取人群，然后分批次进行活动触发。

如果是通过诸葛分析平台的人群进行触发，只需要指定人群的ID即可(人群的ID可通过分析平台的开放API获得)：

```json
{
  "name": "unit_0",
  "type": "crowdTrigger",
  "args": {
     "crowd": -1
   },
   "success": [
      "unit_1"
   ]
}
```

* `type` 类型为`crowdTrigger`
* `args`
  * `crowd` 人群ID，如果填写-1，则表示所有用户。

### 手动活动触发单元 - 自定义数据源

除了使用ID指定现有人群，开发者也可以通过自定义接口，来自定义数据源。

```json
{
  "name": "unit_0",
  "type": "crowdTrigger",
  "args": {
     "crowdUrl": "http://test.com/crowd"
   },
   "success": [
      "unit_1"
   ]
}
```

这样系统就会自动从指定的URL地址`crowdUrl`来获取数据。`crowdUrl`指定的地址需要满足一定的协议：

* 能够接收GET方法的请求

* 可接收分页参数：

  * `page` page为第几页
  * `limit` 为每页的最大记录数目。比如系统第一次会请求`?page=1&limit=1000`，会返回前1000条；第二次会请求`?page=2&limit=1000`，会返回第二个1000条。

* 返回的Content-Type为`application/json;charset=utf-8`

* 返回的数据格式需要满足指定格式：

  ```json
  {
    "code": 200,
    "data": {
      "users": [
        "tom@zhugeio.com",
        "jack@zhugeio.com",
        "james@zhugeio.com",
      ]
    }
  }
  ```

  users为用户ID列表。其中的用户ID，要与诸葛分析平台identify使用的用户ID一致。

### 组合起来 

#### 定义自动活动触发类

当新用户注册1分钟后，发送一封欢迎邮件

```json
{
  "units": [
    {
      "name": "unitTrigger",
      "type": "onceEventTrigger",
      "args": {
        "events": [
          {
            "eventName": "注册成功"
          }
        ]
      },
      "success": [
        "unitSleep"
      ]
    },
    {
      "name": "unitSleep",
      "type": "sleep",
      "args": {
        "time": "1 minutes"
      },
      "success": [
        "unitSendMail"
      ]
    },
    {
      "name": "unitSendMail",
      "type": "webhook",
      "args": {
        "channelId": 3,
        "params": {
          "subject": [
            "您好，",
            {"propertyName": "姓名"}
          ],
          "content": [
            "欢迎注册XXX"
          ]
        }
      }
    }
  ]
}
```

#### 定义自动活动转化类

当用户提交订单后，半小时内没有支付，发送短信提醒。

```json
{
  "units": [
    {
      "name": "unitTrigger",
      "type": "onceEventTrigger",
      "args": {
        "events": [
          {
            "eventName": "提交订单"
          }
        ],
        "target": {
          "timeout": "30 minutes",
          "events": [
            {
              "eventName": "支付成功"
            }
          ]
        }
      },
      "success": [
        "unitSendSMS"
      ]
    },
    {
      "name": "unitSendSMS",
      "type": "sms",
      "args": {
        "channel": "diexin",
    		"tplId": "tplId",
    		"tplArgs": [
      		"text1",
      		{
        		"propertyName": "zg_id"
      		},
      		"text2"
    		]
      }
    }
  ]
}
```

#### 定义手动活动

对指定的人群发起直播通知推送，并跟踪收到推送的转化情况。

```json
{
  "units": [
    {
      "name": "unit_0",
      "type": "crowdTrigger",
      "args": {
         "crowd": 1
      },
      "success": [
         "unit_1"
      ]
    },
    {
      "name": "unit_1",
      "type": "push",
      "args": {
        "title": [
          "你好",
          {
            "propertyName": "name"
          }
        ],
        "message": [
          "欢迎参加618电商直播"
        ]
      },
      "success": [
        "unit_2"
      ]
    },
    {
      "name": "unit_2",
      "type": "target",
      "args": {
        "timeout": "1 days",
        "events": [
          {
            "eventName": "进入直播页面"
          }
        ]
      }
    }
  ]
}
```

## API Demo

我们通过上述API，很容易就利用Python编写了一个命令行版的智能触达工具。工具源码位于本项目的`api_demo.py`文件中。您可以借鉴此工具的代码，来使用API完成您的任务。

运行该Demo的先决条件：

* Python >= 3.5

* 安装相关Python依赖：

  * `pip3 install click`
  * `pip3 install requirements`

* 根据自己的环境，以环境变量的方式设置API访问地址和用户名密码：

  ```shell
  export ANALYZE_API_URL="http://localhost:8081"  # 分析API base url
  export MARKETING_API_URL="http://localhost:8081"  # 触达API base url

  export ZHUGE_API_USERNAME="sam"  # API用户名
  export ZHUGE_API_PASSWORD="xxxxxxxxxxxx"  # 密码
  ```

接下来就可以使用了。

直接运行，可以查看拥有哪些功能模块：

```
[root@realtime-3 logs]# python3 ./api_demo.py
Usage: api_demo.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  continue-activity         恢复已经暂停的活动
  create-auto-activity      创建自动活动示例
  create-manual-activity    创建手动活动示例
  delete-activity           删除指定活动
  get-activity-list         根据类型查询活动列表
  get-all-groups            获取分析平台人群列表
  get-all-webhook-channels  获取所有webhook类型渠道配置
  pause-activity            暂停活动执行
  query-user-records        查询活动的用户洞察记录
  view-activity             查看活动详情
```

通过`--help`查看功能的命令行选项：

```shell
[root@realtime-3 logs]# python3 ./api_demo.py create-auto-activity --help
Usage: api_demo.py create-auto-activity [OPTIONS]

  创建自动活动示例

Options:
  --app_id INTEGER            应用ID  [required]
  --name TEXT                 活动名称  [required]
  --trigger_event_name TEXT   触发事件名称  [required]
  --channel_id INTEGER        渠道ID  [required]
  --channel_params_json TEXT  渠道参数JSON描述  [required]
  --sleep_time_expr TEXT      触发后的休眠时间  [required]
  --target_event_name TEXT    目标事件名称  [required]
  --timeout_expr TEXT         超时时间表达式  [required]
  --creator TEXT              创建者账号  [required]
  --begin_time TEXT           活动开始时间
  --end_time TEXT             活动结束时间
  --help                      Show this message and exit.
```

查看当前有哪些人群，需要把`--app_id`替换为自己的应用ID：

```shell
python3 ./api_demo.py get-all-groups --app_id 20000318
```

查看当前的webhook渠道配置：

```shell
python3 ./api_demo.py get-all-webhook-channels --app_id 20000318
```

创建一个自动活动，需要把其中的参数，根据自己的平台进行替换：

```shell
python3 ./api_demo.py create-auto-activity --app_id 20000318 --name test_auto --trigger_event_name 22 --channel_id 1 --channel_params_json '{"name": ["aaaaa"]}' --sleep_time_expr "1 minutes" --target_event_name 44 --timeout_expr "5 minutes" --creator zhuge@zhugeio.com
```

刷新智能触达的产品的页面，应该就可以看见新创建的活动了。

查看活动详情：

```shell
python3 ./api_demo.py view-activity --activity_id 100
```

暂停活动：

```shell
python3 ./api_demo.py pause-activity --activity_id 100
```

恢复活动：

```shell
python3 ./api_demo.py continue-activity --activity_id 100
```

删除活动：

```shell
python3 ./api_demo.py delete-activity --activity_id 100
```

查看指定应用的自动活动列表：

```shell
python3 ./api_demo.py get-activity-list --app_id 20000318 --activity_type auto
```

**一点技巧**

通过json的方式来编写活动定义，肯定不如使用图形界面来创建活动定义方便。如果我们需要通过API来创建活动，可以先通过图形界面创建一个大致类似的，然后再通过API获取其json定义，再在此基础之上对定义进行修改。这样往往会更加方便一些，也不容易出错。
