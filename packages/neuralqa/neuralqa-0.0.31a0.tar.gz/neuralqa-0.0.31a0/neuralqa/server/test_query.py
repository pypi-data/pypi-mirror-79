# # temporary file for testing search abstractions
# # TODO: Delete this file!!

# from elasticsearch import Elasticsearch, ConnectionError

# es = Elasticsearch([{'host': "localhost", 'port': 9200}])

# def parse_field_content(field_name, content):
#     """Parse content fields if nested using dot notation, else return content as is.
#     e.g. for acrray content and field_name casebody.data.opinions.text, we return
#     content[casebody][data][opinions][text]. If any nest level is an array we return only the
#     first instance of this array. e.g. if opinions is an array, we return
#     content[casebody][data][opinions][0][text].

#     Args:
#         field_name ([str]): [description]
#         content ([dict]): [description]

#     Returns:
#         [str]: content of field
#     """

#     if ("." not in field_name):
#         return content[field_name]
#     else:
#         fields = field_name.split(".")
#         for field in fields:
#             print("\t",content.keys(), field)
#             content =  content[field]
#             if (isinstance(content, list)):
#                 content = content[0]
#         return content

# def run_query(index_name, search_query, body_field, secondary_fields, max_documents=5, highlight_span=100, relsnip=True, num_fragments=5):

#     tags = {"pre_tags": [""], "post_tags": [""]}
#     highlight_params = {
#         "fragment_size": highlight_span,
#         "fields": {
#             body_field: tags
#         },
#         "number_of_fragments": num_fragments,
#         # "order": "score"
#     }

#     search_query = {
#         "query": {
#             "multi_match": {
#                 "query":    search_query,
#                 "fields": [body_field]
#             }
#         },
#         "_source": {"includes": [body_field]},
#         "size": max_documents
#     }

#     status = True
#     results = {}

#     if (relsnip):
#         search_query["highlight"] = highlight_params
#     # else:
#     #     search_query["_source"] = {"includes": [body_field]}

#     try:
#         # print(search_query)
#         query_result = es.search(index=index_name, body=search_query)
#         # RelSnip: for each document, we concatenate all
#         # fragments in each document and return as the document.

#         highlights = [" *** ".join(hit["highlight"][body_field])
#                         for hit in query_result["hits"]["hits"] if "highlight" in hit]
#         docs = [parse_field_content(body_field, hit["_source"])
#                 for hit in query_result["hits"]["hits"] if hit["_source"]]
#         took = query_result["took"]
#         results = {"took": took,  "highlight": highlights, "docs": docs}

#     except (ConnectionRefusedError, Exception) as e:
#         status = False
#         results["errormsg"] = str(e)

#     results["status"] = status
#     return results


# search_query = "what arson"
# max_documents = 2
# highlight_span = 50
# body_field = "casebody.data.opinions.text"
# secondary_fields = ["author"]
# num_fragments = 2

# results = run_query("cases", search_query, body_field, secondary_fields,
#                     max_documents=5, highlight_span=highlight_span, relsnip=True, num_fragments=num_fragments)
# # print(results)
# import logging
# from neuralqa.expander import MLMExpander

# logging.basicConfig()
# logging.getLogger().setLevel(logging.INFO)
# # logging.getLogger("root").setLevel(logging.INFO)

# expander = MLMExpander()
# expanded_query = expander.expand_query(
#     "what is the goal of the fourth amendment?  ")
# terms = " ".join([term["token"] for term in expanded_query["terms"]])
# print(expanded_query)

# import requests

# solr_protocol = "http"
# solr_host = "localhost"
# solr_port = 8983
# base_solr_url = solr_protocol + "://" + \
#     solr_host + ":" + str(solr_port) + "/solr"


# def create_collection(name):
#     create_url = base_solr_url + "/admin/cores"
#     params = {"action": "CREATE", "configSet": "_default",
#               "name": name, "wt": "json"}
#     response = requests.get(create_url, params=params)
#     print(response.url)
#     print(response.text)


# def run_query(index_name, search_query, max_documents=5, fragment_size=100, relsnip=True, num_fragments=5, highlight_tags=True):
#     query_url = base_solr_url + "/" + index_name + "/select"
#     body_field = "plain_text"
#     params = {"df": body_field, "fl": body_field,
#               "wt": "json", "q": search_query, "rows": max_documents}

#     hl_params = {"hl": "true", "hl.method": "unified", "hl.snippets": num_fragments,
#                  "hl.fragsize": num_fragments, "hl.usePhraseHighlighter": "true"}
#     if not highlight_tags:
#         hl_params["hl.tags.pre"] = ""
#         hl_params["hl.tags.post"] = ""

#     if relsnip:
#         params = {**params, **hl_params}
#     else:
#         params["fl"] = "null"

#     response = requests.get(query_url, params=params)
#     highlights = []
#     docs = []
#     results = {}
#     status = False

#     if (response.status_code == 200):
#         status = True
#         print(response.url, response.status_code)
#         response = response.json()
#         print((response.keys()))
#         highlights = [" ".join(response["highlighting"][key][body_field])
#                       for key in response["highlighting"].keys()] if "highlighting" in response else highlights
#         docs = [" ".join(doc[body_field])
#                 for doc in response["response"]["docs"]]
#         results = {"took": response["responseHeader"]
#                    ["QTime"],  "highlights": highlights, "docs": docs}
#     else:
#         print("An error has occured", response.status_code, response.__dict__)
#         status = False
#         results["errormsg"] = str(response.status_code)
#     results["status"] = status
#     return results


# response = requests.get(
#     'http://localhost:8983/solr/collection_name/select?q=cheese&wt=python')
# print(response.status_code, response, response.text)


# index_name = "scotus"
# search_query = "arson crime"
# print(run_query(index_name, search_query, max_documents=2))

from neuralqa.retriever import SolrRetriever

solr_params = {"host": "localhost"}

retriever = SolrRetriever(**solr_params)
print(retriever)
