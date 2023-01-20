#!/usr/bin/env python
# coding: utf-8

# # Combining graphs from multiple data sources
# In this notebook you will be able to search for protein interactions (Uniprot), expressions in tissues (Bgee). Finally you will lear how to assemble a new graph of co-expressed gene.  

# In[1]:


get_ipython().system('pip install rdflib')
get_ipython().system('pip install sparqlwrapper')


# In[2]:


import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE


# ## 1. Find interacting proteins with SCN5A (from Uniprot)

# By browsing http://uniprot.org, find the web page describing SCN5A_HUMAN. 

# ## 2. Look at the RDF graph describing SCN5A 
# 
# You can directly access RDF https://www.uniprot.org/uniprotkb/Q14524.ttl . 

# By using the following graph pattern write a SPARQL query to find the proteins interacting with SCN5A. 

# <https://www.uniprot.org/uniprotkb/Q14524.ttl>

# Find all PPI in which Q14524 is a participant.
# You can use the following graph pattern : 
# ```
# VALUES ?P1 {uniprot:Q14524}
# ?interaction up:participant ?P1 . 
# ?interaction up:participant ?P2 .
# ?P1 up:mnemonic ?P1_label .
# ?P2 up:mnemonic ?P2_label .
# FILTER (?P2 != ?P1)
# ```
# 

# In[3]:


uniprot_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>

PREFIX taxon: <http://purl.uniprot.org/taxonomy/>
PREFIX uniprot: <http://purl.uniprot.org/uniprot/>
PREFIX up:<http://purl.uniprot.org/core/>

SELECT * WHERE {

    VALUES ?P1 {uniprot:Q14524}
    ?P1 up:mnemonic ?P1_label .
    ?P1 up:organism ?org . 
    ?P1 up:interaction ?interaction . 
    ?P2 up:interaction ?interaction .
    ?P2 up:mnemonic ?P2_label .
    ?interaction up:experiments ?nb_exp .

} limit 10

"""

sparql = SPARQLWrapper("http://sparql.uniprot.org/sparql/")
sparql.setQuery(uniprot_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results['results']['bindings'])

list_of_genes = ["SCN5A"]
for r in results['results']['bindings']:
    #print(f"{r['P1_label']['value']} <-> {r['P2_label']['value']} in {r['nb_expe']['value']} experiments.")
    #list_of_genes.append(r['P2_label']['value'].split("_HUMAN")[0])
    print(f"{r}")

list_of_genes


# In[4]:


get_ipython().system('pip install networkx')
get_ipython().system('pip install matplotlib')
get_ipython().system('pip install scipy')


# In[5]:


import networkx as nx
from matplotlib import pyplot as plt

g = nx.Graph()

for r in results['results']['bindings']:
    g.add_edge(r['P1_label']['value'], r['P2_label']['value'], nbExperiments = r['nb_exp']['value'])
    
nx.draw(g, with_labels=True)
plt.show()


# ## 3. Post process your results get a list of gene identifiers (remove the "_HUMAN" postfix)
# 
# you should get something like `['SCN5A', 'KCC2D', 'FGF12', 'ZMY19', 'EMC9', 'BANP', 'Q49AR9', 'TEKT4', 'PTN3']`

# In[6]:


genes = '\"'+"\" \"".join(list_of_genes)+'\"'
genes


# ## 4. Filter tissues in which genes are expressed (from Bgee)

# ### 4.1. Find tissues in which SCN5A is expressed 
# 
# Bgee is a gene expression RDF dataset which integrates GTex.  
# 
# Based on the following graph patterns, assemble a SPARQL query to retrieve tissues in which TEKT4 is expressed, for HUMANS (http://purl.uniprot.org/taxonomy/9606). 
# 
# *Anatomical entities*
# ```
# ?anatEntity a genex:AnatomicalEntity ;
#                 rdfs:label ?anatName .
# ```
# 
# *Case insensitive matching of a string value*
# ```
# FILTER (?geneName = 'TEKT4')
# ```
# 
# *Human organisms*
# ```
# ?organism obo:RO_0002162 <http://purl.uniprot.org/taxonomy/9606> . 
# ```
# 
# *Some genes from some organisms*
# ```
# ?seq a orth:Gene;
#      orth:organism ?organism ;
#      rdfs:label ?geneName .
# ```
# 
# *Some genes expressed in some tissues*
# ```
# ?seq genex:isExpressedIn ?anatEntity.
# ```
# 

# In[7]:


bgee_query = """
PREFIX orth: <http://purl.org/net/orth#>
PREFIX genex: <http://purl.org/genex#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?anatEntity ?anatName WHERE {
    ?anatEntity a genex:AnatomicalEntity ;
                rdfs:label ?anatName .
    ?organism obo:RO_0002162 <http://purl.uniprot.org/taxonomy/9606> . 
    ?seq a orth:Gene;
     orth:organism ?organism ;
     rdfs:label ?geneName .
    ?seq genex:isExpressedIn ?anatEntity.
    FILTER (?geneName = 'TEKT4')
    
}
"""

sparql = SPARQLWrapper("http://bgee.org/sparql")
sparql.setQuery(bgee_query)
sparql.setReturnFormat(JSON)
res = sparql.query().convert()
#print(res["results"]["bindings"])
for r in res["results"]["bindings"]:
    print(f"{r['anatEntity']['value']}: {r['anatName']['value']}")


# ## 4.2. Build a subgraph with a CONSTRUCT ... WHERE query 
# A "CONSTRUCT" query builds a sub-graph from a graph pattern matched in the where clause. 
# 
# Structure of a "CONSTRUCT" query: 
# ```
# CONSTRUCT {
# ... sub graph pattern ...
# } WHERE {
# ... graph pattern ...
# }
# ```
# 
# Reuse the "WHERE" clause of the previous query to build a subgraph with only `genex:isExpressedIn` and `rdfs:label` relations. 

# In[8]:


bgee_subgraph = """
PREFIX orth: <http://purl.org/net/orth#>
PREFIX genex: <http://purl.org/genex#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX etbii: <http://etbii/>

CONSTRUCT {
   ?seq etbii:isTissu ?anatName .

} WHERE {
    ?anatEntity a genex:AnatomicalEntity ;
                rdfs:label ?anatName .
    ?organism obo:RO_0002162 <http://purl.uniprot.org/taxonomy/9606> . 
    ?seq a orth:Gene;
     orth:organism ?organism ;
     rdfs:label ?geneName .
    ?seq genex:isExpressedIn ?anatEntity.
    FILTER (?geneName = 'TEKT4')
}
"""
sparql = SPARQLWrapper("http://bgee.org/sparql")
sparql.setQuery(bgee_subgraph)
results = sparql.query().convert()
print(len(results))
#print(results)
print(results.serialize(format="turtle"))

KG = results


# Now you can use a VALUES clause to inject the results of the previous query `VALUES ?x { v1 v2 v3 ... vN }` in this new query. 
# 
# Modify the query to inject `"SCN5A" "KCC2D" "FGF12" "ZMY19" "EMC9" "BANP" "Q49AR9" "TEKT4" "PTN3"` as gene of interest.  

# In[9]:


bgee_subgraph = """
PREFIX orth: <http://purl.org/net/orth#>
PREFIX genex: <http://purl.org/genex#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

CONSTRUCT {
   ?seq genex:isExpressedIn ?anatEntity ;
   rdfs:label ?geneName .

} WHERE {
    VALUE(?g_label {"""+genes+"""}) .

    ?anatEntity a genex:AnatomicalEntity ;
                rdfs:label ?anatName .
    ?organism obo:RO_0002162 <http://purl.uniprot.org/taxonomy/9606> . 
    ?seq a orth:Gene;
     orth:organism ?organism ;
     rdfs:label ?geneName .
    ?seq genex:isExpressedIn ?anatEntity.
    FILTER (regex(?anatEntity, "CL_"))
}
"""
sparql = SPARQLWrapper("http://bgee.org/sparql")
sparql.setQuery(bgee_subgraph)
results = sparql.query().convert()
print(len(results))
#print(results)
print(results.serialize(format="turtle"))


# ## 5. Build a network of genes that are co-expressed in the same tissue
# 
# The result of a "CONSTRUCT" is a graph object. You can now write and execute a CONSTRUCT query on this graph to create new `coExpressedWith` between genes. 

# In[ ]:


q2 = """
PREFIX genex: <http://purl.org/genex#>
PREFIX etbii:<http://etbii.fr/ontology/>

CONSTRUCT {
    
    ?gene1 etbii:coExpressedWith ?gene2 .
    
} WHERE {
    gene1 genex:isExpressedIN ?tissue .
    gene2 genex:isExpressedIN ?tissue .
    FILTER(gene1 != gene2)
    
}
"""

coExNet = KG.query(q2)
print(coExNet.serialize(format="turtle").decode())

