import enum

class ConceptEnum(enum.Enum):

    @classmethod
    def member_values(cls):
        return (s.value for s in cls)
    
    @classmethod
    def is_member(cls, val):
        return not val or val in [s.value for s in cls]
    
    @classmethod
    def labels(cls):
        return [s.name for s in cls]

    @classmethod
    def get_name(cls, val):
        try:
            return cls(val).name
        except:
            return ''
    
class Unknown(ConceptEnum):
    generic = 4129922    # SNOMED Unknown
    gender = 4214687     # SNOMED Gender Unkown
    condition = 44790729 # SNOMED Unknown problem
    cancer = 36402660    # ICDO3 Unknown histology of unknown primary site
    grade = 4264626      # SNOMED Grade not determined
    stage = 36768646     # Cancer Modifier Origin Grade X: Unknown or no information, Not documented in patient record
    stage_edition = 1634449 # For unknown edition, default to current (8th)
    
    # unknown treatment regimen assignments
    drug_trial = 4090378          # clinical drug trial (SNOMED)
    therapeutic_regimen = 4207655 # prescription of therapeutic regimen concept (SNOMED)

    @classmethod
    def is_unknown(cls, val):
        return not val or val in [s.value for s in cls]


class ModifierFields(ConceptEnum):
    condition_occurrence_id = 1147127
    drug_exposure_id = 1147707
    procedure_occurrence_id = 1147082
    episode_id = 756290

class ModifierTables(ConceptEnum):
    drug_exposure = 1147339
    episode = 35225440
    observation = 1147304

class TreatmentEpisode(ConceptEnum):
    treatment_regimen = 32531         # Assignment to or derivation of chemo treatment regimen   
    treatment_cycle = 32532           # Assignment to or derivation of chemo treatment cycle
    cancer_surgery = 32939            # Surgical treatment episode
    radiotherapy = 32940              # Radiotherapy treatment episode
    
class Modality(ConceptEnum):
    chemotherapy = 35803401
    radiotherapy = 35803411
    
class DiseaseEpisodeConcepts(ConceptEnum):   
    episode_of_care = 32533           # Overarching disease episode

    confined = 32528                  # Confined disease extent
    invasive = 32677                  # Invasive disease extent
    metastatic = 32944                # Invasive disease extent

    stable_disease = 32948            # Stable disease dynamic
    disease_progression = 32949       # Progression disease dynamic
    partial_response = 32947          # Partial response disease dynamic
    complete_response = 32947         # Complete response disease dynamic

class EpisodeTypes(ConceptEnum):
    ehr_defined = 32544               # Episode defined in EHR
    ehr_derived = 32545               # Episode derived algorithmically from EHR
    ehr_prescription = 32838          # EHR prescription
    ehr_planned_dispensing = 32837    # EHR planned dispensation
    ehr_encounter_record = 32827      # EHR encounter
    
class ConditionModifiers(ConceptEnum):
    # for measurement_concept_id grouping
    init_diag = 734306                # Cancer Modifier - Initial Diagnosis
    tnm = 734320                      # Cancer Modifier - Parent AJCC/UICC concept
    mets = 36769180                   # Cancer Modifier - Parent metastasis hierarchy parent


class TreatmentModifiers(ConceptEnum):
    ...


class TStageConcepts(ConceptEnum):
    # used to group tnm mappings into their relevant subtypes
    # preferably create a concept that is the parent of all these T concepts, but for now...
    t0 = 1634213
    t1 = 1635564
    t2 = 1635562
    t3 = 1634376
    t4 = 1634654
    ta = 1635682
    tx = 1635682
    tis = 1635682

class NStageConcepts(ConceptEnum):
    # as above for n...
    n0 = 1633440
    n1 = 1634434
    n2 = 1634119
    n3 = 1635320
    n4 = 1635445
    nx = 1633885

class MStageConcepts(ConceptEnum):
    # and m...
    m0 = 1635624
    m1 = 1635142
    mx = 1633547

class GroupStageConcepts(ConceptEnum):
    # there's a pattern here
    stage0 = 1633754
    stageI = 1633306
    stageII = 1634209
    stageIII = 1633650
    stageIV = 1633650

class ConditionConcepts(ConceptEnum):
    ehr_problem_list = 32840
    resolved_condition = 32906
    confirmed_diagnosis = 32893

class StageType(ConceptEnum):
    c = 0
    p = 1

class StageEdition(ConceptEnum):
    _6th = 1634647
    _7th = 1633496
    _8th = 1634449

class ModifierConcepts(ConceptEnum):
    grade = 35918328
    laterality = 35918306
    derived_value = 45754907
    tumor_size = 4139794
    primary_tumor = 36768229


class DrugExposureConcepts(ConceptEnum):
    drug_dose = 4162374
    ehr_drug_admin = 32818
    placebo = 1379408