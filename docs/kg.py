

"""
@api {get} entities/:id Get Entity
@apiName GetEntity
@apiGroup EntityCoreAPI
@apiDescription 按ID获取实体。注意，实体的@type为 实体所有@type基于cnschema分类继承关系的传递闭包，例如 [MusicGroup] => [MusicGroup, Organization, Thing]
@apiVersion 0.1.0

@apiParam {String} id <code>必须</code> Entity's unique ID.

@apiSuccess {String} type  DDefault 'EntitySearchResult'.
@apiSuccess {Object} result An Entity Object.

@apiError EntityNotFound 404. The <code>id</code> of the Entity was not found.
@apiErrorExample {json} EntityNotFound(404):
     HTTP/1.1 404 Not Found
     {
       "error": "Entity Not Found"
     }

@apiError RequestUnautorized 401. The request is unauthorized, usually missing app_key.
@apiErrorExample {json} RequestUnautorized(401):
     HTTP/1.1 401 Not Found
     {
       "error": "Request Unautorized"
     }

 @apiSuccessExample Success-Response:
      HTTP/1.1 200 OK
      {
        "@type": "EntitySearchResult",
        "result":  {
            "@id": "kg:19a1321",
            "@type": [
                "Thing",
                "Person"
            ],
            "name": "刘德华",
            "alternateName": ["华仔"],
            "dateModified": "2017-01-17T14:40:00+8:00",
            "entityScore": 192802,
            "description": "香港实力派演员、歌手。"
        }
      }
"""


"""
@api {post} entities/ Lookup Entities
@apiName LookupEntities
@apiGroup EntityCoreAPI
@apiDescription  redis lookup service。按名字 获取一组实体简略信息（@id, @type, name, entityScore)。
@apiVersion 0.1.0

@apiParam {String[]} names <code>必须</code> list of Entity name, match whole word.

@apiSuccess {String} type Defaut 'ItemList'.
@apiSuccess {Object[]} itemListElement  List of EntitySearchResult (Array of Objects).
@apiSuccess {String} itemListElement.type Defaut 'EntitySearchResult'.
@apiSuccess {String} itemListElement.result An Entity Brief Info ().


@apiParamExample {json}  Lookup Query
 {
   "names": [ "华仔","唱歌"]
 }

 @apiSuccessExample {json} Success-Response:
      HTTP/1.1 200 OK
 {
   "@type": "ItemList",
   "itemListElement": [{
           "@type": "ItemList",
           "query": "华仔",
           "itemListElement": [{
               "@type": "EntitySearchResult",
               "result": {
                   "@id": "6c84fb90-12c4-11e1-840d-7b25c5ee775a",
                   "@type": [
                       "Thing",
                       "Organization",
                       "MusicGroup"
                   ],
                   "name": "刘德华",
                   "entityScore": 192802
               }
           }]
       },
       {
           "@type": "ItemList",
           "query": "唱歌",
           "itemListElement": []
       }
   ]
 }
"""






"""
@api {get} /entities:list List Entities
@apiName ListEntities
@apiGroup EntitySyncAPI
@apiDescription  支持同步知识图谱。目前只传递实体索引相关的部分，不要求全量传递数据。
@apiVersion 0.4.0

@apiParam {String[]} types Entity type, List of String, use cnschema name . any entity whose type overlapping with types counts at a match.
@apiParam {Integer} limit number results to be returned.
@apiParam {String} since 所有返回结果更新时间不早于此时间，格式 ISO8601 e.g. "2017-01-17T14:40:00Z".
@apiParam {String} sort none:不在意是否排序  random:每次结果随机排序  score:按entityScore倒序  modified:按更新时间倒序
@apiParam {String} indexOnly 1:only return index (@id, @type, name, alternateName, dateModified, description) (right now 1 is the only and default value. future may add 0 for passing complete entity data)

@apiSuccess {String} type Defaut 'ItemList'.
@apiSuccess {Object[]} itemListElement  List of EntitySearchResult (Array of Objects).
@apiSuccess {String} itemListElement.type Defaut 'EntitySearchResult'.
@apiSuccess {String} itemListElement.result An Entity.

 @apiSuccessExample Success-Response:
      HTTP/1.1 200 OK
      {
     	"@type": "ItemList",
 		"numberOfItems": 1,
     	"itemListElement": [{
     		"@type": "EntitySearchResult",
     		"result": {
     			"@id": "6c84fb90-12c4-11e1-840d-7b25c5ee775a",
     			"@type": [
     				"Thing",
     				"Organization",
     				"MusicGroup"
     			],
     			"name": "刘德华",
     			"alternateName": ["华仔"],
     			"dateModified": "2017-01-17T14:40:00+8:00",
     			"description": "香港实力派演员、歌手。"
     		}
     	}]
     }
"""




"""
@api {post} /entities:index:es ElasticSearch Query
@apiName GraphEs
@apiGroup EntityIndexAPI
@apiDescription 基于Elastic Search 查询的图查询API。目前只支持one step。 需要进一步明确ES的数据模型。
@apiVersion 0.2.0

@apiParam {String} query  <code>必须</code>  graph query expressed in Elastic Search Query.

@apiParamExample {json} Elastic Search Query
  {
	"query": {
		"size": 10,
		"_source": ["name", "byArtist", "@id", "mergedFrom"],
		"query": {
			"function_score": {
				"query": {
					"filtered": {
						"filter": {
							"bool": {
								"must": [{
									"term": {
										"@type.raw": "MusicRecording"
									}
								}, {
									"term": {
										"mergedFrom.statedIn.raw": "music.163.com"
									}
								}, {
									"term": {
										"byArtist.@id.raw": "歌手2"
									}
								}, {
									"term": {
										"byArtist.@id.raw": "黑豹"
									}
								}]
							}
						}
					}
				},
				"functions": [{
					"filter": {
						"term": {
							"name.raw": "朋友"
						}
					},
					"weight": 1000
				}]
			}
		}
	}
}


@apiSuccess {String} type Defaut 'ItemList'.
@apiSuccess {Object[]} itemListElement  List of EntitySearchResult (Array of Objects).
@apiSuccess {String} itemListElement.type Defaut 'EntitySearchResult'.
@apiSuccess {String} itemListElement.result An Entity.
@apiSuccess {Float} itemListElement.resultScore Matching result score.

 @apiSuccessExample Success-Response:
      HTTP/1.1 200 OK
      {
     	"@type": "ItemList",
     	"itemListElement": [{
     		"@type": "EntitySearchResult",
     		"result": {
     			"@id": "kg:12da321",
     			"@type": [
     				"Thing",
     				"Organization",
     				"MusicGroup"
     			],
     			"name": "刘德华",
     			"alternateName": ["华仔"],
     			"dateModified": "2017-01-17T14:40:00+8:00",
     			"entityScore": 192802,
     			"description": "香港实力派演员、歌手。"
     		}
     	}]
     }
"""



"""
@api {post} /entities:index:cypher Cypher Graph Query
@apiName GraphCypher
@apiGroup EntityIndexAPI
@apiDescription 基于cypher查询的图查询API。
@apiVersion 0.3.0

@apiParam {String} query  <code>必须</code>  graph query expressed in Cypher. 需要进一步明确NEO4j的数据模型。

@apiParamExample {json} Cypher Query
                   {
                        "query":  "MATCH (user)-[:friend]->(follower) WHERE user.name IN ['Joe', 'John', 'Sara', 'Maria', 'Steve'] AND follower.name =~ 'S.*' RETURN user.name, follower.name"
                   }


@apiSuccess {String} type Defaut 'ItemList'.
@apiSuccess {Object[]} itemListElement  List of EntitySearchResult (Array of Objects).
@apiSuccess {String} itemListElement.type Defaut 'EntitySearchResult'.
@apiSuccess {String} itemListElement.result An Entity.
@apiSuccess {Float} itemListElement.resultScore Matching result score.


"""






"""
@api {put} /entities Update/Create an entity
@apiName EntityUpdate
@apiGroup EntitySyncAPI
@apiDescription 更新/增加实体详情。
@apiVersion 0.4.0

@apiParam {Object} item  <code>必须</code>  the entity to be updated, created if missing. must include valid @id @type in item.


@apiSuccess {String} text "ok" if update operation succeed.
"""



"""
@api {DELETE} /entities/:id Delete an entity
@apiName EntityDelete
@apiGroup EntitySyncAPI
@apiDescription mark delete an entity。
@apiVersion 0.4.0

@apiParam {String} id  <code>必须</code>  entity id.
@apiParam {Object} item  <code>必须</code>  the entity.


@apiSuccess {String} text "ok" if update succeed.
"""



"""
@api {POST} /entities:batch Batch Update
@apiName EntityBatchUpdate
@apiGroup EntitySyncAPI
@apiDescription Batch Operation on entity store。
@apiVersion 0.4.0

@apiParam {String} operation  <code>必须</code>  任选 "update", "create", "delete".
@apiParam {Object[]} itemListElement  <code>必须</code>  the entities to be updated.

@apiSuccess {String} text "ok" if update succeed.
"""


"""
@api {get} /entities:search Template Fulltext Search
@apiName TemplateSearch
@apiGroup EntityTemplateAPI
@apiDescription similar to google entity search
@apiVersion 0.5.0

@apiParam {String} query <code>必须</code> full text search on name, description.
@apiParam {String[]} types 必须之一 Entity type, List of String, use cnschema name . any entity whose type overlapping with types counts at a match.
@apiParam {Integer} limit number results to be returned.
@apiParam {String} since 所有返回结果更新时间不早于此时间，格式 ISO8601 e.g. "2017-01-17T14:40:00Z".
@apiParam {String} sort none:不在意是否排序  random:每次结果随机排序  score:按entityScore倒序  modified:按更新时间倒序

@apiSuccess {String} type Defaut 'ItemList'.
@apiSuccess {Object[]} itemListElement  List of EntitySearchResult (Array of Objects).
@apiSuccess {String} itemListElement.type Defaut 'EntitySearchResult'.
@apiSuccess {String} itemListElement.result An Entity.
@apiSuccess {Float} itemListElement.resultScore Matching result score.

 @apiSuccessExample Success-Response:
      HTTP/1.1 200 OK
      {
     	"@type": "ItemList",
 		"numberOfItems": 1,
     	"itemListElement": [{
     		"@type": "EntitySearchResult",
     		"result": {
     			"@id": "6c84fb90-12c4-11e1-840d-7b25c5ee775a",
     			"@type": [
     				"Thing",
     				"Organization",
     				"MusicGroup"
     			],
     			"name": "刘德华",
     			"alternateName": ["华仔"],
     			"dateModified": "2017-01-17T14:40:00+8:00",
     			"entityScore": 192802,
     			"description": "香港实力派演员、歌手。"
     		},
            "resultScore": 1992.2
     	}]
     }
"""



"""
@api {post} /entities:EntitySyncAPI:simple Template Simple Query
@apiName TemplateSimple
@apiGroup EntityTemplateAPI
@apiDescription 模版查询，简单版。
@apiVersion 0.5.0

@apiParam {Object[]} wherePV <code>必须之一</code>  属性-值匹配条件.
@apiParam {String} wherePV.property 属性名路径，e.g. birthPlace.name
@apiParam {String} wherePV.value 属性值.
@apiParam {String[]} types <code>必须之一</code> Entity type, List of String, use cnschema name .
@apiParam {String[]} selectP 过滤需要输出的属性值。如果不设置，缺省返回所有属性。@id, @type, 总会返回
@apiParam {Integer} limit number results to be returned.
@apiParam {String} sort none:不在意是否排序  randomBest:每次结果按entityScore倒序，前几位随机排序 random:每次结果随机排序  score:按entityScore倒序  modified:按更新时间倒序

@apiParamExample {json} Template Simple
 {
 	"wherePV": [{
 			"property": "byArtist.name",
 			"value": "刘德华"
 		},
 		{
 			"property": "keywords",
 			"value": "舒缓"
 		}
 	],
 	"selectP": ["name", "byArtist", "image"],
 	"types": ["MusicRecording"],
 	"limit": 10,
 	"sort": "randomBest"
 }

@apiSuccess {String} type Defaut 'ItemList'.
@apiSuccess {Object[]} itemListElement  List of EntitySearchResult (Array of Objects).
@apiSuccess {String} itemListElement.type Defaut 'EntitySearchResult'.
@apiSuccess {String} itemListElement.result An Entity.
@apiSuccess {Float} itemListElement.resultScore Matching result score.

 @apiSuccessExample Success-Response:
      HTTP/1.1 200 OK
      {
     	"@type": "ItemList",
 		"numberOfItems": 1,
     	"itemListElement": [{
     		"@type": "EntitySearchResult",
     		"result": {
     			"@id": "kg:12da321",
     			"@type": [
     				"Thing",
     				"Organization",
     				"MusicGroup"
     			],
     			"name": "刘德华",
     			"alternateName": ["华仔"],
     			"dateModified": "2017-01-17T14:40:00+8:00",
     			"entityScore": 192802,
     			"description": "香港实力派演员、歌手。"
     		},
            "resultScore": 1992.2
     	}]
     }
"""
