#!/usr/bin/env python
# coding: utf-8

# # Life Science ontologies and Knowledge Graphs, HANDS-ON
# 
# *Alban Gaignard, alban.gaignard@univ-nantes.fr, Olivier Dameron, olivier.dameron@univ-rennes1.fr*
# 
# *HANDS-ON session given as part of ETBII 2023*
# 
# At the end of this hands-on session, you will be able to
#  - explore and search publicly available biomedical ontologies, combine knowledge provided by multiple ontologies,
#  - computationally exploit these ontologies: explore node neighborhood, navigate class hierarchies, retrieve synonyms,
#  - understand how biochemical regulations are modeled in BioPAX,
#  - assemble/summarize new graphs based on graph patterns.

# ## 1. Exploring Life Science ontologies
# 
# BioPortal (https://bioportal.bioontology.org) is a large repository of biomedical ontologies gathering 600+ ontologies and 8+ million classes. We will use this web resource to navigate and retrieve biomedical knowledge.

# ### Question 1
# Search for two definitions of “mitral valve prolapse”, coming from two different ontologies.

# ### Question 2
# In the human phenotype ontology, search for all sub-classes of “mitral stenosis”. You will use the “jump to” search box to directly display the corresponding class.

# ### Question 3
# Still from the Human Phenotype Ontology, list “mitral valve prolapse” class mappings. Based on its corresponding class in the OMIM ontology (Online Mendelian Inheritance in Man), retrieve possibly involved genes. You will need to navigate through “manifestation of” and “gene symbol” properties.

# ---

# Up to now we browsed web pages to retrieve biomedical knowledge. In the following questions, we will use the *beta* BioPortal SPARQL endpoint (http://sparql.bioontology.org) to automate information retrieval.

# ### Question 4
# Execute a SPARQL DESCRIBE query to display all the outgoing properties of “mitral valve prolapse” (```http://purl.bioontology.org/ontology/OMIM/MTHU001468```)

# In[1]:


query = """
# (Optionnal) Declare your namespaces here
# General syntax: 
# For the usual namespaces, you can use http://prefix.cc/

PREFIX omim: <http://purl.bioontology.org/ontology/OMIM/>

DESCRIBE  omim:MTHU001468 
"""


# ### Question 5. 
# Write a SPARQL SELECT query to list all genes possibly involved in mitral valve prolapse (you can execute a SPARQL DESCRIBE on a `manifestation` to find the property URI linking gene symbols.

# In[2]:


query = """
PREFIX omim: <http://purl.bioontology.org/ontology/OMIM/>

SELECT *
WHERE {
  omim:MTHU001468 omim:manifestation_of ?x
}

"""

# count the results
query = """
PREFIX omim: <http://purl.bioontology.org/ontology/OMIM/>

SELECT (count(*) AS ?nbdisease)
WHERE {
  omim:MTHU001468 omim:manifestation_of ?x
}
"""


# ### Question 6
# Write a SPARQL SELECT query to list the direct subclasses of heart valve diseases and their synonyms. You will use the `DOID ontology`, the `rdfs:subClassOf` and `obo:hasExactSynonym` properties. Don’t forget to start by describing the `DOID_4079` resource (`DESCRIBE` query).

# In[3]:


#DESCRIBE <http://purl.obolibrary.org/obo/DOID_4079>

query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX obo: <http://www.geneontology.org/formats/oboInOwl#>

"""


# ## 2. Querying gene regulation resources  
# 
# We will now use PathwayCommons (http://www.pathwaycommons.org), an RDF dataset used to integrated biological signaling pathways (5,772 pathways, 2,424,055 interactions) from 22 regulation data sources. PathwayCommons can be queried through its SPARQL endpoint (http://rdf.pathwaycommons.org/sparql). Since this server is down (jan 2023), we will use this mirror deployed at IFB : http://134.214.213.234/sparql  
# 
# PathwayCommons uses the BioPAX ontology to represent regulation and signaling knowledge. Have a look on Figure 3 and Figure 4 of the BioPAX paper (https://www.researchgate.net/publication/46191859_BioPAX_-_A_community_standard_for_pathway_data_sharing) to have a quick overview of BioPAX. 
# 
# We are interested in **activation** or **inhibition** gene regulations. The following *turtle* syntax shows how they can be represented in BioPAX. 
# 
# ```
# @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . 
# @prefix pc2: <http://pathwaycommons.org/pc2/> .
# @prefix bp: <http://www.biopax.org/release/biopax-level3.owl#> .
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
# 
# pc2:TemplateReactionRegulation_145afc203ffa1cb5a00fa445a5a63c64 rdf:type bp:TemplateReactionRegulation .
# 
# pc2:TemplateReactionRegulation_145afc203ffa1cb5a00fa445a5a63c64 bp:comment " REPLACED http://www.ctdbase.org/#EXP_2556811"^^xsd:string ;
#     bp:controlType "ACTIVATION"^^xsd:string ;
#     bp:controlled pc2:TemplateReaction_9129e01e3c570005d993c44e75b2134c ; 
#     bp:controller pc2:SmallMolecule_38f43f385b04215c6ac89a44cdc22f67 ; 
#     bp:dataSource pc2:ctd ;
#     bp:displayName "Phenobarbital results in increased expression of CYP2B6 protein "^^xsd:string ;
#     bp:xref <http://identifiers.org/pubmed/19084549> , 
#             <http://identifiers.org/pubmed/12571232> , 
#             <http://identifiers.org/pubmed/19952500> , 
#             <http://identifiers.org/pubmed/21778469> ,
#             <http://identifiers.org/pubmed/24224465> , 
#             <http://identifiers.org/pubmed/21227907> , 
#             <http://identifiers.org/pubmed/25512232> , 
#             <http://identifiers.org/pubmed/14977870> , 
#             <http://identifiers.org/pubmed/15548381> , 
#             <http://identifiers.org/pubmed/20361990> .
# ```
# 

# ### Question 7
# On a piece of paper, draw the corresponding directed labelled graph. 

# ### Question 8
# 1. Test the `DESCRIBE pc2:TemplateReactionRegulation_145afc203ffa1cb5a00fa445a5a63c64` query directly at <http://134.214.213.234/sparql>
# 2. Test the same query directly in this notebook: 
# ```python
# query = "YOUR QUERY"
# sparql = SPARQLWrapper("http://134.214.213.234/sparql")
# sparql.setQuery(query)
# results = sparql.queryAndConvert()
# ```

# In[4]:


query = """

"""
sparql = SPARQLWrapper("http://134.214.213.234/sparql")
sparql.setQuery(query)
results = sparql.queryAndConvert()
print(results.serialize(format="turtle"))


# **In the remainder of the question we will use the SPARQL endpoint web interface (<http://134.214.213.234/sparql>).**

# ### Question 9
# Based on this description, write a query to show the names of all genes that regulate (activation or inhibition) SCN5A. We will proceed in multiple progressive steps. 
# 
# 1. identify regulation reactions with resources of type `bp:TemplateReactionRegulation` (don’t forget to use a LIMIT 10 to get fast results)
# 2. show their control type (`bp:controlType` property) and filter only “activation” or “inhibition”.
# 3. show the associated scientific publication with the `bp:xref` property. Make sure that “pubmed” is contained in its URI (you can use a FILTER fonction: `FILTER (regex(?publi, "pubmed"))`).
# 4. identify the source of the regulation (`bp:controller`) and its display name (`bp:displayName`).
# 5. identify the target of the regulation (`bp:controlled`) and its display name (`bp:displayName`). Make sure (FILTER) that the display name is our target gene: SCN5A.

# ####  Question 9.1
# Identify regulation reactions with resources of type `bp:TemplateReactionRegulation` (don’t forget to use a LIMIT 10 to get fast results)

# In[6]:


query = """
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

"""


# ####  Question 9.2
# Show their control type (`bp:controlType` property). You can filter only “ACTIVATION” or “INHIBITION”. 
# Use a FILTER clause, the or  `||` operator and `regex(variable,"pattern")` function. 

# In[7]:


query = """
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

"""


# #### Question 9.3
# Show the associated scientific publication with the `bp:xref` property. Make sure that “pubmed” is contained in its URI. Use a FILTER clause, and a `regex(variable,"pattern")` function. We want to get reaction, even  if no publication isassociated, for that we will enclose the triple pattern within an `OPTIONAL {}` clause.

# In[8]:


query = """
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

"""


# #### Question 9.4
# Identify the source of the regulation (`bp:controller`) and its display name (`bp:displayName`).

# In[9]:


query = """
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

"""


# #### Question 9.5
# Identify the target of the regulation (`bp:controlled`) and its display name (`bp:displayName`). Make sure (FILTER) that the display name is our target gene: SCN5A.

# In[10]:


query = """
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>


"""


# ### Question 10
# From the previous query, retrieve a tabular file (CSV) with 3 columns for the source name, the regulation type, and the target name. Use the http://app.rawgraphs.io web tool to generate an alluvial flow chart which displays the relations between the source and target nodes. You should obtain something like : 
# ![:scale 50%](fig/viz.png)

# ### Question 11
# Use what you learned (recently) to produce a SIF file for this regulation information and display it through Cytoscape. 

# In[12]:


queryString = """


"""


# In[ ]:





# In[13]:


## Here we create the output SIF file:
import csv

with open('output.sif', 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    # ...

