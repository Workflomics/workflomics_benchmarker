# -*- coding: utf-8 -*-
"""benchmarker.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ROublBcju9S0bAcdcaVUXLlefFGF9hl_

# g:Profiler benchmark
"""

import json
import jsonpath_ng.ext
import re




"""# GOEnrichment benchmark"""




"""# Generic and specific mzIdentML benchmarks

Note that the mzIdentML file will have different fields depending on which search engine or engines (Comet, X!Tandem, MSFragger etc.) were used. If the PSM-level probability is present then this should be used for the benchmark. I can add the expressions for the search engines we have below. The generic benchmark should always be used if PeptideProphet or similar tool has been used.

If a search engine has not been used, the benchmark will be 0. It would be possible to check this from the mzIdentML file header, if we want to distinguish when a tool has been used but not produced any (good) results from when a tool has not been used at all.
"""

tree = etree.parse('interact.pep.mzid') # mzIdentML file
root = tree.getroot()
namespaces = {'mzid': 'http://psidev.info/psi/pi/mzIdentML/1.2'}

# Generic benchmark using PSM-level probability (this could also be a PeptideProphet benchmark):
values = root.xpath('/mzid:MzIdentML/mzid:DataCollection/mzid:AnalysisData/mzid:SpectrumIdentificationList/mzid:SpectrumIdentificationResult/mzid:SpectrumIdentificationItem//mzid:cvParam[@name="PSM-level probability"]/@value', namespaces=namespaces)
benchmark = sum(float(value) for value in values) # sum up all PSM probabilities, if avalilable
print(benchmark)

# Comet-specific mzIdentML benchmark:
values = root.xpath('/mzid:MzIdentML/mzid:DataCollection/mzid:AnalysisData/mzid:SpectrumIdentificationList/mzid:SpectrumIdentificationResult/mzid:SpectrumIdentificationItem//mzid:cvParam[@name="Comet:expectation value"]/@value', namespaces=namespaces)
benchmark = sum((float(value)<1)*(1-float(value)) for value in values) # sum of 1-expectation value of PSMs with expectation value < 1, if avalilable
print(benchmark)

# X!Tandem-specific mzIdentML benchmark:
# tree = etree.parse('140131.LC2.IT2.XX.P01347_2-C,6_01_5970.tandem.pep.mzid') # mzIdentML file from X!Tandem (no PeptideProphet)
root = tree.getroot()
values = root.xpath('/mzid:MzIdentML/mzid:DataCollection/mzid:AnalysisData/mzid:SpectrumIdentificationList/mzid:SpectrumIdentificationResult/mzid:SpectrumIdentificationItem//mzid:userParam[@name="X! Tandem (k-score):expect"]/@value', namespaces=namespaces)
benchmark = sum((float(value)<1)*(1-float(value)) for value in values) # sum of 1-expect value of PSMs with expectation value < 1, if avalilable
print(benchmark)

"""# X!Tandem PepXML benchmark"""

tree = etree.parse('140131.LC2.IT2.XX.P01347_2-C,6_01_5970.tandem.pep.xml') # the X!Tandem PepXML output
root = tree.getroot()
namespaces = {'pepxml': 'http://regis-web.systemsbiology.net/pepXML'}
values = root.xpath('//pepxml:msms_pipeline_analysis/pepxml:msms_run_summary/pepxml:spectrum_query/pepxml:search_result/pepxml:search_hit[@hit_rank="1"]//pepxml:search_score[@name="expect"]/@value', namespaces=namespaces)
benchmark = sum((float(value)<0.05)*(1-float(value)) for value in values) # sum of 1-expect value of PSMs with expectation value < 1, if avalilable
print(benchmark)

"""# Comet PepXML benchmark

*Right now this is exactly the same formula as for X!Tandem - so they may be combined.*


"""

tree = etree.parse('140131.LC2.IT2.XX.P01347_2-C,6_01_5970.pep.xml') # the Comet PepXML output
root = tree.getroot()
namespaces = {'pepxml': 'http://regis-web.systemsbiology.net/pepXML'}
values = root.xpath('//pepxml:msms_pipeline_analysis/pepxml:msms_run_summary/pepxml:spectrum_query/pepxml:search_result/pepxml:search_hit[@hit_rank="1"]//pepxml:search_score[@name="expect"]/@value', namespaces=namespaces)
benchmark = sum((float(value)<0.05)*(1-float(value)) for value in values) # sum of 1-expect value of PSMs with expectation value < 1, if avalilable
print(benchmark)