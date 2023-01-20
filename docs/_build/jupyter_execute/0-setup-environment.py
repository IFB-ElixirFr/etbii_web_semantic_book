#!/usr/bin/env python
# coding: utf-8

# # Software environment setup

# In[1]:


get_ipython().system('pip install rdflib')
get_ipython().system('pip install sparqlwrapper')
get_ipython().system('pip install ipycytoscape')
get_ipython().system('pip install ipywidgets')
get_ipython().system('pip install ipywidgets --upgrade')


# In[2]:


import sys  
get_ipython().system('{sys.executable} -m pip install --user jupyterquiz')


# In[3]:


try:
    import rdflib
    from SPARQLWrapper import SPARQLWrapper
except ImportError as e:
    assert False, e


# In[4]:


from SPARQLWrapper import SPARQLWrapper

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("DESCRIBE <http://dbpedia.org/resource/Porquerolles>")

results = sparql.queryAndConvert()
print(results.serialize(format="turtle"))

assert(len(results) >= 40)


# In[5]:


from rdflib import Graph

