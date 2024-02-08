# this module holds all global namespace vocabulary lookups as equivalent to singleton instances
from collections import defaultdict
import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.sql.sqltypes as sss
import sqlalchemy.sql.expression as exp
import re

from ..db import Base, engine
from ..tables.vocabulary import Concept, Concept_Relationship

class VocabLookup:
    # base class for custom vocabulary lookups

    # correction parameter holds an ordered list of callable corrections 
    # - try match the raw input string first 
    # - then apply corrections in order and return the first match 
    # - examples of correction functions would be stripping punctuation, 
    #   spelling correction functions

    def __init__(self, 
                 unknown=0,     # TODO: tbd do we want to define behaviours when mapping is not found?
                 parent=None,   # used when you want to pull all child concepts under a given parent into the lookup
                 domain=None):  # otherwise we are grabbing by specification of domain
        self._unknown = unknown
        self._lookup = defaultdict(self.return_unknown)
        self._domain = domain
        # parent parameter is the high-level concept under which you want to pull
        # in all available matches - e.g. TNM stages, which can grab all concepts 
        # that fall under the parent concept from the concept_relationship table
        self._parent = parent
        self._correction = None
        with so.Session(engine) as session:
            # TBD: question - do we need to provide support for combining parent 
            # definition with domain def? is this a likely use-case? it won't fail 
            # for now, but perhaps check?
            if parent is not None:
                self.get_lookup(self._lookup, parent.value, session)
            if domain is not None:
                self.get_domain_lookup(session)
        
        # TODO: consider generalisable creation of custom maps to host 
        # manual mappings of local concepts to OMOP concepts as well?

    
    def get_domain_lookup(self, session):
        # returns a default dictionary that contains all
        # concepts under a given domain for rapid lookups
        
        d = session.query(Concept.concept_name,
                          Concept.concept_id
                         ).filter(Concept.domain_id==self._domain).all()
        for row in d:
            self._lookup[row.concept_name.lower().strip()] = row.concept_id
    
    def get_children(self, concept_id_tuple, session):
        # TODO: check if we can do this thru Concept_Ancestor instead
        # if confirmed we only want to be doing for standard concepts?
        # this is iterative and slow way of doing it to arbitrary depths
        # otherwise...
        return session.query(Concept_Relationship.concept_id_1, 
                             Concept_Relationship.concept_id_2
                            ).filter(Concept_Relationship.concept_id_1.in_(concept_id_tuple)
                            ).filter(Concept_Relationship.relationship_id=='Subsumes').distinct()
    
    def get_all_concepts_in_hierarchy(self, children, concepts, session):
        # uses the subsumes relationship to get all higher-granularity items in the 
        # conceptual hierarchy
        next_level = []
        if len(children) == 0:
            return concepts
        for child in children:
            next_level = self.get_children(child.concept_id_2, session)
            #concepts.append(get_concept(child.concept_id_2, targ_sess))
            self.get_all_concepts_in_hierarchy(next_level, concepts, session)

    def get_lookup(self, session):
        # returns a default dictionary that contains all
        # concepts under a given parent concept and the
        # appropriate unknown value for the target context
        first_level = self.get_children((self._parent), session)
        concepts = []
        self.get_all_concepts_in_hierarchy(first_level, concepts, session)
        for c in concepts:
            self._lookup[c.concept_name.lower()] = c.concept_id

    def return_unknown(self):
        return self._unknown.value

    def lookup_exact(self, term):
        if term == None:
            term = ''
        return self._lookup[term.lower().strip()]

    def lookup(self, term):
        if term == None:
            term = ''
        value = self._lookup[term.lower().strip()]
        if self._correction is not None:
            for c in self._correction:
                if value != self._unknown:
                    break
                value = self._lookup[c(term).lower().strip()]
        return value




# class StandardVocabLookup(VocabLookup):
#     # standard vocabulary is a lookup that filters 
#     # on vocabulary and domain
#     # codes_only flag will restrict to matching only
#     # on codes, rather than concept string matching
#     # with_synonyms flag uses the concept_synonym
#     # table to provide alternative string matching
#     # (with_synonyms overrides codes_only)

#     def __init__(self, vocabulary, domain, 
#                  unknown, corrections, 
#                  codes_only=False, with_synonyms=False):
#         super().__init__(unknown)
#         self._correction = corrections
#         get_standard_vocab(vocabulary, domain, self._lookup, codes_only, with_synonyms)


# class HierarchicalLookup():
#     # this class holds an ordered list of standard vocabularies and 
#     # will try match them in order of priority, restricted
#     # to the target domain

#     def __init__(self, domain, vocab_list, unknown=Unknown.generic.value, corrections=None):
#         self._unknown = unknown
#         self._lookup_list = [StandardVocabLookup(v, domain, unknown, corrections) for v in vocab_list]

#     def lookup(self, term):
#         value = self._unknown
#         for l in self._lookup_list:
#             if value != self._unknown:
#                 break
#             value = l.lookup_exact(term)
#         for l in self._lookup_list:
#             if value != self._unknown:
#                 break
#             value = l.lookup(term)
#         return value

# def remove_slash(term):
#     return term.replace('/', '')

# def insert_slash(term):
#     try:
#         return f'{term[:-1]}/{term[-1]}'
#     except:
#         return ''

# def regexp_find_icd(term):
#     # match full ICD10 code of form C00.00
#     return re.search('[a-zA-Z]\d{1,2}\.\d{1,2}|$', term).group()

# def regexp_icd_group(term):
#     # match higher (less specific) ICD term when full term 
#     # isn't possible e.g. C92
#     return re.search('[a-zA-Z]\d{1,2}|$', term).group()

# class ConditionLookup(VocabLookup):
    
#     # a condition lookup object can be used to map a combination of 
#     # fields into a single target.
#     # it was originally created so that morph and topog could
#     # be combined to lookup condition, using the object 
#     # CTL.condition_lookup, but could be used validly to lookup
#     # any n:1 concept lookup by populating a similar control
#     # schema table.

#     def __init__(self, unknown, object_lookup, source, target, vocabulary):
#         super().__init__(unknown)
#         self._correction = None
#         get_custom_lookup(object_lookup, source, target, vocabulary, self._lookup)
    

# def get_custom_lookup(ObjectLookup, source, target, vocabulary, lookup):
    
#     with db_session(control_engine) as ctl_sess:
#         object_lookup = dataframe_from_query(ctl_sess.query(ObjectLookup)).fillna('0')
#         object_lookup['source']=object_lookup.apply(lambda x: '-'.join(list(x[source])), axis=1)
#         object_lookup['target']=object_lookup.apply(lambda x: '-'.join(list(x[target])), axis=1)

#         concept_filter = tuple(object_lookup.target.dropna().unique())
#         with db_session(target_engine) as targ_sess:
#             concept_lookup = dataframe_from_query(targ_sess.query(CDM.concept)
#                                                   .filter(CDM.concept.concept_code.in_(concept_filter))
#                                                   .filter(CDM.concept.vocabulary_id==vocabulary))
#         object_lookup = object_lookup.merge(concept_lookup, left_on='target', right_on='concept_code')
#         for k, v in zip(object_lookup.source, object_lookup.concept_id):
#             lookup[k.lower()]=v

# class CoordinatedCondition(HierarchicalLookup):
#     def __init__(self):
#         super().__init__(domain='Condition', 
#                          vocab_list=['ICDO3'], 
#                          unknown=Unknown.condition,
#                          corrections=[remove_slash, regexp_find_icd, 
#                                       regexp_icd_group, insert_slash])

# class GenderLookup(VocabLookup):
#     def __init__(self):
#         super().__init__(unknown=Unknown.gender, domain='Gender')
#                          #parent=SNOMED_hierarchy.sex)  

# class LanguageLookup(VocabLookup):
#     def __init__(self):
#         super().__init__(unknown=Unknown.generic, 
#                          parent=SNOMED_hierarchy.language,
#                          table='prompt', 
#                          context='admin.language_spoken_pro_id') 
#         self._correction = [self.append_language]

#     def append_language(self, term):
#         return term.lower().strip() + ' language'

# class RaceLookup(VocabLookup):

#     def __init__(self):
#         super().__init__(unknown=Unknown.generic, 
#                          parent=None, 
#                          table='prompt', 
#                          context='race.pro_id')

# #try:
# cava_log.log('Loading custom concept lookup objects', 'debug')
# lookup_gender = GenderLookup()
# lookup_language = LanguageLookup()
# lookup_race = RaceLookup()
# lookup_condition = ConditionLookup(unknown=Unknown.cancer, object_lookup=CTL.condition_lookup, source=['morph', 'topog'], target=['condition'], vocabulary='ICDO3') # Unknown histology of unknown primary site
# #    lookup_observation = ConditionLookup('Observation')
# #    lookup_coordinated = CoordinatedCondition()
# lookup_icd = HierarchicalLookup('Condition', ['ICD10', 'ICD9CM', 'ICDO3'], Unknown.condition, [remove_slash, insert_slash, regexp_find_icd, regexp_icd_group])
# lookup_laterality = MappingLookup('medical', 'paired_organ')
# lookup_stage = MappingLookup('tnmstage', ['t_stage', 'n_stage', 'm_stage', 'stage'])
# lookup_grade = MappingLookup('medical', 'hist_grade')
# lookup_drugs = MappingLookup('drug', 'drug')
# lookup_units = MappingLookup('drug', 'unit')
# lookup_route = MappingLookup('drug', 'route')
# lookup_eviq = MappingLookup('eviq', ['component', 'regimen'])

# cava_log.log('Custom concept lookup loading complete', 'debug')
# # except Exception as e:
# #     cava_log.log('Unable to load custom concept lookup objects', 'error')
# #     cava_log.log(f'{e}', 'error')